# Audit & actieplan ino-elektra.nl (v2)

## 1. Wat er mis was in de code (en nu is opgelost)

| # | Probleem | Gevolg | Status v2 |
|---|---|---|---|
| 1 | `emoji_cleaner.py` verwijderde alle tekens in het Unicode-blok 2600–27BF | 67 vinkjes ✓, 20 review-sterren ★, het menu-icoon ☰ (mobiele menuknop onzichtbaar op élke pagina) en het sluitkruis van de kaart waren weg | Opgelost: alleen echte pictogram-emoji worden verwijderd |
| 2 | Dezelfde cleaner verving `"> "` door `">"` | Woorden plakten aan elkaar ("hoofdschakelaar**in**") | Opgelost |
| 3 | FAQ-script paste het eerste `<span>` aan | Op de spoedpagina veranderde de vraag in "−" na klikken | Opgelost + toegankelijk (aria-expanded) |
| 4 | Verwijzingen naar `Gemini_Generated_Image_*.jpg` die niet bestaan | Elke paginaweergave eerst een 404, dan pas de foto (trager, fouten in Search Console) | Opgelost |
| 5 | Homepagefoto 2752 px / 2,4 MB, zonder breedte/hoogte | Trage LCP (belangrijkste snelheidsmeting van Google), verspringende layout | Nu WebP 11–22 KB, responsive, met afmetingen en preload |
| 6 | Relatieve paden (`style.css`, `logo.png`) | Opmaak breekt op `/diensten/`-varianten | Alle paden absoluut |
| 7 | `public/` = complete kopie van de site | Dubbele content, verwarrend voor Google | Verwijderd |
| 8 | Tarieven tegenstrijdig (08–17 vs 08–18, "weekend" vs "zaterdag/zondag") | Onbetrouwbaar voor klant én Google | Eén bron: `bouw/config.py` |
| 9 | Google Fonts via `@import` in CSS | Blokkeert het tonen van de pagina | Asynchroon geladen, variabel lettertype |
| 10 | Font-shorthand zonder fallback (`font:700 15px Inter`) | Serif-letter als het font niet laadt | Opgelost |
| 11 | Dubbele FAQ-markup (microdata + JSON-LD) op spoed | Tegenstrijdige signalen | Eén centrale JSON-LD-graph per pagina |
| 12 | 4 dienstpagina's zonder `<main>` | Slechtere toegankelijkheid / structuur | Elke pagina heeft `<main>`, skip-link, kruimelpad |
| 13 | WhatsApp-knop: witte tekst op lichtgroen | Onvoldoende contrast (WCAG) | Donkere tekst |
| 14 | Formulieren met `_captcha=false` en geen spamfilter | Spam in je mailbox | Honeypot toegevoegd |
| 15 | Geen KvK-nummer, geen privacyverklaring | Wettelijk verplicht (Handelsregisterwet, AVG) | Privacypagina gemaakt; KvK-veld klaar in config |
| 16 | Veel generieke titels ("Tarieven \| INO Techniek en Installatie") | Weinig kans om te ranken op zoekwoorden | Alle titels herschreven met zoekwoord + plaats + voordeel |

## 2. Wat er nieuw is

