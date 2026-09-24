"""
Browsertest (optioneel): `python3 build.py --test`
Opent elke pagina op telefoonbreedte (390 px) en op desktop (1280 px) en meldt:
- pagina breder dan het scherm (horizontaal scrollen)
- JavaScript-fouten
- verspringen tijdens laden (CLS > 0,1)
Nodig: pip install playwright && playwright install chromium
Zonder playwright wordt de test overgeslagen (met een melding).
"""
import functools, http.server, socketserver, threading


def draai(root, paden):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ["browsertest overgeslagen: playwright niet geïnstalleerd (pip install playwright)"]

    class Stil(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Stil, directory=root)
    srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
    poort = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    meldingen = []
    try:
        with sync_playwright() as pw:
            try:
                browser = pw.chromium.launch()
            except Exception as e:
                return [f"browsertest overgeslagen: geen browser ({e.__class__.__name__})"]
            for breedte, hoogte, naam in [(390, 844, "mobiel"), (1280, 800, "desktop")]:
                page = browser.new_page(viewport={"width": breedte, "height": hoogte})
                fouten = []
                page.on("pageerror", lambda e: fouten.append(str(e)))
                page.add_init_script("""window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries())
                  if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});""")
                for pad in paden:
                    fouten.clear()
                    page.goto(f"http://127.0.0.1:{poort}{pad}", wait_until="load")
                    page.wait_for_timeout(300)
                    sw, cls = page.evaluate("[document.documentElement.scrollWidth, window.__cls]")
                    if sw > breedte:
                        meldingen.append(f"{naam} {pad}: pagina is {sw}px breed op een scherm van {breedte}px (schuift opzij)")
                    if cls > 0.1:
                        meldingen.append(f"{naam} {pad}: layout verspringt (CLS {cls:.2f}, moet < 0,1)")
                    for f in fouten:
                        meldingen.append(f"{naam} {pad}: JavaScript-fout: {f[:120]}")
                page.close()
            browser.close()
    finally:
        srv.shutdown()
    return meldingen
