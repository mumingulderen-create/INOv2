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
    "werkspot": "",                            # VUL_IN: volledige URL van je Werkspot-profiel
    "actief_sinds": "2021",
    # --- Wettelijk verplicht op je website (Handelsregisterwet): KvK-nummer ---
    "kvk": "",                                 # VUL_IN: bijv. "12345678"
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

GOOGLE_SITE_VERIFICATION = "xHeZ_iY8KLYVB6SQZzxa5C9qnocjO7YkzjrELzLSXWw"

# FormSubmit endpoint (formulieren -> je mailbox)
FORM_ENDPOINT = "https://formsubmit.co/ajax/d0d9de6bb2a30083d92c3fe4775b9ce6"

# ---------------------------------------------------------------------------
# TARIEVEN — alle bedragen incl. 21% btw. Eén bron voor de hele site.
# ---------------------------------------------------------------------------
TARIEVEN = {
    "uur_dag": 90,            # ma-vr 08:00-18:00
    "uur_avond": 120,         # ma-vr 18:00-22:00 en zaterdag
    "uur_nacht": 145,         # 22:00-08:00, zondag en feestdagen
    "kwartier_dag": "22,50",
    "kwartier_avond": "30,00",
    "kwartier_nacht": "36,25",
    "voorrijkosten_utrecht": 0,
    "km_tarief": "0,40",      # buiten gemeente Utrecht
    "schouw": 90,             # wordt verrekend bij opdracht
    "groepenkast_1f": 620,
    "groepenkast_3f": 720,
    "extra_groep": 60,
    "perilex_aansluiten": 120,
    "perilex_kookgroep": 150,
    "stopcontact_verleggen": 120,
    "frezen_per_meter": 10,
    "garantie_maanden": 12,
}

# Tekstblokjes die op meerdere plekken terugkomen (automatisch consistent)
T = TARIEVEN
TARIEF_ZIN = (
    f"Ma–vr 08:00–18:00 € {T['uur_dag']}, ma–vr 18:00–22:00 en zaterdag € {T['uur_avond']}, "
    f"22:00–08:00, zondag en feestdagen € {T['uur_nacht']} (eerste uur, incl. btw)"
)
VOORRIJ_ZIN = (
    f"Binnen de gemeente Utrecht rekenen we € {T['voorrijkosten_utrecht']},- voorrijkosten. "
    f"Daarbuiten geldt een vast kilometertarief van € {T['km_tarief']} per km."
)

# ---------------------------------------------------------------------------
# NAVIGATIE (header). 'sub' = uitklapmenu.
# ---------------------------------------------------------------------------
NAV = [
    {"label": "Spoed 24/7", "href": "/spoed-elektricien-utrecht", "key": "spoed", "sub": [
        {"label": "Spoed elektricien 24/7", "href": "/spoed-elektricien-utrecht"},
        {"label": "Geen stroom in huis", "href": "/stroomstoring-utrecht"},
        {"label": "Aardlekschakelaar springt eruit", "href": "/aardlekschakelaar-springt-eruit"},
        {"label": "Kortsluiting / groep valt uit", "href": "/kortsluiting-utrecht"},
        {"label": "Stopcontact werkt niet of wordt warm", "href": "/stopcontact-werkt-niet"},
    ]},
    {"label": "Diensten", "href": "/diensten", "key": "diensten", "sub": [
        {"label": "Alle diensten", "href": "/diensten"},
        {"label": "Groepenkast vervangen", "href": "/groepenkast"},
        {"label": "Perilex & kookgroep", "href": "/perilex"},
        {"label": "Laadpaal installeren", "href": "/laadpaal-installeren"},
        {"label": "Krachtstroom 400V", "href": "/krachtstroom-aanleggen"},
        {"label": "Frezen & stopcontacten", "href": "/frezen-stopcontacten-verleggen"},
        {"label": "Tuinverlichting", "href": "/tuinverlichting-buitenelektra"},
    ]},
    {"label": "Tarieven", "href": "/tarieven", "key": "tarieven"},
    {"label": "Werkgebied", "href": "/werkgebied", "key": "werkgebied", "sub": "WIJKEN"},  # automatisch gevuld
    {"label": "Werkwijze", "href": "/werkwijze", "key": "werkwijze"},
    {"label": "Reviews", "href": "/reviews", "key": "reviews"},
    {"label": "Contact", "href": "/contact", "key": "contact"},
]

# Welke pagina-sleutel hoort bij welk hoofdmenu-item (voor 'actief' markeren)
NAV_GROEP = {
    "groepenkast": "diensten", "perilex": "diensten", "laadpaal-installeren": "diensten",
    "krachtstroom-aanleggen": "diensten", "frezen-stopcontacten-verleggen": "diensten",
    "tuinverlichting-buitenelektra": "diensten", "diensten": "diensten",
    "spoed-elektricien-utrecht": "spoed", "stroomstoring-utrecht": "spoed",
    "aardlekschakelaar-springt-eruit": "spoed", "kortsluiting-utrecht": "spoed",
    "stopcontact-werkt-niet": "spoed",
    "werkgebied": "werkgebied", "wijken": "werkgebied",
}
