// Tests voor GET /api/reviews. Google en de Cloudflare-cache worden nagebootst.
import { test, beforeEach } from "node:test";
import assert from "node:assert/strict";
import worker from "../src/index.js";

const ORIGIN = "https://ino-elektra.nl";
let googleCalls, opslag, wacht;

const env = (extra = {}) => ({
  ALLOWED_ORIGINS: "https://ino-elektra.nl,https://www.ino-elektra.nl",
  GOOGLE_PLACES_API_KEY: "gkey",
  GOOGLE_PLACE_ID: "ChIJtest",
  ...extra,
});
const ctx = () => ({ waitUntil: (p) => wacht.push(p) });
const vraag = (method = "GET", origin = ORIGIN) =>
  new Request("https://api.ino-elektra.nl/api/reviews", { method, headers: origin ? { Origin: origin } : {} });

beforeEach(() => {
  googleCalls = 0; opslag = new Map(); wacht = [];
  globalThis.caches = { default: {
    match: async (r) => { const v = opslag.get(r.url); return v ? new Response(v) : undefined; },
    put: async (r, res) => { opslag.set(r.url, await res.text()); },
  } };
  globalThis.fetch = async (url, init) => {
    assert.ok(String(url).startsWith("https://places.googleapis.com/v1/places/ChIJtest"));
    assert.equal(init.headers["X-Goog-Api-Key"], "gkey");
    googleCalls++;
    return new Response(JSON.stringify({
      rating: 4.9, userRatingCount: 42, googleMapsUri: "https://maps.google.com/?cid=1",
      reviews: [
        { rating: 5, relativePublishTimeDescription: "een week geleden", text: { text: "Top  service" },
          authorAttribution: { displayName: "Sanne", uri: "https://www.google.com/maps/contrib/1", photoUri: "https://lh3.x/foto" } },
        { rating: 5, text: { text: "" }, authorAttribution: { displayName: "Leeg" } },
      ],
    }));
  };
});

test("geeft score, aantal en reviews zonder foto's en zonder API-key", async () => {
  const r = await worker.fetch(vraag(), env(), ctx());
  assert.equal(r.status, 200);
  assert.equal(r.headers.get("access-control-allow-origin"), ORIGIN);
  const tekst = await r.text();
  assert.ok(!tekst.includes("gkey") && !tekst.includes("lh3"));
  const d = JSON.parse(tekst);
  assert.equal(d.score, 4.9); assert.equal(d.aantal, 42);
  assert.equal(d.reviews.length, 1);
  assert.equal(d.reviews[0].tekst, "Top service");
});

test("tweede verzoek komt uit de cache", async () => {
  await worker.fetch(vraag(), env(), ctx()); await Promise.all(wacht);
  await worker.fetch(vraag(), env(), ctx());
  assert.equal(googleCalls, 1);
});

test("zonder instellingen: 503, geen verzoek naar Google", async () => {
  const r = await worker.fetch(vraag(), env({ GOOGLE_PLACE_ID: "" }), ctx());
  assert.equal(r.status, 503); assert.equal(googleCalls, 0);
});

test("fout bij Google wordt niet gecachet", async () => {
  globalThis.fetch = async () => { googleCalls++; return new Response("{}", { status: 403 }); };
  const r = await worker.fetch(vraag(), env(), ctx());
  assert.equal(r.status, 502); assert.equal(opslag.size, 0);
});

test("alleen GET; vreemde origin krijgt geen CORS", async () => {
  assert.equal((await worker.fetch(vraag("POST"), env(), ctx())).status, 405);
  const r = await worker.fetch(vraag("GET", "https://evil.example"), env(), ctx());
  assert.equal(r.headers.get("access-control-allow-origin"), null);
});
