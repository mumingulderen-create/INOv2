"""
Sjablonen voor pagina's die uit data worden gemaakt (wijken, storingen) en
voor blokken die in content-bestanden kunnen worden gezet met {{BLOK_NAAM}}.
"""
from html import escape
from config import SITE_URL, BEDRIJF as B, TARIEVEN as T, TARIEF_ZIN, VOORRIJ_ZIN
from layout import wa_url, ICON_TEL, ICON_WA


def fmt(s):
    """Vul {uur_dag}, {km_tarief} enz. in vanuit TARIEVEN."""
    return s.format(**T) if "{" in s else s


def faq_html(faq, titel="Veelgestelde vragen", intro=""):
    items = "".join(
        f'<button class="faq-q" type="button">{escape(fmt(q))}<span aria-hidden="true">+</span></button>'
        f'<div class="faq-a">{escape(fmt(a))}</div>' for q, a in faq)
    intro_html = f"<p>{intro}</p>" if intro else ""
    return f"""<section class="section" id="vragen">
  <div class="container narrow">
    <div class="section-heading"><h2>{titel}</h2>{intro_html}</div>
    <div class="faq">{items}</div>
  </div>
</section>"""


def cta_band(titel="Direct hulp of een vaste prijs?", tekst="Bel, app een foto van je meterkast of vraag een offerte aan. Je hoort altijd vooraf wat het kost.", wijk=""):
    q = f"?wijk={wijk}" if wijk else ""
    return f"""<section class="contact-cta">
  <div class="container">
    <h2>{titel}</h2>
    <p>{tekst}</p>
    <div class="hero-actions">
      <a class="btn btn-light" href="tel:{B['telefoon_e164']}" data-track="bellen">Bel {B['telefoon_tonen']}</a>
      <a class="btn btn-outline-light" href="{wa_url('Hallo INO, ik heb een vraag.')}" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp</a>
      <a class="btn btn-outline-light" href="/offerte{q}">Offerte aanvragen</a>
    </div>
  </div>
</section>"""


def tarief_kaarten(voorrij=True):
    extra = f'<p class="price-note form-note">{VOORRIJ_ZIN} Een schouw op locatie kost € {T["schouw"]} en verrekenen we volledig als je de klus laat uitvoeren.</p>' if voorrij else ""
    return f"""<div class="price-grid">
  <div class="price-card"><h3>Overdag</h3><div class="price-amount">€ {T['uur_dag']}<span> 1e uur</span></div><p>Ma–vr 08:00–18:00. Daarna € {T['kwartier_dag']} per kwartier.</p></div>
  <div class="price-card"><h3>Avond &amp; zaterdag</h3><div class="price-amount">€ {T['uur_avond']}<span> 1e uur</span></div><p>Ma–vr 18:00–22:00 en zaterdag. Daarna € {T['kwartier_avond']} per kwartier.</p></div>
  <div class="price-card highlight"><h3>Nacht, zondag &amp; feestdag</h3><div class="price-amount">€ {T['uur_nacht']}<span> 1e uur</span></div><p>22:00–08:00, zondag en feestdagen. Daarna € {T['kwartier_nacht']} per kwartier.</p></div>
</div>
<p class="form-note">Alle bedragen inclusief 21% btw en foutdiagnose. Meer werk of een onderdeel nodig? Dan hoor je eerst de prijs en beslis jij.</p>{extra}"""


KLUS_LINKS = [
    (("groepenkast", "kast"), "/groepenkast"),
    (("perilex", "kookgroep", "inductie", "koken"), "/perilex"),
    (("laadpaal",), "/laadpaal-installeren"),
    (("krachtstroom", "400v"), "/krachtstroom-aanleggen"),
    (("stopcontact", "frezen", "verbouwing", "keuken"), "/frezen-stopcontacten-verleggen"),
    (("tuin", "buiten", "schuur"), "/tuinverlichting-buitenelektra"),
    (("aardlek",), "/aardlekschakelaar-springt-eruit"),
    (("groep valt", "uitval"), "/kortsluiting-utrecht"),
    (("storing", "doormeten", "bedrading"), "/stroomstoring-utrecht"),
]


