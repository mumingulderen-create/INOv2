// Engelse formulieren (ino-elektra.nl/en/...): de site stuurt het veld "taal" = "en" mee.
// De foutmeldingen aan de klant worden dan in het Engels teruggegeven. Valt een melding
// hier niet onder, dan blijft hij Nederlands (beter dan niets).

export function taalVan(fd) {
  return fd.get("taal") === "en" ? "en" : "nl";
}

const EN = {
  "Geef toestemming om contact op te nemen.": "Please give permission for us to contact you.",
  "Dit veld is verplicht.": "This field is required.",
  "Vul een geldige naam in.": "Please enter a valid name.",
  "Vul een geldig telefoonnummer in.": "Please enter a valid phone number.",
  "Vul een geldig e-mailadres in.": "Please enter a valid email address.",
  "Vul een geldige postcode in, bijv. 3511 AA.": "Please enter a valid Dutch postcode, e.g. 3511 AA.",
  "Kies een datum vanaf vandaag.": "Please choose a date from today onwards.",
  "Kies een tijd uit de lijst.": "Please choose a time from the list.",
  "Een foto is groter dan 4 MB.": "A photo is larger than 4 MB.",
  "De foto's zijn samen groter dan 10 MB.": "The photos are larger than 10 MB in total.",
  "Alleen foto's in JPG- of PNG-formaat zijn toegestaan.": "Only photos in JPG or PNG format are allowed.",
  "Een foto is beschadigd of geen geldige afbeelding.": "A photo is damaged or not a valid image.",
};

export function melding(tekst, taal) {
  if (taal !== "en") return tekst;
  if (EN[tekst]) return EN[tekst];
  let m;
  if ((m = /^Maximaal (\d+) tekens\.$/.exec(tekst))) return `Maximum ${m[1]} characters.`;
  if ((m = /^Maximaal (\d+) foto's\.$/.exec(tekst))) return `Maximum ${m[1]} photos.`;
  return tekst;
}

export function meldingen(velden, taal) {
  return Object.fromEntries(Object.entries(velden).map(([k, v]) => [k, melding(v, taal)]));
}
