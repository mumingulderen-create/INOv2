#!/usr/bin/env python3
"""
INO Elektra – website bouwen
============================
Gebruik:   python3 build.py
Vereist:   Python 3.9+  en  Pillow + beautifulsoup4  (pip install pillow beautifulsoup4)

Wat het doet:
  1. Foto's uit assets/foto/ -> snelle WebP/JPG-varianten in img/
  2. Leest content/*.html (bewerkbare pagina's) + bouw/wijken.py + bouw/storingen.py
  3. Zet er header, footer, SEO-tags en structured data (JSON-LD) omheen
  4. Schrijft de pagina's naar de hoofdmap (zoals GitHub Pages ze serveert)
  5. Maakt sitemap.xml (met échte 'lastmod' per pagina) en robots.txt
  6. Controleert alles: kapotte links, dubbele titels, te lange titels, ontbrekende alt-teksten
"""
import sys, os, re, json, glob, hashlib, datetime, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "bouw"))

from bs4 import BeautifulSoup
from config import SITE_URL, BEDRIJF as B, TARIEVEN as T, TARIEF_ZIN, VOORRIJ_ZIN
from wijken import WIJKEN, OVERIGE_UTRECHT, OVERIGE_REGIO
from storingen import STORINGEN
import layout, paginas, beelden

MAAK_MAPPEN = True   # ook /pagina/index.html schrijven (extra zekerheid voor hosting)
FONT_URL = "https://fonts.googleapis.com/css2?family=Inter:wght@400..800&display=swap"
TODAY = datetime.date.today().isoformat()
LASTMOD_FILE = os.path.join(ROOT, "bouw", "lastmod.json")

PLACEHOLDERS = {
    "tel": B["telefoon_tonen"], "tel_e164": B["telefoon_e164"], "whatsapp": B["whatsapp"],
    "email": B["email"], "instagram": B["instagram"], "google_maps": B["google_maps"],
    "werkspot": B["werkspot"] or "https://www.werkspot.nl",
    "tarief_zin": TARIEF_ZIN, "tarief_zin_klein": TARIEF_ZIN[0].lower() + TARIEF_ZIN[1:],
    "voorrij_zin": VOORRIJ_ZIN, "actief_sinds": B["actief_sinds"], "jaar": str(datetime.date.today().year),
    **{k: str(v) for k, v in T.items()},
}

BREADCRUMB_NAMEN = {
    "diensten": [("Diensten", None)],
    "groepenkast": [("Diensten", "/diensten"), ("Groepenkast", None)],
    "perilex": [("Diensten", "/diensten"), ("Perilex", None)],
    "laadpaal-installeren": [("Diensten", "/diensten"), ("Laadpaal installeren", None)],
    "krachtstroom-aanleggen": [("Diensten", "/diensten"), ("Krachtstroom", None)],
    "frezen-stopcontacten-verleggen": [("Diensten", "/diensten"), ("Frezen & stopcontacten", None)],
    "tuinverlichting-buitenelektra": [("Diensten", "/diensten"), ("Tuinverlichting", None)],
    "spoed-elektricien-utrecht": [("Spoed elektricien", None)],
    "tarieven": [("Tarieven", None)], "werkwijze": [("Werkwijze", None)],
    "werkgebied": [("Werkgebied", None)], "wijken": [("Werkgebied", "/werkgebied"), ("Wijken", None)],
    "vakmanschap": [("Vakmanschap", None)], "reviews": [("Reviews", None)],
    "offerte": [("Offerte", None)], "afspraak": [("Afspraak", None)], "faq": [("Veelgestelde vragen", None)],
    "contact": [("Contact", None)], "privacy": [("Privacy", None)],
}
PRIORITY = {"": "1.0", "spoed-elektricien-utrecht": "0.9", "groepenkast": "0.9", "perilex": "0.9",
            "tarieven": "0.8", "diensten": "0.8", "offerte": "0.6", "afspraak": "0.5", "contact": "0.6"}

warnings = []


def warn(msg):
    warnings.append(msg)


def url_of(slug):
    return f"{SITE_URL}/{slug}" if slug else f"{SITE_URL}/"


