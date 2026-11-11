"""Donkere weergave: maakt donker.css uit de gewone stylesheets.

De site blijft in assets/style.css licht ontworpen. Dit bestand leidt daar per regel
een donkere tegenhanger uit af (lichte vlakken worden donker, donkere tekst wordt licht)
en zet die in donker.css. layout.py laadt dat bestand met
media="(prefers-color-scheme: dark)": het volgt dus de instelling van het toestel.

Klopt een kleur niet in het donker, zet dan een regel in HANDMATIG onderaan.
"""
import colorsys
import re

# Vaste donkere tinten (groenig zwart, passend bij --dark)
PAGINA = "#0e1410"
GROEN_TEKST = "#7ddc62"
VARS = ":root{color-scheme:dark;--ink:#e8ede9;--muted:#a3ada6;--soft:#131a15;--line:#2b352d}"

# Regels die de automaat niet goed kan raden. Staan achteraan en winnen dus.
HANDMATIG = """
body{background:%s}
.nav-cta{color:#111827}
.floating-wa-text strong{color:#0b2e17}
.floating-wa-text small{color:rgba(11,46,23,.85)}
""" % PAGINA

HEX = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![0-9a-fA-F])")
RGBA = re.compile(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)")


def _rgb(h):
    h = h.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(r, g, b):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v * 255))) for v in (r, g, b))


def _hls(h):
    return colorsys.rgb_to_hls(*_rgb(h))


def vlak(h):
    """Lichte achtergrond -> donker vlak (None = laten staan)."""
    hue, l, s = _hls(h)
    if l < 0.78:
        return None
    if s < 0.08:
        hue, s = 0.375, 0.13          # wit/grijs: neutraal groenig
    else:
        s = min(s, 0.32)
    return _hex(*colorsys.hls_to_rgb(hue, 0.115 + (1 - l) * 0.75, s))


def tekst(h):
    """Donkere tekst -> lichte tekst (None = laten staan)."""
    hue, l, s = _hls(h)
    if l >= 0.5:
        return None
    return _hex(*colorsys.hls_to_rgb(hue, 0.9 - 0.5 * l, min(s, 0.75)))


def rand(h):
    """Lichte rand -> donkere rand (None = laten staan)."""
    hue, l, s = _hls(h)
    if l < 0.72:
        return None
    if s < 0.08:
        hue, s = 0.375, 0.1
    return _hex(*colorsys.hls_to_rgb(hue, 0.2 + (1 - l) * 0.5, min(s, 0.3)))


def _wit_rgba(m, fn):
    r, g, b = (float(m.group(i)) / 255 for i in (1, 2, 3))
    a = float(m.group(4)) if m.group(4) else 1.0
    if a < 0.5:
        return None
    nieuw = fn(_hex(r, g, b))
    if not nieuw:
        return None
    rr, gg, bb = (round(v * 255) for v in _rgb(nieuw))
    return f"rgba({rr},{gg},{bb},{a:g})"


def _vervang(waarde, fn):
    """Vervang elke kleur in een waarde; geeft (nieuwe waarde, gewijzigd?)."""
    gewijzigd = [False]

    def hx(m):
        if len(m.group(1)) in (4, 8):
            return m.group(0)
        n = fn(m.group(0))
        if n:
            gewijzigd[0] = True
            return n
        return m.group(0)

    def rg(m):
        n = _wit_rgba(m, fn)
        if n:
            gewijzigd[0] = True
            return n
        return m.group(0)

    return RGBA.sub(rg, HEX.sub(hx, waarde)), gewijzigd[0]


def _is_licht_vlak(waarde):
    """Zet deze achtergrond een licht vlak neer?"""
    w = waarde.replace(" ", "").lower()
    if w in ("none", "transparent", "inherit") or w.startswith("var(--soft)") or w.startswith("var(--line)"):
        return True
    kleuren = HEX.findall(waarde)      # met spaties: "#e6f6e3 0%" moet één kleur blijven
    if kleuren:
        return all(_hls("#" + k)[1] >= 0.78 for k in kleuren if len(k) in (3, 6))
    m = RGBA.search(w)
    if m:
        return (float(m.group(4)) if m.group(4) else 1) < 0.3 or \
            colorsys.rgb_to_hls(*(float(m.group(i)) / 255 for i in (1, 2, 3)))[1] >= 0.78
    return False


