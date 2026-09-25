// Tests voor de formulieren-Worker. Draaien met: npm test (Node 20+).
// Turnstile en Brevo worden hier nagebootst; er gaat niets het internet op.
import { test, beforeEach } from "node:test";
import assert from "node:assert/strict";
import worker from "../src/index.js";
import { valideer } from "../src/validatie.js";
import { stripJpeg, stripPng, verwerkFotos } from "../src/foto.js";
import { escHtml, headerVeilig, onderwerp } from "../src/mail.js";

const ORIGIN = "https://ino-elektra.nl";
let verzonden, turnstileAntwoord, brevoStatus, limiter;

const env = () => ({
  ALLOWED_ORIGINS: "https://ino-elektra.nl,https://www.ino-elektra.nl",
  TURNSTILE_HOSTNAMES: "ino-elektra.nl,www.ino-elektra.nl",
  TURNSTILE_SECRET: "geheim",
  BREVO_API_KEY: "sleutel",
  MAIL_TO: "info@ino-elektra.nl",
  MAIL_FROM: "formulier@ino-elektra.nl",
  BEVESTIGING_KLANT: "true",
  RATE_LIMITER: limiter,
});

beforeEach(() => {
  verzonden = [];
  turnstileAntwoord = (form) => ({ success: true, hostname: "ino-elektra.nl", action: form });
  brevoStatus = 201;
  let n = 0;
  limiter = { limit: async () => ({ success: ++n <= 5 }) };
  globalThis.fetch = async (url, init) => {
    if (String(url).includes("siteverify")) {
      const fd = init.body;
      if (fd.get("response") === "gebruikt") return new Response(JSON.stringify({ success: false, "error-codes": ["timeout-or-duplicate"] }));
      return new Response(JSON.stringify(turnstileAntwoord(fd.get("response"))));
    }
    if (String(url).includes("brevo")) {
      assert.equal(init.headers["api-key"], "sleutel");
      verzonden.push(JSON.parse(init.body));
      return new Response("{}", { status: brevoStatus });
    }
    throw new Error("onverwachte fetch " + url);
  };
});

function jpegMetExif() {
  // SOI, APP0 (JFIF), APP1 (Exif met "GPS"), COM, SOS + data, EOI
  const app0 = [0xff, 0xe0, 0x00, 0x07, 0x4a, 0x46, 0x49, 0x46, 0x00];
  const exif = [0x45, 0x78, 0x69, 0x66, 0x00, 0x00, 0x47, 0x50, 0x53];
  const app1 = [0xff, 0xe1, 0x00, exif.length + 2, ...exif];
  const com = [0xff, 0xfe, 0x00, 0x05, 0x68, 0x69, 0x21];
  return new Uint8Array([0xff, 0xd8, ...app0, ...app1, ...com, 0xff, 0xda, 0x00, 0x02, 0x11, 0x22, 0xff, 0xd9]);
}
function pngMetTekst() {
  const sig = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  const chunk = (type, data) => [0, 0, 0, data.length, ...[...type].map((c) => c.charCodeAt(0)), ...data, 0, 0, 0, 0];
  return new Uint8Array([...sig, ...chunk("IHDR", Array(13).fill(1)), ...chunk("tEXt", [0x47, 0x50, 0x53]), ...chunk("IDAT", [1, 2]), ...chunk("IEND", [])]);
}

function formulier(type, velden, extra = {}) {
  const fd = new FormData();
  fd.set("formulier", type);
  fd.set("cf-turnstile-response", type);
  for (const [k, v] of Object.entries(velden)) fd.set(k, v);
  for (const [k, v] of Object.entries(extra)) fd.append(k, v);
  return fd;
}
const OFFERTE = { name: "Jan de Vries", phone: "06 12345678", email: "jan@example.nl", message: "Groepenkast vervangen,\nnu nog stoppen.", akkoord: "ja", service: "Meterkast vernieuwen", termijn: "Binnen 2 weken", postcode: "3561 AB", number: "12" };
const SPOED = { name: "Piet", phone: "+31612345678", message: "Aardlek springt eruit" };
function morgen() { return new Date(Date.now() + 864e5).toISOString().slice(0, 10); }
const AFSPRAAK = () => ({ name: "Sara", phone: "0612345678", email: "sara@example.nl", datum: morgen(), tijd: "10:00 – 12:00" });

