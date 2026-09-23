#!/usr/bin/env python3
"""
INO Elektra – website bouwen
============================
Gebruik:   python3 build.py
Wat het doet:
  1. Responsive WebP/JPG-afbeeldingen in img/
  2. Leest content/*.html + bouw/wijken.py + bouw/storingen.py
  3. Plaatst header, footer, SEO-tags en JSON-LD gestructureerde data
  4. Schrijft alle pagina's als schone directory-structuur (/pagina/index.html)
  5. Genereert sitemap.xml en robots.txt
  6. Valideert links, alt-teksten, meta-titels en descriptions
"""
import sys, os, re, json, glob, hashlib, datetime, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "bouw"))

from config import SITE_URL, BEDRIJF as B, TARIEVEN as T, TARIEF_ZIN, VOORRIJ_ZIN, AANRIJTIJD
from wijken import WIJKEN, OVERIGE_UTRECHT, OVERIGE_REGIO
from storingen import STORINGEN
import layout, paginas, beelden

MAAK_MAPPEN = True   # /pagina/index.html schrijven voor schone SEO URLs
TODAY = datetime.date.today().isoformat()
LASTMOD_FILE = os.path.join(ROOT, "bouw", "lastmod.json")

PLACEHOLDERS = {
    "tel": B["telefoon_tonen"],
    "tel_e164": B["telefoon_e164"],
    "whatsapp": B["whatsapp"],
    "email": B["email"],
    "instagram": B["instagram"],
    "google_maps": B["google_maps"],
    "google_score": B["google_score"],
    "google_aantal": B["google_aantal"],
    "werkspot": B["werkspot"] or "https://www.werkspot.nl",
    "tarief_zin": TARIEF_ZIN,
    "tarief_zin_klein": TARIEF_ZIN[0].lower() + TARIEF_ZIN[1:],
    "voorrij_zin": VOORRIJ_ZIN,
    "actief_sinds": B["actief_sinds"],
    "jaar": str(datetime.date.today().year),
    "icon_wa": layout.ICON_WA,
    "icon_tel": layout.ICON_TEL,
    "icon_mail": layout.ICON_MAIL,
    **{k: str(v) for k, v in T.items()},
    **AANRIJTIJD,
}

BREADCRUMB_NAMEN = {
    "diensten": [("Diensten", None)],
    "groepenkast": [("Diensten", "/diensten/"), ("Groepenkast", None)],
    "perilex": [("Diensten", "/diensten/"), ("Perilex", None)],
    "laadpaal-installeren": [("Diensten", "/diensten/"), ("Laadpaal", None)],
    "krachtstroom-aanleggen": [("Diensten", "/diensten/"), ("Krachtstroom", None)],
    "frezen-stopcontacten-verleggen": [("Diensten", "/diensten/"), ("Frezen & stopcontacten", None)],
    "extra-groep-aanleggen": [("Diensten", "/diensten/"), ("Extra groep aanleggen", None)],
    "tuinverlichting-buitenelektra": [("Diensten", "/diensten/"), ("Tuinverlichting", None)],
    "tarieven": [("Tarieven", None)],
    "werkgebied": [("Werkgebied", None)],
    "wijken": [("Werkgebied", "/werkgebied/"), ("Alle wijken", None)],
    "werkwijze": [("Werkwijze", None)],
    "vakmanschap": [("Vakmanschap", None)],
    "reviews": [("Reviews", None)],
    "offerte": [("Offerte", None)],
    "afspraak": [("Afspraak", None)],
    "faq": [("Veelgestelde vragen", None)],
    "contact": [("Contact", None)],
    "privacy": [("Privacy", None)],
}

PRIORITY = {
    "": "1.0",
    "spoed-elektricien-utrecht": "0.9",
    "groepenkast": "0.9",
    "perilex": "0.9",
    "tarieven": "0.8",
    "diensten": "0.8",
    "offerte": "0.6",
    "afspraak": "0.5",
    "contact": "0.6"
}

warnings = []

def warn(msg):
    warnings.append(msg)

def url_of(slug):
    if not slug:
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{slug}/"