def _decls(blok):
    for d in blok.split(";"):
        if ":" in d:
            p, w = d.split(":", 1)
            yield p.strip().lower(), w.strip()


def _regel(blok):
    """Donkere declaraties voor één regelblok."""
    decls = list(_decls(blok))
    eigen_donker_vlak = any(p in ("background", "background-color") and not _is_licht_vlak(w) for p, w in decls)
    uit = []
    for p, w in decls:
        belangrijk = "!important" in w
        kern = w.replace("!important", "").strip()
        nieuw = None
        if p in ("background", "background-color"):
            if "url(" in kern:
                continue
            n, ok = _vervang(kern, vlak)
            nieuw = n if ok else None
        elif p in ("color", "fill", "-webkit-text-fill-color") and not eigen_donker_vlak:
            if kern.replace(" ", "") == "var(--green-dark)":
                nieuw = GROEN_TEKST
            else:
                n, ok = _vervang(kern, tekst)
                nieuw = n if ok else None
        elif p.startswith("border") and not p.endswith(("radius", "width", "style", "collapse", "spacing")) or p == "outline":
            n, ok = _vervang(kern, rand)
            nieuw = n if ok else None
        if nieuw:
            uit.append(f"{p}:{nieuw}{'!important' if belangrijk else ''}")
    return ";".join(uit)


def _loop(css):
    """Loop door de CSS; geeft donkere CSS terug (met dezelfde @media-omhulling)."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    uit, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        kop = css[i:j].strip()
        # bijbehorende sluitaccolade zoeken
        diepte, k = 1, j + 1
        while k < n and diepte:
            diepte += (css[k] == "{") - (css[k] == "}")
            k += 1
        inhoud = css[j + 1:k - 1]
        if kop.startswith("@media") or kop.startswith("@supports"):
            binnen = _loop(inhoud)
            if binnen:
                uit.append(f"{kop}{{{binnen}}}")
        elif kop.startswith("@"):
            pass                       # @font-face, @keyframes: niets te doen
        elif not kop.startswith(":root"):
            d = _regel(inhoud)
            if d:
                uit.append(f"{kop}{{{d}}}")
        i = k
    return "".join(uit)


def _inline(bronnen):
    """style="…" in de pagina's zelf: overschrijven via een attribuutselector."""
    uit, gezien = [], set()
    for tekst_ in bronnen:
        for stijl in re.findall(r'style="([^"]*)"', tekst_):
            if stijl in gezien or "{" in stijl or "'" in stijl or "\\" in stijl:
                continue
            gezien.add(stijl)
            d = _regel(stijl)          # hele stijl in één keer: zo telt een eigen donker vlak mee
            if d:
                d = ";".join(x.replace("!important", "") + "!important" for x in d.split(";"))
                uit.append("[style='%s']{%s}" % (stijl, d))
    return "".join(uit)


def maak(stylesheets, html_bronnen=()):
    """stylesheets: lijst CSS-teksten (style.css eerst, dan extra's)."""
    # <style>-blokken in sjablonen (bouw/*.py) staan in de body en dus ná donker.css:
    # hun donkere tegenhanger krijgt !important om toch te winnen.
    ingebed = []
    for bron in html_bronnen:
        for blok in re.findall(r"<style[^>]*>(.*?)</style>", bron, flags=re.S):
            d = _loop(blok.replace("{{", "{").replace("}}", "}"))
            ingebed.append(re.sub(r"(?<!important)(;|})", lambda m: "!important" + m.group(1), d.replace("!important", "")))
    delen = [VARS] + [_loop(c) for c in stylesheets] + ingebed + [_inline(html_bronnen), HANDMATIG.strip()]
    return "\n".join(d for d in delen if d)