- **8 wijk- en plaatspagina's**: `/elektricien-overvecht`, `-kanaleneiland`, `-transwijk`, `-leidsche-rijn`, `-maarssen`, `-nieuwegein`, `-vianen`, `-breukelen`. Elke pagina bevat unieke tekst over het woningtype, typische klussen, buurten, lokale voorrij-info en een eigen FAQ.
- **4 probleempagina's** voor zoekopdrachten van mensen mét een probleem: `/stroomstoring-utrecht`, `/aardlekschakelaar-springt-eruit`, `/kortsluiting-utrecht`, `/stopcontact-werkt-niet`. Ze bevatten veilige eerste stappen, waarschuwingen, tarieven, FAQ en een grote belknop.
- **Nieuwe homepage** met eigen inhoud: probleemknoppen, prijzen, wijken, werkwijze, reviews en FAQ.
- **Topbalk met spoednummer** op elke pagina, en een menu "Spoed 24/7" en "Werkgebied" met uitklap.
- **Footer met interne links** naar alle wijken en storingen. Zo vindt Google alles en geef je elke pagina "kracht".
- **Structured data op elke pagina**: Electrician + EmergencyService (bedrijf, 24/7, werkgebied, tarieven), WebSite, WebPage, BreadcrumbList, Service en FAQPage.
- **Sitemap met echte lastmod** (verandert alleen als de pagina echt verandert). Google negeert lastmod als die altijd "vandaag" is.
- **404-pagina**, **privacypagina**, **klikmeting** voor bellen/WhatsApp (werkt zodra je GA4 of Tag Manager toevoegt).
- **Build-controle**: kapotte links, dubbele of te lange titels, ontbrekende alt-teksten, ongeldige structured data.

## 3. Hoe Google lokale elektriciens rangschikt (en wat jij daaraan doet)

Bij "elektricien Utrecht" of "stroomstoring" toont Google eerst het **kaartblok met 3 bedrijven** (Local Pack) en daaronder de gewone resultaten. Dit zijn twee verschillende systemen.

**Kaartblok (Google Bedrijfsprofiel).** Google weegt hier relevantie, afstand en bekendheid. Dit blok krijgt bij spoedzoekopdrachten de meeste kliks. Je website helpt mee, maar je **Bedrijfsprofiel is hier de grootste hefboom**.

**Gewone resultaten (je website).** Die volgen Google Search Essentials:
- Technisch vindbaar: sitemap, geen dubbele content, snelle mobiele pagina's. Dit is nu geregeld.
- Nuttige, eerlijke inhoud die de vraag van de zoeker beantwoordt ("helpful content"). De probleempagina's zijn hierop gebouwd.
- E-E-A-T (ervaring, deskundigheid, betrouwbaarheid): KvK-nummer, echte foto's, echte reviews, certificeringen, duidelijke prijzen.
- Core Web Vitals (LCP < 2,5 s, CLS < 0,1, INP < 200 ms). De grote winst is geboekt met de foto's en het lettertype.

**Wat Google níet beloont of juist afstraft:**
- Pagina's die alleen de plaatsnaam wisselen (doorway pages). Houd de wijkpagina's uniek.
- Nep-reviews of review-sterren-markup over je eigen bedrijf.
- Onware claims.

**Goed om te weten:** FAQ-uitklappers verschijnen sinds 2023 nauwelijks nog in Google zelf. De FAQ-markup helpt Google (en AI-zoekmachines) wel om je pagina te begrijpen, maar verwacht er geen extra zichtbaarheid van in de zoekresultaten.

## 4. Actieplan

### Deze week (voor livegang)
1. **KvK-nummer invullen** in `bouw/config.py` en builden.
2. **Claims op de spoedpagina controleren**: "lokaal familiebedrijf met vaste werkplaats", "bussen strategisch onderweg", "85% binnen het eerste uur", "KvK geregistreerd". Klopt iets niet, dan moet het eruit.
3. **Tarieven checken** in `config.py`. Gekozen: ma–vr 08–18 € 90, ma–vr 18–22 en zaterdag € 120, 22–08/zondag/feestdag € 145.
4. **Aanrijtijden** Vianen/Breukelen invullen, of leeg laten (dan staat er "bel voor de actuele aanrijtijd").
5. **Zet de v2 live** (zie "Livegang" onderaan) en test op je telefoon: menu, bellen, WhatsApp, offerteformulier (stuur een test).

### Direct na livegang
6. **Google Search Console** (je verificatiecode staat er al in):
   - Dien `https://ino-elektra.nl/sitemap.xml` in bij Sitemaps.
   - Vraag via URL-inspectie indexering aan voor de homepage, spoed, de 4 probleempagina's en de 8 wijkpagina's.
   - Check na 1–2 weken het rapport Pagina's en Core Web Vitals.
