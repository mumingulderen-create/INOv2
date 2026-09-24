# Instructies voor Claude (Claude Code) — ino-elektra.nl

Statische site, gegenereerd door `python3 build.py`. Hosting: GitHub Pages vanuit de repo-root.

## Taakverdeling (afspraak eigenaar, sept 2026)
- Claude werkt alleen in INOv2. Google AI Studio werkt alleen in v1 (Ino-elektra). Niet door elkaar heen, anders overschrijven we elkaars werk.
- Claude deelt eerst een voorstel met de eigenaar en voert pas uit na akkoord.

## Regels
- **Bewerk nooit** gegenereerde bestanden in de root (`*.html`, `*/index.html`, `style.css`, `script.js`, `wizard.*`, `reviews.*`, `sitemap.xml`, `robots.txt`, `img/`). Bewerk de bron: `content/`, `bouw/`, `assets/`.
- Bedrijfsgegevens en prijzen staan **alleen** in `bouw/config.py`. Nooit prijzen hardcoden in content; gebruik placeholders (`{{uur_dag}}` e.d., zie README).
- Draai na elke wijziging `python3 build.py` en los alle "aandachtspunten" op voordat je commit.
- Taal: Nederlands, je/jij-vorm, zakelijk-vriendelijk, korte zinnen.
- Eén `<h1>` per pagina. Title ≤ 60 tekens, description 120–160 tekens.
- Afbeeldingen: origineel in `assets/foto/`, altijd met beschrijvende `alt`.
- Structured data wordt centraal gemaakt in `bouw/layout.py`. FAQ-schema wordt automatisch gemaakt uit `.faq-q`/`.faq-a`-blokken. Geen microdata (`itemprop`) toevoegen.

## SEO-principes die niet overtreden mogen worden
- Wijk-/plaatspagina's moeten **echt unieke** inhoud hebben (Google: doorway pages / scaled content abuse). Nooit een pagina maken door alleen de plaatsnaam te wisselen.
- Geen `AggregateRating`/`Review`-schema over het eigen bedrijf (niet toegestaan voor LocalBusiness-zelfreviews).
- Geen verzonnen claims, aantallen of reviews.
- Veiligheid: nooit instructies geven om zelf aan de groepenkast of leidingen te werken.

## Nog open (door eigenaar in te vullen/te bevestigen)
- `BEDRIJF["werkspot"]` (URL). Het blok "5.0 op Werkspot" is verborgen tot dit is ingevuld. Eventueel `btw`.
- Veilige eerste stappen op storingspagina's (aardlek omhoog zetten): blijft voorlopig staan, later herzien.
- Echte foto's (assets/foto/) en echte praktijkvoorbeelden per wijk (`"praktijk"` in wijken.py).

## Bevestigd door eigenaar
- Prijzen van de live site (Ino-elektra) kloppen; v2 volgt die.
- Kookgroep meterkast → perilex: `perilex_kookgroep` (€ 150). Alleen perilex-stekker plaatsen: `perilex_aansluiten` (€ 120). € 275 bestaat niet.
- Niet NEN 1010-gecertificeerd, wel alles volgens NEN 1010. Nooit "NEN 1010 gecertificeerd" schrijven.
- Aanrijtijden (vanuit Overvecht): gemeente Utrecht 5–30 min, daarbuiten 15–40 min. Staat in `AANRIJTIJD` in config.py.
- Groepenkast all-in: 1-fase € 640, 3-fase € 760 (sept 2026). Calculator rekent met dezelfde bedragen.
- Google: 5,0 uit 37 reviews (gecontroleerd 24 sept 2026). KvK 86669346.
- NEN 3140-gecertificeerd: klopt (bevestigd). NEN 1010 blijft "volgens", niet gecertificeerd.
- Werkgebied omvat ook De Bilt, Woerden, Amersfoort en Veenendaal (bevestigd).

## Afspraken
- Zie ook `RICHTLIJNEN-AI.md` (korte regels om aan AI Studio mee te geven).
- `python3 build.py --test` draait een browsertest (mobiel 390 px + desktop): te brede pagina's, JS-fouten, CLS. Budgetten (CSS 55 KB, JS 30 KB, HTML 80 KB) staan bovenin build.py.
- Interne links zonder slash worden door de build verbeterd én gemeld; pas dan de bron aan.
- /review/ (noindex) stuurt door naar `google_review_url` in config (leeg = Maps-profiel). QR-code en A6-reviewkaart staan in assets/qr/ en komen op /qr/.
- Rekenhulp storingskosten (`{{STORING_REKENHULP}}`, extra "rekenhulp") staat alleen op /tarieven/ (eigenaar: op de spoedpagina moet de klant direct kunnen bellen, geen rekenwerk).
- Voltfix Elektrotechniek (regio Amsterdam, eigenaar Hassan) is een bevriende elektricien; we sturen elkaar klanten door. Link alleen op /werkgebied/ (#collega-netwerk) en /contact/, niet sitewide in header/footer. Geen claims over hun diensten verzinnen.
- Mobiel: pagina mag nooit breder zijn dan het scherm (test op 390 px: scrollWidth = 390).
- Pagina-specifieke css/js staat in `assets/extra/<naam>.css|js` en laadt alleen op pagina's met `"extra": ["<naam>"]` in de front-matter (nu: `wizard` op /offerte/, `reviews` op /reviews/).
- `/pagina.html` is een korte doorverwijzing naar `/pagina/` (geen dubbele content). Interne links altijd `/pagina/`.
- Reviews: alleen echte Google-reviews letterlijk in `REVIEWS` (config.py). Score/aantal in `BEDRIJF["google_score"/"google_aantal"]`, alleen zichtbaar tonen, nooit als AggregateRating-schema.
- Bij live zetten: in de live repo ook `public/`, `src/`, `package*.json`, `bun.lock`, `vite.config.ts`, `tsconfig.json`, `metadata.json`, `*_cleaner.py`, `generate_site_part*.py`, `build_and_deploy.py`, `build_components.py` en losse root-`.jpg`'s verwijderen.
- Google Analytics laadt alleen na akkoord in de cookiemelding (`bouw/layout.py` + `initCookies` in `assets/script.js`).
- Conditioneel blok in content: `<!--ALS sleutel-->…<!--/ALS-->` toont alleen als `BEDRIJF[sleutel]` gevuld is.
- De groepenkast-calculator haalt zijn prijzen uit `config.py` (data-prijzen).
