// Server-side validatie per formulier. Alleen velden uit de witte lijst worden
// gebruikt; al het andere wat een browser of bot meestuurt, wordt genegeerd.

export const TIJDSLOTEN = ["08:00 – 10:00", "10:00 – 12:00", "12:00 – 14:00", "14:00 – 16:00", "16:00 – 18:00"];

// Controletekens (incl. CR/LF) weg; tabs en regeleinden alleen in lange tekst.
function schoon(v, meerRegels) {
  if (typeof v !== "string") return "";
  let s = v.normalize("NFC");
  s = meerRegels
    ? s.replace(/\r\n?/g, "\n").replace(/[\u0000-\u0008\u000B-\u001F\u007F\u2028\u2029]/g, "")
    : s.replace(/[\u0000-\u001F\u007F\u2028\u2029]/g, " ");
  return s.trim();
}

const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]{1,64}@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$/;
const TEL_RE = /^\+?[0-9]{8,15}$/;
const POSTCODE_RE = /^[1-9][0-9]{3} ?[A-Za-z]{2}$/;
const DATUM_RE = /^\d{4}-\d{2}-\d{2}$/;

// Veldregels: [bronveld, label, verplicht, maxLengte, soort]
const REGELS = {
  offerte: [
    ["name", "naam", true, 80, "naam"],
    ["phone", "telefoon", true, 30, "tel"],
    ["email", "email", true, 254, "email"],
    ["service", "klus", false, 300, "tekst"],
    ["termijn", "termijn", false, 100, "tekst"],
    ["message", "bericht", true, 3000, "lang"],
    ["postcode", "postcode", false, 7, "postcode"],
    ["number", "huisnummer", false, 10, "tekst"],
    ["wijk", "wijk", false, 60, "tekst"],
    ["akkoord", "akkoord", true, 3, "akkoord"],
  ],
  spoed: [
    ["name", "naam", true, 80, "naam"],
    ["phone", "telefoon", true, 30, "tel"],
    ["message", "bericht", true, 2000, "lang"],
  ],
  afspraak: [
    ["name", "naam", true, 80, "naam"],
    ["phone", "telefoon", true, 30, "tel"],
    ["email", "email", false, 254, "email"],
    ["datum", "datum", true, 10, "datum"],
    ["tijd", "tijd", true, 20, "tijd"],
    ["message", "bericht", false, 2000, "lang"],
  ],
};

export const FORMULIEREN = Object.keys(REGELS);

// Vandaag in Nederland als JJJJ-MM-DD (vergelijking op tekst werkt voor ISO-datums).
function vandaagNL(nu) {
  return new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Amsterdam" }).format(nu);
}

/**
 * @returns {{ok: true, data: Object} | {ok: false, velden: Object<string,string>}}
 */
export function valideer(formulier, fd, nu = new Date()) {
  const regels = REGELS[formulier];
  const data = {};
  const velden = {};
  for (const [bron, doel, verplicht, max, soort] of regels) {
    const ruw = fd.get(bron);
    const waarde = schoon(typeof ruw === "string" ? ruw : "", soort === "lang");
    if (!waarde) {
      if (verplicht) velden[bron] = soort === "akkoord" ? "Geef toestemming om contact op te nemen." : "Dit veld is verplicht.";
      continue;
    }
    if (waarde.length > max) { velden[bron] = `Maximaal ${max} tekens.`; continue; }
    switch (soort) {
      case "naam":
        if (waarde.length < 2 || /[<>{}\\]|https?:|www\./i.test(waarde)) { velden[bron] = "Vul een geldige naam in."; continue; }
        break;
      case "tel": {
        const kaal = waarde.replace(/[\s().-]/g, "");
        if (!TEL_RE.test(kaal)) { velden[bron] = "Vul een geldig telefoonnummer in."; continue; }
        break;
      }
      case "email":
        if (!EMAIL_RE.test(waarde)) { velden[bron] = "Vul een geldig e-mailadres in."; continue; }
        break;
      case "postcode":
        if (!POSTCODE_RE.test(waarde)) { velden[bron] = "Vul een geldige postcode in, bijv. 3511 AA."; continue; }
        break;
      case "datum": {
        const vandaag = vandaagNL(nu);
        const max = vandaagNL(new Date(nu.getTime() + 366 * 864e5));
        const d = new Date(waarde + "T12:00:00Z");
        if (!DATUM_RE.test(waarde) || isNaN(d) || d.toISOString().slice(0, 10) !== waarde || waarde < vandaag || waarde > max) {
          velden[bron] = "Kies een datum vanaf vandaag."; continue;
        }
        break;
      }
      case "tijd":
        if (!TIJDSLOTEN.includes(waarde)) { velden[bron] = "Kies een tijd uit de lijst."; continue; }
        break;
      case "akkoord":
        if (waarde !== "ja") { velden[bron] = "Geef toestemming om contact op te nemen."; continue; }
        break;
    }
    data[doel] = waarde;
  }
  return Object.keys(velden).length ? { ok: false, velden } : { ok: true, data };
}
