# Formulier-API (Cloudflare Worker `ino-form-api`)

```
ino-elektra.nl (GitHub Pages, statisch)
  quoteForm / spoedForm / appointmentForm  + Turnstile (onzichtbaar)
        │  POST https://api.ino-elektra.nl/api/form   (multipart, veld "formulier")
        ▼
Worker ino-form-api:  CORS → grootte → rate limit → honeypot → validatie → foto's → Turnstile
        │  BREVO_API_KEY (secret)
        ▼
Brevo transactional API ──► info@ino-elektra.nl  (Reply-To = klant)
                        └─► klant: bevestiging (vaste tekst, alleen als e-mail is ingevuld)
```

De website blijft op GitHub Pages. Alleen het versturen van formulieren gaat via de Worker.

## Keuzes

- **Eén endpoint `POST /api/form`**. Het veld `formulier` (`offerte`, `spoed` of `afspraak`) bepaalt de validatie en de e-mail. Nieuwe formulieren voeg je toe in `src/validatie.js` en `src/mail.js`.
- **`multipart/form-data`, geen JSON**, omdat de offerte foto's kan meesturen. Hetzelfde formaat voor alle formulieren houdt de frontend eenvoudig.
- **`api.ino-elektra.nl` als eigen subdomein**. Het is net zo veilig als het gratis `…workers.dev`-adres, maar professioneler. Je domein moet dan wel via Cloudflare DNS lopen. Tot dat actief is, werkt het `workers.dev`-adres.
- **E-mailtemplates in de code, niet in Brevo**. Er zijn vier aparte templates:
  - offerte (groen, `[Offerte] …`);
  - spoed (rood, `[SPOED] Terugbelverzoek – naam – telefoon`);
  - afspraak (blauw, `[Afspraak] datum tijd – naam`);
  - klantbevestiging.

  Alle klantinvoer wordt ge-escaped. De templates staan in git, worden getest en werken meteen. In Brevo hoef je dus geen templates te maken.
- **Spoed** houdt dezelfde velden als nu (naam, telefoon, omschrijving). De klant vult geen e-mailadres in, dus er komt geen Reply-To en geen bevestigingsmail. Je belt de klant terug.

## Wat de Worker controleert

| Controle | Bij fout |
|---|---|
| Alleen HTTPS, alleen `POST` en `OPTIONS` op `/api/form` | 403 / 405 / 404 |
| Origin moet `https://ino-elektra.nl` of `www.` zijn (CORS, geen `*`) | 403 |
| Content-type `multipart/form-data` of `x-www-form-urlencoded`; ander type of JSON wordt geweigerd | 415 |
| Verzoek maximaal 12 MB | 413 |
| Rate limit: 5 per minuut per IP (IP wordt niet opgeslagen of gelogd) | 429 |
| Honeypot `_honey` gevuld | 200, maar er wordt niets verstuurd |
| Validatie per formulier: verplichte velden, e-mail, telefoon, postcode, datum, tijdslot, maximale lengtes, geen regeleinden in naam of e-mail; onbekende velden worden genegeerd | 422 + velden |
| Foto's: max. 5, 4 MB per stuk, 10 MB totaal, alleen echte JPG of PNG; EXIF/GPS wordt verwijderd; niets opgeslagen | 422 |
| Turnstile op de server (siteverify): token eenmalig geldig, hostname en formuliertype moeten kloppen | 403 |
| Brevo niet bereikbaar of fout | 502 |

Logs bevatten alleen formuliertype, uitkomst en foutcode. Nooit naam, telefoon, e-mail, IP of bericht.

## Secrets en instellingen

| | Naam | Waar |
|---|---|---|
| **OPENBAAR** | `TURNSTILE_SITEKEY` en `FORM_ENDPOINT` | `bouw/config.py` (komen in de website) |
| **GEHEIM** | `TURNSTILE_SECRET_KEY` | `npx wrangler secret put TURNSTILE_SECRET_KEY` |
| **GEHEIM** | `BREVO_API_KEY` | `npx wrangler secret put BREVO_API_KEY` |
| instelling | `ALLOWED_ORIGINS`, `TURNSTILE_HOSTNAMES`, `MAIL_TO`, `MAIL_FROM`, `MAIL_FROM_NAME`, `BEVESTIGING_KLANT`, `BEDRIJF_*` | `wrangler.toml` (niet geheim) |

Geheimen komen **nooit** in git, HTML of JavaScript:
- lokaal testen gebeurt met `worker/.dev.vars`, dat door `.gitignore` buiten git blijft;
- `_config.yml` zorgt dat `worker/` niet op de website komt.

## Deployment: stap voor stap

Doe het in deze volgorde. De live site blijft de hele tijd werken.

### 1. Brevo (e-mail)
1. Maak een account op **brevo.com**. Typ het adres zelf in, niet via een advertentie. Kies het plan **Free**.
2. **Senders, Domains & Dedicated IPs → Domains → Add a domain**: `ino-elektra.nl`. Kies "Authenticate the domain yourself". Brevo toont nu de DNS-records: een `brevo-code` TXT, DKIM-records en een DMARC-advies. Laat dit scherm open; de records zet je in stap 4.
3. **Senders → Add a sender**: e-mail `formulier@ino-elektra.nl`, naam `Website INO`. Dit hoeft geen echte mailbox te zijn, zodra het domein geauthenticeerd is.
4. **SMTP & API → API Keys → Generate a new API key**, naam `ino-form-api`. Kopieer de sleutel; je ziet hem maar één keer.
5. Zet open- en kliktracking voor transactionele mails uit (**Transactional → Settings**), zodat je klanten niet gevolgd worden.

