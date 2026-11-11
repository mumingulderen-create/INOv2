"""
Layout-onderdelen die op ELKE pagina terugkomen: <head>, header, footer,
mobiele belbalk en de structured data (JSON-LD) voor Google.
"""
import json, datetime
from html import escape
from config import SITE_URL, BEDRIJF as B, NAV, NAV_GROEP, GOOGLE_SITE_VERIFICATION, GA4_MEASUREMENT_ID, GOOGLE_ADS_ID, TARIEVEN as T
import taal
from taal import L, pad

JAAR = datetime.date.today().year

ICON_MENU = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
ICON_TEL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
ICON_WA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5z"/></svg>'
ICON_MAIL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'


FLAG_NL = '<svg viewBox="0 0 9 6" aria-hidden="true"><path fill="#ae1c28" d="M0 0h9v2H0z"/><path fill="#fff" d="M0 2h9v2H0z"/><path fill="#21468b" d="M0 4h9v2H0z"/></svg>'
FLAG_EN = ('<svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><clipPath id="vlagUk"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath>'
           '<path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/>'
           '<path d="M0 0l60 30m0-30L0 30" clip-path="url(#vlagUk)" stroke="#c8102e" stroke-width="4"/>'
           '<path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#c8102e" stroke-width="6"/></svg>')


