"""
TALEN (NL / EN)
===============
De site bestaat in het Nederlands (hoofdtaal, /pagina/) en het Engels (/en/page/).

- Elke Nederlandse pagina heeft een Engelse tegenhanger. De koppeling staat in EN_SLUG
  (Nederlandse slug -> Engelse slug, zonder "en/").
- Engelse contentbestanden staan in content/en/ en hebben DEZELFDE bestandsnaam als het
  Nederlandse bestand (content/en/groepenkast.html hoort bij content/groepenkast.html).
- Wijken: bouw/wijken_en.py, storingen: bouw/storingen_en.py.
- In sjablonen (layout.py, paginas.py): L("Nederlands", "English") en pad("/nl-pad/").
- Links in content/en/ schrijf je direct naar de Engelse adressen (/en/quote/). De build
  waarschuwt als een Engelse pagina naar een Nederlandse pagina linkt (en andersom).

Nieuwe pagina? Voeg de slug toe aan EN_SLUG en maak content/en/<zelfde-naam>.html.
"""

TAAL = "nl"          # huidige taal tijdens het bouwen van één pagina (zet() in build.py)
TALEN = ("nl", "en")

EN_SLUG = {
    "": "",
    "spoed-elektricien-utrecht": "emergency-electrician-utrecht",
    "stroomstoring-utrecht": "power-outage-utrecht",
    "aardlekschakelaar-springt-eruit": "rcd-keeps-tripping",
    "kortsluiting-utrecht": "short-circuit-utrecht",
    "stopcontact-werkt-niet": "socket-not-working",
    "diensten": "services",
    "groepenkast": "fuse-box-replacement",
    "perilex": "perilex-cooker-connection",
    "laadpaal-installeren": "ev-charger-installation",
    "thuisbatterij-installeren": "home-battery-installation",
    "krachtstroom-aanleggen": "three-phase-power",
    "frezen-stopcontacten-verleggen": "moving-sockets-wall-chasing",
    "extra-groep-aanleggen": "extra-circuit",
    "tuinverlichting-buitenelektra": "garden-lighting-outdoor-electrics",
    "buitengesloten-cilinder-vervangen": "locked-out-lock-cylinder",
    "slim-deurslot-installeren": "smart-lock-installation",
    "videodeurbel-installeren": "video-doorbell-installation",
    "inductiekookplaat-aansluiten": "induction-hob-installation",
    "tv-ophangen": "tv-wall-mounting",
    "mv-box-vervangen": "ventilation-unit-replacement",
    "aardpen-slaan": "earth-rod-installation",
    "tarieven": "prices",
    "werkgebied": "service-area",
    "wijken": "neighbourhoods",
    "werkwijze": "how-we-work",
    "vakmanschap": "qualifications",
    "reviews": "reviews",
    "offerte": "quote",
    "afspraak": "appointment",
    "faq": "faq",
    "contact": "contact",
    "privacy": "privacy",
    "review": "review",
}

# Wijkslugs: /elektricien-<slug>/ -> /en/electrician-<engelse slug>/
EN_WIJK = {
    "utrecht-binnenstad": "utrecht-city-centre",
    "utrecht-oost": "utrecht-east",
    "utrecht-noordoost": "utrecht-northeast",
}


def registreer_wijken(wijken):
    for w in wijken:
        EN_SLUG[f"elektricien-{w['slug']}"] = "electrician-" + EN_WIJK.get(w["slug"], w["slug"])


def zet(taal):
    global TAAL
    TAAL = taal


def L(nl, en):
    """Tekst in de huidige taal."""
    return en if TAAL == "en" else nl


def en(taal=None):
    return (taal or TAAL) == "en"


def slug_in(nl_slug, taal=None):
    """Volledige slug (zoals in de URL, zonder slashes) van een pagina in een taal."""
    if not en(taal):
        return nl_slug
    e = EN_SLUG.get(nl_slug)
    if e is None:
        return None
    return "en" if e == "" else f"en/{e}"


def pad(nl_pad, taal=None):
    """'/groepenkast/?x=1#a' -> '/en/fuse-box-replacement/?x=1#a' als de taal Engels is."""
    if not en(taal) or not nl_pad.startswith("/") or nl_pad.startswith("//"):
        return nl_pad
    rest = ""
    for teken in "?#":
        if teken in nl_pad:
            i = nl_pad.index(teken)
            nl_pad, rest = nl_pad[:i], nl_pad[i:] + rest
            break
    kaal = nl_pad.strip("/")
    if "." in kaal.split("/")[-1]:      # bestand (/img/x.png, /qr/kaart.pdf)
        return nl_pad + rest
    s = slug_in(kaal, "en")
    if s is None:
        return nl_pad + rest
    return f"/{s}/" + rest


# Kruimelpad-namen (BREADCRUMB_NAMEN in build.py) in het Engels
CRUMB_EN = {
    "Diensten": "Services",
    "Groepenkast": "Fuse box",
    "Perilex": "Perilex",
    "Laadpaal": "EV charger",
    "Thuisbatterij installeren": "Home battery",
    "Krachtstroom": "Three-phase power",
    "Frezen & stopcontacten": "Moving sockets",
    "Extra groep aanleggen": "Extra circuit",
    "Tuinverlichting": "Garden lighting",
    "Buitengesloten": "Locked out",
    "Slim deurslot": "Smart lock",
    "Videodeurbel": "Video doorbell",
    "Kookplaat aansluiten": "Induction hob",
    "TV ophangen": "TV mounting",
    "MV-box vervangen": "Ventilation unit",
    "Aardpen slaan": "Earth rod",
    "Tarieven": "Prices",
    "Werkgebied": "Service area",
    "Alle wijken": "All neighbourhoods",
    "Wijken": "Neighbourhoods",
    "Werkwijze": "How we work",
    "Vakmanschap": "Qualifications",
    "Reviews": "Reviews",
    "Offerte": "Quote",
    "Afspraak": "Appointment",
    "Veelgestelde vragen": "FAQ",
    "Contact": "Contact",
    "Privacy": "Privacy",
    "Spoed 24/7": "Emergency 24/7",
}

# Bedragen en scores in Engelse notatie (punt in plaats van komma)
def getal_en(v):
    return str(v).replace(",", ".")
