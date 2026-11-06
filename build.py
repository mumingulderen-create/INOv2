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
from config import TARIEF_ZIN_EN, VOORRIJ_ZIN_EN
from wijken import WIJKEN, OVERIGE_UTRECHT, OVERIGE_REGIO
from storingen import STORINGEN
from wijken_en import WIJKEN_EN
from storingen_en import STORINGEN_EN
import layout, paginas, beelden, taal, vertaling_js

taal.registreer_wijken(WIJKEN)

# Snelheidsbudget: de build meldt een aandachtspunt als iets hierboven komt.
BUDGET_CSS_KB = 55      # style.css (op elke pagina)
BUDGET_JS_KB = 30       # script.js (op elke pagina)
BUDGET_HTML_KB = 80     # één pagina (HTML zelf, zonder foto's)

MAAK_MAPPEN = True   # /pagina/index.html schrijven voor schone SEO URLs
TODAY = datetime.date.today().isoformat()
LASTMOD_FILE = os.path.join(ROOT, "bouw", "lastmod.json")

PLACEHOLDERS = {
    "tel": B["telefoon_tonen"],
    "tel_e164": B["telefoon_e164"],
    "whatsapp": B["whatsapp"],
    "email": B["email"],
    "instagram": B["instagram"],
    "linkedin": B["linkedin"],
    "google_maps": B["google_maps"],
    "google_review_url": B["google_review_url"] or B["google_maps"],
    "google_score": B["google_score"],
    "google_aantal": B["google_aantal"],
    "werkspot": B["werkspot"] or "https://www.werkspot.nl",
    "tarief_zin": TARIEF_ZIN,
    "tarief_zin_klein": TARIEF_ZIN[0].lower() + TARIEF_ZIN[1:],
    "voorrij_zin": VOORRIJ_ZIN,
    "actief_sinds": B["actief_sinds"],
    "kvk": B["kvk"],
    "jaar": str(datetime.date.today().year),
    "icon_wa": layout.ICON_WA,
    "icon_tel": layout.ICON_TEL,
    "icon_mail": layout.ICON_MAIL,
    **{k: str(v) for k, v in T.items()},
    **AANRIJTIJD,
}

# Engelse pagina's (/en/): dezelfde placeholders, maar zinnen in het Engels en
# getallen met een punt (0.40 i.p.v. 0,40).
PLACEHOLDERS_EN = dict(PLACEHOLDERS)
PLACEHOLDERS_EN.update({k: taal.getal_en(v) for k, v in T.items()})
PLACEHOLDERS_EN.update({
    "tarief_zin": TARIEF_ZIN_EN,
    "tarief_zin_klein": TARIEF_ZIN_EN[0].lower() + TARIEF_ZIN_EN[1:],
    "voorrij_zin": VOORRIJ_ZIN_EN,
    "google_score": taal.getal_en(B["google_score"]),
})


def wijken_in(t=None):
    """Wijkdata in de gevraagde taal (Engels: alleen wijken met een vertaling in wijken_en.py)."""
    if not taal.en(t):
        return WIJKEN
    return [dict(w, **WIJKEN_EN[w["slug"]]) for w in WIJKEN if w["slug"] in WIJKEN_EN]


def storingen_in(t=None):
    if not taal.en(t):
        return STORINGEN
    return [dict(s, **STORINGEN_EN[s["slug"]]) for s in STORINGEN if s["slug"] in STORINGEN_EN]


