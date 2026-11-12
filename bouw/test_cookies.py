"""
Browsertest cookiemelding en Google-meting (onderdeel van `python3 build.py --test`).
Draait de gebouwde site in Chromium alsof het https://ino-elektra.nl is. Google, Cloudflare Turnstile
en de formulier-Worker worden NIET echt aangeroepen: Playwright vangt die verzoeken af en geeft een
nep-antwoord. Zo testen we wat onze eigen code doet (welke verzoeken, cookies, Consent Mode en events),
zonder echte meting of e-mail. Of Google Ads de conversie echt ontvangt, controleer je in Tag Assistant.

Gecontroleerd: eerste bezoek, weigeren, alleen statistieken, alleen advertentiemeting, alles accepteren,
intrekken, verlopen keuze (> 365 dagen), oude 'ja' uit de vorige melding, Engelse melding,
bellen/WhatsApp/offerte-wizard/formulier zonder dubbele conversies.
"""
import json, os, time
from contextlib import contextmanager
from urllib.parse import urlparse

SITE = "https://ino-elektra.nl"
GTAG_STUB = """(function(){var c=(window.dataLayer||[]).filter(function(a){return a[0]==='config'}).map(function(a){return a[1]});
if(c.some(function(i){return i.indexOf('G-')===0}))document.cookie='_ga=GA1.1.1.1; path=/; domain=ino-elektra.nl; max-age=9999999';
if(c.some(function(i){return i.indexOf('AW-')===0}))document.cookie='_gcl_au=1.1.1.1; path=/; domain=ino-elektra.nl; max-age=9999999';})();"""
TURNSTILE_STUB = ("window.turnstile={render:function(){return 1},getResponse:function(){return 'test'},reset:function(){}};"
                  "if(window.inoTurnstileKlaar)window.inoTurnstileKlaar();")
# tel:- en WhatsApp-links niet echt openen; window.open (offerte-wizard) alleen tellen
INIT = """window.__geopend=[];window.open=function(u){window.__geopend.push(String(u));return null};
window.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');
if(a&&/^tel:|wa\\.me/.test(a.getAttribute('href')||''))e.preventDefault();},true);"""
TYPES = {".html": "text/html", ".js": "application/javascript", ".css": "text/css", ".svg": "image/svg+xml",
         ".webp": "image/webp", ".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2",
         ".ico": "image/x-icon", ".xml": "application/xml", ".txt": "text/plain", ".json": "application/json"}