def klus_link(titel):
    t = titel.lower()
    for keys, href in KLUS_LINKS:
        if any(k in t for k in keys):
            return href
    return "/diensten"


# --------------------------------------------------------------------------- wijkpagina
def wijk_pagina(w, alle):
    naam = w["naam"]
    in_utrecht = w["type"] == "wijk"
    voorrij = "Geen voorrijkosten" if in_utrecht else f"€ {T['km_tarief']}/km voorrijden"
    locatie = f"{naam}, Utrecht" if in_utrecht else naam
    buurten = "".join(f"<span>{escape(b)}</span>" for b in w["buurten"])
    klussen = "".join(
        f'<article class="service-card"><h3>{escape(k)}</h3><p>{escape(fmt(u))}</p>'
        f'<a href="{klus_link(k + " " + u)}">Meer over deze klus</a></article>' for k, u in w["klussen"])
    aanrij = f'<span>Bij spoed: {w["aanrijtijd"]}</span>' if w["aanrijtijd"] else '<span>Bij spoed: bel voor de actuele aanrijtijd</span>'
    andere = [x for x in alle if x["slug"] != w["slug"]]
    andere_links = "".join(f'<a href="/elektricien-{x["slug"]}">Elektricien {x["naam"]}</a>' for x in andere)
    tarief_voorrij = (f"Binnen de gemeente Utrecht, en dus ook in {naam}, rekenen we geen voorrijkosten."
                      if in_utrecht else
                      f"{naam} ligt buiten de gemeente Utrecht. Voorrijden kost € {T['km_tarief']} per km; dat bedrag hoor je altijd vooraf.")
    wa = wa_url(f"Hallo INO, ik woon in {naam} en heb een vraag. Hierbij een foto.")
    body = f"""<section class="lp-hero">
  <div class="container">
    <div class="badge">Elektricien {escape(locatie)}</div>
    <h1>Elektricien {escape(naam)}: snel geholpen, vaste prijs vooraf</h1>
    <p>{escape(fmt(w['intro']))}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="tel:{B['telefoon_e164']}" data-track="bellen">{ICON_TEL} Bel {B['telefoon_tonen']}</a>
      <a class="btn btn-whatsapp" href="{wa}" target="_blank" rel="noopener" data-track="whatsapp">{ICON_WA} WhatsApp een foto</a>
      <a class="btn btn-secondary" href="/offerte?wijk={w['slug']}">Offerte aanvragen</a>
    </div>
    <div class="meta-row"><span>24/7 bij storingen</span>{aanrij}<span>{voorrij}</span><span>{T['garantie_maanden']} mnd garantie</span></div>
  </div>
</section>

<section class="section">
  <div class="container area-layout">
    <div>
      <h2>Woningen in {escape(naam)} en wat dat betekent voor je elektra</h2>
      <p>{escape(fmt(w['woningen']))}</p>
      <p>{escape(fmt(w['lokaal']))}</p>
      <div class="area-chips" aria-label="Buurten in {escape(naam)}">{buurten}</div>
    </div>
    <aside class="area-card">
      <h3>Wat kost een elektricien in {escape(naam)}?</h3>
      <ul class="include-items compact">
        <li>Overdag: € {T['uur_dag']} (1e uur, incl. btw)</li>
        <li>Avond &amp; zaterdag: € {T['uur_avond']}</li>
        <li>Nacht, zondag &amp; feestdag: € {T['uur_nacht']}</li>
        <li>Groepenkast 1-fase: vanaf € {T['groepenkast_1f']} all-in</li>
        <li>Perilex aansluiten: € {T['perilex_aansluiten']}</li>
      </ul>
      <p class="form-note">{escape(tarief_voorrij)}</p>
      <a class="mini-link" href="/tarieven">Alle tarieven bekijken</a>
    </aside>
  </div>
</section>

<section class="section soft">
  <div class="container">
    <div class="section-heading"><h2>Veelgevraagde klussen in {escape(naam)}</h2>
    <p>Dit doen we het vaakst voor bewoners in {escape(naam)}. Staat jouw klus er niet tussen? Bekijk <a class="mini-link" href="/diensten">alle diensten</a>.</p></div>
    <div class="service-grid">{klussen}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <a class="alert-banner" href="/spoed-elektricien-utrecht">
      <div><strong>Nu een storing in {escape(naam)}?</strong>
      <span>Geen stroom, een aardlek die blijft uitvallen of brandlucht? Bel {B['telefoon_tonen']}, ook 's nachts en in het weekend.</span></div>
      <span class="arrow" aria-hidden="true">→</span>
    </a>
    <div class="quick-help">
      <a href="/stroomstoring-utrecht">Geen stroom in huis</a>
      <a href="/aardlekschakelaar-springt-eruit">Aardlek springt eruit</a>
      <a href="/kortsluiting-utrecht">Groep valt steeds uit</a>
      <a href="/stopcontact-werkt-niet">Stopcontact werkt niet</a>
    </div>
  </div>
</section>

{faq_html(w['faq'], f"Vragen van bewoners uit {escape(naam)}")}

<section class="section soft">
  <div class="container">
    <h2>Ook actief in de buurt</h2>
    <div class="link-cloud">{andere_links}<a href="/wijken">Alle wijken en plaatsen</a></div>
  </div>
</section>

{cta_band(f"Elektricien nodig in {escape(naam)}?", wijk=w['slug'])}
"""
    title = f"Elektricien {naam} | 24/7 storing & vaste prijs | INO Techniek"
    if len(title) > 62:
        title = f"Elektricien {naam} | 24/7 & vaste prijs | INO"
    desc = (f"Elektricien in {naam} nodig? Storing, groepenkast, Perilex of laadpaal. Vaste prijs vooraf, "
            f"24/7 bereikbaar, {'geen voorrijkosten' if in_utrecht else 'eerlijke km-vergoeding'}. Bel {B['telefoon_tonen']}.")
    schema = [{
        "@type": "Service", "@id": f"{SITE_URL}/elektricien-{w['slug']}#service",
        "name": f"Elektricien {naam}", "serviceType": "Elektricien",
        "areaServed": {"@type": "City" if not in_utrecht else "Place", "name": locatie},
        "description": fmt(w["intro"]),
    }]
    return {
        "slug": f"elektricien-{w['slug']}", "title": title, "description": desc, "body": body,
        "nav": "wijken", "schema": schema, "faq": [[fmt(q), fmt(a)] for q, a in w["faq"]],
        "crumbs": [("Werkgebied", "/werkgebied"), ("Wijken", "/wijken"), (f"Elektricien {naam}", None)],
        "og_image": "storingsdienst-meting.jpg", "priority": "0.8",
    }