def taalwissel(wissel):
    """Vlag-schakelaar NL | EN. wissel = {"nl": "/pad/", "en": "/en/path/"}."""
    def optie(t, vlag, code, label):
        if taal.TAAL == t:
            return f'<span aria-current="true" lang="{t}" title="{label}">{vlag}<b>{code}</b></span>'
        return f'<a href="{wissel[t]}" hreflang="{t}" lang="{t}" aria-label="{label}" title="{label}">{vlag}<b>{code}</b></a>'
    return ('<div class="lang-switch" role="group" aria-label="Taal / Language">'
            + optie("nl", FLAG_NL, "NL", "Nederlandse versie")
            + optie("en", FLAG_EN, "EN", "English version") + '</div>')


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
    same = [u for u in [B["instagram"], B.get("linkedin"), B["google_maps"], B["werkspot"]] if u]
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
        "priceRange": f"€{T['uur_dag']}-€{T['uur_nacht']} " + L("per uur", "per hour"),
        "currenciesAccepted": "EUR",
        "paymentAccepted": L("iDEAL, betaalverzoek, bankoverschrijving, contant", "iDEAL, payment request, bank transfer, cash"),
        "foundingDate": B["actief_sinds"],
        "address": adres,
        "geo": {"@type": "GeoCoordinates", "latitude": B["lat"], "longitude": B["lng"]},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59"}],
        "areaServed": areas,
        "knowsAbout": [
            "NEN 1010", "NEN 3140", "NEN 3140 VP", "BEI LS VP", "BEI BLS", "VCA VOL",
            "MBO 2 Laagspanningsdistributie", "groepenkast vervangen", "meterkast vervangen",
            "Perilex aansluiten", "laadpaal installatie", "thuisbatterij installatie",
            "krachtstroom aanleggen", "storingsdienst"
        ],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "MBO 2 Laagspanningsdistributie"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "NEN 3140 VP (Vakbekwaam Persoon)"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "BEI LS VP (Vakbekwaam Persoon Laagspanning)"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "VCA VOL (Veiligheid voor Operationeel Leidinggevenden)"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "SBB Erkend Leerbedrijf (Relatienummer: 100850431)"},
        ],
        "award": L("SBB Erkend Leerbedrijf – Wij leiden vakmensen op", "SBB Accredited Training Company – we train future electricians"),
        "knowsLanguage": ["nl", "en"],
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
        "name": B["naam"], "inLanguage": ["nl-NL", "en"], "publisher": {"@id": f"{SITE_URL}/#business"}}]
    wp = {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": page["title"],
          "description": page["description"], "inLanguage": L("nl-NL", "en"),
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
    alts = ""
    if page.get("alternates") and not page.get("noindex"):
        alts = "".join(f'\n<link rel="alternate" hreflang="{t}" href="{u}">' for t, u in page["alternates"])
        alts += f'\n<link rel="alternate" hreflang="x-default" href="{dict(page["alternates"])["nl"]}">'
    pre = ""
    if page.get("lcp"):
        href, srcset, sizes = page["lcp"]
        pre = (f'\n<link rel="preload" as="image" type="image/webp" href="{href}" imagesrcset="{srcset}"'
               f' imagesizes="{sizes}" fetchpriority="high" media="(min-width: 801px)">')
    ads_config = f"\n    window.inoAds = '{GOOGLE_ADS_ID}'; gtag('config', '{GOOGLE_ADS_ID}');" if GOOGLE_ADS_ID else ""
    # GA4 en Google Ads laden pas NA toestemming (cookiemelding in script.js). Zonder akkoord: geen cookies, geen verzoek naar Google.
    ga4_tag = f"""\n<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  window.inoGA4 = function () {{
    if (window.inoGA4geladen) return; window.inoGA4geladen = true;
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}';
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', '{GA4_MEASUREMENT_ID}', {{ anonymize_ip: true }});{ads_config}
  }};
  try {{ var host = location.hostname || ''; if (host === 'ino-elektra.nl' || host === 'www.ino-elektra.nl') {{ if (localStorage.getItem('ino_cookies') === 'ja') window.inoGA4(); }} }} catch (e) {{}}
</script>""" if GA4_MEASUREMENT_ID else ""
    return f"""<!doctype html>
<html lang="{taal.TAAL}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{ga4_tag}
<title>{t}</title>
<meta name="description" content="{d}">
{canon}
<meta name="robots" content="{robots}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#278a1d">
<meta name="format-detection" content="telephone=yes">
<meta property="og:locale" content="{L("nl_NL", "en_GB")}">{alts}
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
def header(nav_key, wijken, variant="standaard", wissel=None):
    groep = NAV_GROEP.get(nav_key, nav_key)
    topbar = (
        f'<div class="topbar"><div class="container topbar-inner">'
        + L('<span>Storing? <strong>24/7 bereikbaar</strong> · geen voorrijkosten in Utrecht</span>',
            '<span>Power fault? <strong>Available 24/7</strong> · English spoken · no call-out charge in Utrecht</span>')
        + f'<a href="tel:{B["telefoon_e164"]}" data-track="bellen">{ICON_TEL} {B["telefoon_tonen"]}</a>'
        f'</div></div>'
    )
    def lab(it):
        return it.get("label_en", it["label"]) if taal.en() else it["label"]
    items = []
    for it in NAV:
        active = ' aria-current="page"' if groep == it["key"] else ""
        cls_active = " active" if groep == it["key"] else ""
        sub = it.get("sub")
        href = pad(it["href"])
        if sub == "WIJKEN":
            top_links = (
                f'<div class="nav-dd-top">'
                f'  <a href="{pad("/werkgebied/")}" class="nav-dd-featured">'
                + L('    <strong>Werkgebied &amp; kaart</strong>    <span>Overzicht actieradius &amp; aanrijtijden</span>',
                    '    <strong>Service area &amp; map</strong>    <span>Where we work &amp; response times</span>')
                + f'  </a>'
                f'  <a href="{pad("/wijken/")}" class="nav-dd-all">'
                + L(f'    <span>Alle {len(wijken)} wijken &amp; plaatsen</span> →',
                    f'    <span>All {len(wijken)} neighbourhoods &amp; towns</span> →')
                + f'  </a>'
                f'</div>'
                f'<div class="nav-dd-divider"></div>'
                f'<div class="nav-dd-caption">{L("Direct naar wijk:", "Go to neighbourhood:")}</div>'
            )
            wijk_links = "".join(f'<a href="{pad("/elektricien-" + w["slug"] + "/")}" class="nav-dd-wijk-link">{w["naam"]}</a>' for w in wijken)
            menu_html = f'{top_links}<div class="nav-dd-scroll">{wijk_links}</div>'
            items.append(
                f'<div class="nav-dd nav-dd-werkgebied"><a href="{href}" class="nav-dd-toggle{cls_active}"{active}>{lab(it)} '
                f'<span class="caret" aria-hidden="true">▾</span></a><div class="nav-dd-menu">{menu_html}</div></div>')
        elif sub:
            links = "".join(f'<a href="{pad(x["href"])}">{lab(x)}</a>' for x in sub)
            items.append(
                f'<div class="nav-dd"><a href="{href}" class="nav-dd-toggle{cls_active}"{active}>{lab(it)} '
                f'<span class="caret" aria-hidden="true">▾</span></a><div class="nav-dd-menu">{links}</div></div>')
        else:
            items.append(f'<a href="{href}" class="{cls_active.strip()}"{active}>{lab(it)}</a>'.replace(' class=""', ""))
    nav = "\n      ".join(items)
    wissel_html = taalwissel(wissel) if wissel else ""
    return f"""<a class="skip-link" href="#inhoud">{L("Naar de inhoud", "Skip to content")}</a>
{topbar}
<header class="site-header">
  <div class="container nav-wrap">
    <a class="brand" href="{pad("/")}" aria-label="{B['naam']} – {L("elektricien Utrecht, naar de homepage", "electrician Utrecht, go to the homepage")}">
      <img src="/img/logo-390.png" alt="{B['naam']} – {L("elektricien Utrecht", "electrician Utrecht")}" width="130" height="54" decoding="async">
    </a>
    <nav id="nav" aria-label="{L("Hoofdmenu", "Main menu")}">
      {nav}
      <a class="nav-cta" href="{pad("/offerte/")}">{L("Offerte aanvragen", "Request a quote")}</a>
    </nav>
    {wissel_html}
    <button class="menu-btn" id="menuBtn" type="button" aria-label="{L("Menu openen", "Open menu")}" aria-expanded="false" aria-controls="nav">{ICON_MENU}</button>
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
    return f'<nav class="crumbs container" aria-label="{L("Kruimelpad", "Breadcrumb")}">{sep.join(parts)}</nav>'


# --------------------------------------------------------------------------- footer
def footer(wijken, storingen, variant="standaard", js="/script.js"):
    def wl(w):
        return f'<a href="{pad("/elektricien-" + w["slug"] + "/")}">{w["naam"]}</a>'
    top_links = "".join(wl(w) for w in wijken[:5])
    overige_links = "".join(wl(w) for w in wijken[5:])
    wijk_html = f"""<div class="footer-wijk-wrap">
      {top_links}
      <details class="footer-wijk-details">
        <summary class="footer-wijk-toggle">
          <span class="toggle-more">{L(f"+ Toon alle wijken ({len(wijken) - 5} meer)", f"+ Show all neighbourhoods ({len(wijken) - 5} more)")}</span>
          <span class="toggle-less">{L("− Minder wijken tonen", "− Show fewer")}</span>
        </summary>
        <div class="footer-wijk-more">
          {overige_links}
        </div>
      </details>
      <a href="{pad("/wijken/")}" class="footer-wijk-all">{L(f"Alle {len(wijken)} wijken &amp; kaart →", f"All {len(wijken)} neighbourhoods &amp; map →")}</a>
    </div>"""
    storing_links = "".join(f'<a href="{pad("/" + s["slug"] + "/")}">{s["kort"]}</a>' for s in storingen)
    kvk = (f' · KvK {B["kvk"]}' if B["kvk"] else "")
    btw = (f' · {L("btw", "VAT")} {B["btw"]}' if B["btw"] else "")
    if variant == "spoed":
        bar = f"""<div class="mobile-bar-emergency" role="navigation" aria-label="{L("Directe spoedacties", "Emergency actions")}">
  <a class="m-btn-call" href="tel:{B['telefoon_e164']}" data-track="bellen">{ICON_TEL}<span>{L("Bel nu (24/7)", "Call now (24/7)")}</span></a>
  <a class="m-btn-whatsapp" href="{wa_url(L('Hallo INO, ik heb nu een stroomstoring. Hierbij een foto van de meterkast.', 'Hello INO, I have a power fault right now. Here is a photo of my meter cupboard.'))}" target="_blank" rel="noopener" data-track="whatsapp">{ICON_WA}<span>{L("WhatsApp foto", "WhatsApp photo")}</span></a>
</div>"""
    else:
        bar = f"""<div class="mobile-bar-optimized" role="navigation" aria-label="{L("Snel contact", "Quick contact")}">
  <a href="tel:{B['telefoon_e164']}" class="mobile-btn-call" data-track="bellen">{ICON_TEL}<span>{L("Direct bellen", "Call now")}</span></a>
  <a href="{wa_url(L('Hallo INO, ik wil graag een foto sturen voor een prijsindicatie.', 'Hello INO, I would like to send a photo for a price estimate.'))}" target="_blank" rel="noopener" class="mobile-btn-whatsapp" data-track="whatsapp">{ICON_WA}<span>{L("WhatsApp foto", "WhatsApp photo")}</span></a>
</div>"""
    floating_wa = f"""<a href="{wa_url(L('Hallo INO Techniek, ik heb een vraag over een elektra klus. Kan ik een foto sturen voor advies?', 'Hello INO Techniek, I have a question about an electrical job. Can I send a photo for advice?'))}" class="floating-wa" target="_blank" rel="noopener" aria-label="{L("Direct chatten via WhatsApp", "Chat with us on WhatsApp")}" data-track="whatsapp" id="floatingWa">
  <span class="floating-wa-badge"><span class="floating-wa-pulse"></span>{L("Direct contact", "Quick contact")}</span>
  <span class="floating-wa-inner">
    <span class="floating-wa-icon">{ICON_WA}</span>
    <span class="floating-wa-text">
      <strong>{L("WhatsApp ons", "WhatsApp us")}</strong>
      <small>{L("Foto sturen &amp; richtprijs", "Send a photo &amp; get a price")}</small>
    </span>
  </span>
</a>"""
    diensten = [
        ("/diensten/", "Alle diensten", "All services"),
        ("/groepenkast/", "Groepenkast vervangen", "Fuse box replacement"),
        ("/perilex/", "Perilex &amp; kookgroep", "Perilex &amp; cooking circuit"),
        ("/laadpaal-installeren/", "Laadpaal installeren", "EV charger installation"),
        ("/krachtstroom-aanleggen/", "Krachtstroom 400V", "Three-phase power 400V"),
        ("/extra-groep-aanleggen/", "Extra groep aanleggen", "Extra circuit"),
        ("/frezen-stopcontacten-verleggen/", "Frezen &amp; stopcontacten", "Moving sockets &amp; chasing"),
        ("/tuinverlichting-buitenelektra/", "Tuinverlichting", "Garden lighting"),
        ("/offerte/", "Offerte aanvragen", "Request a quote"),
        ("/afspraak/", "Afspraak of schouw", "Appointment or site visit"),
    ]
    diensten_html = "".join(f'<a href="{pad(u)}">{L(n, e)}</a>' for u, n, e in diensten)
    cookie = (f' · <a href="#cookies" data-cookie-instellingen>{L("Cookie-instellingen", "Cookie settings")}</a>' if GA4_MEASUREMENT_ID else '')
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <img src="/img/logo-390.png" alt="{B['naam']} logo" class="footer-logo" width="130" height="54" loading="lazy" decoding="async">
      <p>{L("Elektricien in Utrecht en omstreken. Vaste prijs vooraf en 24/7 bereikbaar bij storingen.", "Electrician in Utrecht and the surrounding area. Fixed price upfront and available 24/7 for power faults.")}</p>
      <p><a href="tel:{B['telefoon_e164']}" data-track="bellen"><strong>{B['telefoon_tonen']}</strong></a><br>
      <a href="mailto:{B['email']}">{B['email']}</a></p>
      <div style="margin-top:14px;">
        <a href="{pad("/vakmanschap/")}" title="{L("INO Techniek is een SBB Erkend Leerbedrijf", "INO Techniek is an SBB Accredited Training Company")}">
          <img src="/img/sbb-erkend-leerbedrijf.svg" alt="{L("SBB Erkend Leerbedrijf - Wij leiden vakmensen op", "SBB Erkend Leerbedrijf (accredited training company) - we train future electricians")}" width="140" height="70" loading="lazy" style="display:block;border-radius:6px;">
        </a>
      </div>
    </div>
    <div><h2 class="footer-h">{L("Diensten", "Services")}</h2>{diensten_html}</div>
    <div><h2 class="footer-h">{L("Storing?", "Power fault?")}</h2><a href="{pad("/spoed-elektricien-utrecht/")}">{L("Spoed elektricien 24/7", "Emergency electrician 24/7")}</a>{storing_links}<a href="{pad("/tarieven/")}">{L("Tarieven", "Prices")}</a><a href="{pad("/faq/")}">{L("Veelgestelde vragen", "FAQ")}</a></div>
    <div><h2 class="footer-h">{L("Werkgebied", "Service area")}</h2><a href="{pad("/werkgebied/")}">{L("Werkgebied &amp; voorrijkosten", "Service area &amp; call-out charges")}</a>{wijk_html}</div>
  </div>
  <div class="copyright">© {JAAR} {B['naam']}{kvk}{btw} · <a href="{pad("/werkwijze/")}">{L("Werkwijze", "How we work")}</a> · <a href="{pad("/vakmanschap/")}">{L("Vakmanschap", "Qualifications")}</a> · <a href="{pad("/reviews/")}">Reviews</a> · <a href="{pad("/contact/")}">Contact</a> · <a href="{pad("/privacy/")}">{L("Privacy &amp; Cookies", "Privacy &amp; cookies")}</a>{cookie} · <a href="{B['instagram']}" target="_blank" rel="noopener">Instagram</a></div>
</footer>
{bar}
{floating_wa}
<script src="{js}?v={{JS_V}}" defer></script>"""