def fill(text):
    # <!--ALS sleutel-->…<!--/ALS--> wordt alleen getoond als die sleutel in config gevuld is
    text = re.sub(r"<!--ALS\s+([A-Za-z0-9_]+)\s*-->(.*?)<!--/ALS-->",
                  lambda m: m.group(2) if (B.get(m.group(1)) if m.group(1) in B else PLACEHOLDERS.get(m.group(1))) else "", text, flags=re.S)
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
    "CALCULATOR": lambda: paginas.groepenkast_calculator(),
    "STEDIN_CHECKER": lambda: paginas.blok_stedin_checker(),
    "REVIEWS_CAROUSEL": lambda: paginas.blok_reviews_carousel(),
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
    out = []
    matches = re.findall(
        r'<button[^>]*class="[^"]*faq-q[^"]*"[^>]*>(.*?)</button>\s*<div[^>]*class="[^"]*faq-a[^"]*"[^>]*>(.*?)</div>',
        body, re.S
    )
    for q_raw, a_raw in matches:
        q = re.sub(r'<[^>]+>', ' ', q_raw)
        q = re.sub(r'\s+', ' ', q).rstrip('+−- ').strip()
        a = re.sub(r'<[^>]+>', ' ', a_raw)
        a = re.sub(r'\s+', ' ', a).strip()
        if q and a:
            out.append([q, a])
    return out

def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()

def doorverwijzing(p):
    from html import escape
    doel = "/" + p["slug"] + "/"
    t = escape(p["title"], quote=False)
    return ('<!doctype html>\n<html lang="nl"><head><meta charset="utf-8">'
            f'<title>{t}</title>'
            f'<link rel="canonical" href="{p["url"]}">'
            f'<meta http-equiv="refresh" content="0; url={doel}">'
            f'<script>location.replace("{doel}"+location.search+location.hash)</script>'
            f'</head><body><p><a href="{doel}">Ga naar {t}</a></p></body></html>\n')