function post(fd, { origin = ORIGIN, url = "https://ino-formulieren.test.workers.dev/", headers = {} } = {}) {
  return new Request(url, { method: "POST", body: fd, headers: { Origin: origin, "CF-Connecting-IP": "203.0.113.9", ...headers } });
}
const ctx = () => { const p = []; return { waitUntil: (x) => p.push(x), klaar: () => Promise.all(p) }; };
async function stuur(req, e = env()) { const c = ctx(); const r = await worker.fetch(req, e, c); await c.klaar(); return [r, await r.json().catch(() => null)]; }

// ---------------------------------------------------------------- offerte
test("offerte: normale aanvraag -> 200, mail aan info@ met Reply-To + bevestiging", async () => {
  const [r, j] = await stuur(post(formulier("offerte", OFFERTE)));
  assert.equal(r.status, 200); assert.deepEqual(j, { ok: true });
  assert.equal(r.headers.get("access-control-allow-origin"), ORIGIN);
  assert.equal(verzonden.length, 2);
  const [m, b] = verzonden;
  assert.deepEqual(m.to, [{ email: "info@ino-elektra.nl" }]);
  assert.deepEqual(m.replyTo, { email: "jan@example.nl", name: "Jan de Vries" });
  assert.match(m.subject, /^\[Offerte\] Meterkast vernieuwen – Jan de Vries$/);
  assert.match(m.htmlContent, /Offerteaanvraag/); assert.match(m.htmlContent, /3561 AB/);
  assert.deepEqual(b.to, [{ email: "jan@example.nl" }]);
  assert.deepEqual(b.replyTo, { email: "info@ino-elektra.nl" });
  assert.ok(!b.htmlContent.includes("Jan") && !b.htmlContent.includes("Groepenkast"), "bevestiging bevat geen klantinvoer");
});

test("offerte: verplichte velden ontbreken -> 422 met veldnamen, niets verstuurd", async () => {
  const [r, j] = await stuur(post(formulier("offerte", { name: "", phone: "", email: "", message: "" })));
  assert.equal(r.status, 422);
  assert.deepEqual(Object.keys(j.velden).sort(), ["akkoord", "email", "message", "name", "phone"]);
  assert.equal(verzonden.length, 0);
});

test("offerte: ongeldig e-mailadres en header-injectie in e-mail -> 422", async () => {
  for (const email of ["geen-email", "a@b", "x@example.nl\r\nBcc: spam@evil.test", "<script>@x.nl"]) {
    const [r, j] = await stuur(post(formulier("offerte", { ...OFFERTE, email })));
    assert.equal(r.status, 422, email); assert.ok(j.velden.email);
  }
  assert.equal(verzonden.length, 0);
});

test("offerte: extreem lange invoer -> 422", async () => {
  const [r, j] = await stuur(post(formulier("offerte", { ...OFFERTE, message: "a".repeat(3001), name: "b".repeat(81) })));
  assert.equal(r.status, 422); assert.ok(j.velden.message && j.velden.name);
});

test("offerte: XSS in bericht wordt ge-escaped in de mail", async () => {
  const [r] = await stuur(post(formulier("offerte", { ...OFFERTE, message: '<img src=x onerror=alert(1)><script>x</script>' })));
  assert.equal(r.status, 200);
  assert.ok(!verzonden[0].htmlContent.includes("<script>x"));
  assert.ok(verzonden[0].htmlContent.includes("&lt;img src=x onerror=alert(1)&gt;"));
});

test("offerte: URL of HTML in de naam wordt geweigerd; CR/LF in naam wordt spatie", async () => {
  const [r] = await stuur(post(formulier("offerte", { ...OFFERTE, name: "Koop nu https://spam.test" })));
  assert.equal(r.status, 422);
  const [r2] = await stuur(post(formulier("offerte", { ...OFFERTE, name: "Jan\r\nBcc: x@y.z" })));
  assert.equal(r2.status, 200);
  assert.ok(!/[\r\n]/.test(verzonden[0].subject) && !/[\r\n]/.test(verzonden[0].replyTo.name));
});

test("offerte: foto's -> metadata weg, vaste bestandsnamen, als bijlage", async () => {
  const fd = formulier("offerte", OFFERTE);
  fd.append("photos", new File([jpegMetExif()], "../../etc/passwd.jpg", { type: "image/jpeg" }));
  fd.append("photos", new File([pngMetTekst()], "scan.png", { type: "image/png" }));
  const [r] = await stuur(post(fd));
  assert.equal(r.status, 200);
  const att = verzonden[0].attachment;
  assert.deepEqual(att.map((a) => a.name), ["foto-1.jpg", "foto-2.png"]);
  for (const a of att) assert.ok(!Buffer.from(a.content, "base64").includes("GPS"), a.name);
});

