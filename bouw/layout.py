"""
Layout-onderdelen die op ELKE pagina terugkomen: <head>, header, footer,
mobiele belbalk en de structured data (JSON-LD) voor Google.
"""
import json, datetime
from html import escape
from config import SITE_URL, BEDRIJF as B, NAV, NAV_GROEP, GOOGLE_SITE_VERIFICATION, GA4_MEASUREMENT_ID, TARIEVEN as T

JAAR = datetime.date.today().year

ICON_MENU = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
ICON_TEL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
ICON_WA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5z"/></svg>'
ICON_MAIL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'


def wa_url(tekst="Hallo INO, ik heb een vraag."):
    from urllib.parse import quote
    return f"https://wa.me/{B['whatsapp']}?text={quote(tekst)}"


# --------------------------------------------------------------------------- schema
def business_node(wijken):
    areas = [{"@type": "City", "name": "Utrecht"}]
    for w in wijken:
        if w["type"] == "plaats":
            areas.append({"@type": "City", "name": w["naam"]})
        else:
            areas.append({"@type": "Place", "name": f"{w['naam']}, Utrecht"})
    for extra in ["Houten", "Zeist", "IJsselstein", "De Bilt", "Woerden"]:
        areas.append({"@type": "City", "name": extra})
    adres = {"@type": "PostalAddress", "addressLocality": B["plaats"],
             "addressRegion": B["provincie"], "addressCountry": "NL"}
    if B["straat"]:
        adres["streetAddress"] = B["straat"]
    if B["postcode"]:
        adres["postalCode"] = B["postcode"]
    same = [u for u in [B["instagram"], B["google_maps"], B["werkspot"]] if u]
    node = {
        "@type": ["Electrician", "EmergencyService"],
        "@id": f"{SITE_URL}/#business",
        "name": B["naam"],
        "alternateName": B["alternatieve_naam"],
        "url": f"{SITE_URL}/",
        "logo": f"{SITE_URL}/logo.png",
        "image": f"{SITE_URL}/img/og-hero-elektricien.jpg",
        "telephone": B["telefoon_e164"],
        "email": B["email"],
        "priceRange": f"€{T['uur_dag']}-€{T['uur_nacht']} per uur",
        "currenciesAccepted": "EUR",
        "paymentAccepted": "iDEAL, betaalverzoek, bankoverschrijving, contant",
        "foundingDate": B["actief_sinds"],
        "address": adres,
        "geo": {"@type": "GeoCoordinates", "latitude": B["lat"], "longitude": B["lng"]},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59"}],
        "areaServed": areas,
        "knowsAbout": ["NEN 1010", "NEN 3140", "groepenkast vervangen", "Perilex", "laadpaal installatie",
                       "krachtstroom", "storingsdienst"],
        "sameAs": same,
    }
    if B["kvk"]:
        node["identifier"] = {"@type": "PropertyValue", "propertyID": "KvK", "value": B["kvk"]}
        node["taxID"] = B["kvk"]
    if B["btw"]:
        node["vatID"] = B["btw"]
    return node


