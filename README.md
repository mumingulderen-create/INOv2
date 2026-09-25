# ino-elektra.nl — website v2

Statische website van INO Techniek en Installatie. Geen frameworks. Gehost via GitHub Pages (`CNAME` = ino-elektra.nl). Formulieren gaan naar een eigen Cloudflare Worker (`worker/`).

Regels en bevestigde feiten voor AI-assistenten: `CLAUDE.md`.

## Wat pas je waar aan?

| Wat | Waar |
|---|---|
| Telefoon, e-mail, KvK, Google-score, reviews | `bouw/config.py` → `BEDRIJF`, `REVIEWS` |
| Tarieven en aanrijtijden (werken overal door, ook in Google-data) | `bouw/config.py` → `TARIEVEN`, `AANRIJTIJD` |
| Menu | `bouw/config.py` → `NAV` |
| Tekst van een pagina | `content/<pagina>.html` |
| Wijkpagina's of een nieuwe wijk | `bouw/wijken.py` |
| Storingspagina's (geen stroom, aardlek, …) | `bouw/storingen.py` |
| Opmaak en scripts | `assets/style.css`, `assets/script.js`; alleen voor één pagina: `assets/extra/` |
| Foto's | `assets/foto/` (de build maakt WebP-varianten in `img/`) |
| Formulieren | frontend: `assets/script.js` (`wire`) en `assets/extra/formulier.js`; adres en Turnstile-sitekey: `bouw/config.py`; server: `worker/` (zie `worker/README.md`) |

## Bouwen

```bash
pip install pillow beautifulsoup4     # eenmalig (optioneel: playwright voor --test)
python3 build.py                      # of: python3 build.py --test  (browsertest mobiel + desktop)
```

De build schrijft alle pagina's, `sitemap.xml`, `robots.txt`, `style.css`, `script.js`, `img/` en `qr/`. Daarna controleert hij op:
- kapotte links;
- titels en descriptions (lengte, dubbel);
- H1;
- alt-teksten;
- structured data;
- budgetten voor paginagrootte;
- achtergebleven placeholders.

Staat er "Geen fouten gevonden"? Dan committen en pushen.

## Placeholders in `content/*.html`

- Contact: `{{tel}}` `{{tel_e164}}` `{{whatsapp}}` `{{email}}` `{{instagram}}` `{{google_maps}}` `{{google_review_url}}` `{{google_score}}` `{{google_aantal}}`
- Tarieven en aanrijtijden: elke sleutel uit `TARIEVEN` en `AANRIJTIJD`, bijvoorbeeld `{{uur_dag}}`, `{{groepenkast_1f}}` of `{{aanrijtijd_utrecht}}`
- Zinnen: `{{tarief_zin}}` `{{voorrij_zin}}`
- Blokken: `{{STORING_KAARTEN}}` `{{WIJK_CHIPS}}` `{{WIJKEN_HUB}}` `{{TARIEF_KAARTEN}}` `{{CTA}}` `{{CALCULATOR}}` `{{STEDIN_CHECKER}}` `{{REVIEWS_CAROUSEL}}` `{{STORING_REKENHULP}}`

Bovenaan elk content-bestand staat een JSON-blok met `slug`, `title`, `description` en eventueel `og_image`, `extra` en `"noindex": true`.

## Structuur

```
build.py        bouwt de site
bouw/           instellingen (config.py), data (wijken, storingen) en sjablonen
content/        pagina's (bron)
assets/         bron-CSS/JS, foto's, fonts, QR-bestanden
worker/         formulier-backend (Cloudflare Worker)
_config.yml     zorgt dat alleen de gegenereerde site online komt
alles overige   gegenereerd, niet met de hand aanpassen
```
