"""
CENTRALE INSTELLINGEN — INO Techniek en Installatie
===================================================
Dit is de ENIGE plek waar bedrijfsgegevens en tarieven staan.
Pas hier iets aan -> draai `python3 build.py` -> alle pagina's, structured data
(Google) en de sitemap worden automatisch bijgewerkt.

Velden met "VUL_IN" zijn nog leeg. Zolang ze leeg zijn worden ze nergens getoond.
"""

SITE_URL = "https://ino-elektra.nl"

BEDRIJF = {
    "naam": "INO Techniek en Installatie",
    "korte_naam": "INO",
    "alternatieve_naam": "INO Elektra Utrecht",
    "slogan": "Techniek · Installatie · Innovatie",
    "telefoon_e164": "+31628763775",          # voor tel:-links en schema
    "telefoon_tonen": "06 28 76 37 75",        # zoals mensen het lezen
    "whatsapp": "31628763775",
    "email": "info@ino-elektra.nl",
    "instagram": "https://www.instagram.com/ino_techniek_en_installatie",
    # Google Bedrijfsprofiel (cid uit je bestaande reviews-link)
    "google_maps": "https://maps.google.com/?cid=15258938996024411928",
    # Google-score zoals Google hem toont (gecontroleerd 24 sept 2026). Bijwerken als het aantal groeit. Alleen zichtbaar tonen met link naar Google,
    # NIET als AggregateRating-schema (Google staat zelf-reviews voor LocalBusiness niet toe).
    # Directe "review schrijven"-link uit je Google Bedrijfsprofiel (knop "Vraag om reviews",
    # ziet eruit als https://g.page/r/XXXX/review). Leeg = /review/ stuurt naar je Maps-profiel.
    "google_review_url": "https://g.page/r/CRgHZOsrpMLTEBM/review",
    "google_score": "5,0",
    "google_aantal": "37",
    "werkspot": "",                            # VUL_IN: volledige URL van je Werkspot-profiel
    "actief_sinds": "2021",
    # --- Wettelijk verplicht op je website (Handelsregisterwet): KvK-nummer ---
    "kvk": "86669346",
    "btw": "",                                 # VUL_IN (optioneel)
    # Adres: alleen invullen als je dit ook in Google Bedrijfsprofiel toont.
    # Werk je vanuit huis als servicegebied-bedrijf? Laat straat/postcode leeg.
    "straat": "",
    "postcode": "",
    "plaats": "Utrecht",
    "provincie": "Utrecht",
    "lat": 52.0907,
    "lng": 5.1214,
}

# Echte Google-reviews (letterlijk overnemen van je Google-profiel, nooit zelf verzinnen).
# Voeg nieuwe reviews toe als {"naam": ..., "tekst": ...}; de carrousel op /reviews/ groeit vanzelf mee.
REVIEWS = [
    {"naam": "Ali", "tekst": "Zeer tevreden over de service. Professioneel, netjes gewerkt en duidelijke communicatie. Zeker een aanrader!"},
    {"naam": "Hasan Demir", "tekst": "Geweldige klusbedrijf, zeker aan te raden! Heel netjes en snel afgehandeld."},
]

# Bevriende collega (bevestigd door eigenaar): we sturen elkaar klanten door buiten het eigen werkgebied.
# Alleen linken vanaf /werkgebied/ en /contact/, niet in header/footer (sitewide links ziet Google als linkruil).
PARTNER_VOLTFIX = {
    "naam": "Voltfix Elektrotechniek",
    "url": "https://www.voltfix.nl/",
    "regio": "Amsterdam",
}

GOOGLE_SITE_VERIFICATION = "xHeZ_iY8KLYVB6SQZzxa5C9qnocjO7YkzjrELzLSXWw"

# Google Analytics 4 (GA4) Meet-ID (bijv. "G-XXXXXXXXXX" of leeg laten)
GA4_MEASUREMENT_ID = "G-HR6L1S8V7P"

# FormSubmit endpoint (formulieren -> je mailbox)
FORM_ENDPOINT = "https://formsubmit.co/ajax/d0d9de6bb2a30083d92c3fe4775b9ce6"

# ---------------------------------------------------------------------------
# AANRIJTIJDEN bij spoed (vertrek vanuit Overvecht). Gebruik {{aanrijtijd_utrecht}} / {{aanrijtijd_regio}}.
# ---------------------------------------------------------------------------
AANRIJTIJD = {
    "aanrijtijd_utrecht": "5–30",   # gemeente Utrecht
    "aanrijtijd_regio": "15–40",    # plaatsen buiten de gemeente Utrecht
}

