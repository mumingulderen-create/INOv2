# Regels voor AI-assistenten (Claude, Google AI Studio) — ino-elektra.nl

Dit is het enige regelbestand. Geef het mee aan elke AI die aan de site werkt. Uitleg voor mensen (wat staat waar, hoe bouwen): `README.md`. Formulier-backend: `worker/README.md`.

## Taakverdeling
- Claude werkt alleen in **INOv2**. Google AI Studio werkt alleen in **v1** (Ino-elektra). Niet door elkaar heen, anders overschrijven we elkaars werk.
- Eerst een voorstel aan de eigenaar, pas uitvoeren na akkoord. Niets live zetten zonder dat de eigenaar letterlijk "zet live" zegt.

## Werkwijze
- Bewerk alleen de bron: `content/`, `bouw/`, `assets/`, `worker/`. Alles in de root (`*.html`, `*/index.html`, `style.css`, `script.js`, `wizard.*`, `reviews.*`, `rekenhulp.*`, `formulier.js`, `sitemap.xml`, `robots.txt`, `img/`, `qr/`, `fonts/`) is gegenereerd.
- Bedrijfsgegevens, prijzen, aanrijtijden, Google-score en reviews staan **alleen** in `bouw/config.py`. In teksten altijd placeholders (`{{uur_dag}}`, `{{groepenkast_1f}}`, `{{aanrijtijd_utrecht}}`, `{{google_score}}` …); in `bouw/wijken.py` en `bouw/storingen.py` met enkele accolades (`{uur_dag}`).
- Na elke wijziging `python3 build.py --test` (zonder playwright: `python3 build.py`) en alle aandachtspunten oplossen vóór je commit. Na wijzigingen in `worker/`: `cd worker && npm test`.

## Bevestigd door de eigenaar
- Prijzen van de live site kloppen. Groepenkast all-in: 1-fase € 640, 3-fase € 760 (de calculator rekent met dezelfde bedragen).
- Perilex-stekker aansluiten € 120 (`perilex_aansluiten`), nieuwe kookgroep € 150 (`perilex_kookgroep`). Er bestaat geen € 275.
- Zaterdag, zondag, feestdagen en 22:00–08:00: nachttarief.
- Aanrijtijd vanuit Overvecht: gemeente Utrecht 5–30 min, daarbuiten 15–40 min (`AANRIJTIJD`). Geen andere tijden noemen.
- **Niet** NEN 1010-gecertificeerd, wel werken **volgens** NEN 1010. **Wel** NEN 3140-gecertificeerd.
- Ruim 85% van de storingen is binnen het eerste uur opgelost.
- Google: 5,0 uit 37 reviews (24 sept 2026), `google_score`/`google_aantal`. KvK 86669346.
- Werkgebied: Utrecht met alle wijken, Maarssen, Nieuwegein, Vianen, Breukelen, Houten, Zeist, IJsselstein, De Bilt, Woerden, Amersfoort, Veenendaal. Niets daarbuiten zonder akkoord.
- Voltfix Elektrotechniek (Amsterdam, eigenaar Hassan) is een bevriende elektricien. Link alleen op /werkgebied/ (#collega-netwerk) en /contact/, nooit in header of footer. Geen claims over hun diensten.

## Nooit doen
- Reviews, namen, cijfers, certificaten, claims of aanrijtijden verzinnen. Bij twijfel: vragen.
- `AggregateRating`- of `Review`-schema over het eigen bedrijf. Score alleen zichtbaar tonen.
- Microdata (`itemprop`). Structured data komt alleen uit `bouw/layout.py` (JSON-LD; FAQ-schema automatisch uit `.faq-q`/`.faq-a`).
- Uitleg hoe klanten zelf aan de groepenkast of leidingen werken (de bestaande veilige eerste stappen op storingspagina's niet uitbreiden).
- Wijkpagina's maken door alleen de plaatsnaam te wisselen (doorway pages). Elke wijk: eigen woningtypes, buurten, klussen en FAQ; `"praktijk"` alleen met echte klussen.
- Sitewide links naar andere bedrijven.
- Google Analytics laden vóór akkoord in de cookiemelding (`bouw/layout.py` + `initCookies` in `assets/script.js`).
- Secrets (API-keys, wachtwoorden) in de repo, HTML of JavaScript.

## SEO en tekst
- Title ≤ 60 tekens, description 120–160, precies één H1 met zoekwoord.
- Je/jij-vorm, zakelijk-vriendelijk, korte zinnen, duidelijke prijzen.
- Interne links altijd met slash (`/offerte/`). `/pagina.html` is een doorverwijzing naar `/pagina/`.

## Code en snelheid
- Budgetten: `style.css` 55 KB, `script.js` 30 KB, pagina 80 KB HTML (build waarschuwt).
- CSS/JS voor één pagina: `assets/extra/<naam>.css|js` + front-matter `"extra": ["<naam>"]` (nu: `wizard` en `formulier` op /offerte/, `formulier` op /afspraak/ en spoed, `reviews` op /reviews/, `rekenhulp` op /tarieven/).
- Geen externe scripts of fonts (Inter staat lokaal), behalve Cloudflare Turnstile op de formulierpagina's. Geen `backdrop-filter` of zware animaties.
- Afbeeldingen: origineel in `assets/foto/`, altijd met beschrijvende `alt`; de build maakt WebP-varianten en ruimt varianten van verwijderde foto's op.
- Mobiel: geen pagina breder dan 390 px (`build.py --test` controleert dit).
- Conditioneel blok: `<!--ALS sleutel-->…<!--/ALS-->` toont alleen als `BEDRIJF[sleutel]` gevuld is.
- Rekenhulp storingskosten alleen op /tarieven/ (op spoed moet de klant direct kunnen bellen).
- /review/ (noindex) stuurt door naar `google_review_url`; QR-code en A6-kaart: `assets/qr/` → /qr/.
- Formulieren (quoteForm, spoedForm, appointmentForm) → eigen Cloudflare Worker (`worker/`) → Brevo → info@ino-elektra.nl. Geen FormSubmit. Nieuwe formuliervelden ook toevoegen aan de witte lijst in `worker/src/validatie.js`.

## Nog open (eigenaar)
- Formulieren activeren: Brevo + domeinverificatie (DNS bij Mijndomein), Turnstile-widget, Worker deployen, daarna `FORM_ENDPOINT` en `TURNSTILE_SITEKEY` invullen. Tot dan tonen de formulieren een foutmelding met het telefoonnummer. Stappen: `worker/README.md`.
- `BEDRIJF["werkspot"]` (URL; het Werkspot-blok blijft verborgen tot dit is ingevuld), eventueel `btw`.
- Echte foto's (`assets/foto/`) en echte praktijkvoorbeelden per wijk.
- Bij live zetten in de live repo ook verwijderen: `public/`, `src/`, `package*.json`, `bun.lock`, `vite.config.ts`, `tsconfig.json`, `metadata.json`, `*_cleaner.py`, `generate_site_part*.py`, `build_and_deploy.py`, `build_components.py` en losse root-`.jpg`'s.