def draai(root):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ["cookietest overgeslagen: playwright niet geïnstalleerd (pip install playwright)"]
    fouten = []

    def check(ok, tekst):
        if not ok:
            fouten.append("cookietest: " + tekst)

    with sync_playwright() as pw:
        open_ctx = []

        @contextmanager
        def scenario(naam):
            # Elk scenario apart: een fout wordt een melding en de andere scenario's lopen door.
            try:
                yield
            except Exception as e:
                fouten.append(f"cookietest {naam}: {str(e).strip().splitlines()[0][:160]}")
            finally:
                for c in open_ctx:
                    try:
                        c.close()
                    except Exception:
                        pass
                open_ctx.clear()

        try:
            browser = pw.chromium.launch()
        except Exception as e:
            return [f"cookietest overgeslagen: geen browser ({e.__class__.__name__})"]

        def nieuw(breedte=1280, hoogte=800):
            ctx = browser.new_context(viewport={"width": breedte, "height": hoogte})
            open_ctx.append(ctx)
            log = []

            def route(r):
                u = urlparse(r.request.url)
                if u.hostname in ("ino-elektra.nl", "www.ino-elektra.nl"):
                    pad = u.path.lstrip("/")
                    if pad == "" or pad.endswith("/"):
                        pad += "index.html"
                    bestand = os.path.join(root, pad)
                    if not os.path.isfile(bestand):
                        return r.fulfill(status=404, body="niet gevonden")
                    with open(bestand, "rb") as f:
                        return r.fulfill(status=200, body=f.read(),
                                         headers={"Content-Type": TYPES.get(os.path.splitext(bestand)[1], "application/octet-stream")})
                log.append(r.request.url)
                if u.hostname == "www.googletagmanager.com":
                    return r.fulfill(status=200, body=GTAG_STUB, headers={"Content-Type": "application/javascript"})
                if u.hostname == "challenges.cloudflare.com":
                    return r.fulfill(status=200, body=TURNSTILE_STUB, headers={"Content-Type": "application/javascript"})
                if u.hostname == "api.ino-elektra.nl":
                    return r.fulfill(status=200, body=json.dumps({"ok": True}),
                                     headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})
                return r.abort()

            ctx.route("**/*", route)
            ctx.add_init_script(INIT)
            page = ctx.new_page()
            js_fouten = []
            page.on("pageerror", lambda e: js_fouten.append(str(e)))
            return ctx, page, log, js_fouten

        def google(log):
            return [u for u in log if "google" in urlparse(u).hostname]

        def consent(page):
            return page.evaluate("(window.dataLayer||[]).filter(a=>a[0]==='consent').map(a=>[a[1],a[2]])")

        def events(page):
            return page.evaluate("(window.dataLayer||[]).filter(a=>a[0]==='event').map(a=>a[1])")

        def configs(page):
            return page.evaluate("(window.dataLayer||[]).filter(a=>a[0]==='config').map(a=>a[1])")

        def cookies(ctx):
            return sorted(c["name"] for c in ctx.cookies(SITE))

        def opslag(page):
            return page.evaluate("localStorage.getItem('ino_cookies')")

        def melding(page):
            page.wait_for_selector(".consent:not([hidden])", timeout=5000)

        def zichtbaar(page):
            return page.evaluate("!!document.querySelector('.consent:not([hidden])')")

        def zet(page, sel, aan):
            # klikken zoals een bezoeker: op de schakelaar (label), niet op het verborgen vinkje
            if page.is_checked(sel) != aan:
                page.locator(sel).locator("xpath=..").click()

        def kies(page, stat, ads):
            melding(page)
            if page.is_visible('.consent [data-consent="voorkeuren"]'):
                page.click('.consent [data-consent="voorkeuren"]')
            zet(page, ".consent [data-consent-stat]", stat)
            zet(page, ".consent [data-consent-ads]", ads)
            page.click('.consent [data-consent="opslaan"]')
            page.wait_for_timeout(300)

        def bel(page, n=1):
            for _ in range(n):
                page.click("a[href^='tel:']:visible >> nth=0")
            page.wait_for_timeout(100)

        try:
            # 1. Eerste bezoek: melding, niets naar Google, Consent Mode standaard 'denied', niets vooraf aan
            with scenario("1. Eerste bezoek"):
                ctx, page, log, js = nieuw()
                page.goto(SITE + "/", wait_until="load")
                melding(page)
                tekst = page.inner_text(".consent")
                check("Google Ads" in tekst and "Google Analytics" in tekst, "melding noemt Google Analytics en Google Ads niet")
                check("Geen advertenties" not in tekst, "melding zegt nog 'Geen advertenties'")
                check(page.is_visible('.consent [data-consent="nee"]') and page.is_visible('.consent [data-consent="ja"]'),
                      "weigeren en accepteren staan niet allebei in de eerste laag")
                page.click('.consent [data-consent="voorkeuren"]')
                check(not page.is_checked(".consent [data-consent-stat]") and not page.is_checked(".consent [data-consent-ads]"),
                      "optionele keuzes staan vooraf aan")
                c = consent(page)
                check(c and c[0][0] == "default" and all(v == "denied" for k, v in c[0][1].items() if k != "wait_for_update"),
                      f"Consent Mode-standaard is niet alles 'denied': {c}")
                bel(page)
                check(not google(log), f"Google-verzoek vóór toestemming: {google(log)}")
                check(not events(page), f"events vóór toestemming: {events(page)}")
                check(not js, f"JavaScript-fout: {js[:1]}")
                ctx.close()

            # 2. Weigeren: niets laden, ook niet na herladen
            with scenario("2. Weigeren"):
                ctx, page, log, js = nieuw(390, 844)
                page.goto(SITE + "/", wait_until="load")
                melding(page)
                page.click('.consent [data-consent="nee"]')
                check(json.loads(opslag(page) or "{}") == {"stat": False, "ads": False}, f"weigeren niet goed opgeslagen: {opslag(page)}")
                page.reload(wait_until="load")
                page.wait_for_timeout(300)
                bel(page)
                check(not zichtbaar(page), "melding komt terug na weigeren")
                check(not google(log) and not events(page), "na weigeren toch Google-verzoek of event")
                ctx.close()

            # 3. Alleen statistieken: GA4 wel, Google Ads niet
            with scenario("3. Alleen statistieken"):
                ctx, page, log, js = nieuw()
                page.goto(SITE + "/", wait_until="load")
                kies(page, True, False)
                upd = [x[1] for x in consent(page) if x[0] == "update"][-1]
                check(upd["analytics_storage"] == "granted" and upd["ad_storage"] == "denied" and upd["ad_user_data"] == "denied"
                      and upd["ad_personalization"] == "denied", f"Consent Mode bij alleen statistieken klopt niet: {upd}")
                check(any("id=G-" in u for u in log) and not any("AW-" in x for x in configs(page)), f"alleen statistieken: verkeerde tags {configs(page)}")
                bel(page)
                ev = events(page)
                check("klik_bellen" in ev and "conversion_event_contact" not in ev, f"alleen statistieken: events {ev}")
                check("_ga" in cookies(ctx) and not any(n.startswith("_gcl") for n in cookies(ctx)), f"alleen statistieken: cookies {cookies(ctx)}")
                ctx.close()

            # 4. Alleen advertentiemeting: Ads wel, GA4 niet; één conversie per actie
            with scenario("4. Alleen advertentiemeting"):
                ctx, page, log, js = nieuw()
                page.goto(SITE + "/", wait_until="load")
                kies(page, False, True)
                upd = [x[1] for x in consent(page) if x[0] == "update"][-1]
                check(upd["ad_storage"] == "granted" and upd["ad_user_data"] == "granted" and upd["ad_personalization"] == "denied"
                      and upd["analytics_storage"] == "denied", f"Consent Mode bij alleen advertentiemeting klopt niet: {upd}")
                check(any("id=AW-" in u for u in log) and not any(x.startswith("G-") for x in configs(page)), f"alleen ads: verkeerde tags {configs(page)}")
                bel(page, 2)  # dubbel tikken
                ev = events(page)
                check(ev.count("conversion_event_contact") == 1 and "klik_bellen" not in ev, f"dubbel tikken op bellen: {ev}")
                page.click("a[href*='wa.me']:visible >> nth=0")
                page.wait_for_timeout(100)
                check(events(page).count("conversion_event_contact") == 2, f"WhatsApp telt niet als conversie: {events(page)}")
                check("_gcl_au" in cookies(ctx) and "_ga" not in cookies(ctx), f"alleen ads: cookies {cookies(ctx)}")
                # offerte-wizard via WhatsApp (twee keer klikken = één conversie) en daarna het formulier versturen
                page.goto(SITE + "/offerte/", wait_until="load")
                check(not zichtbaar(page), "melding komt terug terwijl er een keuze is")
                page.click("#wizardStep1Next")
                page.fill('#quoteForm textarea[name="message"]', "Groepenkast vervangen")
                page.click('[data-step="2"] [data-wizard-next]')
                page.fill('#quoteForm input[name="name"]', "Test")
                page.fill('#quoteForm input[name="phone"]', "0612345678")
                page.fill('#quoteForm input[name="email"]', "test@example.nl")
                page.check('#quoteForm input[name="akkoord"]')
                page.click("#btnSendWhatsApp")
                page.click("#btnSendWhatsApp")
                page.wait_for_timeout(100)
                check(events(page).count("conversion_event_contact") == 1, f"offerte-wizard WhatsApp: {events(page)}")
                check(len(page.evaluate("window.__geopend")) >= 1, "offerte-wizard opent WhatsApp niet")
                page.click("#btnSendEmail")
                page.wait_for_selector(".form-result", timeout=8000)
                check("succesvol" in page.inner_text(".form-result"), f"formulier niet verstuurd: {page.inner_text('.form-result')[:80]}")
                check(events(page).count("conversion_event_contact") == 2, f"formulier verstuurd: {events(page)}")
                check(not js, f"JavaScript-fout: {js[:1]}")
                ctx.close()

            # 5. Alles accepteren, daarna intrekken via Cookie-instellingen
            with scenario("5. Alles accepteren, daarna intrekken via Cookie-instellingen"):
                ctx, page, log, js = nieuw()
                page.goto(SITE + "/", wait_until="load")
                melding(page)
                page.click('.consent [data-consent="ja"]')
                page.wait_for_timeout(300)
                upd = [x[1] for x in consent(page) if x[0] == "update"][-1]
                check(upd["analytics_storage"] == "granted" and upd["ad_storage"] == "granted" and upd["ad_personalization"] == "denied",
                      f"Consent Mode bij alles accepteren klopt niet: {upd}")
                check({"_ga", "_gcl_au"} <= set(cookies(ctx)), f"alles accepteren: cookies {cookies(ctx)}")
                bel(page)
                check(events(page).count("conversion_event_contact") == 1, f"alles accepteren, bellen: {events(page)}")
                page.click("[data-cookie-instellingen]")
                melding(page)
                check(page.is_checked(".consent [data-consent-stat]") and page.is_checked(".consent [data-consent-ads]"),
                      "Cookie-instellingen toont de huidige keuze niet")
                zet(page, ".consent [data-consent-stat]", False)
                zet(page, ".consent [data-consent-ads]", False)
                with page.expect_navigation():
                    page.click('.consent [data-consent="opslaan"]')
                page.wait_for_load_state("load")
                log.clear()
                page.wait_for_timeout(300)
                bel(page)
                check(not google(log) and not events(page), f"na intrekken nog Google-verzoek of event: {google(log)} {events(page)}")
                check(not any(n.startswith(("_ga", "_gcl")) for n in cookies(ctx)), f"na intrekken nog Google-cookies: {cookies(ctx)}")
                ctx.close()

            # 6. Verlopen keuze (> 365 dagen) en oude 'ja' uit de vorige melding: opnieuw vragen, niets laden
            with scenario("6. Verlopen keuze (> 365 dagen) en oude 'ja' uit de vorige melding"):
                for waarde, datum, naam in (('{"stat":true,"ads":true}', int(time.time() * 1000) - 400 * 86400000, "verlopen keuze"),
                                            ("ja", int(time.time() * 1000), "oude 'ja'")):
                    ctx, page, log, js = nieuw()
                    page.goto(SITE + "/privacy/", wait_until="load")
                    page.evaluate("([w,d])=>{localStorage.setItem('ino_cookies',w);localStorage.setItem('ino_cookies_datum',String(d))}", [waarde, datum])
                    log.clear()
                    page.reload(wait_until="load")
                    melding(page)
                    check(not google(log), f"{naam}: Google toch geladen")
                    check(opslag(page) is None, f"{naam}: oude keuze niet opgeruimd")
                    ctx.close()

            # 7. Engelse melding en privacyverklaring
            with scenario("7. Engelse melding en privacyverklaring"):
                ctx, page, log, js = nieuw(390, 844)
                page.goto(SITE + "/en/", wait_until="load")
                melding(page)
                page.click('.consent [data-consent="voorkeuren"]')
                tekst = page.inner_text(".consent")
                for nl in ("Jouw privacy", "Voorkeuren", "Alleen noodzakelijk", "Noodzakelijk", "Statistieken", "Advertentiemeting"):
                    check(nl not in tekst, f"Engelse melding bevat nog '{nl}'")
                check("Ad measurement (Google Ads)" in tekst and page.get_attribute(".consent #consentTekst a", "href") == "/en/privacy/",
                      "Engelse melding mist Google Ads of de link naar /en/privacy/")
                ctx.close()
                for pad in ("privacy", "en/privacy"):
                    with open(os.path.join(root, pad, "index.html"), encoding="utf-8") as f:
                        html = f.read()
                    check(all(n in html for n in ("ino_cookies", "_ga", "_gcl_au")), f"/{pad}/: cookietabel mist ino_cookies, _ga of _gcl_au")
        finally:
            browser.close()
    return fouten