# ---------------------------------------------------------------------------
# TARIEVEN — alle bedragen incl. 21% btw. Eén bron voor de hele site.
# ---------------------------------------------------------------------------
TARIEVEN = {
    "uur_dag": 90,            # ma-vr 08:00-18:00
    "uur_avond": 120,         # ma-vr 18:00-22:00
    "uur_nacht": 145,         # 22:00-08:00, zaterdag, zondag en feestdagen
    "kwartier_dag": "22,50",
    "kwartier_avond": "30,00",
    "kwartier_nacht": "36,25",
    "voorrijkosten_utrecht": 0,
    "km_tarief": "0,40",      # buiten gemeente Utrecht
    "schouw": 90,             # wordt verrekend bij opdracht
    "groepenkast_1f": 640,        # 1-fase tot 8 groepen, all-in (bevestigd eigenaar)
    "groepenkast_3f": 760,        # 3-fase tot 8 groepen, all-in (bevestigd eigenaar)
    "extra_groep": 60,
    "perilex_aansluiten": 120,
    "perilex_kookgroep": 150,
    "stopcontact_verleggen": 120,
    "frezen_per_meter": 10,
    "garantie_maanden": 12,
    # Extra groep (pagina /extra-groep-aanleggen)
    "extra_groep_leiding": 165,        # aparte groep + leiding trekken (richtprijs vanaf)
    "extra_groep_leiding_max": 220,    # meestal tussen .._leiding en dit bedrag
    "extra_krachtgroep_3fase": 185,    # 3-fase krachtgroep 400V
    # Frezen & stopcontacten
    "frezen_steen_per_meter": 15,      # baksteen / kalkzandsteen
    "frezen_beton_per_meter": 30,      # (gewapend) beton
    "stopcontact_complex_min": 130,    # lastige locatie / grotere afstand
    "stopcontact_complex_max": 250,
    # Groepenkast: opties bij vervangen (ook gebruikt door de calculator)
    "optie_kookgroep": 85,
    "optie_pv": 95,
    "optie_kracht_4p": 185,
    "optie_automaat": 45,
    "optie_din_stopcontact": 39,
    "optie_beltrafo": 49,
    "optie_spd": 169,
    # Groepenkast-calculator (zelfde bedragen als op de live site)
}
# Calculator rekent met dezelfde bedragen als de rest van de site
TARIEVEN["calc_basis_1f"] = TARIEVEN["groepenkast_1f"]
TARIEVEN["calc_meer_3f"] = TARIEVEN["groepenkast_3f"] - TARIEVEN["groepenkast_1f"]

# Tekstblokjes die op meerdere plekken terugkomen (automatisch consistent)
T = TARIEVEN
TARIEF_ZIN = (
    f"Ma–vr 08:00–18:00 € {T['uur_dag']}, ma–vr 18:00–22:00 € {T['uur_avond']}, "
    f"22:00–08:00 en zaterdag & zondag € {T['uur_nacht']} (eerste uur incl. diagnose en btw)"
)
VOORRIJ_ZIN = (
    f"Binnen de gemeente Utrecht rekenen we € {T['voorrijkosten_utrecht']},- voorrijkosten. "
    f"Daarbuiten geldt een vast kilometertarief van € {T['km_tarief']} per km."
)

# ---------------------------------------------------------------------------
# NAVIGATIE (header). 'sub' = uitklapmenu.
# ---------------------------------------------------------------------------
NAV = [
    {"label": "Spoed 24/7", "href": "/spoed-elektricien-utrecht/", "key": "spoed", "sub": [
        {"label": "Spoed elektricien 24/7", "href": "/spoed-elektricien-utrecht/"},
        {"label": "Geen stroom in huis", "href": "/stroomstoring-utrecht/"},
        {"label": "Aardlekschakelaar springt eruit", "href": "/aardlekschakelaar-springt-eruit/"},
        {"label": "Kortsluiting / groep valt uit", "href": "/kortsluiting-utrecht/"},
        {"label": "Stopcontact werkt niet of wordt warm", "href": "/stopcontact-werkt-niet/"},
    ]},
    {"label": "Diensten", "href": "/diensten/", "key": "diensten", "sub": [
        {"label": "Alle diensten", "href": "/diensten/"},
        {"label": "Groepenkast vervangen", "href": "/groepenkast/"},
        {"label": "Perilex & kookgroep", "href": "/perilex/"},
        {"label": "Laadpaal installeren", "href": "/laadpaal-installeren/"},
        {"label": "Krachtstroom 400V", "href": "/krachtstroom-aanleggen/"},
        {"label": "Frezen & stopcontacten", "href": "/frezen-stopcontacten-verleggen/"},
        {"label": "Extra groep aanleggen", "href": "/extra-groep-aanleggen/"},
        {"label": "Tuinverlichting", "href": "/tuinverlichting-buitenelektra/"},
    ]},
    {"label": "Tarieven", "href": "/tarieven/", "key": "tarieven"},
    {"label": "Werkgebied", "href": "/werkgebied/", "key": "werkgebied", "sub": "WIJKEN"},  # automatisch gevuld
    {"label": "Werkwijze", "href": "/werkwijze/", "key": "werkwijze"},
    {"label": "Reviews", "href": "/reviews/", "key": "reviews"},
    {"label": "Contact", "href": "/contact/", "key": "contact"},
]

# Welke pagina-sleutel hoort bij welk hoofdmenu-item (voor 'actief' markeren)
NAV_GROEP = {
    "groepenkast": "diensten", "perilex": "diensten", "laadpaal-installeren": "diensten",
    "krachtstroom-aanleggen": "diensten", "frezen-stopcontacten-verleggen": "diensten",
    "extra-groep-aanleggen": "diensten", "tuinverlichting-buitenelektra": "diensten", "diensten": "diensten",
    "spoed-elektricien-utrecht": "spoed", "stroomstoring-utrecht": "spoed",
    "aardlekschakelaar-springt-eruit": "spoed", "kortsluiting-utrecht": "spoed",
    "stopcontact-werkt-niet": "spoed",
    "werkgebied": "werkgebied", "wijken": "werkgebied",
}
