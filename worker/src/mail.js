// E-mails opbouwen en versturen via de Brevo transactional API.
// Alles wat de klant invult, wordt ge-escaped (HTML) en zit nooit in een
// e-mailheader behalve als losse JSON-waarde (Brevo zet de headers zelf op).

const BREVO_URL = "https://api.brevo.com/v3/smtp/email";

export function escHtml(v) {
  return String(v).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// Voor onderwerpregels en namen in headers: geen regeleinden, beperkte lengte.
export function headerVeilig(v, max = 80) {
  return String(v).replace(/[\u0000-\u001F\u007F\u2028\u2029]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);
}

const SOORT = {
  offerte: { label: "Offerteaanvraag", tag: "Offerte", kleur: "#1f7a16", bron: "Offerteformulier (/offerte/)" },
  spoed: { label: "Spoedaanvraag – terugbelverzoek", tag: "SPOED", kleur: "#b42318", bron: "Spoedformulier (/spoed-elektricien-utrecht/)" },
  afspraak: { label: "Afspraakaanvraag", tag: "Afspraak", kleur: "#1d4ed8", bron: "Afspraakformulier (/afspraak/)" },
};

const LABELS = [
  ["naam", "Naam"], ["telefoon", "Telefoon"], ["email", "E-mail"],
  ["klus", "Klus(sen)"], ["termijn", "Gewenste termijn"],
  ["datum", "Gewenste datum"], ["tijd", "Voorkeurstijd"],
  ["postcode", "Postcode"], ["huisnummer", "Huisnummer"], ["wijk", "Wijk (via pagina)"],
];

function datumNL(iso) {
  const [j, m, d] = iso.split("-");
  return `${d}-${m}-${j}`;
}

export function onderwerp(formulier, d) {
  const naam = headerVeilig(d.naam, 60);
  if (formulier === "spoed") return `[SPOED] Terugbelverzoek – ${naam} – ${headerVeilig(d.telefoon, 20)}`;
  if (formulier === "afspraak") return `[Afspraak] ${datumNL(d.datum)} ${d.tijd} – ${naam}`;
  return `[Offerte] ${headerVeilig(d.klus || "Nieuwe aanvraag", 60)} – ${naam}`;
}

export function aanvraagMail(formulier, d, aantalFotos, ontvangen = new Date()) {
  const s = SOORT[formulier];
  const tijd = new Intl.DateTimeFormat("nl-NL", { timeZone: "Europe/Amsterdam", dateStyle: "full", timeStyle: "short" }).format(ontvangen);
  const rijen = LABELS.filter(([k]) => d[k]).map(([k, l]) => {
    let w = k === "datum" ? datumNL(d[k]) : d[k];
    let html = escHtml(w);
    if (k === "telefoon") html = `<a href="tel:${escHtml(d[k].replace(/[^\d+]/g, ""))}">${html}</a>`;
    if (k === "email") html = `<a href="mailto:${escHtml(d[k])}">${html}</a>`;
    return { l, w, html };
  });
  if (formulier === "offerte") rijen.push({ l: "Toestemming contact", w: "Ja", html: "Ja" });
  if (aantalFotos) rijen.push({ l: "Foto's", w: `${aantalFotos} als bijlage`, html: `${aantalFotos} als bijlage` });

  const html = `<!doctype html><html lang="nl"><body style="margin:0;background:#f4f7f2;font-family:Arial,Helvetica,sans-serif;color:#14201a">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f7f2;padding:24px 12px"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#fff;border:1px solid #dde5da;border-radius:10px">
<tr><td style="background:${s.kleur};color:#fff;padding:18px 24px;border-radius:10px 10px 0 0;font-size:20px;font-weight:bold">${escHtml(s.label)}</td></tr>
<tr><td style="padding:20px 24px 4px;font-size:14px;color:#56615a">Via: ${escHtml(s.bron)}<br>Ontvangen: ${escHtml(tijd)}</td></tr>
<tr><td style="padding:12px 24px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:15px">
${rijen.map((r) => `<tr><td style="padding:7px 12px 7px 0;color:#56615a;vertical-align:top;white-space:nowrap">${escHtml(r.l)}</td><td style="padding:7px 0;font-weight:bold">${r.html}</td></tr>`).join("\n")}
</table></td></tr>
${d.bericht ? `<tr><td style="padding:4px 24px 20px"><div style="font-size:13px;color:#56615a;margin-bottom:6px">Bericht van de klant</div><div style="background:#f4f7f2;border-radius:8px;padding:14px;font-size:15px;line-height:1.5;white-space:pre-wrap">${escHtml(d.bericht)}</div></td></tr>` : ""}
<tr><td style="padding:14px 24px 20px;font-size:12px;color:#56615a;border-top:1px solid #dde5da">${d.email ? "Beantwoorden gaat rechtstreeks naar de klant (Reply-To)." : "De klant heeft geen e-mailadres opgegeven: neem telefonisch contact op."} Verwijder aanvragen die niet tot een opdracht leiden binnen 12 maanden (privacyverklaring).</td></tr>
</table></td></tr></table></body></html>`;

  const tekst = [
    `${s.label}`, `Via: ${s.bron}`, `Ontvangen: ${tijd}`, "",
    ...rijen.map((r) => `${r.l}: ${r.w}`),
    ...(d.bericht ? ["", "Bericht van de klant:", d.bericht] : []),
  ].join("\n");
  return { html, tekst };
}

// Vaste tekst zonder klantinvoer: zo kan het formulier niet misbruikt worden om
// via ons domein berichten naar willekeurige adressen te sturen.
export function bevestigingMail(formulier, bedrijf) {
  const wat = { offerte: "offerteaanvraag", spoed: "aanvraag", afspraak: "afspraakaanvraag" }[formulier];
  const vervolg = formulier === "afspraak"
    ? "We nemen zo snel mogelijk contact met je op om de afspraak te bevestigen."
    : "We nemen zo snel mogelijk contact met je op.";
  const onderwerpRegel = `We hebben je ${wat} ontvangen – ${bedrijf.naam}`;
  const tekst = [
    "Hallo,", "",
    `Bedankt voor je ${wat} bij ${bedrijf.naam}. We hebben je aanvraag goed ontvangen. ${vervolg}`, "",
    `Is het dringend, bijvoorbeeld een stroomstoring? Bel ons dan direct: ${bedrijf.telefoon} (24/7).`, "",
    "Met vriendelijke groet,", bedrijf.naam, bedrijf.website, "",
    "Dit is een automatisch bericht. Je kunt op deze e-mail antwoorden als je nog iets wilt aanvullen.",
    "Heb je deze aanvraag niet zelf gedaan? Dan kun je deze e-mail negeren.",
  ].join("\n");
  const html = `<!doctype html><html lang="nl"><body style="margin:0;background:#f4f7f2;font-family:Arial,Helvetica,sans-serif;color:#14201a">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f7f2;padding:24px 12px"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#fff;border:1px solid #dde5da;border-radius:10px">
<tr><td style="padding:24px 24px 8px;font-size:20px;font-weight:bold;color:#1f7a16">${escHtml(bedrijf.naam)}</td></tr>
<tr><td style="padding:8px 24px;font-size:15px;line-height:1.6">
<p style="margin:0 0 14px">Hallo,</p>
<p style="margin:0 0 14px">Bedankt voor je ${wat} bij ${escHtml(bedrijf.naam)}. We hebben je aanvraag goed ontvangen. ${vervolg}</p>
<p style="margin:0 0 14px">Is het dringend, bijvoorbeeld een stroomstoring? Bel ons dan direct: <a href="tel:${escHtml(bedrijf.telefoonE164)}" style="color:#1f7a16;font-weight:bold">${escHtml(bedrijf.telefoon)}</a> (24/7).</p>
<p style="margin:0">Met vriendelijke groet,<br>${escHtml(bedrijf.naam)}<br><a href="${escHtml(bedrijf.website)}" style="color:#1f7a16">${escHtml(bedrijf.website.replace(/^https?:\/\//, ""))}</a></p>
</td></tr>
<tr><td style="padding:16px 24px 22px;font-size:12px;color:#56615a">Dit is een automatisch bericht. Je kunt op deze e-mail antwoorden als je nog iets wilt aanvullen. Heb je deze aanvraag niet zelf gedaan? Dan kun je deze e-mail negeren.</td></tr>
</table></td></tr></table></body></html>`;
  return { onderwerp: onderwerpRegel, html, tekst };
}

export async function stuurBrevo(env, bericht) {
  const r = await fetch(env.BREVO_API_URL || BREVO_URL, {
    method: "POST",
    headers: { "api-key": env.BREVO_API_KEY, "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify(bericht),
  });
  if (!r.ok) {
    // Alleen de statuscode loggen: de foutmelding van Brevo kan adressen bevatten.
    throw new Error(`brevo_${r.status}`);
  }
}