# --------------------------------------------------------------------------- storingpagina
def storing_pagina(s, alle):
    stappen = "".join(
        f'<li><h3>{escape(t)}</h3><p>{escape(fmt(u))}</p></li>' for t, u in s["stappen"])
    oorzaken = "".join(
        f'<div class="cert-card"><h3>{escape(t)}</h3><p>{escape(fmt(u))}</p></div>' for t, u in s["oorzaken"])
    gerel = {x["slug"]: x for x in alle}
    rel = "".join(f'<a href="/{r}">{gerel[r]["kort"]}</a>' for r in s["gerelateerd"] if r in gerel)
    wa = wa_url(f"Hallo INO, ik heb een probleem: {s['kort'].lower()}. Hierbij een foto van mijn meterkast.")
    body = f"""<section class="lp-hero storing-hero">
  <div class="container">
    <div class="badge">24/7 hulp bij storingen in Utrecht e.o.</div>
    <h1>{escape(s['h1'])}</h1>
    <p>{escape(fmt(s['intro']))}</p>
    <div class="hero-actions">
      <a class="btn btn-primary btn-lg" href="tel:{B['telefoon_e164']}" data-track="bellen">{ICON_TEL} Direct een elektricien: {B['telefoon_tonen']}</a>
      <a class="btn btn-whatsapp" href="{wa}" target="_blank" rel="noopener" data-track="whatsapp">{ICON_WA} Stuur foto via WhatsApp</a>
    </div>
    <div class="meta-row"><span>Direct de monteur aan de lijn</span><span>Vaste prijs vóór we beginnen</span><span>Geen voorrijkosten in Utrecht</span></div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    <div class="danger-box" role="note"><strong>Eerst je veiligheid</strong><p>{escape(s['gevaar'])}</p></div>
    <h2>{escape(s['stappen_titel'])}</h2>
    <ol class="check-steps">{stappen}</ol>
    <p class="safety-note">Werk nooit zelf aan de groepenkast of aan leidingen. Een schakelaar omhoog of omlaag zetten en stekkers eruit halen kan veilig; al het andere laat je aan een elektricien over.</p>
  </div>
</section>

<section class="section soft">
  <div class="container">
    <div class="section-heading"><h2>{escape(s['oorzaken_titel'])}</h2></div>
    <div class="cert-grid">{oorzaken}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-heading"><h2>Lukt het niet? Dit kost het als wij komen</h2>
    <p>Geen woekertarieven of verrassingen: we werken met vaste, eerlijke tarieven die op de site staan. Je spreekt direct de monteur, geen callcenter.</p></div>
    {tarief_kaarten()}
  </div>
</section>

{faq_html(s['faq'])}

<section class="section soft">
  <div class="container">
    <h2>Andere storingen</h2>
    <div class="link-cloud">{rel}<a href="/spoed-elektricien-utrecht">Spoed elektricien 24/7</a><a href="/wijken">Werkgebied per wijk</a></div>
  </div>
</section>

{cta_band("Kom je er niet uit? Wij komen direct.", "Bel of app, ook 's avonds, 's nachts en in het weekend. Je hoort vooraf wat het kost.")}
"""
    return {
        "slug": s["slug"], "title": s["title"], "description": s["description"], "body": body,
        "nav": s["slug"], "faq": [[fmt(q), fmt(a)] for q, a in s["faq"]],
        "crumbs": [("Spoed 24/7", "/spoed-elektricien-utrecht"), (s["kort"], None)],
        "og_image": "storingsdienst-meting.jpg", "priority": "0.8",
        "schema": [{"@type": "Service", "name": s["kort"] + " verhelpen", "serviceType": "Storingsdienst elektra",
                    "areaServed": {"@type": "City", "name": "Utrecht"}}],
    }