test("offerte: verkeerd bestandstype (SVG/HTML/exe als .jpg) -> 422", async () => {
  for (const [inhoud, naam] of [['<svg onload="alert(1)"/>', "x.svg"], ["<html>", "foto.jpg"], ["MZ\x90\x00", "foto.jpg"]]) {
    const fd = formulier("offerte", OFFERTE);
    fd.append("photos", new File([inhoud], naam, { type: "image/jpeg" }));
    const [r, j] = await stuur(post(fd));
    assert.equal(r.status, 422, naam); assert.ok(j.velden.photos);
  }
  assert.equal(verzonden.length, 0);
});

test("offerte: te veel of te grote foto's -> 422", async () => {
  const fd = formulier("offerte", OFFERTE);
  for (let i = 0; i < 6; i++) fd.append("photos", new File([jpegMetExif()], "f.jpg"));
  assert.equal((await stuur(post(fd)))[0].status, 422);
  const groot = new Uint8Array(4 * 1024 * 1024 + 1); groot.set([0xff, 0xd8, 0xff]);
  const fd2 = formulier("offerte", OFFERTE); fd2.append("photos", new File([groot], "g.jpg"));
  assert.equal((await stuur(post(fd2)))[0].status, 422);
});

test("request groter dan 12 MB -> 413", async () => {
  const req = new Request("https://ino-formulieren.test.workers.dev/", { method: "POST", body: "x", headers: { Origin: ORIGIN, "content-type": "multipart/form-data; boundary=x", "content-length": String(13 * 1024 * 1024) } });
  assert.equal((await stuur(req))[0].status, 413);
});

// ---------------------------------------------------------------- spoed
test("spoed: normale aanvraag -> [SPOED]-onderwerp, geen Reply-To, geen bevestiging", async () => {
  const [r] = await stuur(post(formulier("spoed", SPOED)));
  assert.equal(r.status, 200); assert.equal(verzonden.length, 1);
  assert.match(verzonden[0].subject, /^\[SPOED\] Terugbelverzoek – Piet – \+31612345678$/);
  assert.equal(verzonden[0].replyTo, undefined);
});
test("spoed: validatie (telefoon, bericht verplicht)", async () => {
  const [r, j] = await stuur(post(formulier("spoed", { name: "Piet", phone: "123", message: "" })));
  assert.equal(r.status, 422); assert.deepEqual(Object.keys(j.velden).sort(), ["message", "phone"]);
});
test("spoed: honeypot gevuld -> 200 maar niets verstuurd", async () => {
  const [r] = await stuur(post(formulier("spoed", { ...SPOED, _honey: "http://spam" })));
  assert.equal(r.status, 200); assert.equal(verzonden.length, 0);
});

// ---------------------------------------------------------------- afspraak
test("afspraak: normale aanvraag -> [Afspraak]-onderwerp met datum en tijd + bevestiging", async () => {
  const a = AFSPRAAK();
  const [r] = await stuur(post(formulier("afspraak", a)));
  assert.equal(r.status, 200); assert.equal(verzonden.length, 2);
  const [j, m, d] = a.datum.split("-");
  assert.equal(verzonden[0].subject, `[Afspraak] ${d}-${m}-${j} 10:00 – 12:00 – Sara`);
  assert.match(verzonden[1].subject, /afspraakaanvraag ontvangen/);
});
test("afspraak: datum in het verleden, ongeldig tijdslot -> 422", async () => {
  const [r, j] = await stuur(post(formulier("afspraak", { ...AFSPRAAK(), datum: "2020-01-01", tijd: "03:00" })));
  assert.equal(r.status, 422); assert.deepEqual(Object.keys(j.velden).sort(), ["datum", "tijd"]);
});
test("afspraak: zonder e-mail -> geen bevestiging, geen Reply-To", async () => {
  const a = AFSPRAAK(); delete a.email;
  const [r] = await stuur(post(formulier("afspraak", a)));
  assert.equal(r.status, 200); assert.equal(verzonden.length, 1); assert.equal(verzonden[0].replyTo, undefined);
});
test("afspraak: honeypot -> niets verstuurd", async () => {
  const [r] = await stuur(post(formulier("afspraak", { ...AFSPRAAK(), _honey: "x" })));
  assert.equal(r.status, 200); assert.equal(verzonden.length, 0);
});

