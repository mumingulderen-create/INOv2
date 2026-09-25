# Formulieren-endpoint (Cloudflare Worker)

```
ino-elektra.nl (GitHub Pages, statisch)
  quoteForm (/offerte/) ──────────────┐
  spoedForm (/spoed-elektricien-utrecht/) ─┼─► Worker "ino-formulieren" ─► Brevo API ─► info@ino-elektra.nl
  appointmentForm (/afspraak/) ────────┘        │                                 └─► bevestiging aan klant
                                                └─ Turnstile siteverify
```

De website blijft 100% statisch op GitHub Pages. Alleen het versturen van een formulier gaat naar deze Worker.

## Wat de Worker doet (in deze volgorde)

1. Alleen HTTPS, alleen `POST` op `/` (of `/aanvraag`), alleen van `ALLOWED_ORIGINS` (CORS).
2. Verzoek maximaal 12 MB (`413`).
3. Rate limit: maximaal 5 inzendingen per minuut per IP-adres (`429`). Het IP-adres wordt alleen geteld, niet opgeslagen of gelogd.
4. Honeypot `_honey` gevuld: antwoord `200`, maar er wordt niets verstuurd.
5. Validatie per formulier (`422` met `velden`). Alleen velden uit de witte lijst in `src/validatie.js` worden gebruikt.
6. Foto's (alleen offerte):
   - maximaal 5 foto's, 4 MB per foto en 10 MB totaal;
   - alleen JPEG en PNG, gecontroleerd op de echte bestandsinhoud;
   - EXIF-, GPS- en tekstgegevens worden verwijderd;
   - vaste namen `foto-1.jpg` enzovoort.

   Er wordt niets opgeslagen. De browser verkleint foto's vooraf al naar maximaal 2000 px JPEG.
7. Cloudflare Turnstile, gecontroleerd op de server (`403`). Een token werkt maar één keer, dus een dubbele inzending wordt geweigerd. Hostname en action (het formuliertype) worden gecontroleerd.
8. Mail aan `MAIL_TO` via Brevo (`502` als dat mislukt):
   - onderwerp `[Offerte]`, `[SPOED]` of `[Afspraak]`;
   - `Reply-To` is het e-mailadres van de klant.
9. Pas daarna, en alleen als de klant een e-mailadres gaf: een bevestigingsmail met een **vaste tekst**, zonder klantinvoer. Zo kan niemand via jouw domein zelfgekozen tekst naar anderen sturen.
10. Logregels bevatten alleen `formulier`, uitkomst en foutcode. Nooit naam, telefoon, e-mail, IP of bericht.

## Eenmalig instellen

### 1. Brevo (e-mail versturen)
1. Maak een account op brevo.com.
2. **Senders, Domains & Dedicated IPs → Domains → Add a domain**: `ino-elektra.nl`.
3. Brevo toont nu DNS-records (een `brevo-code` TXT, twee DKIM-records en een DMARC-advies). Zet ze bij **Mijndomein** (zie DNS hieronder) en klik in Brevo op **Authenticate**.
4. **Senders → Add a sender**: `formulier@ino-elektra.nl`, naam "Website INO". Dit adres hoeft geen echte mailbox te zijn, want het domein is geauthenticeerd.
5. **SMTP & API → API Keys → Generate a new API key**. Bewaar de sleutel even; die heb je bij stap 3 nodig.
6. Privacy: zet bij **Transactional → Settings** het volgen van opens en kliks uit, als je dat niet wilt.

### 2. Cloudflare Turnstile
1. Maak een gratis Cloudflare-account. Je domein hoeft **niet** naar Cloudflare.
2. **Turnstile → Add widget**:
   - naam "INO formulieren";
   - hostnames `ino-elektra.nl` en `www.ino-elektra.nl`;
   - widget mode **Managed**.
3. Noteer de **Site Key** (openbaar) en de **Secret Key** (geheim).

### 3. Worker deployen
```bash
cd worker
npm install
npx wrangler login                      # opent de browser, log in bij Cloudflare
npx wrangler secret put TURNSTILE_SECRET   # plak de Turnstile Secret Key
npx wrangler secret put BREVO_API_KEY      # plak de Brevo API-key
npx wrangler deploy
```
`deploy` toont het adres, bijvoorbeeld `https://ino-formulieren.<jouw-account>.workers.dev`.

### 4. Website naar de Worker laten wijzen
In `bouw/config.py`:
```python
FORM_ENDPOINT = "https://ino-formulieren.<jouw-account>.workers.dev"
TURNSTILE_SITEKEY = "0x4AAAA..."   # Site Key uit stap 2 (openbaar)
```
Daarna `python3 build.py`, committen en pushen.