# --------------------------------------------------------------------------- blokken voor content
def blok_storing_kaarten(storingen):
    return '<div class="quick-help quick-help-lg">' + "".join(
        f'<a href="/{s["slug"]}">{s["kort"]}</a>' for s in storingen) + \
        '<a href="/spoed-elektricien-utrecht" class="qh-urgent">Iets anders / acuut</a></div>'


def blok_wijk_chips(wijken):
    return '<div class="link-cloud">' + "".join(
        f'<a href="/elektricien-{w["slug"]}">{w["naam"]}</a>' for w in wijken) + \
        '<a href="/wijken">Alle wijken</a></div>'


def blok_wijken_hub(wijken, overige_utrecht, overige_regio):
    def card(naam, sub, href):
        return (f'<a class="wijk-card" href="{href}"><div><h3>Elektricien {escape(naam)}</h3>'
                f'<p>{escape(sub)}</p></div></a>')
    u = [card(w["naam"], " · ".join(w["buurten"][:3]), f"/elektricien-{w['slug']}") for w in wijken if w["type"] == "wijk"]
    u += [card(n, sub, f"/offerte?wijk={n.replace(' ', '-')}") for n, sub in overige_utrecht]
    r = [card(w["naam"], " · ".join(w["buurten"][:3]), f"/elektricien-{w['slug']}") for w in wijken if w["type"] == "plaats"]
    r += [card(n, sub, f"/offerte?wijk={n.replace(' ', '-')}") for n, sub in overige_regio]
    return (f'<h2 class="wijk-label">Gemeente Utrecht · geen voorrijkosten</h2><div class="wijk-grid">{"".join(u)}</div>'
            f'<h2 class="wijk-label">Regio Utrecht · € {T["km_tarief"]} per km</h2><div class="wijk-grid">{"".join(r)}</div>')