// ---------------------------------------------------------------- beveiliging
test("Turnstile mislukt of hergebruikt (dubbele inzending) -> 403", async () => {
  turnstileAntwoord = () => ({ success: false });
  assert.equal((await stuur(post(formulier("spoed", SPOED))))[0].status, 403);
  turnstileAntwoord = (f) => ({ success: true, hostname: "evil.test", action: f });
  assert.equal((await stuur(post(formulier("spoed", SPOED))))[0].status, 403);
  turnstileAntwoord = () => ({ success: true, hostname: "ino-elektra.nl", action: "offerte" });
  assert.equal((await stuur(post(formulier("spoed", SPOED))))[0].status, 403, "token van ander formulier");
  const fd = formulier("spoed", SPOED); fd.set("cf-turnstile-response", "gebruikt");
  assert.equal((await stuur(post(fd)))[0].status, 403);
  const fd2 = formulier("spoed", SPOED); fd2.delete("cf-turnstile-response");
  assert.equal((await stuur(post(fd2)))[0].status, 403);
  assert.equal(verzonden.length, 0);
});
test("CORS: vreemde origin -> 403 zonder CORS-headers; preflight alleen voor eigen site", async () => {
  const [r] = await stuur(post(formulier("spoed", SPOED), { origin: "https://evil.test" }));
  assert.equal(r.status, 403); assert.equal(r.headers.get("access-control-allow-origin"), null);
  const pre = await worker.fetch(new Request("https://x.workers.dev/", { method: "OPTIONS", headers: { Origin: ORIGIN } }), env(), ctx());
  assert.equal(pre.status, 204); assert.equal(pre.headers.get("access-control-allow-origin"), ORIGIN);
  const pre2 = await worker.fetch(new Request("https://x.workers.dev/", { method: "OPTIONS", headers: { Origin: "https://evil.test" } }), env(), ctx());
  assert.equal(pre2.status, 403);
});
test("HTTP (geen HTTPS) -> 403; GET -> 405; onbekend pad -> 404; onbekend formulier -> 400", async () => {
  assert.equal((await stuur(post(formulier("spoed", SPOED), { url: "http://x.workers.dev/" })))[0].status, 403);
  assert.equal((await worker.fetch(new Request("https://x.workers.dev/", { headers: { Origin: ORIGIN } }), env(), ctx())).status, 405);
  assert.equal((await stuur(post(formulier("spoed", SPOED), { url: "https://x.workers.dev/admin" })))[0].status, 404);
  assert.equal((await stuur(post(formulier("bestelling", SPOED))))[0].status, 400);
});
test("rate limit: 6e inzending binnen een minuut -> 429", async () => {
  const e = env();
  const codes = [];
  for (let i = 0; i < 6; i++) codes.push((await stuur(post(formulier("spoed", SPOED)), e))[0].status);
  assert.deepEqual(codes, [200, 200, 200, 200, 200, 429]);
});
test("Brevo-fout -> 502 en geen bevestiging aan de klant", async () => {
  brevoStatus = 401;
  const [r, j] = await stuur(post(formulier("offerte", OFFERTE)));
  assert.equal(r.status, 502); assert.equal(j.fout, "mail"); assert.equal(verzonden.length, 1);
});
test("logs bevatten geen persoonsgegevens", async () => {
  const regels = []; const orig = console.log; console.log = (s) => regels.push(String(s));
  try {
    await stuur(post(formulier("offerte", OFFERTE)));
    await stuur(post(formulier("offerte", { ...OFFERTE, email: "fout" })));
  } finally { console.log = orig; }
  const alles = regels.join("\n");
  for (const pii of ["Jan", "0612345678", "06 12345678", "jan@example", "203.0.113.9", "Groepenkast", "3561"]) assert.ok(!alles.includes(pii), pii);
});

// ---------------------------------------------------------------- eenheden
test("hulpfuncties", () => {
  assert.equal(escHtml(`<a href="x">'&`), "&lt;a href=&quot;x&quot;&gt;&#39;&amp;");
  assert.equal(headerVeilig("a\r\nb\tc"), "a b c");
  assert.equal(onderwerp("spoed", { naam: "A\nB", telefoon: "06" }), "[SPOED] Terugbelverzoek – A B – 06");
  assert.ok(!Buffer.from(stripJpeg(jpegMetExif())).includes("GPS"));
  assert.ok(!Buffer.from(stripPng(pngMetTekst())).includes("GPS"));
  assert.throws(() => stripJpeg(new Uint8Array([0xff, 0xd8, 0x00])));
  const fd = new FormData(); fd.set("name", "Jan"); fd.set("phone", "06-1234 5678"); fd.set("message", "x"); fd.set("onbekend", "negeren");
  const v = valideer("spoed", fd);
  assert.ok(v.ok); assert.equal(v.data.onbekend, undefined);
});
test("verwerkFotos: lege bestandsvelden worden genegeerd", async () => {
  const r = await verwerkFotos([new File([], ""), ""]);
  assert.deepEqual(r, { ok: true, bijlagen: [] });
});