### 2. Cloudflare-account en Turnstile
1. Maak een gratis account op **dash.cloudflare.com**.
2. **Turnstile → Add widget**:
   - naam `INO formulieren`;
   - hostnames `ino-elektra.nl` en `www.ino-elektra.nl`;
   - **Widget mode: Managed**. Bezoekers zien meestal niets; alleen bij twijfel een vinkje, geen puzzels.
3. Noteer de **Site Key** (openbaar) en de **Secret Key** (geheim).

### 3. Worker deployen (Wrangler, vanaf je pc)
Eenmalig Node.js installeren van nodejs.org (LTS). Daarna in de map `INOv2\worker`:
```bash
npm install
npx wrangler login                          # opent de browser, log in bij Cloudflare
npx wrangler secret put TURNSTILE_SECRET_KEY   # plak de Turnstile Secret Key
npx wrangler secret put BREVO_API_KEY          # plak de Brevo API-key
npx wrangler deploy
```
`deploy` toont het adres, bijvoorbeeld `https://ino-form-api.<jouw-account>.workers.dev`. Test het met:
```bash
curl -i https://ino-form-api.<jouw-account>.workers.dev/api/form
```
Verwacht `405`, want alleen POST mag.

### 4. Domein naar Cloudflare DNS (voor `api.ino-elektra.nl`)
Je website blijft op GitHub Pages en je mail blijft bij Mijndomein. Alleen het beheer van de DNS-records verhuist.
1. Cloudflare → **Add a domain** → `ino-elektra.nl` → plan **Free**. Cloudflare leest je huidige records in.
2. **Vergelijk die lijst met de DNS-records in Mijndomein** (Mijndomein → Domeinen → DNS beheren). Alles moet er zijn, vooral:
   - **MX-records** (je mailbox) en de **SPF-TXT** (`v=spf1 …`), precies zoals bij Mijndomein;
   - de records van GitHub Pages: `A` voor `@` naar `185.199.108.153`, `.109.153`, `.110.153` en `.111.153`, en `CNAME` voor `www` naar `mumingulderen-create.github.io`. Neem over wat er nu staat; verzin niets.
   - Zet bij de GitHub Pages-records de **Proxy status op "DNS only"** (grijze wolk). Dan blijft GitHub zelf het HTTPS-certificaat regelen.
3. Voeg de Brevo-records uit stap 1.2 toe (TXT en DKIM, eventueel DMARC). Is er al een SPF-record en vraagt Brevo om SPF? Voeg dan `include:spf.brevo.com` toe aan dat **ene** record en maak geen tweede SPF-record.
4. Mijndomein → je domein → **Nameservers wijzigen** naar de twee nameservers die Cloudflare toont. Het duurt een paar minuten tot 24 uur voordat het domein in Cloudflare "Active" is.
5. Klik in Brevo op **Authenticate**. Alles moet groen worden.
6. Haal in `worker/wrangler.toml` het `#` weg voor de regel `routes = [...]` en draai opnieuw `npx wrangler deploy`. Cloudflare maakt `api.ino-elektra.nl` en het certificaat zelf aan. Maak dit DNS-record dus niet zelf.

### 5. Website koppelen
In `bouw/config.py`:
```python
FORM_ENDPOINT = "https://api.ino-elektra.nl/api/form"
TURNSTILE_SITEKEY = "0x4AAAA..."   # Site Key uit stap 2
```
Draai `python3 build.py --test`, commit en push naar INOv2.

### 6. Productiecontrole
- [ ] Offerte met foto: mail in info@ met onderwerp `[Offerte] …` en bijlage `foto-1.jpg`. "Beantwoorden" gaat naar de klant. De klant krijgt een bevestiging.
- [ ] Spoed: mail `[SPOED] Terugbelverzoek – naam – telefoon`.
- [ ] Afspraak met en zonder e-mail: met e-mail volgt een bevestiging, zonder niet.
- [ ] Mail zit niet in spam. Kijk in de mailheaders ("Origineel weergeven") naar `dkim=pass` voor `ino-elektra.nl`.
- [ ] Verplicht veld leeg: de browser houdt het tegen. Ongeldig e-mailadres zoals `a@b`: melding "Controleer de ingevulde gegevens…".
- [ ] Zes keer binnen een minuut versturen: melding "wacht een minuut".
- [ ] https://ino-elektra.nl en https://www.ino-elektra.nl werken nog, met slotje. GitHub → Settings → Pages: "Enforce HTTPS" aan.
- [ ] Cloudflare → Workers → ino-form-api → **Logs**: alleen regels als `{"evt":"verstuurd","formulier":"offerte"}`, zonder persoonsgegevens.
- [ ] Mail aan info@ komt gewoon binnen (MX goed overgenomen).

## Lokaal testen
```bash
cd worker && npm test          # 25 tests: validatie, foto's, CORS, Turnstile, rate limit, Brevo-fout, logs
```
Met de echte Workers-runtime:
```bash
printf 'TURNSTILE_SECRET_KEY=1x0000000000000000000000000000000AA\nBREVO_API_KEY=test\n' > .dev.vars
npx wrangler dev --var ALLOW_HTTP:true
```
Dit gebruikt de test-secret van Cloudflare, die altijd slaagt. `ALLOW_HTTP`, `TURNSTILE_VERIFY_URL` en `BREVO_API_URL` zijn alleen voor lokaal testen; zet ze nooit in productie.

## Automatisch deployen (optioneel)
`.github/workflows/formulieren-worker.yml` draait de tests bij elke wijziging in `worker/`. Deployen doet hij alleen als je in GitHub → Settings → Secrets → Actions `CLOUDFLARE_API_TOKEN` (sjabloon "Edit Cloudflare Workers") en `CLOUDFLARE_ACCOUNT_ID` zet.