def schrijf(rel, content):
    # Alleen naar de root (GitHub Pages). Geen kopie in public/: dat gaf dubbele content.
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    print("1/6 Afbeeldingen optimaliseren…")
    beelden.verwerk()
    beelden.verwerk_logo()

    print("2/6 Assets (css/js/fonts)…")
    # Inter zelf hosten: geen verbinding meer naar fonts.googleapis.com en
    # fonts.gstatic.com (sneller op mobiel, en geen IP-adressen naar Google).
    fonts_in = os.path.join(ROOT, "assets", "fonts")
    if os.path.isdir(fonts_in):
        os.makedirs(os.path.join(ROOT, "fonts"), exist_ok=True)
        for fn in sorted(os.listdir(fonts_in)):
            if fn.endswith(".woff2"):
                shutil.copyfile(os.path.join(fonts_in, fn), os.path.join(ROOT, "fonts", fn))
    else:
        warn("assets/fonts/ ontbreekt: Inter wordt niet meegeleverd")

    css = open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8").read()
    css_min = minify_css(css)
    css_v = hashlib.md5(css_min.encode()).hexdigest()[:8]
    schrijf("style.css", css_min)

    js = open(os.path.join(ROOT, "assets", "script.js"), encoding="utf-8").read()
    from config import FORM_ENDPOINT
    js = js.replace("__FORM_ENDPOINT__", FORM_ENDPOINT).replace("__TEL__", B["telefoon_tonen"]).replace("__TEL_E164__", B["telefoon_e164"])
    js_v = hashlib.md5(js.encode()).hexdigest()[:8]
    schrijf("script.js", js)

    # Extra css/js die alleen op bepaalde pagina's laadt (front-matter: "extra": ["wizard"])
    extra_v = {}
    for pad in sorted(glob.glob(os.path.join(ROOT, "assets", "extra", "*.*"))):
        naam = os.path.basename(pad)
        inhoud = open(pad, encoding="utf-8").read()
        if naam.endswith(".css"):
            inhoud = minify_css(inhoud)
        else:
            inhoud = inhoud.replace("__WHATSAPP__", B["whatsapp"])
        extra_v[naam] = hashlib.md5(inhoud.encode()).hexdigest()[:8]
        schrijf(naam, inhoud)

    print("3/6 Pagina's samenstellen…")
    pages = lees_content()
    pages += [paginas.wijk_pagina(w, WIJKEN) for w in WIJKEN]
    pages += [paginas.storing_pagina(s, STORINGEN) for s in STORINGEN]

    lastmod = json.load(open(LASTMOD_FILE)) if os.path.exists(LASTMOD_FILE) else {}
    rendered = {}

    for p in pages:
        slug = p["slug"]
        p["url"] = url_of(slug)
        p["title"] = fill(p["title"])
        p["description"] = fill(p["description"])
        if p.get("schema"):
            p["schema"] = json.loads(fill(json.dumps(p["schema"], ensure_ascii=False)))
        body = fill(p["body"])
        # microdata weg (we gebruiken gestructureerde JSON-LD tags)
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

        # lastmod op basis van content hash
        h = hashlib.md5((p["title"] + p["description"] + body).encode()).hexdigest()
        if lastmod.get(slug or "index", {}).get("hash") != h:
            lastmod[slug or "index"] = {"hash": h, "date": TODAY}
        p["lastmod"] = lastmod[slug or "index"]["date"]

        variant = "spoed" if slug == "spoed-elektricien-utrecht" else "standaard"
        html = "\n".join([
            layout.head(p, WIJKEN, css_v),
            "<body>",
            layout.header(p.get("nav", slug), WIJKEN, variant),
            f'<main id="inhoud">',
            layout.breadcrumbs_html(p["breadcrumbs"]) if slug else "",
            body,
            "</main>",
            layout.footer(WIJKEN, STORINGEN, variant).replace("{JS_V}", js_v),
            "</body>", "</html>", ""
        ])
        for x in p.get("extra", []):
            if f"{x}.css" in extra_v:
                html = html.replace("</head>", f'<link rel="stylesheet" href="/{x}.css?v={extra_v[x + ".css"]}">\n</head>', 1)
            if f"{x}.js" in extra_v:
                html = html.replace("</body>", f'<script src="/{x}.js?v={extra_v[x + ".js"]}" defer></script>\n</body>', 1)
            if f"{x}.css" not in extra_v and f"{x}.js" not in extra_v:
                warn(f"{slug}: extra '{x}' bestaat niet in assets/extra/")
        rendered[slug] = (p, html)

    print("4/6 Bestanden schrijven…")
    for slug, (p, html) in rendered.items():
        if slug == "":
            schrijf("index.html", html)
        else:
            if MAAK_MAPPEN and slug != "404":
                schrijf(f"{slug}/index.html", html)
                # Oude /pagina.html-adressen: korte doorverwijzing i.p.v. een dubbele kopie
                schrijf(f"{slug}.html", doorverwijzing(p))
            else:
                schrijf(f"{slug}.html", html)

    json.dump(lastmod, open(LASTMOD_FILE, "w"), indent=1, sort_keys=True)

    print("5/6 Sitemap & robots.txt genereren…")
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

    print("6/6 Kwaliteitscontrole…")
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
        if tl > 60:
            warn(f"{naam}: title is {tl} tekens (Google toont ±60)")
        if not (120 <= len(d) <= 160):
            warn(f"{naam}: meta description is {len(d)} tekens (ideaal 120–160)")
        if t in titles:
            warn(f"{naam}: zelfde title als {titles[t]}")
        titles[t] = naam
        if d in descs:
            warn(f"{naam}: zelfde description als {descs[d]}")
        descs[d] = naam

        # Check H1
        h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', html, re.S)
        if len(h1s) != 1:
            warn(f"{naam}: {len(h1s)} H1-koppen (moet er precies 1 zijn)")

        # Check images alt
        for img_tag in re.findall(r'<img\b[^>]*>', html):
            if 'alt=' not in img_tag or 'alt=""' in img_tag:
                warn(f"{naam}: afbeelding zonder alt-tekst in {img_tag[:40]}")

        # Check JSON-LD
        for sc in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
            try:
                json.loads(sc)
            except Exception as e:
                warn(f"{naam}: structured data ongeldig: {e}")

        # Check broken internal links
        for h in re.findall(r'<a\b[^>]*href="([^"]*)"', html):
            if h.startswith("/") and not h.startswith("//"):
                path = h.split("?")[0].split("#")[0].strip("/")
                if path in bestaand or os.path.exists(os.path.join(ROOT, path)) and path:
                    continue
                if path == "":
                    continue
                warn(f"{naam}: mogelijk kapotte link {h}")

        if re.search(r'href=""', html):
            warn(f"{naam}: lege link (href=\"\")")
        if "{{" in html:
            warn(f"{naam}: niet-ingevulde placeholder in pagina")

if __name__ == "__main__":
    main()
