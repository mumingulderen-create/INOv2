# Instructies voor Claude (Claude Code) — ino-elektra.nl

Statische site, gegenereerd door `python3 build.py`. Hosting: GitHub Pages vanuit de repo-root.

## Regels
- **Bewerk nooit** gegenereerde bestanden in de root (`*.html`, `*/index.html`, `style.css`, `script.js`, `sitemap.xml`, `robots.txt`, `img/`). Bewerk de bron: `content/`, `bouw/`, `assets/`.
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

## Nog open (door eigenaar in te vullen)
- `BEDRIJF["kvk"]` (wettelijk verplicht op de website), eventueel `btw`, `werkspot`.
- Aanrijtijden Vianen en Breukelen in `bouw/wijken.py`.
- Claims op `content/spoed-elektricien-utrecht.html` controleren (familiebedrijf/werkplaats/bussen/85%).
