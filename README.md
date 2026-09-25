# ino-elektra.nl — website v2

Statische website voor INO Techniek en Installatie. Snel, zonder frameworks, gehost via GitHub Pages (`CNAME` = ino-elektra.nl).

## In het kort: zo pas je iets aan

| Wat wil je veranderen? | Waar? |
|---|---|
| Telefoonnummer, e-mail, **KvK**, adres | `bouw/config.py` → `BEDRIJF` |
| **Tarieven** (werken automatisch door op álle pagina's + Google-data) | `bouw/config.py` → `TARIEVEN` |
| Tekst van een bestaande pagina | `content/<pagina>.html` |
| Wijkpagina's (tekst, buurten, FAQ) of een **nieuwe wijk** | `bouw/wijken.py` |
| Probleempagina's (geen stroom, aardlek, …) | `bouw/storingen.py` |
| Menu | `bouw/config.py` → `NAV` |
| Opmaak | `assets/style.css` |
| Nieuwe foto | zet hem in `assets/foto/`, gebruik `<img src="/naam.jpg" alt="…">` |
| **Formulieren** (offerte, spoed, afspraak) | frontend: `assets/script.js` (`wire`) + `assets/extra/formulier.js`; adres en Turnstile-sitekey: `bouw/config.py`; server: `worker/` (zie `worker/README.md`) |

Daarna altijd:

```bash
pip install pillow beautifulsoup4     # alleen de eerste keer
python3 build.py
```

De build schrijft alle pagina's, `sitemap.xml`, `robots.txt`, `style.css`, `script.js` en `img/`, en **controleert** op kapotte links, dubbele of te lange titels, ontbrekende alt-teksten en ongeldige structured data. Staat er "Geen fouten gevonden"? Dan committen en pushen:

```bash
git add -A && git commit -m "Update site" && git push
```

## Placeholders in content-bestanden

In `content/*.html` kun je dit gebruiken; de build vult het in vanuit `config.py`:

- `{{tel}}` `{{tel_e164}}` `{{whatsapp}}` `{{email}}` `{{instagram}}` `{{google_maps}}`
- Tarieven: `{{uur_dag}}` `{{uur_avond}}` `{{uur_nacht}}` `{{groepenkast_1f}}` `{{perilex_aansluiten}}` … (alle sleutels uit `TARIEVEN`)
- Zinnen: `{{tarief_zin}}` `{{voorrij_zin}}`
- Blokken: `{{STORING_KAARTEN}}` `{{WIJK_CHIPS}}` `{{WIJKEN_HUB}}` `{{TARIEF_KAARTEN}}` `{{CTA}}`

## Structuur

```
build.py            ← draai dit
bouw/               ← instellingen, data en sjablonen (Python)
content/            ← bewerkbare pagina's (HTML + instellingen bovenaan tussen <!-- -->)
assets/             ← bron-CSS, bron-JS, originele foto's
img/                ← gegenereerd (niet handmatig aanpassen)
*.html, */index.html, style.css, script.js, sitemap.xml, robots.txt ← gegenereerd
```

Bovenaan elk content-bestand staat een blok met `title`, `description`, `og_image` en eventueel `"noindex": true`.

## Verwijderd t.o.v. de Gemini-versie

`public/` (volledige dubbele kopie van de site), `src/`, `vite.config.ts`, `tsconfig.json`, `package*.json`, `bun.lock`, `metadata.json`, `.env.example` (ongebruikte Gemini AI Studio/React-scaffolding), `generate_site_part1-3.py`, `build_and_deploy.py`, `build_components.py`, `emoji_cleaner.py`, `url_cleaner.py` (vervangen door `build.py`), `hero-elektricien.jpg.jpg` (duplicaat). De oude bestanden staan nog in je git-geschiedenis.