7. **Google Bedrijfsprofiel optimaliseren (grootste hefboom voor spoed):**
   - Hoofdcategorie **Elektricien**. Extra categorieën: *Elektrische installateur*, *Laadpaalinstallateur* (als beschikbaar).
   - Stel in als **servicegebied**: Utrecht, Nieuwegein, Maarssen, Vianen, Breukelen, Houten, Zeist enz. Toon geen thuisadres als je daar geen klanten ontvangt.
   - **Openingstijden 24 uur**, gelijk aan de site.
   - Diensten met prijzen overnemen van de tarievenpagina.
   - Website-link naar `https://ino-elektra.nl/`.
   - Wekelijks 1–3 **echte foto's** van klussen (meterkast voor/na, laadpaal), plus een bericht (update).
   - **Reviews actief vragen** na elke klus. Stuur de reviewlink direct via WhatsApp: het meest bepalende signaal na afstand. Reageer op elke review.
8. **Overal dezelfde bedrijfsgegevens** (NAP: naam, telefoon, website, exact hetzelfde): Werkspot, Trustoo, Bing Places, Apple Bedrijfsgegevens (Apple Maps), De Telefoongids/Detelefoongids.nl, Facebook, Instagram-bio. Vul daarna `werkspot` in `config.py`.

### Eerste 1–3 maanden
9. **Echte foto's** in plaats van de (AI-)stockfoto's. Een foto van jou in je bus of bij een meterkast in Utrecht doet meer voor vertrouwen dan welke tekst ook. Zet ze in `assets/foto/` en verwijs ernaar.
10. **Projectverhalen per wijk**: voeg per wijkpagina regelmatig een kort praktijkvoorbeeld toe ("Groepenkast vervangen in een portiekflat aan de Zambesidreef, 1 werkdag, € …"). Dat is precies de "ervaring" die Google zoekt en maakt de pagina's uniek.
11. **Meer wijkpagina's**, alleen als je er echt eigen tekst voor hebt: Binnenstad, Lombok/West, Zuilen, Oost, Houten, Zeist, IJsselstein.
12. **Meer probleempagina's** voor veelgestelde vragen: "groepenkast kapot", "stroom valt uit bij koken", "elektricien 's nachts kosten", "rookmelder aansluiten", "stopcontact buiten plaatsen".
13. **Meten**: installeer Google Analytics 4 (of Plausible voor privacyvriendelijk). De klikmeting voor bellen/WhatsApp staat al klaar in `script.js`. Voeg dan wel een cookiemelding toe als je GA4 gebruikt.
14. Overweeg **Google Ads** met een kleine dagbegroting op spoedzoekwoorden ("elektricien spoed utrecht", "stroomstoring utrecht") met de spoedpagina als bestemming. Organisch hoog komen kost maanden; Ads werkt vanaf dag 1.

### Realistische verwachting
Technische verbeteringen merkt Google binnen enkele weken op. Nieuwe pagina's hoog laten ranken in een concurrerende markt als "elektricien Utrecht" kost doorgaans **3 tot 6 maanden**. Reviews, een actief Bedrijfsprofiel en echte praktijkvoorbeelden bepalen hoe snel het gaat.

## 5. Livegang (GitHub Pages)

1. Maak een back-up-branch van je huidige site: `git checkout -b backup-gemini && git push -u origin backup-gemini && git checkout main`.
2. Verwijder in `main` alle bestanden **behalve de map `.git`**, en pak de v2-zip uit in de repo.
3. `pip install pillow beautifulsoup4` en dan `python3 build.py` (moet "Geen fouten gevonden" geven).
4. `git add -A && git commit -m "Website v2" && git push`.
5. GitHub → Settings → Pages: bron is `main` / root (zoals nu). Controleer dat "Enforce HTTPS" aan staat.

Alle bestaande URL's (`/diensten`, `/groepenkast`, `/spoed-elektricien-utrecht` enz.) blijven gelijk, dus je verliest geen bestaande posities in Google.
