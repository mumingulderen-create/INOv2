// INO formulieren-endpoint (Cloudflare Worker)
// GitHub Pages (quoteForm / spoedForm / appointmentForm) → deze Worker → Brevo → info@ino-elektra.nl
//
// Volgorde per verzoek: HTTPS → CORS/Origin → methode → grootte → rate limit →
// honeypot → validatie → foto's → Turnstile → e-mail → (bevestiging klant).
// Logs bevatten nooit naam, telefoon, e-mail, IP-adres of berichtinhoud.

import { valideer, FORMULIEREN } from "./validatie.js";
import { verwerkFotos } from "./foto.js";
import { aanvraagMail, bevestigingMail, onderwerp, stuurBrevo, headerVeilig } from "./mail.js";

const MAX_BODY = 12 * 1024 * 1024;
const SITEVERIFY = "https://challenges.cloudflare.com/turnstile/v0/siteverify";

function log(evt, extra = {}) {
  console.log(JSON.stringify({ evt, ...extra }));
}

function lijst(v) {
  return String(v || "").split(",").map((s) => s.trim()).filter(Boolean);
}

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function json(status, body, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
      "referrer-policy": "no-referrer",
      ...(origin ? corsHeaders(origin) : {}),
    },
  });
}

async function turnstileOk(env, token, ip, formulier) {
  if (!token || typeof token !== "string" || token.length > 2048) return false;
  const body = new FormData();
  body.append("secret", env.TURNSTILE_SECRET);
  body.append("response", token);
  if (ip) body.append("remoteip", ip);
  const r = await fetch(env.TURNSTILE_VERIFY_URL || SITEVERIFY, { method: "POST", body });
  if (!r.ok) return false;
  const res = await r.json();
  if (!res.success) return false;
  // Token moet op onze eigen site en voor dit formulier zijn aangemaakt.
  const hosts = lijst(env.TURNSTILE_HOSTNAMES);
  if (hosts.length && !hosts.includes(res.hostname)) return false;
  if (res.action && res.action !== formulier) return false;
  return true;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin") || "";
    const toegestaan = lijst(env.ALLOWED_ORIGINS).includes(origin);
    const cors = toegestaan ? origin : "";

    if (url.protocol !== "https:" && env.ALLOW_HTTP !== "true") return json(403, { ok: false, fout: "https" });
    if (url.pathname !== "/" && url.pathname !== "/aanvraag") return json(404, { ok: false, fout: "niet_gevonden" }, cors);

    if (request.method === "OPTIONS") {
      return toegestaan ? new Response(null, { status: 204, headers: corsHeaders(origin) }) : new Response(null, { status: 403 });
    }
    if (request.method !== "POST") return json(405, { ok: false, fout: "methode" }, cors);
    if (!toegestaan) { log("geweigerd", { reden: "origin" }); return json(403, { ok: false, fout: "origin" }); }

    const ct = (request.headers.get("content-type") || "").toLowerCase();
    if (!ct.startsWith("multipart/form-data") && !ct.startsWith("application/x-www-form-urlencoded")) {
      return json(415, { ok: false, fout: "type" }, cors);
    }
    const lengte = Number(request.headers.get("content-length") || 0);
    if (lengte > MAX_BODY) return json(413, { ok: false, fout: "te_groot" }, cors);

    const ip = request.headers.get("CF-Connecting-IP") || "";
    if (env.RATE_LIMITER) {
      const { success } = await env.RATE_LIMITER.limit({ key: ip || "onbekend" });
      if (!success) { log("geweigerd", { reden: "rate_limit" }); return json(429, { ok: false, fout: "te_veel" }, cors); }
    }

    let fd;
    try { fd = await request.formData(); } catch { return json(400, { ok: false, fout: "ongeldig" }, cors); }

    const formulier = String(fd.get("formulier") || "");
    if (!FORMULIEREN.includes(formulier)) return json(400, { ok: false, fout: "formulier" }, cors);

    // Honeypot: mensen zien dit veld niet. Bots krijgen een "ok" zodat ze niet
    // gaan zoeken naar een andere manier, maar er wordt niets verstuurd.
    if (String(fd.get("_honey") || "").trim()) { log("spam", { formulier, reden: "honeypot" }); return json(200, { ok: true }, cors); }

    const v = valideer(formulier, fd);
    if (!v.ok) { log("validatie", { formulier, velden: Object.keys(v.velden) }); return json(422, { ok: false, fout: "validatie", velden: v.velden }, cors); }
    const d = v.data;

    let bijlagen = [];
    if (formulier === "offerte") {
      const f = await verwerkFotos(fd.getAll("photos"));
      if (!f.ok) { log("validatie", { formulier, velden: ["photos"] }); return json(422, { ok: false, fout: "validatie", velden: { photos: f.fout } }, cors); }
      bijlagen = f.bijlagen;
    }

    // Turnstile als laatste controle vóór versturen: een token werkt maar één
    // keer, dus een dubbele inzending met hetzelfde token wordt geweigerd.
    if (!(await turnstileOk(env, fd.get("cf-turnstile-response"), ip, formulier))) {
      log("geweigerd", { formulier, reden: "turnstile" });
      return json(403, { ok: false, fout: "turnstile" }, cors);
    }

    const mailTo = env.MAIL_TO;
    const afzender = { name: headerVeilig(env.MAIL_FROM_NAME || "Website INO", 60), email: env.MAIL_FROM };
    const { html, tekst } = aanvraagMail(formulier, d, bijlagen.length);
    const bericht = {
      sender: afzender,
      to: [{ email: mailTo }],
      subject: onderwerp(formulier, d),
      htmlContent: html,
      textContent: tekst,
      tags: [`formulier-${formulier}`],
    };
    if (d.email) bericht.replyTo = { email: d.email, name: headerVeilig(d.naam, 60) };
    if (bijlagen.length) bericht.attachment = bijlagen;

    try {
      await stuurBrevo(env, bericht);
    } catch (e) {
      log("fout", { formulier, reden: String(e.message || e).slice(0, 40) });
      return json(502, { ok: false, fout: "mail" }, cors);
    }
    log("verstuurd", { formulier, fotos: bijlagen.length });

    // Bevestiging aan de klant pas nadat de aanvraag bij INO is afgeleverd.
    if (d.email && env.BEVESTIGING_KLANT === "true") {
      const b = bevestigingMail(formulier, {
        naam: env.BEDRIJF_NAAM || "INO Techniek en Installatie",
        telefoon: env.BEDRIJF_TELEFOON || "06 28 76 37 75",
        telefoonE164: env.BEDRIJF_TELEFOON_E164 || "+31628763775",
        website: env.BEDRIJF_WEBSITE || "https://ino-elektra.nl",
      });
      b.naamAfzender = env.BEDRIJF_NAAM || "INO Techniek en Installatie";
      ctx.waitUntil(
        stuurBrevo(env, {
          sender: { name: headerVeilig(b.naamAfzender, 60), email: env.MAIL_FROM },
          to: [{ email: d.email }],
          replyTo: { email: mailTo },
          subject: b.onderwerp,
          htmlContent: b.html,
          textContent: b.tekst,
          tags: ["bevestiging-klant"],
        }).then(() => log("bevestiging", { formulier }), (e) => log("fout_bevestiging", { formulier, reden: String(e.message || e).slice(0, 40) }))
      );
    }
    return json(200, { ok: true }, cors);
  },
};
