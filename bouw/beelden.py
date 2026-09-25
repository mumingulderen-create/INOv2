"""
Afbeeldingen: zet originele foto's uit assets/foto/ om naar snelle, responsive versies in /img/.
- WebP (klein, scherp) + JPG-fallback, in meerdere breedtes (mobiel/tablet/desktop)
- OG-afbeelding 1200x630 voor delen op WhatsApp/Facebook/LinkedIn
- Vervangt <img src="/foto.jpg"> in de pagina's automatisch door <picture> met width/height
  (voorkomt verspringen tijdens laden = betere Core Web Vitals / CLS)
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "foto")
OUT = os.path.join(ROOT, "img")
BREEDTES = [480, 800, 1200, 1600]

INFO = {
    "frezen-stopcontacten": {"w": 1200, "h": 800, "breedtes": [480, 800, 1200], "ext": "jpg"},
    "groepenkast-montage": {"w": 1200, "h": 800, "breedtes": [480, 800, 1200], "ext": "jpg"},
    "hero-elektricien": {"w": 1600, "h": 1067, "breedtes": [480, 800, 1200, 1600], "ext": "jpg"},
    "laadpaal-installatie": {"w": 1200, "h": 800, "breedtes": [480, 800, 1200], "ext": "jpg"},
    "perilex-inductie": {"w": 1200, "h": 800, "breedtes": [480, 800, 1200], "ext": "jpg"},
    "storingsdienst-meting": {"w": 1200, "h": 800, "breedtes": [480, 800, 1200], "ext": "jpg"},
    "tuinverlichting-buiten": {"w": 1200, "h": 800, "breedtes": [480, 800, 1200], "ext": "jpg"},
}


def _save(im, path, fmt, **kw):
    if os.path.exists(path):
        return
    im.save(path, fmt, **kw)


# Logo: het origineel (410x170 RGBA, 77 kB) wordt op 130x54 getoond in de header
# en de footer. Dat is op élke pagina boven de vouw. Een 390px brede versie met
# een palet van 128 kleuren is visueel identiek en ~11 kB. Het origineel
# /logo.png blijft staan: dat is de logo-URL in de structured data.
LOGO_BRON = os.path.join(ROOT, "logo.png")
LOGO_UIT = os.path.join(OUT, "logo-390.png")
LOGO_BREEDTE = 390
LOGO_KLEUREN = 128


def verwerk_logo():
    if not os.path.exists(LOGO_BRON):
        return
    if os.path.exists(LOGO_UIT) and os.path.getmtime(LOGO_UIT) >= os.path.getmtime(LOGO_BRON):
        return
    try:
        from PIL import Image
    except ImportError:
        return
    im = Image.open(LOGO_BRON).convert("RGBA")
    h = round(im.height * LOGO_BREEDTE / im.width)
    klein = im.resize((LOGO_BREEDTE, h), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    klein.quantize(colors=LOGO_KLEUREN, method=Image.FASTOCTREE).save(LOGO_UIT, "PNG", optimize=True)


def verwerk():
    os.makedirs(OUT, exist_ok=True)
    try:
        from PIL import Image, ImageOps
    except ImportError:
        # Geen Pillow in deze omgeving; gebruik reeds gegenereerde afbeeldingen in img/
        return INFO

    if not os.path.exists(SRC):
        return INFO

    for fn in sorted(os.listdir(SRC)):
        stem, ext = os.path.splitext(fn)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        src = os.path.join(SRC, fn)
        try:
            im = ImageOps.exif_transpose(Image.open(src))
            has_alpha = im.mode in ("RGBA", "LA", "P")
            rgb = im.convert("RGBA" if has_alpha else "RGB")
            w, h = rgb.size
            widths = [b for b in BREEDTES if b < w] + [min(w, BREEDTES[-1])]
            widths = sorted(set(widths))
            for b in widths:
                r = rgb.resize((b, round(h * b / w)), Image.LANCZOS) if b != w else rgb
                _save(r, os.path.join(OUT, f"{stem}-{b}.webp"), "WEBP", quality=78, method=6)
                if has_alpha:
                    _save(r, os.path.join(OUT, f"{stem}-{b}.png"), "PNG", optimize=True)
                else:
                    _save(r, os.path.join(OUT, f"{stem}-{b}.jpg"), "JPEG", quality=80, optimize=True, progressive=True)
            # OG 1200x630
            if not has_alpha:
                og = ImageOps.fit(rgb, (1200, 630), Image.LANCZOS, centering=(0.5, 0.45))
                _save(og, os.path.join(OUT, f"og-{stem}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
            INFO[stem] = {"w": w, "h": h, "breedtes": widths, "ext": "png" if has_alpha else "jpg"}
        except Exception:
            pass
    # Varianten van foto's die niet meer in assets/foto/ staan opruimen
    bronnen = {os.path.splitext(fn)[0] for fn in os.listdir(SRC)}
    for fn in os.listdir(OUT):
        if fn == os.path.basename(LOGO_UIT):
            continue
        stem = re.sub(r"(-\d+)?\.(webp|jpg|png)$", "", fn[3:] if fn.startswith("og-") else fn)
        if stem not in bronnen:
            os.remove(os.path.join(OUT, fn))
    return INFO


def _picture(stem, attrs, eager):
    i = INFO[stem]
    ws = i["breedtes"]
    largest = ws[-1]
    default_w = 800 if 800 in ws else largest
    h = round(i["h"] * largest / i["w"])
    srcset_webp = ", ".join(f"/img/{stem}-{b}.webp {b}w" for b in ws)
    srcset_fb = ", ".join(f"/img/{stem}-{b}.{i['ext']} {b}w" for b in ws)
    sizes = attrs.pop("sizes", "(max-width: 800px) 100vw, 560px")
    attrs.pop("loading", None); attrs.pop("decoding", None); attrs.pop("fetchpriority", None)
    attrs.pop("width", None); attrs.pop("height", None)
    extra = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    # Geen fetchpriority op de <img> zelf: op mobiel staat deze afbeelding onder de
    # vouw en zou hij bandbreedte afsnoepen van lettertype en CSS. Op desktop regelt
    # de preload in de <head> (met media-query) de hoge prioriteit.
    load = 'loading="eager"' if eager else 'loading="lazy"'
    return (
        f'<picture><source type="image/webp" srcset="{srcset_webp}" sizes="{sizes}">'
        f'<img src="/img/{stem}-{default_w}.{i["ext"]}" srcset="{srcset_fb}" sizes="{sizes}" '
        f'width="{largest}" height="{h}" {load} decoding="async" {extra}></picture>'
    ), (f"/img/{stem}-{default_w}.webp", srcset_webp, sizes)


def vervang_img(html):
    """Vervang lokale <img> door <picture>. Geeft (html, lcp_preload) terug."""
    lcp = None
    first = [True]

    def repl(m):
        nonlocal lcp
        tag = m.group(0)
        src = re.search(r'src="/([^"/]+)\.(jpg|jpeg|png)"', tag)
        if not src or src.group(1) not in INFO:
            return tag
        stem = src.group(1)
        attrs = dict(re.findall(r'([a-zA-Z-]+)="([^"]*)"', tag))
        attrs.pop("src", None)
        eager = attrs.get("loading") == "eager" and first[0]
        if eager:
            first[0] = False
        pic, pre = _picture(stem, attrs, eager)
        if eager:
            lcp = pre
        return pic

    html = re.sub(r"<img\b[^>]*>", repl, html)
    return html, lcp


def og_url(stem_or_file, site):
    stem = os.path.splitext(stem_or_file)[0]
    if stem in INFO and INFO[stem]["ext"] == "jpg":
        return f"{site}/img/og-{stem}.jpg"
    return f"{site}/img/og-hero-elektricien.jpg"