### Optioneel: eigen adres `formulier.ino-elektra.nl`
Dit kan alleen als de DNS van ino-elektra.nl bij Cloudflare staat. Dat is niet nodig; het `workers.dev`-adres is net zo veilig (HTTPS).

## Secrets en variabelen

| Naam | Soort | Waar | Waarde |
|---|---|---|---|
| `TURNSTILE_SECRET` | **secret** | `wrangler secret put` | Turnstile Secret Key |
| `BREVO_API_KEY` | **secret** | `wrangler secret put` | Brevo API-key |
| `ALLOWED_ORIGINS` | var | `wrangler.toml` | `https://ino-elektra.nl,https://www.ino-elektra.nl` |
| `TURNSTILE_HOSTNAMES` | var | `wrangler.toml` | `ino-elektra.nl,www.ino-elektra.nl` |
| `MAIL_TO` | var | `wrangler.toml` | `info@ino-elektra.nl` |
| `MAIL_FROM` / `MAIL_FROM_NAME` | var | `wrangler.toml` | `formulier@ino-elektra.nl` / `Website INO` |
| `BEVESTIGING_KLANT` | var | `wrangler.toml` | `true` of `false` |
| `BEDRIJF_*` | var | `wrangler.toml` | naam, telefoon en website in de bevestigingsmail |
| `RATE_LIMITER` | binding | `wrangler.toml` | 5 per 60 s per IP |

Alleen voor lokaal testen: `ALLOW_HTTP`, `TURNSTILE_VERIFY_URL`, `BREVO_API_URL`. Zet die **niet** in productie.

Secrets staan nooit in de repo, HTML of JavaScript. Lokaal testen gebeurt met `worker/.dev.vars`, dat door `.gitignore` buiten git blijft.

## DNS bij Mijndomein

Voeg alleen de records toe die **Brevo zelf** toont bij "Authenticate your domain". Meestal zijn dat:
- TXT `@`: `brevo-code:xxxxxxxx`
- CNAME `brevo1._domainkey` en `brevo2._domainkey` (DKIM)
- TXT `_dmarc`: `v=DMARC1; p=none; rua=mailto:info@ino-elektra.nl`, als je nog geen DMARC-record hebt

Belangrijk:
- **Verander je MX-records niet.** Je mailbox blijft bij Mijndomein.
- Er mag maar **één** SPF-record (`v=spf1 …`) zijn. Vraagt Brevo om SPF, voeg dan `include:spf.brevo.com` toe aan je bestaande record in plaats van een tweede te maken. Bijvoorbeeld: `v=spf1 include:<bestaande-mijndomein-include> include:spf.brevo.com ~all`.

## Automatisch deployen (optioneel)
`.github/workflows/formulieren-worker.yml` draait de tests bij elke wijziging in `worker/`. Wil je dat hij ook deployt, zet dan bij GitHub → Settings → Secrets → Actions:
- `CLOUDFLARE_API_TOKEN`: token met het sjabloon "Edit Cloudflare Workers";
- `CLOUDFLARE_ACCOUNT_ID`.

De secrets van de Worker zelf blijven in Cloudflare; die zet je één keer met `wrangler secret put`.

## Testen
```bash
cd worker && npm test          # 25 tests: validatie, foto's, CORS, Turnstile, rate limit, logs
```
Lokaal met de echte Workers-runtime:
```bash
printf 'TURNSTILE_SECRET=1x0000000000000000000000000000000AA\nBREVO_API_KEY=test\n' > .dev.vars
npx wrangler dev --var ALLOW_HTTP:true
```
Dit is de test-secret van Cloudflare, die altijd slaagt.

### Checklist na livegang
- [ ] Offerte met foto: mail in info@ met bijlage `foto-1.jpg`. "Beantwoorden" gaat naar de klant. De klant krijgt een bevestiging.
- [ ] Spoed: mail met onderwerp `[SPOED] Terugbelverzoek – naam – telefoon`.
- [ ] Afspraak met en zonder e-mail: met e-mail volgt een bevestiging, zonder niet.
- [ ] Verplicht veld leeg: de browser houdt het tegen. Ongeldig e-mailadres zoals `a@b`: rode melding "Controleer: e-mailadres".
- [ ] Zesde inzending binnen een minuut: melding "wacht een minuut".
- [ ] PDF of SVG als foto: melding "Alleen foto's in JPG- of PNG-formaat".
- [ ] Cloudflare → Workers → ino-formulieren → Logs: alleen `{"evt":"verstuurd","formulier":"offerte",…}`, zonder persoonsgegevens.
- [ ] Mail komt niet in spam. Controleer de headers op `dkim=pass` voor ino-elektra.nl.
