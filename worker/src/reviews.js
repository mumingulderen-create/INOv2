// GET /api/reviews — actuele Google-score en de nieuwste reviews van INO.
//
// De Worker vraagt Google Places API (New) om Place Details en bewaart het
// antwoord in de Cloudflare-cache. Zo blijft de API-key geheim (alleen in
// Cloudflare als secret GOOGLE_PLACES_API_KEY) en doet de site per cacheperiode
// hooguit één verzoek per Cloudflare-datacenter bij Google.
//
// Nodig in Cloudflare:
//   secret  GOOGLE_PLACES_API_KEY   (npx wrangler secret put GOOGLE_PLACES_API_KEY)
//   var     GOOGLE_PLACE_ID         (Place ID van het bedrijfsprofiel, begint met "ChIJ")
//   var     REVIEWS_CACHE_SECONDS   (optioneel, standaard 21600 = 6 uur)

const PLACES = "https://places.googleapis.com/v1/places/";
const VELDEN = "rating,userRatingCount,reviews,googleMapsUri";

function schoon(v, max) {
  return String(v || "").replace(/\s+/g, " ").trim().slice(0, max);
}

// Alleen wat de site nodig heeft; geen profielfoto's (die laden vanaf Google-servers).
export function vertaal(p) {
  const reviews = (Array.isArray(p.reviews) ? p.reviews : [])
    .map((r) => ({
      naam: schoon(r.authorAttribution && r.authorAttribution.displayName, 60),
      profiel: schoon(r.authorAttribution && r.authorAttribution.uri, 300),
      sterren: Math.max(0, Math.min(5, Math.round(Number(r.rating) || 0))),
      tekst: schoon((r.originalText && r.originalText.text) || (r.text && r.text.text), 1200),
      wanneer: schoon(r.relativePublishTimeDescription, 40),
      link: schoon(r.googleMapsUri, 300),
    }))
    .filter((r) => r.naam && r.tekst);
  return {
    ok: true,
    score: Number(p.rating) || null,
    aantal: Number(p.userRatingCount) || null,
    url: schoon(p.googleMapsUri, 300),
    reviews,
  };
}

export async function reviews(request, env, ctx, headers) {
  const antwoord = (status, body, maxAge) =>
    new Response(JSON.stringify(body), {
      status,
      headers: {
        ...headers,
        "content-type": "application/json; charset=utf-8",
        "cache-control": maxAge ? `public, max-age=${maxAge}` : "no-store",
        "x-content-type-options": "nosniff",
      },
    });

  if (!env.GOOGLE_PLACES_API_KEY || !env.GOOGLE_PLACE_ID) return antwoord(503, { ok: false, fout: "niet_ingesteld" });

  const ttl = Math.max(300, Number(env.REVIEWS_CACHE_SECONDS) || 21600);
  const cache = caches.default;
  const sleutel = new Request("https://cache.ino-elektra.nl/api/reviews/v1", { method: "GET" });

  let data;
  const hit = await cache.match(sleutel);
  if (hit) {
    data = await hit.json();
  } else {
    const r = await fetch(PLACES + encodeURIComponent(env.GOOGLE_PLACE_ID) + "?languageCode=nl&regionCode=NL", {
      headers: { "X-Goog-Api-Key": env.GOOGLE_PLACES_API_KEY, "X-Goog-FieldMask": VELDEN },
    });
    if (!r.ok) {
      console.log(JSON.stringify({ evt: "reviews_fout", status: r.status }));
      return antwoord(502, { ok: false, fout: "google" });
    }
    data = vertaal(await r.json());
    ctx.waitUntil(
      cache.put(sleutel, new Response(JSON.stringify(data), {
        headers: { "content-type": "application/json", "cache-control": `public, max-age=${ttl}` },
      }))
    );
    console.log(JSON.stringify({ evt: "reviews_opgehaald", aantal: data.aantal }));
  }
  // Browser mag het een uur bewaren; de Worker-cache zorgt voor de rest.
  return antwoord(200, data, Math.min(3600, ttl));
}