def fill(text):
    def r(m):
        k = m.group(1)
        if k in PLACEHOLDERS:
            return PLACEHOLDERS[k]
        if k in BLOKKEN:
            return BLOKKEN[k]()
        warn(f"onbekende placeholder {{{{{k}}}}}")
        return m.group(0)
    return re.sub(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}", r, text)


BLOKKEN = {
    "STORING_KAARTEN": lambda: paginas.blok_storing_kaarten(STORINGEN),
    "WIJK_CHIPS": lambda: paginas.blok_wijk_chips(WIJKEN),
    "WIJKEN_HUB": lambda: paginas.blok_wijken_hub(WIJKEN, OVERIGE_UTRECHT, OVERIGE_REGIO),
    "TARIEF_KAARTEN": lambda: paginas.tarief_kaarten(),
    "CTA": lambda: paginas.cta_band(),
}


def lees_content():
    pages = []
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "*.html"))):
        raw = open(path, encoding="utf-8").read()
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->\s*(.*)$", raw, re.S)
        if not m:
            warn(f"{path}: geen front-matter gevonden, overgeslagen")
            continue
        fm = json.loads(m.group(1))
        fm["body"] = m.group(2)
        crumbs = BREADCRUMB_NAMEN.get(fm["slug"], [])
        fm.setdefault("crumbs", crumbs)
        pages.append(fm)
    return pages


def faq_uit_body(body):
    s = BeautifulSoup(body, "html.parser")
    out = []
    for b in s.select("button.faq-q"):
        q = b.get_text(" ", strip=True).rstrip("+−- ").strip()
        a = b.find_next_sibling(class_="faq-a")
        if q and a:
            out.append([q, " ".join(a.get_text(" ", strip=True).split())])
    return out


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