def schema_graph(page, wijken):
    url = page["url"]
    g = [business_node(wijken), {
        "@type": "WebSite", "@id": f"{SITE_URL}/#website", "url": f"{SITE_URL}/",
        "name": B["naam"], "inLanguage": "nl-NL", "publisher": {"@id": f"{SITE_URL}/#business"}}]
    wp = {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": page["title"],
          "description": page["description"], "inLanguage": "nl-NL",
          "isPartOf": {"@id": f"{SITE_URL}/#website"}, "about": {"@id": f"{SITE_URL}/#business"},
          "dateModified": page.get("lastmod")}
    if page.get("og_image_url"):
        wp["primaryImageOfPage"] = {"@type": "ImageObject", "url": page["og_image_url"]}
    crumbs = page.get("breadcrumbs") or []
    if crumbs:
        wp["breadcrumb"] = {"@id": f"{url}#breadcrumb"}
        g.append({"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    g.append(wp)
    for s in page.get("schema", []):
        s = dict(s)
        s.setdefault("provider", {"@id": f"{SITE_URL}/#business"})
        s.setdefault("url", url)
        g.append(s)
    if page.get("faq"):
        g.append({"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in page["faq"]]})
    data = {"@context": "https://schema.org", "@graph": g}
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# --------------------------------------------------------------------------- head
def head(page, wijken, css_v, font_url=None):
    t, d = page["title"], page["description"]
    robots = "noindex, follow" if page.get("noindex") else "index, follow, max-image-preview:large, max-snippet:-1"
    og_img = page.get("og_image_url") or f"{SITE_URL}/img/og-hero-elektricien.jpg"
    canon = "" if page.get("slug") == "404" else f'<link rel="canonical" href="{page["url"]}">'
    pre = ""
    if page.get("lcp"):
        href, srcset, sizes = page["lcp"]
        pre = (f'\n<link rel="preload" as="image" type="image/webp" href="{href}" imagesrcset="{srcset}"'
               f' imagesizes="{sizes}" fetchpriority="high" media="(min-width: 801px)">')
    # GA4 laadt pas NA toestemming (cookiemelding in script.js). Zonder akkoord: geen cookies, geen verzoek naar Google.
    ga4_tag = f"""\n<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  window.inoGA4 = function () {{
    if (window.inoGA4geladen) return; window.inoGA4geladen = true;
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}';
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', '{GA4_MEASUREMENT_ID}', {{ anonymize_ip: true }});
  }};
  try {{ if (localStorage.getItem('ino_cookies') === 'ja') window.inoGA4(); }} catch (e) {{}}
</script>""" if GA4_MEASUREMENT_ID else ""
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{ga4_tag}
<title>{t}</title>
<meta name="description" content="{d}">
{canon}
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#278a1d">
<meta name="format-detection" content="telephone=yes">
<meta property="og:locale" content="nl_NL">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{B['naam']}">
<meta property="og:title" content="{page.get('og_title') or t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{page['url']}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" href="/fonts/inter-latin.woff2" crossorigin>{pre}
<link rel="stylesheet" href="/style.css?v={css_v}">
<script type="application/ld+json">{schema_graph(page, wijken)}</script>
</head>"""


# --------------------------------------------------------------------------- header
def header(nav_key, wijken, variant="standaard"):
    groep = NAV_GROEP.get(nav_key, nav_key)
    topbar = (
        f'<div class="topbar"><div class="container topbar-inner">'
        f'<span>Storing? <strong>24/7 bereikbaar</strong> · geen voorrijkosten in Utrecht</span>'
        f'<a href="tel:{B["telefoon_e164"]}" data-track="bellen">{ICON_TEL} {B["telefoon_tonen"]}</a>'
        f'</div></div>'
    )
    items = []
    for it in NAV:
        active = ' aria-current="page"' if groep == it["key"] else ""
        cls_active = " active" if groep == it["key"] else ""
        sub = it.get("sub")
        if sub == "WIJKEN":
            top_links = (
                f'<div class="nav-dd-top">'
                f'  <a href="/werkgebied/" class="nav-dd-featured">'
                f'    <strong>Werkgebied &amp; kaart</strong>'
                f'    <span>Overzicht actieradius &amp; aanrijtijden</span>'
                f'  </a>'
                f'  <a href="/wijken/" class="nav-dd-all">'
                f'    <span>Alle {len(wijken)} wijken &amp; plaatsen</span> →'
                f'  </a>'
                f'</div>'
                f'<div class="nav-dd-divider"></div>'
                f'<div class="nav-dd-caption">Direct naar wijk:</div>'
            )
            wijk_links = "".join(f'<a href="/elektricien-{w["slug"]}/" class="nav-dd-wijk-link">{w["naam"]}</a>' for w in wijken)
            menu_html = f'{top_links}<div class="nav-dd-scroll">{wijk_links}</div>'
            items.append(
                f'<div class="nav-dd nav-dd-werkgebied"><a href="{it["href"]}" class="nav-dd-toggle{cls_active}"{active}>{it["label"]} '
                f'<span class="caret" aria-hidden="true">▾</span></a><div class="nav-dd-menu">{menu_html}</div></div>')
        elif sub:
            links = "".join(f'<a href="{s["href"]}">{s["label"]}</a>' for s in sub)
            items.append(
                f'<div class="nav-dd"><a href="{it["href"]}" class="nav-dd-toggle{cls_active}"{active}>{it["label"]} '
                f'<span class="caret" aria-hidden="true">▾</span></a><div class="nav-dd-menu">{links}</div></div>')
        else:
            items.append(f'<a href="{it["href"]}" class="{cls_active.strip()}"{active}>{it["label"]}</a>'.replace(' class=""', ""))
    nav = "\n      ".join(items)
    return f"""<a class="skip-link" href="#inhoud">Naar de inhoud</a>
{topbar}
<header class="site-header">
  <div class="container nav-wrap">
    <a class="brand" href="/" aria-label="{B['naam']} – elektricien Utrecht, naar de homepage">
      <img src="/img/logo-390.png" alt="{B['naam']} – elektricien Utrecht" width="130" height="54" decoding="async">
    </a>
    <button class="menu-btn" id="menuBtn" type="button" aria-label="Menu openen" aria-expanded="false" aria-controls="nav">{ICON_MENU}</button>
    <nav id="nav" aria-label="Hoofdmenu">
      {nav}
      <a class="nav-cta" href="/offerte/">Offerte aanvragen</a>
    </nav>
  </div>
</header>"""


# --------------------------------------------------------------------------- breadcrumbs (zichtbaar)
def breadcrumbs_html(crumbs):
    if not crumbs or len(crumbs) < 2:
        return ""
    parts = []
    for i, (n, u) in enumerate(crumbs):
        link = u.replace(SITE_URL, "") or "/"
        if not link.endswith("/") and not link.startswith("#"):
            link += "/"
        if i == len(crumbs) - 1:
            parts.append(f'<span aria-current="page">{n}</span>')
        else:
            parts.append(f'<a href="{link}">{n}</a>')
    sep = ' <span aria-hidden="true">/</span> '
    return f'<nav class="crumbs container" aria-label="Kruimelpad">{sep.join(parts)}</nav>'


# --------------------------------------------------------------------------- footer
def footer(wijken, storingen, variant="standaard"):
    wijk_links = "".join(f'<a href="/elektricien-{w["slug"]}/">Elektricien {w["naam"]}</a>' for w in wijken)
    storing_links = "".join(f'<a href="/{s["slug"]}/">{s["kort"]}</a>' for s in storingen)
    kvk = f' · KvK {B["kvk"]}' if B["kvk"] else ""
    btw = f' · btw {B["btw"]}' if B["btw"] else ""
    if variant == "spoed":
        bar = f"""<div class="mobile-bar-emergency" role="navigation" aria-label="Directe spoedacties">
  <a class="m-btn-call" href="tel:{B['telefoon_e164']}" data-track="bellen">{ICON_TEL}<span>Bel nu (24/7)</span></a>
  <a class="m-btn-whatsapp" href="{wa_url('Hallo INO, ik heb nu een stroomstoring. Hierbij een foto van de meterkast.')}" target="_blank" rel="noopener" data-track="whatsapp">{ICON_WA}<span>WhatsApp foto</span></a>
</div>"""
    else:
        bar = f"""<div class="mobile-bar-optimized" role="navigation" aria-label="Snel contact">
  <a href="tel:{B['telefoon_e164']}" class="mobile-btn-call" data-track="bellen">{ICON_TEL}<span>Direct bellen</span></a>
  <a href="{wa_url('Hallo INO, ik wil graag een foto sturen voor een prijsindicatie.')}" target="_blank" rel="noopener" class="mobile-btn-whatsapp" data-track="whatsapp">{ICON_WA}<span>WhatsApp foto</span></a>
</div>"""
    floating_wa = f"""<a href="{wa_url('Hallo INO Techniek, ik heb een vraag over een elektra klus. Kan ik een foto sturen voor advies?')}" class="floating-wa" target="_blank" rel="noopener" aria-label="Direct chatten via WhatsApp" data-track="whatsapp" id="floatingWa">
  <span class="floating-wa-badge"><span class="floating-wa-pulse"></span>Direct contact</span>
  <span class="floating-wa-inner">
    <span class="floating-wa-icon">{ICON_WA}</span>
    <span class="floating-wa-text">
      <strong>WhatsApp ons</strong>
      <small>Foto sturen &amp; richtprijs</small>
    </span>
  </span>
</a>"""
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <img src="/img/logo-390.png" alt="{B['naam']} logo" class="footer-logo" width="130" height="54" loading="lazy" decoding="async">
      <p>Elektricien in Utrecht en omstreken. Vaste prijs vooraf, 24/7 bereikbaar bij storingen, NEN 1010.</p>
      <p><a href="tel:{B['telefoon_e164']}" data-track="bellen"><strong>{B['telefoon_tonen']}</strong></a><br>
      <a href="mailto:{B['email']}">{B['email']}</a></p>
    </div>
    <div><h2 class="footer-h">Diensten</h2><a href="/diensten/">Alle diensten</a><a href="/groepenkast/">Groepenkast vervangen</a><a href="/perilex/">Perilex &amp; kookgroep</a><a href="/laadpaal-installeren/">Laadpaal installeren</a><a href="/krachtstroom-aanleggen/">Krachtstroom 400V</a><a href="/frezen-stopcontacten-verleggen/">Frezen &amp; stopcontacten</a><a href="/tuinverlichting-buitenelektra/">Tuinverlichting</a></div>
    <div><h2 class="footer-h">Storing?</h2><a href="/spoed-elektricien-utrecht/">Spoed elektricien 24/7</a>{storing_links}<a href="/tarieven/">Tarieven</a><a href="/faq/">Veelgestelde vragen</a></div>
    <div><h2 class="footer-h">Werkgebied</h2>{wijk_links}<a href="/wijken/">Alle wijken &amp; plaatsen</a></div>
  </div>
  <div class="copyright">© {JAAR} {B['naam']}{kvk}{btw} · <a href="/werkwijze/">Werkwijze</a> · <a href="/vakmanschap/">Vakmanschap</a> · <a href="/reviews/">Reviews</a> · <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy &amp; Cookies</a>{' · <a href="#cookies" data-cookie-instellingen>Cookie-instellingen</a>' if GA4_MEASUREMENT_ID else ''} · <a href="{B['instagram']}" target="_blank" rel="noopener">Instagram</a></div>
</footer>
{bar}
{floating_wa}
<script src="/script.js?v={{JS_V}}" defer></script>"""