BREADCRUMB_NAMEN = {
    "diensten": [("Diensten", None)],
    "groepenkast": [("Diensten", "/diensten/"), ("Groepenkast", None)],
    "perilex": [("Diensten", "/diensten/"), ("Perilex", None)],
    "laadpaal-installeren": [("Diensten", "/diensten/"), ("Laadpaal", None)],
    "thuisbatterij-installeren": [("Diensten", "/diensten/"), ("Thuisbatterij installeren", None)],
    "krachtstroom-aanleggen": [("Diensten", "/diensten/"), ("Krachtstroom", None)],
    "frezen-stopcontacten-verleggen": [("Diensten", "/diensten/"), ("Frezen & stopcontacten", None)],
    "extra-groep-aanleggen": [("Diensten", "/diensten/"), ("Extra groep aanleggen", None)],
    "tuinverlichting-buitenelektra": [("Diensten", "/diensten/"), ("Tuinverlichting", None)],
    "buitengesloten-cilinder-vervangen": [("Diensten", "/diensten/"), ("Buitengesloten", None)],
    "slim-deurslot-installeren": [("Diensten", "/diensten/"), ("Slim deurslot", None)],
    "videodeurbel-installeren": [("Diensten", "/diensten/"), ("Videodeurbel", None)],
    "inductiekookplaat-aansluiten": [("Diensten", "/diensten/"), ("Kookplaat aansluiten", None)],
    "tv-ophangen": [("Diensten", "/diensten/"), ("TV ophangen", None)],
    "mv-box-vervangen": [("Diensten", "/diensten/"), ("MV-box vervangen", None)],
    "aardpen-slaan": [("Diensten", "/diensten/"), ("Aardpen slaan", None)],
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
    ph = PLACEHOLDERS_EN if taal.en() else PLACEHOLDERS
    # <!--ALS sleutel-->…<!--/ALS--> wordt alleen getoond als die sleutel in config gevuld is
    text = re.sub(r"<!--ALS\s+([A-Za-z0-9_]+)\s*-->(.*?)<!--/ALS-->",
                  lambda m: m.group(2) if (B.get(m.group(1)) if m.group(1) in B else ph.get(m.group(1))) else "", text, flags=re.S)
    def r(m):
        k = m.group(1)
        if k in ph:
            return ph[k]
        if k in BLOKKEN:
            return BLOKKEN[k]()
        warn(f"onbekende placeholder {{{{{k}}}}}")
        return m.group(0)
    return re.sub(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}", r, text)

BLOKKEN = {
    "STORING_KAARTEN": lambda: paginas.blok_storing_kaarten(storingen_in()),
    "WIJK_CHIPS": lambda: paginas.blok_wijk_chips(wijken_in()),
    "WIJKEN_HUB": lambda: paginas.blok_wijken_hub(wijken_in(), OVERIGE_UTRECHT, OVERIGE_REGIO),
    "TARIEF_KAARTEN": lambda: paginas.tarief_kaarten(),
    "CTA": lambda: paginas.cta_band(),
    "CALCULATOR": lambda: paginas.groepenkast_calculator(),
    "STEDIN_CHECKER": lambda: paginas.blok_stedin_checker(),
    "REVIEWS_CAROUSEL": lambda: paginas.blok_reviews_carousel(),
    "STORING_REKENHULP": lambda: paginas.blok_storing_rekenhulp(),
}

def lees_content():
    """content/*.html (Nederlands) en content/en/*.html (Engels, zelfde bestandsnaam)."""
    pages = []
    for t, map_ in (("nl", "content"), ("en", os.path.join("content", "en"))):
        for path in sorted(glob.glob(os.path.join(ROOT, map_, "*.html"))):
            raw = open(path, encoding="utf-8").read()
            m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->\s*(.*)$", raw, re.S)
            if not m:
                warn(f"{path}: geen front-matter gevonden, overgeslagen")
                continue
            fm = json.loads(m.group(1))
            fm["body"] = m.group(2)
            fm["taal"] = t
            if t == "nl":
                fm["nl_slug"] = fm["slug"]
                fm.setdefault("crumbs", BREADCRUMB_NAMEN.get(fm["slug"], []))
            else:
                nl_slug = os.path.basename(path)[:-5]
                nl_slug = "" if nl_slug == "index" else nl_slug
                en_slug = taal.slug_in(nl_slug, "en")
                if en_slug is None:
                    warn(f"{path}: geen Engelse slug in bouw/taal.py (EN_SLUG), overgeslagen")
                    continue
                fm["slug"], fm["nl_slug"] = en_slug, nl_slug
                fm.setdefault("nav", nl_slug)
                fm.setdefault("crumbs", [(taal.CRUMB_EN.get(n, n), taal.pad(u, "en") if u else None)
                                         for n, u in BREADCRUMB_NAMEN.get(nl_slug, [])])
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
    ga = "Go to" if p.get("taal") == "en" else "Ga naar"
    return (f'<!doctype html>\n<html lang="{p.get("taal", "nl")}"><head><meta charset="utf-8">'
            f'<title>{t}</title>'
            f'<link rel="canonical" href="{p["url"]}">'
            f'<meta http-equiv="refresh" content="0; url={doel}">'
            f'<script>location.replace("{doel}"+location.search+location.hash)</script>'
            f'</head><body><p><a href="{doel}">{ga} {t}</a></p></body></html>\n')

INTERNE_LINK = re.compile(r'href="/((?:en/)?[a-z0-9][a-z0-9-]*)([#?][^"]*)?"')

def normaliseer_links(html):
    """/offerte -> /offerte/ . Op GitHub Pages laadt /offerte eerst de doorverwijspagina
    offerte.html en pas daarna /offerte/ (twee keer laden). Bestanden (met punt) blijven ongemoeid."""
    return INTERNE_LINK.subn(lambda m: f'href="/{m.group(1)}/{m.group(2) or ""}"', html)

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

    # QR-code en printbare reviewkaart (assets/qr/ -> /qr/)
    qr_in = os.path.join(ROOT, "assets", "qr")
    if os.path.isdir(qr_in):
        os.makedirs(os.path.join(ROOT, "qr"), exist_ok=True)
        for fn in sorted(os.listdir(qr_in)):
            shutil.copyfile(os.path.join(qr_in, fn), os.path.join(ROOT, "qr", fn))

    css = open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8").read()
    css_min = minify_css(css)
    css_v = hashlib.md5(css_min.encode()).hexdigest()[:8]
    schrijf("style.css", css_min)
    if len(css_min.encode()) > BUDGET_CSS_KB * 1024:
        warn(f"style.css is {len(css_min.encode())//1024} KB (budget {BUDGET_CSS_KB} KB). Zet pagina-specifieke CSS in assets/extra/.")

    js = open(os.path.join(ROOT, "assets", "script.js"), encoding="utf-8").read()
    from config import FORM_ENDPOINT, TURNSTILE_SITEKEY, REVIEWS_ENDPOINT
    if not FORM_ENDPOINT or not TURNSTILE_SITEKEY:
        warn("FORM_ENDPOINT en/of TURNSTILE_SITEKEY in bouw/config.py zijn leeg: formulieren versturen niets (zie worker/README.md)")
    js = js.replace("__REVIEWS_ENDPOINT__", REVIEWS_ENDPOINT).replace("__FORM_ENDPOINT__", FORM_ENDPOINT).replace("__TEL__", B["telefoon_tonen"]).replace("__TEL_E164__", B["telefoon_e164"])
    # Engelse variant (script-en.js) via de vertaaltabel in bouw/vertaling_js.py
    js_en = vertaal_js("script.js", js)
    js_v = {"nl": hashlib.md5(js.encode()).hexdigest()[:8], "en": hashlib.md5(js_en.encode()).hexdigest()[:8]}
    schrijf("script.js", js)
    schrijf("script-en.js", js_en)
    for naam, inhoud in (("script.js", js), ("script-en.js", js_en)):
        if len(inhoud.encode()) > BUDGET_JS_KB * 1024:
            warn(f"{naam} is {len(inhoud.encode())//1024} KB (budget {BUDGET_JS_KB} KB). Zet pagina-specifieke JS in assets/extra/.")

    # Extra css/js die alleen op bepaalde pagina's laadt (front-matter: "extra": ["wizard"])
    extra_v = {}
    for pad in sorted(glob.glob(os.path.join(ROOT, "assets", "extra", "*.*"))):
        naam = os.path.basename(pad)
        inhoud = open(pad, encoding="utf-8").read()
        if naam.endswith(".css"):
            inhoud = minify_css(inhoud)
        else:
            inhoud = inhoud.replace("__WHATSAPP__", B["whatsapp"]).replace("__TURNSTILE_SITEKEY__", TURNSTILE_SITEKEY)
        extra_v[naam] = hashlib.md5(inhoud.encode()).hexdigest()[:8]
        schrijf(naam, inhoud)
        if naam.endswith(".js") and naam in vertaling_js.JS_EN:
            naam_en = naam[:-3] + "-en.js"
            inhoud_en = vertaal_js(naam, inhoud)
            extra_v[naam_en] = hashlib.md5(inhoud_en.encode()).hexdigest()[:8]
            schrijf(naam_en, inhoud_en)

    print("3/6 Pagina's samenstellen…")
    pages = lees_content()
    for t in taal.TALEN:
        taal.zet(t)
        pages += [paginas.wijk_pagina(w, wijken_in()) for w in wijken_in()]
        pages += [paginas.storing_pagina(s, storingen_in()) for s in storingen_in()]
    taal.zet("nl")

    # Taalparen: elke pagina kent zijn tegenhanger (hreflang + vlag-schakelaar)
    paren = {}
    for p in pages:
        paren.setdefault(p["nl_slug"], {})[p["taal"]] = p
    for nl_slug, paar in sorted(paren.items()):
        if nl_slug != "404" and set(paar) != set(taal.TALEN):
            mist = ", ".join(t for t in taal.TALEN if t not in paar)
            warn(f"{nl_slug or 'index'}: geen {mist}-versie (vertaling ontbreekt)")
    for p in pages:
        paar = paren[p["nl_slug"]]
        p["wissel"] = {t: (f"/{paar[t]['slug']}/" if paar[t]["slug"] else "/") if t in paar else ("/en/" if t == "en" else "/")
                       for t in taal.TALEN}
        if len(paar) > 1 and not p.get("noindex"):
            p["alternates"] = [(t, url_of(paar[t]["slug"])) for t in taal.TALEN if t in paar]

    lastmod = json.load(open(LASTMOD_FILE)) if os.path.exists(LASTMOD_FILE) else {}
    rendered = {}

    for p in pages:
        taal.zet(p["taal"])
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
        if p["nl_slug"]:
            home = f"{SITE_URL}/en/" if taal.en() else f"{SITE_URL}/"
            p["breadcrumbs"] = [("Home", home)] + [
                (n, f"{SITE_URL}{u}" if u else p["url"]) for n, u in p.get("crumbs", [])]
        else:
            p["breadcrumbs"] = []

        # lastmod op basis van content hash
        h = hashlib.md5((p["title"] + p["description"] + body).encode()).hexdigest()
        if lastmod.get(slug or "index", {}).get("hash") != h:
            lastmod[slug or "index"] = {"hash": h, "date": TODAY}
        p["lastmod"] = lastmod[slug or "index"]["date"]

        variant = "spoed" if p["nl_slug"] == "spoed-elektricien-utrecht" else "standaard"
        js_naam = "/script-en.js" if taal.en() else "/script.js"
        html = "\n".join([
            layout.head(p, WIJKEN, css_v),
            "<body>",
            layout.header(p.get("nav", p["nl_slug"]), wijken_in(), variant, p["wissel"]),
            f'<main id="inhoud">',
            layout.breadcrumbs_html(p["breadcrumbs"]) if p["nl_slug"] else "",
            body,
            "</main>",
            layout.footer(wijken_in(), storingen_in(), variant, js_naam).replace("{JS_V}", js_v[p["taal"]]),
            "</body>", "</html>", ""
        ])
        for x in p.get("extra", []):
            if f"{x}.css" in extra_v:
                html = html.replace("</head>", f'<link rel="stylesheet" href="/{x}.css?v={extra_v[x + ".css"]}">\n</head>', 1)
            xjs = f"{x}-en.js" if taal.en() and f"{x}-en.js" in extra_v else f"{x}.js"
            if xjs in extra_v:
                html = html.replace("</body>", f'<script src="/{xjs}?v={extra_v[xjs]}" defer></script>\n</body>', 1)
            if f"{x}.css" not in extra_v and f"{x}.js" not in extra_v:
                warn(f"{slug}: extra '{x}' bestaat niet in assets/extra/")
        html, n_fix = normaliseer_links(html)
        if n_fix:
            warn(f"{slug or 'index'}: {n_fix} interne link(s) zonder slash automatisch verbeterd; pas de bron aan naar /pagina/")
        if len(html.encode()) > BUDGET_HTML_KB * 1024:
            warn(f"{slug or 'index'}: pagina is {len(html.encode())//1024} KB (budget {BUDGET_HTML_KB} KB)")
        rendered[slug] = (p, html)
    taal.zet("nl")

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
        pr = p.get("priority") or PRIORITY.get(p["nl_slug"], "0.7")
        if p["taal"] == "en" and not p.get("priority"):
            pr = f"{max(0.1, float(pr) - 0.2):.1f}"
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{t}" href="{u}"/>' for t, u in p.get("alternates", []))
        if alt:
            alt += f'<xhtml:link rel="alternate" hreflang="x-default" href="{dict(p["alternates"])["nl"]}"/>'
        urls.append(f"  <url><loc>{p['url']}</loc><lastmod>{p['lastmod']}</lastmod><priority>{pr}</priority>{alt}</url>")

    schrijf("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(urls) + "\n</urlset>\n")
    schrijf("robots.txt", "User-agent: *\nAllow: /\n\n"
            f"Sitemap: {SITE_URL}/sitemap.xml\n")

    print("6/6 Kwaliteitscontrole…")
    controleer(rendered)
    if "--test" in sys.argv:
        import test_mobiel
        for w in test_mobiel.draai(ROOT, [p["url"].replace(SITE_URL, "") for p, _ in rendered.values() if p["slug"] != "404"]):
            warn(w)

    n_en = sum(1 for p, _ in rendered.values() if p["taal"] == "en")
    print(f"\nKlaar: {len(rendered)} pagina's ({len(rendered) - n_en} NL, {n_en} EN), {len(urls)} in sitemap.")
    if warnings:
        print(f"\n{len(warnings)} aandachtspunt(en):")
        for w in warnings:
            print("  -", w)
    else:
        print("Geen fouten gevonden.")


def vertaal_js(naam, js):
    """Maak de Engelse variant van een script met de tabel in bouw/vertaling_js.py.
    Elke Nederlandse tekst moet precies voorkomen; anders een aandachtspunt (script is aangepast)."""
    for nl, en_ in vertaling_js.JS_EN.get(naam, []):
        if nl not in js:
            warn(f"vertaling_js: tekst niet gevonden in {naam}: {nl[:50]!r}")
            continue
        js = js.replace(nl, en_)
    return js


def controleer(rendered):
    bestaand = set(rendered.keys())
    titles, descs = {}, {}
    for slug, (p, html) in rendered.items():
        naam = slug or "index"
        if "formsubmit" in html.lower():
            warn(f"{naam}: bevat nog een verwijzing naar FormSubmit")
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

        # Check broken internal links + taal: Engelse pagina's linken naar /en/, Nederlandse niet
        # (uitzondering: de vlag-schakelaar, die heeft hreflang)
        for tag, h in re.findall(r'(<a\b[^>]*href="([^"]*)"[^>]*>)', html):
            if h.startswith("/") and not h.startswith("//"):
                path = h.split("?")[0].split("#")[0].strip("/")
                if path and "hreflang=" not in tag and "." not in path.split("/")[-1]:
                    is_en = path == "en" or path.startswith("en/")
                    if p["taal"] == "en" and not is_en:
                        warn(f"{naam}: Engelse pagina linkt naar Nederlandse pagina {h}")
                    elif p["taal"] == "nl" and is_en:
                        warn(f"{naam}: Nederlandse pagina linkt naar Engelse pagina {h}")
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