def schrijf(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("1/6 Afbeeldingen optimaliseren…")
    beelden.verwerk()

    print("2/6 Assets (css/js)…")
    css = open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8").read()
    css_min = minify_css(css)
    css_v = hashlib.md5(css_min.encode()).hexdigest()[:8]
    schrijf("style.css", css_min)
    js = open(os.path.join(ROOT, "assets", "script.js"), encoding="utf-8").read()
    from config import FORM_ENDPOINT
    js = js.replace("__FORM_ENDPOINT__", FORM_ENDPOINT).replace("__TEL__", B["telefoon_tonen"]).replace("__TEL_E164__", B["telefoon_e164"])
    js_v = hashlib.md5(js.encode()).hexdigest()[:8]
    schrijf("script.js", js)

    print("3/6 Pagina's samenstellen…")
    pages = lees_content()
    pages += [paginas.wijk_pagina(w, WIJKEN) for w in WIJKEN]
    pages += [paginas.storing_pagina(s, STORINGEN) for s in STORINGEN]

    lastmod = json.load(open(LASTMOD_FILE)) if os.path.exists(LASTMOD_FILE) else {}
    rendered = {}
    for p in pages:
        slug = p["slug"]
        p["url"] = url_of(slug)
        body = fill(p["body"])
        # microdata weg (we gebruiken JSON-LD); voorkomt dubbele/conflicterende markup
        body = re.sub(r'\s+item(prop|scope|type)(="[^"]*")?', "", body)
        body, lcp = beelden.vervang_img(body)
        p["lcp"] = lcp
        if not p.get("faq"):
            p["faq"] = faq_uit_body(body)
        p["og_image_url"] = beelden.og_url(p.get("og_image", "hero-elektricien.jpg"), SITE_URL)
        # breadcrumbs
        if slug:
            p["breadcrumbs"] = [("Home", f"{SITE_URL}/")] + [
                (n, f"{SITE_URL}{u}" if u else p["url"]) for n, u in p.get("crumbs", [])]
        else:
            p["breadcrumbs"] = []
        # lastmod op basis van echte inhoudswijziging
        h = hashlib.md5((p["title"] + p["description"] + body).encode()).hexdigest()
        if lastmod.get(slug or "index", {}).get("hash") != h:
            lastmod[slug or "index"] = {"hash": h, "date": TODAY}
        p["lastmod"] = lastmod[slug or "index"]["date"]

        variant = "spoed" if slug == "spoed-elektricien-utrecht" else "standaard"
        html = "\n".join([
            layout.head(p, WIJKEN, css_v, FONT_URL),
            "<body>",
            layout.header(p.get("nav", slug), WIJKEN, variant),
            f'<main id="inhoud">',
            layout.breadcrumbs_html(p["breadcrumbs"]) if slug else "",
            body,
            "</main>",
            layout.footer(WIJKEN, STORINGEN, variant).replace("{JS_V}", js_v),
            "</body>", "</html>", ""])
        rendered[slug] = (p, html)

    print("4/6 Schrijven…")
    # oude gegenereerde bestanden opruimen (alleen .html in root en slug-mappen die wij maken)
    for slug, (p, html) in rendered.items():
        if slug == "":
            schrijf("index.html", html)
        else:
            schrijf(f"{slug}.html", html)
            if MAAK_MAPPEN and slug != "404":
                schrijf(f"{slug}/index.html", html)
    json.dump(lastmod, open(LASTMOD_FILE, "w"), indent=1, sort_keys=True)

    print("5/6 Sitemap & robots…")
    urls = []
    for slug, (p, _) in sorted(rendered.items(), key=lambda kv: (kv[0] != "", kv[0])):
        if p.get("noindex") or p.get("sitemap") is False:
            continue
        pr = p.get("priority") or PRIORITY.get(slug, "0.7")
        urls.append(f"  <url><loc>{p['url']}</loc><lastmod>{p['lastmod']}</lastmod><priority>{pr}</priority></url>")
    schrijf("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    schrijf("robots.txt", "User-agent: *\nAllow: /\nDisallow: /assets/\nDisallow: /bouw/\nDisallow: /content/\n\n"
            f"Sitemap: {SITE_URL}/sitemap.xml\n")

    print("6/6 Controleren…")
    controleer(rendered)
    print(f"\nKlaar: {len(rendered)} pagina's, {len(urls)} in sitemap.")
    if warnings:
        print(f"\n{len(warnings)} aandachtspunt(en):")
        for w in warnings:
            print("  -", w)
    else:
        print("Geen fouten gevonden.")


def controleer(rendered):
    bestaand = set(rendered.keys())
    titles, descs = {}, {}
    for slug, (p, html) in rendered.items():
        naam = slug or "index"
        t, d = p["title"], p["description"]
        tl = len(re.sub(r"&amp;", "&", t))
        if tl > 65:
            warn(f"{naam}: title is {tl} tekens (Google toont ±60)")
        if not (70 <= len(d) <= 165):
            warn(f"{naam}: meta description is {len(d)} tekens (ideaal 120–160)")
        if t in titles:
            warn(f"{naam}: zelfde title als {titles[t]}")
        titles[t] = naam
        if d in descs:
            warn(f"{naam}: zelfde description als {descs[d]}")
        descs[d] = naam
        s = BeautifulSoup(html, "html.parser")
        h1 = s.find_all("h1")
        if len(h1) != 1:
            warn(f"{naam}: {len(h1)} H1-koppen (moet er precies 1 zijn)")
        for img in s.find_all("img"):
            if not img.get("alt"):
                warn(f"{naam}: afbeelding zonder alt-tekst ({img.get('src')})")
        for sc in s.find_all("script", type="application/ld+json"):
            try:
                json.loads(sc.string)
            except Exception as e:
                warn(f"{naam}: structured data ongeldig: {e}")
        for a in s.find_all("a", href=True):
            h = a["href"]
            if h.startswith("/") and not h.startswith("//"):
                path = h.split("?")[0].split("#")[0].strip("/")
                if path in bestaand or os.path.exists(os.path.join(ROOT, path)) and path:
                    continue
                if path == "":
                    continue
                warn(f"{naam}: kapotte link {h}")
        if "{{" in html:
            warn(f"{naam}: niet-ingevulde placeholder in pagina")


if __name__ == "__main__":
    main()
