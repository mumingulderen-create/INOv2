"""
Sjablonen voor pagina's die uit data worden gemaakt (wijken, storingen) en
voor blokken die in content-bestanden kunnen worden gezet met {{BLOK_NAAM}}.
"""
import json
from html import escape
from config import SITE_URL, BEDRIJF as B, TARIEVEN as T, TARIEF_ZIN, VOORRIJ_ZIN, AANRIJTIJD
from config import TARIEF_ZIN_EN, VOORRIJ_ZIN_EN
from layout import wa_url, ICON_TEL, ICON_WA
import taal
from taal import L, pad


def tv(k):
    """Tarief zoals getoond: in het Engels met een punt (0.40) in plaats van een komma (0,40)."""
    return taal.getal_en(T[k]) if taal.en() else T[k]


def fmt(s):
    """Vul {uur_dag}, {km_tarief} enz. in vanuit TARIEVEN."""
    if "{" not in s:
        return s
    waarden = {k: tv(k) for k in T}
    return s.format(**waarden, **AANRIJTIJD)


def faq_html(faq, titel=None, intro=""):
    titel = titel or L("Veelgestelde vragen", "Frequently asked questions")
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


def cta_band(titel=None, tekst=None, wijk=""):
    titel = titel or L("Direct hulp of een vaste prijs?", "Need help now or a fixed price?")
    tekst = tekst or L("Bel, app een foto van je meterkast of vraag een offerte aan. Je hoort altijd vooraf wat het kost.",
                       "Call, WhatsApp a photo of your meter cupboard or request a quote. You always know the price upfront.")
    q = f"?wijk={wijk}" if wijk else ""
    return f"""<section class="contact-cta" id="contact">
  <div class="container">
    <h2>{titel}</h2>
    <p>{tekst}</p>
    <div class="hero-actions">
      <a class="btn btn-light" href="tel:{B['telefoon_e164']}" data-track="bellen">{L("Bel", "Call")} {B['telefoon_tonen']}</a>
      <a class="btn btn-outline-light" href="{wa_url(L('Hallo INO, ik heb een vraag.', 'Hello INO, I have a question.'))}" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp</a>
      <a class="btn btn-outline-light" href="{pad('/offerte/')}{q}">{L("Offerte aanvragen", "Request a quote")}</a>
    </div>
  </div>
</section>"""


def blok_stedin_checker(toon_kop=True):
    # Als toon_kop=True: geen grote koptekst erboven zodat de kaarten direct hoog staan!
    kop_html = f"""<div class="hp"><h2>{L("Stedin of INO bellen bij stroomuitval", "Power cut: call Stedin or INO?")}</h2></div>"""
    voet_uitleg = f"""<p style="text-align:center;margin:18px auto 0;max-width:640px;font-size:14px;color:#556457">{L("Twijfel je wie je moet inschakelen bij stroomuitval? Bekijk hierboven direct het verschil tussen een netstoring en een storing in jouw eigen installatie.", "Not sure who to call during a power cut? Compare the difference above between a grid outage and a fault in your own installation.")}</p>""" if toon_kop else """"""
    return f"""<section class="section soft" id="stedin-check">
  <div class="container">
    {kop_html}

    <!-- 2 Kolommen Naast Elkaar: Stedin vs INO -->
    <div class="stedin-compare-grid">
      <!-- Kolom 1: Stedin -->
      <div class="stedin-col-card stedin-col-net">
        <div class="stedin-col-header">
          <span class="stedin-col-badge badge-stedin">🏛️ {L("Netbeheerder Stedin", "Grid operator Stedin")}</span>
          <h3>{L("Wanneer bel je Stedin?", "When do you call Stedin?")}</h3>
          <p class="stedin-col-sub">{L("Bij storingen in het energienetwerk van de wijk of aan de verzegelde hoofdaansluiting.", "For faults in the neighbourhood power grid or at the sealed main connection.")}</p>
        </div>
        
        <div class="stedin-col-body">
          <h4 class="stedin-list-title">{L("Herkenbare kenmerken:", "Typical signs:")}</h4>
          <ul class="stedin-check-list">
            <li><span>✕</span> {L("<strong>Hele straat of buren</strong> hebben ook geen stroom", "<strong>The whole street or your neighbours</strong> have no power either")}</li>
            <li><span>✕</span> {L("<strong>Straatverlichting buiten</strong> is uit of knippert", "<strong>Street lights outside</strong> are off or flickering")}</li>
            <li><span>✕</span> {L("<strong>Display van kWh-meter</strong> is compleet zwart/uit", "<strong>The electricity meter display</strong> is completely blank")}</li>
            <li><span>✕</span> {L("<strong>Verzegelde hoofdzekering</strong> onder de meter is uitgevallen", "<strong>The sealed main fuse</strong> below the meter has blown")}</li>
          </ul>
        </div>

        <div class="stedin-col-footer">
          <div class="stedin-action-box">
            <span class="stedin-action-label">{L("Actie: Neem contact op met netbeheerder", "Action: contact the grid operator")}</span>
            <a class="btn btn-secondary full" href="tel:08009009">📞 {L("Bel Stedin", "Call Stedin")}: 0800 9009</a>
            <a class="stedin-official-link" href="https://www.stedin.net/storing-en-onderhoud" target="_blank" rel="noopener">{L("Officiële storingsprocedure op Stedin.net", "Official outage procedure on Stedin.net (Dutch)")} ↗</a>
          </div>
        </div>
      </div>

      <!-- Kolom 2: INO -->
      <div class="stedin-col-card stedin-col-ino">
        <div class="stedin-col-header">
          <span class="stedin-col-badge badge-ino">⚡ {L("INO Elektrotechniek (24/7 Spoed)", "INO electricians (24/7 emergency)")}</span>
          <h3>{L("Wanneer bel je INO?", "When do you call INO?")}</h3>
          <p class="stedin-col-sub" style="font-weight:600;color:var(--ink);line-height:1.45">
            {L("Vast all-in tarief", "Fixed all-in rate")}: <strong>€ {T['uur_dag']}</strong> ({L("08–18u", "08:00–18:00")}) · <strong>€ {T['uur_avond']}</strong> ({L("18–22u", "18:00–22:00")}) · <strong>€ {T['uur_nacht']}</strong> ({L("nacht &amp; weekend", "night &amp; weekend")})
          </p>
        </div>

        <div class="stedin-col-body">
          <h4 class="stedin-list-title">{L("Herkenbare kenmerken:", "Typical signs:")}</h4>
          <ul class="stedin-check-list list-ino">
            <li><span>✓</span> {L("<strong>Alleen bij jou thuis</strong> is het donker (buren hebben licht)", "<strong>Only your home</strong> is dark (the neighbours have power)")}</li>
            <li><span>✓</span> {L("<strong>Aardlekschakelaar (knop 'T')</strong> klapt steeds omlaag", "<strong>The RCD (the switch with the 'T' button)</strong> keeps tripping")}</li>
            <li><span>✓</span> {L("<strong>Groepenschakelaar</strong> springt direct terug bij aanzetten", "<strong>A circuit breaker</strong> trips again as soon as you switch it on")}</li>
            <li><span>✓</span> {L("<strong>Knetterend geluid of brandlucht</strong> bij een stopcontact of kast", "<strong>Crackling or a burning smell</strong> at a socket or the fuse box")}</li>
          </ul>
        </div>

        <div class="stedin-col-footer">
          <div class="stedin-action-box">
            <span class="stedin-action-label">{L("Actie: Direct storingsdienst inschakelen", "Action: call our emergency service")}</span>
            <a class="btn btn-primary full" href="tel:{B['telefoon_e164']}" data-track="bellen">📞 {L("Bel direct INO", "Call INO now")}: {B['telefoon_tonen']}</a>
            <span class="stedin-fast-note">⚡ {L("Bij spoed in Utrecht binnen", "Emergency in Utrecht: within")} {AANRIJTIJD["aanrijtijd_utrecht"]} min, {L("regio", "region")} {AANRIJTIJD["aanrijtijd_regio"]} min</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Brede Hulpbalk: Twijfel / WhatsApp Meekijkservice -->
    <div class="stedin-helper-banner">
      <div class="stedin-helper-icon">📸</div>
      <div class="stedin-helper-text">
        <h4>{L("Twijfel je wat je ziet in je meterkast?", "Not sure what you are looking at in your meter cupboard?")}</h4>
        <p>{L("Je hoeft geen verstand te hebben van groepenkasten. Maak met je mobiel een foto van je meterkast en stuur deze via WhatsApp. Wij kijken gratis mee en vertellen je wie je moet bellen.", "You do not need to know anything about fuse boxes. Take a photo of your meter cupboard with your phone and send it via WhatsApp. We take a look for free and tell you who to call.")}</p>
      </div>
      <div class="stedin-helper-action">
        <a class="btn btn-whatsapp" href="{wa_url(L('Hallo INO, ik heb een storing en stuur hierbij een foto van mijn meterkast. Kunnen jullie even gratis meekijken?', 'Hello INO, I have a power fault. Here is a photo of my meter cupboard. Could you take a quick look?'))}" target="_blank" rel="noopener" data-track="whatsapp">💬 {L("Stuur foto via WhatsApp", "Send a photo via WhatsApp")}</a>
      </div>
    </div>

  </div>
{voet_uitleg}
</section>"""


def tarief_kaarten(voorrij=True):
    zin = L(f'{VOORRIJ_ZIN} Een schouw op locatie kost € {T["schouw"]} en verrekenen we volledig als je de klus laat uitvoeren.',
            f'{VOORRIJ_ZIN_EN} A site visit costs € {T["schouw"]}, which we deduct in full if you go ahead with the job.')
    extra = f'<p class="price-note form-note">{zin}</p>' if voorrij else ""
    eerste = L("1e uur", "1st hour")
    return f"""<div class="price-grid">
  <div class="price-card"><h3>{L("Overdag", "Daytime")}</h3><div class="price-amount">€ {T['uur_dag']}<span> {eerste}</span></div><p>{L("Ma–vr 08:00–18:00. Daarna", "Mon–Fri 08:00–18:00. Then")} € {tv('kwartier_dag')} {L("per kwartier", "per quarter hour")}.</p></div>
  <div class="price-card"><h3>{L("Avond", "Evening")}</h3><div class="price-amount">€ {T['uur_avond']}<span> {eerste}</span></div><p>{L("Ma–vr 18:00–22:00. Daarna", "Mon–Fri 18:00–22:00. Then")} € {tv('kwartier_avond')} {L("per kwartier", "per quarter hour")}.</p></div>
  <div class="price-card highlight"><h3>{L("Nacht &amp; weekend", "Night &amp; weekend")}</h3><div class="price-amount">€ {T['uur_nacht']}<span> {eerste}</span></div><p>{L("22:00–08:00, complete zaterdagen, zondagen en feestdagen. Daarna", "22:00–08:00, all day Saturday, Sunday and public holidays. Then")} € {tv('kwartier_nacht')} {L("per kwartier", "per quarter hour")}.</p></div>
</div>
<p class="form-note">{L("Alle bedragen inclusief 21% btw en foutdiagnose. Meer werk of een onderdeel nodig? Dan hoor je eerst de prijs en beslis jij.", "All prices include 21% VAT and fault diagnosis. More work or a part needed? You hear the price first and you decide.")}</p>{extra}"""


def groepenkast_calculator():
    # Alle calculatorprijzen komen uit config.py (TARIEVEN)
    drie_fase_meer = T["calc_meer_3f"]
    start = T["calc_basis_1f"] + drie_fase_meer + T["optie_kookgroep"]
    prijzen = json.dumps({"basis": T["calc_basis_1f"], "driefase": drie_fase_meer, "kookgroep": T["optie_kookgroep"],
                          "kracht": T["optie_kracht_4p"], "pv": T["optie_pv"], "groep": T["optie_automaat"]})
    wa_default = wa_url(L(f"Hallo INO, via jullie online calculator kom ik uit op een 3-fase groepenkast met 8 groepen (indicatie € {T['groepenkast_3f']}). Hierbij stuur ik een foto van mijn huidige meterkast mee voor een vaste offerte.",
                          f"Hello INO, your online calculator suggests a three-phase fuse box with 8 circuits (estimate € {T['groepenkast_3f']}). I am sending a photo of my current meter cupboard for a fixed quote."))
    return f"""<section class="section soft calc-section" id="keuzehulp" data-prijzen='{prijzen}'>
  <style>
    .calc-section {{ padding: 60px 0; }}
    .calc-card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 18px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.04); }}
    .calc-grid {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 36px; align-items: start; }}
    .calc-step-header {{ display: flex; align-items: center; gap: 14px; margin-bottom: 20px; }}
    .calc-step-num {{ width: 32px; height: 32px; background: #1ed760; color: #0d1f0f; font-weight: 800; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; }}
    .calc-step-header h3 {{ margin: 0; font-size: 18px; font-weight: 700; color: #111827; }}
    .calc-step-header p {{ margin: 2px 0 0; font-size: 13px; color: #64748b; }}
    .calc-sub-label {{ font-size: 13px; font-weight: 700; color: #334155; margin-bottom: 8px; }}
    .calc-device-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    .calc-item {{ display: block; position: relative; cursor: pointer; margin: 0; user-select: none; }}
    .calc-item input[type="checkbox"] {{ position: absolute; opacity: 0; width: 1px; height: 1px; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); }}
    .calc-box {{ display: flex; align-items: center; justify-content: space-between; padding: 14px 16px; background: #fafbfa; border: 1.5px solid #e2e8f0; border-radius: 12px; transition: border-color 0.15s ease, background 0.15s ease; min-height: 72px; gap: 12px; }}
    .calc-item:hover .calc-box {{ border-color: #1ed760; background: #ffffff; }}
    .calc-item input:checked + .calc-box {{ border-color: #1ed760; background: #f2fbf4; }}
    .calc-item-text {{ display: flex; flex-direction: column; gap: 3px; min-width: 0; flex: 1; }}
    .calc-item-text strong {{ font-size: 14px; font-weight: 700; color: #0f172a; line-height: 1.3; }}
    .calc-item-text span {{ font-size: 12px; color: #64748b; line-height: 1.25; }}
    .calc-check {{ width: 22px; height: 22px; border-radius: 6px; border: 1.5px solid #cbd5e1; background: #ffffff; flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: all 0.15s ease; }}
    .calc-item input:checked + .calc-box .calc-check {{ background: #1ed760; border-color: #1ed760; }}
    .calc-item input:checked + .calc-box .calc-check::after {{ content: ""; display: block; width: 5px; height: 10px; border: solid #0d1f0f; border-width: 0 2.5px 2.5px 0; transform: rotate(45deg); margin-bottom: 2px; }}
    
    .calc-radio-group {{ display: grid; grid-template-columns: 1fr; gap: 10px; }}
    .calc-radio-item {{ display: block; position: relative; cursor: pointer; margin: 0; }}
    .calc-radio-item input[type="radio"] {{ position: absolute; opacity: 0; width: 0; height: 0; }}
    .calc-radio-box {{ display: flex; align-items: center; gap: 14px; padding: 12px 16px; background: #fafbfa; border: 1.5px solid #e2e8f0; border-radius: 12px; transition: all 0.15s ease; }}
    .calc-radio-item:hover .calc-radio-box {{ border-color: #1ed760; background: #ffffff; }}
    .calc-radio-item input:checked + .calc-radio-box {{ border-color: #1ed760; background: #f2fbf4; }}
    .calc-radio-circle {{ width: 20px; height: 20px; border-radius: 50%; border: 1.5px solid #cbd5e1; background: #fff; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }}
    .calc-radio-item input:checked + .calc-radio-box .calc-radio-circle {{ border-color: #1ed760; }}
    .calc-radio-item input:checked + .calc-radio-box .calc-radio-circle::after {{ content: ""; width: 10px; height: 10px; border-radius: 50%; background: #1ed760; }}
    .calc-radio-text strong {{ display: block; font-size: 14px; color: #0f172a; }}
    .calc-radio-text span {{ display: block; font-size: 12px; color: #64748b; }}

    .calc-summary-card {{ background: linear-gradient(145deg, #112314 0%, #0a160c 100%); color: #ffffff; border-radius: 16px; padding: 28px 24px; box-shadow: 0 14px 36px rgba(10,22,12,0.18); position: sticky; top: 90px; }}
    .calc-badge {{ display: inline-block; background: rgba(30,215,96,0.16); color: #1ed760; font-size: 11px; font-weight: 800; letter-spacing: 0.8px; padding: 4px 10px; border-radius: 999px; margin-bottom: 16px; text-transform: uppercase; }}
    .calc-kpi-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom: 16px; }}
    .calc-kpi-label {{ display: block; font-size: 12px; color: rgba(255,255,255,0.65); margin-bottom: 4px; }}
    .calc-kpi strong {{ display: block; font-size: 17px; font-weight: 800; color: #ffffff; }}
    .calc-explanation {{ margin-bottom: 18px; }}
    .calc-explain-title {{ font-size: 15px; font-weight: 700; color: #1ed760; margin-bottom: 6px; }}
    .calc-explanation p {{ font-size: 13px; color: rgba(255,255,255,0.8); line-height: 1.45; margin: 0; }}
    
    .calc-breakdown {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 14px 16px; margin-bottom: 16px; }}
    .calc-breakdown-title {{ font-size: 11px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; color: rgba(255,255,255,0.7); margin-bottom: 8px; }}
    .calc-breakdown-list {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }}
    .calc-breakdown-item {{ display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: rgba(255,255,255,0.85); }}
    .calc-breakdown-item span:last-child {{ font-weight: 700; color: #1ed760; }}

    .calc-stedin-notice {{ background: rgba(30,215,96,0.08); border: 1px solid rgba(30,215,96,0.25); border-radius: 12px; padding: 14px; margin-bottom: 18px; }}
    .calc-stedin-title strong {{ display: block; font-size: 13px; font-weight: 800; color: #1ed760; margin-bottom: 4px; }}
    .calc-stedin-notice p {{ font-size: 12px; color: rgba(255,255,255,0.8); line-height: 1.4; margin: 0 0 8px; }}
    .calc-stedin-role {{ background: rgba(0,0,0,0.25); border-radius: 8px; padding: 10px; font-size: 11px; color: rgba(255,255,255,0.85); line-height: 1.4; }}
    .calc-stedin-role strong {{ color: #ffffff; display: block; margin-bottom: 2px; }}

    .calc-price-box {{ background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 16px; margin-bottom: 18px; text-align: center; }}
    .calc-price-label {{ display: block; font-size: 11px; letter-spacing: 0.5px; text-transform: uppercase; color: rgba(255,255,255,0.65); margin-bottom: 4px; }}
    .calc-price-val {{ font-size: 32px; font-weight: 900; color: #ffffff; line-height: 1; }}
    .calc-price-val span {{ font-size: 14px; font-weight: 400; color: #1ed760; margin-left: 4px; }}
    .calc-price-sub {{ display: block; font-size: 11px; color: rgba(255,255,255,0.6); margin-top: 6px; line-height: 1.35; }}
    .calc-actions {{ display: grid; gap: 10px; margin-bottom: 14px; }}
    .calc-guarantee-note {{ display: grid; gap: 4px; font-size: 11px; color: rgba(255,255,255,0.65); border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px; }}

    @media (max-width: 960px) {{
      .calc-grid {{ grid-template-columns: 1fr; }}
      .calc-summary-card {{ position: static; margin-top: 24px; }}
    }}
    @media (max-width: 640px) {{
      .calc-device-grid {{ grid-template-columns: 1fr; }}
      .calc-card {{ padding: 20px; }}
    }}
  </style>

  <div class="container">
    <div class="section-heading text-center">
      <span class="badge">{L("GROEPENKAST ADVIES", "FUSE BOX ADVICE")}</span>
      <h2>{L("Groepenkast &amp; Inductie Berekenen", "Fuse box &amp; induction calculator")}</h2>
      <p>{L("Selecteer je apparaten voor een direct technisch advies (1-fase of 3-fase) en all-in prijsindicatie.", "Select your appliances for instant technical advice (single-phase or three-phase) and an all-in price estimate.")}</p>
    </div>

    <div class="calc-card">
      <div class="calc-grid">
        <div class="calc-inputs">
          <div class="calc-step-header">
            <span class="calc-step-num">1</span>
            <div>
              <h3>{L("Welke apparaten wil je aansluiten?", "Which appliances do you want to connect?")}</h3>
              <p>{L("Selecteer de apparaten die in de woning draaien of bijkomen.", "Select the appliances you have now or are adding.")}</p>
            </div>
          </div>

          <div class="calc-device-grid">
            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="inductie" data-groepen="1" checked>
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>{L("Inductiekookplaat", "Induction hob")}</strong>
                  <span>{L("2x230V kookgroep of 3-fase", "2x230V cooking circuit or three-phase")}</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="laadpaal" data-groepen="1">
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>{L("Laadpaal (Wallbox)", "EV charger (wallbox)")}</strong>
                  <span>{L("Krachtstroom 3-fase / 11 kW", "Three-phase power / 11 kW")}</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="zonnepanelen" data-groepen="1">
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>{L("Zonnepanelen (PV)", "Solar panels (PV)")}</strong>
                  <span>{L("Aparte PV-aardlekautomaat", "Separate PV RCBO")}</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="warmtepomp" data-groepen="1">
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>{L("Warmtepomp of Airco", "Heat pump or air conditioning")}</strong>
                  <span>{L("Zware groep / 3-fase kracht", "Heavy-duty circuit / three-phase")}</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="quooker" data-groepen="1">
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>{L("Quooker / Keukenboiler", "Quooker / kitchen water heater")}</strong>
                  <span>{L("Aparte 230V groep (2200W)", "Separate 230V circuit (2200W)")}</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="wasmachine" data-groepen="2" checked>
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>{L("Wasmachine &amp; Droger", "Washing machine &amp; dryer")}</strong>
                  <span>{L("Twee aparte zware groepen", "Two separate heavy-duty circuits")}</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="keuken" data-groepen="2" checked>
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>{L("Oven &amp; Vaatwasser", "Oven &amp; dishwasher")}</strong>
                  <span>{L("Twee aparte keukengroepen", "Two separate kitchen circuits")}</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="basis" data-groepen="3" checked>
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>{L("Woonkamer, slaapkamers &amp; licht", "Living room, bedrooms &amp; lighting")}</strong>
                  <span>{L("Drie basis licht-/wandgroepen", "Three basic lighting/socket circuits")}</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>
          </div>

          <div class="calc-step-header" style="margin-top:28px">
            <span class="calc-step-num">2</span>
            <div>
              <h3>{L("Wat voor meterkast en aansluiting heb je nu?", "What meter cupboard and connection do you have now?")}</h3>
              <p>{L("Kies je huidige situatie voor een passend advies en plan van aanpak.", "Choose your current situation for tailored advice and a plan.")}</p>
            </div>
          </div>

          <div class="calc-sub-label">{L("Huidige netaansluiting (hoofdschakelaar/meter):", "Current grid connection (main switch/meter):")}</div>
          <div class="calc-radio-group" style="margin-bottom:18px">
            <label class="calc-radio-item">
              <input type="radio" name="calc_aansluiting" value="1fase" checked>
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>{L("1-fase aansluiting (230V)", "Single-phase connection (230V)")}</strong>
                  <span>{L("Standaard aansluiting (1x25A of 1x35A op de meter)", "Standard connection (1x25A or 1x35A on the meter)")}</span>
                </div>
              </div>
            </label>

            <label class="calc-radio-item">
              <input type="radio" name="calc_aansluiting" value="3fase">
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>{L("3-fase aansluiting (400V)", "Three-phase connection (400V)")}</strong>
                  <span>{L("Krachtstroom al aanwezig (3x25A op de meter)", "Three-phase already present (3x25A on the meter)")}</span>
                </div>
              </div>
            </label>

            <label class="calc-radio-item">
              <input type="radio" name="calc_aansluiting" value="onbekend">
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>{L("Weet ik niet zeker", "Not sure")}</strong>
                  <span>{L("Ik stuur een foto mee van de hoofdmeter", "I will send a photo of the main meter")}</span>
                </div>
              </div>
            </label>
          </div>

          <div class="calc-sub-label">{L("Type groepenkast:", "Type of fuse box:")}</div>
          <div class="calc-radio-group">
            <label class="calc-radio-item">
              <input type="radio" name="calc_huidig" value="stoppen" checked>
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>{L("Oude stoppenkast", "Old fuse box with screw-in fuses")}</strong>
                  <span>{L("Draaizekeringen met smeltpatronen (volledige vervanging)", "Screw-in fuse cartridges (full replacement)")}</span>
                </div>
              </div>
            </label>

            <label class="calc-radio-item">
              <input type="radio" name="calc_huidig" value="automaat">
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>{L("Bestaande automatenkast", "Existing circuit breaker board")}</strong>
                  <span>{L("Schakelaars met hendeltjes (vervangen of uitbreiden)", "Switches with small levers (replace or extend)")}</span>
                </div>
              </div>
            </label>
          </div>
        </div>

        <div class="calc-summary">
          <div class="calc-summary-card">
            <div class="calc-badge">{L("BEREKEND ADVIES", "CALCULATED ADVICE")}</div>
            
            <div class="calc-kpi-row">
              <div class="calc-kpi">
                <span class="calc-kpi-label">{L("Benodigde groepen", "Circuits needed")}</span>
                <strong id="calcGroepen">{L("8 groepen", "8 circuits")}</strong>
              </div>
              <div class="calc-kpi">
                <span class="calc-kpi-label">{L("Geadviseerde fase", "Recommended phase")}</span>
                <strong id="calcFase">{L("3-fase (400V)", "Three-phase (400V)")}</strong>
              </div>
            </div>

            <div class="calc-explanation">
              <div class="calc-explain-title" id="calcTitel">{L("Aanbevolen: 3-fase Hager of ABB Groepenkast", "Recommended: three-phase Hager or ABB fuse box")}</div>
              <p id="calcUitleg">{L("Door de combinatie van apparaten adviseren we een 3-fase groepenkast voor een optimale belastingverdeling conform NEN 1010.", "Based on this combination of appliances we recommend a three-phase fuse box for the best load distribution in line with NEN 1010.")}</p>
            </div>

            <div class="calc-stedin-notice" id="calcStedinBox">
              <div class="calc-stedin-title">
                <strong>{L("Verzwaring via Stedin naar 3-fase", "Upgrade to three-phase via Stedin")}</strong>
              </div>
              <p>{L("Je woning heeft nu 1-fase, maar je apparaten vragen om 3-fase (kracht). Vraag de netaansluiting-verzwaring aan bij Stedin via mijnaansluiting.nl.", "Your home has a single-phase connection now, but your appliances need three-phase power. Request the connection upgrade from Stedin via mijnaansluiting.nl.")}</p>
              <div class="calc-stedin-role">
                <strong>{L("Hoe INO Techniek dit oplost:", "How INO Techniek handles this:")}</strong>
                {L("Wij monteren en bedraden je nieuwe groepenkast alvast 100% 3-fase voorbereid (met 4-polige hoofdschakelaar). Zodra de Stedin-monteur langskomt, kan deze de fasen direct aansluiten zonder extra ombouwwerk!", "We install and wire your new fuse box fully prepared for three-phase (with a 4-pole main switch). When the Stedin engineer arrives, they can connect the phases straight away without extra rework.")}
              </div>
            </div>

            <div class="calc-breakdown">
              <div class="calc-breakdown-title">{L("Transparante Prijsopbouw", "Transparent price breakdown")}</div>
              <ul class="calc-breakdown-list" id="calcBreakdown">
                <li class="calc-breakdown-item"><span>{L("1-fase basiskast (tot 8 gr.)", "Single-phase base unit (up to 8 circuits)")}</span><span>€ {T['calc_basis_1f']},-</span></li>
                <li class="calc-breakdown-item"><span>{L("3-fase uitvoering &amp; kamrail voorbereiding", "Three-phase version &amp; busbar preparation")}</span><span>+ € {drie_fase_meer},-</span></li>
                <li class="calc-breakdown-item"><span>{L("Inductie kookgroep (incl. kamrail &amp; aansluiting)", "Induction cooking circuit (incl. busbar &amp; connection)")}</span><span>+ € {T['optie_kookgroep']},-</span></li>
              </ul>
            </div>

            <div class="calc-price-box">
              <span class="calc-price-label">{L("Indicatieve all-in investering", "Indicative all-in price")}</span>
              <div class="calc-price-val" id="calcPrijs">€ {start},- <span>all-in</span></div>
              <span class="calc-price-sub">{L("Inclusief A-merk kast, kamrails, klein montagemateriaal, montage, 21% btw en 12 mnd garantie", "Including a premium-brand unit, busbars, small installation materials, labour, 21% VAT and a 12-month guarantee")}</span>
            </div>

            <div class="calc-actions">
              <a href="{pad('/offerte/')}" id="calcOfferteBtn" class="btn btn-primary full">{L("Offerte aanvragen met deze berekening", "Request a quote with this calculation")}</a>
              <a href="{wa_default}" id="calcWaBtn" target="_blank" rel="noopener" class="btn btn-whatsapp full">
                {ICON_WA} {L("WhatsApp deze berekening + foto", "WhatsApp this calculation + photo")}
              </a>
            </div>

            <div class="calc-guarantee-note">
              <span>{L("Bindende vaste all-in prijs vooraf", "Binding fixed all-in price upfront")}</span>
              <span>{L("Geen voorrijkosten binnen de gemeente Utrecht", "No call-out charge within the municipality of Utrecht")}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""


# Trefwoorden in de klustitel (NL en EN) -> dienstpagina
KLUS_LINKS = [
    (("groepenkast", "kast", "fuse box", "consumer unit"), "/groepenkast/"),
    (("perilex", "kookgroep", "inductie", "koken", "cooking", "induction", "cooker"), "/perilex/"),
    (("laadpaal", "ev charger", "charging"), "/laadpaal-installeren/"),
    (("krachtstroom", "400v", "three-phase"), "/krachtstroom-aanleggen/"),
    (("stopcontact", "frezen", "verbouwing", "keuken", "socket", "renovation", "kitchen", "chasing"), "/frezen-stopcontacten-verleggen/"),
    (("tuin", "buiten", "schuur", "garden", "outdoor", "shed"), "/tuinverlichting-buitenelektra/"),
    (("aardlek", "rcd"), "/aardlekschakelaar-springt-eruit/"),
    (("groep valt", "uitval", "circuit trips", "tripping"), "/kortsluiting-utrecht/"),
    (("storing", "doormeten", "bedrading", "fault", "outage", "wiring", "testing"), "/stroomstoring-utrecht/"),
]


def klus_link(titel):
    t = titel.lower()
    for keys, href in KLUS_LINKS:
        if any(k in t for k in keys):
            return pad(href)
    return pad("/diensten/")


# --------------------------------------------------------------------------- wijkpagina
def wijk_pagina(w, alle):
    naam = w["naam"]
    in_utrecht = w["type"] == "wijk"
    voorrij = L("Geen voorrijkosten", "No call-out charge") if in_utrecht else L(f"€ {tv('km_tarief')}/km voorrijden", f"€ {tv('km_tarief')}/km travel")
    locatie = f"{naam}, Utrecht" if in_utrecht else naam
    buurten = "".join(f"<span>{escape(b)}</span>" for b in w["buurten"])
    klussen = "".join(
        f'<article class="service-card"><h3>{escape(k)}</h3><p>{escape(fmt(u))}</p>'
        f'<a href="{klus_link(k + " " + u)}">{L("Meer over deze klus", "More about this job")}</a></article>' for k, u in w["klussen"])
    aanrij = (f'<span>{L("Bij spoed", "Emergency")}: {fmt(w["aanrijtijd"])}</span>' if w["aanrijtijd"]
              else f'<span>{L("Bij spoed: bel voor de actuele aanrijtijd", "Emergency: call for the current response time")}</span>')
    # Alleen buren (lijst staat ruwweg geografisch): minder gedeelde tekst per pagina, de footer/hub linkt de rest
    i = next(n for n, x in enumerate(alle) if x["slug"] == w["slug"])
    andere = [x for x in (alle[max(0, i - 3):i] + alle[i + 1:i + 4]) if x["slug"] != w["slug"]]
    # Echte praktijkvoorbeelden (door eigenaar in te vullen in wijken.py: "praktijk": [["titel", "tekst"], ...])
    praktijk = w.get("praktijk") or []
    praktijk_html = (f'''<section class="section">
  <div class="container">
    <h2>{L("Recent in", "Recently in")} {escape(naam)}</h2>
    <div class="service-grid">{"".join(f'<article class="service-card"><h3>{escape(fmt(t))}</h3><p>{escape(fmt(x))}</p></article>' for t, x in praktijk)}</div>
  </div>
</section>

''') if praktijk else ""
    andere_links = "".join(f'<a href="{pad("/elektricien-" + x["slug"] + "/")}">{L("Elektricien", "Electrician")} {x["naam"]}</a>' for x in andere)
    if in_utrecht:
        tarief_voorrij = L(f"Binnen de gemeente Utrecht, en dus ook in {naam}, rekenen we geen voorrijkosten.",
                           f"Within the municipality of Utrecht, including {naam}, there is no call-out charge.")
    else:
        tarief_voorrij = L(f"{naam} ligt buiten de gemeente Utrecht. Voorrijden kost € {T['km_tarief']} per km; dat bedrag hoor je altijd vooraf.",
                           f"{naam} is outside the municipality of Utrecht. Travel costs € {tv('km_tarief')} per km; you always hear the amount upfront.")
    wa = wa_url(L(f"Hallo INO, ik woon in {naam} en heb een vraag. Hierbij een foto.", f"Hello INO, I live in {naam} and have a question. Here is a photo."))
    body = f"""<section class="lp-hero">
  <div class="container">
    <div class="badge">{L("Elektricien", "Electrician")} {escape(locatie)}</div>
    <h1>{L(f"Elektricien in {escape(naam)} nodig?", f"Need an electrician in {escape(naam)}?")}</h1>
    <p>{escape(fmt(w['intro']))}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="tel:{B['telefoon_e164']}" data-track="bellen">{ICON_TEL} {L("Bel", "Call")} {B['telefoon_tonen']}</a>
      <a class="btn btn-whatsapp" href="{wa}" target="_blank" rel="noopener" data-track="whatsapp">{ICON_WA} {L("WhatsApp een foto", "WhatsApp a photo")}</a>
      <a class="btn btn-secondary" href="{pad('/offerte/')}?wijk={w['slug']}">{L("Offerte aanvragen", "Request a quote")}</a>
    </div>
    <div class="meta-row"><span>{L("24/7 bij storingen", "24/7 for power faults")}</span>{aanrij}<span>{voorrij}</span><span>{T['garantie_maanden']} {L("mnd garantie", "month guarantee")}</span>{L("", "<span>English spoken</span>")}</div>
  </div>
</section>

<section class="section">
  <div class="container area-layout">
    <div>
      <h2>{L(f"Woningen in {escape(naam)} en wat dat betekent voor je elektra", f"Homes in {escape(naam)} and what that means for your electrics")}</h2>
      <p>{escape(fmt(w['woningen']))}</p>
      <p>{escape(fmt(w['lokaal']))}</p>
      <div class="area-chips" aria-label="{L("Buurten in", "Areas in")} {escape(naam)}">{buurten}</div>
    </div>
    <aside class="area-card">
      <h3>{L(f"Wat kost een elektricien in {escape(naam)}?", f"What does an electrician cost in {escape(naam)}?")}</h3>
      <ul class="include-items compact">
        <li>{L("Overdag (08:00–18:00)", "Daytime (08:00–18:00)")}: € {T['uur_dag']} ({L("1e uur, incl. btw", "1st hour, incl. VAT")})</li>
        <li>{L("Avond (ma–vr 18:00–22:00)", "Evening (Mon–Fri 18:00–22:00)")}: € {T['uur_avond']}</li>
        <li>{L("Nacht (22:00–08:00), za, zo en feestdagen", "Night (22:00–08:00), Sat, Sun and public holidays")}: € {T['uur_nacht']}</li>
        <li>{L("Groepenkast 1-fase: vanaf", "Single-phase fuse box: from")} € {T['groepenkast_1f']} all-in</li>
        <li>{L("Perilex aansluiten", "Perilex connection")}: € {T['perilex_aansluiten']}</li>
      </ul>
      <p class="form-note">{escape(tarief_voorrij)}</p>
      <a class="mini-link" href="{pad('/tarieven/')}">{L("Alle tarieven bekijken", "See all prices")}</a>
    </aside>
  </div>
</section>

<section class="section soft">
  <div class="container">
    <div class="section-heading"><h2>{L(f"Veelgevraagde klussen in {escape(naam)}", f"Common jobs in {escape(naam)}")}</h2>
    <p>{L(f"Dit doen we het vaakst voor bewoners in {escape(naam)}. Staat jouw klus er niet tussen? Bekijk", f"This is what we do most often for residents of {escape(naam)}. Your job not listed? See")} <a class="mini-link" href="{pad('/diensten/')}">{L("alle diensten", "all services")}</a>.</p></div>
    <div class="service-grid">{klussen}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <a class="alert-banner" href="{pad('/spoed-elektricien-utrecht/')}">
      <div><strong>{L(f"Nu een storing in {escape(naam)}?", f"Power fault in {escape(naam)} right now?")}</strong>
      <span>{L(f"Geen stroom, een aardlek die blijft uitvallen of brandlucht? Bel {B['telefoon_tonen']}, ook 's nachts en in het weekend.", f"No power, an RCD that keeps tripping or a burning smell? Call {B['telefoon_tonen']}, also at night and at weekends.")}</span></div>
      <span class="arrow" aria-hidden="true">→</span>
    </a>
    <div class="quick-help">
      <a href="{pad('/stroomstoring-utrecht/')}">{L("Geen stroom in huis", "No power at home")}</a>
      <a href="{pad('/aardlekschakelaar-springt-eruit/')}">{L("Aardlek springt eruit", "RCD keeps tripping")}</a>
      <a href="{pad('/kortsluiting-utrecht/')}">{L("Groep valt steeds uit", "Circuit keeps tripping")}</a>
      <a href="{pad('/stopcontact-werkt-niet/')}">{L("Stopcontact werkt niet", "Socket not working")}</a>
    </div>
  </div>
</section>

{faq_html(w['faq'], L(f"Vragen van bewoners uit {escape(naam)}", f"Questions from residents of {escape(naam)}"))}

{praktijk_html}<section class="section soft">
  <div class="container">
    <h2>{L("Ook actief in de buurt", "Also working nearby")}</h2>
    <div class="link-cloud">{andere_links}<a href="{pad('/wijken/')}">{L("Alle wijken en plaatsen", "All neighbourhoods and towns")}</a></div>
  </div>
</section>

{cta_band(L(f"Elektricien nodig in {escape(naam)}?", f"Need an electrician in {escape(naam)}?"), wijk=w['slug'])}
"""
    # Title max 60 tekens, description 120–160 (zie CLAUDE.md): kies de eerste variant die past
    kort = w.get("naam_kort") or naam
    if taal.en():
        return _wijk_meta_en(w, naam, kort, in_utrecht, locatie, body)
    titles = [f"Elektricien {naam} | 24/7 storing & vaste prijs | INO",
              f"Elektricien {naam} | 24/7 & vaste prijs | INO",
              f"Elektricien {kort} | 24/7 & vaste prijs | INO",
              f"Elektricien {kort} | 24/7 storing | INO",
              f"Elektricien {kort} | INO"]
    title = next(t for t in titles if len(t) <= 60 or t is titles[-1])
    voordeel = "geen voorrijkosten" if in_utrecht else "eerlijke km-vergoeding"
    descs = [f"Elektricien in {naam} nodig? Storing, groepenkast of perilex. Vaste prijs vooraf, 24/7 bereikbaar, {voordeel}. Bel {B['telefoon_tonen']}.",
             f"Elektricien in {naam} nodig? Storing, groepenkast of perilex. Vaste prijs vooraf en {voordeel}. Bel {B['telefoon_tonen']}.",
             f"Elektricien in {kort} nodig? Storing, groepenkast of perilex. Vaste prijs vooraf en {voordeel}. Bel {B['telefoon_tonen']}.",
             f"Elektricien in {kort}? Storing of groepenkast: vaste prijs vooraf, 24/7, {voordeel}. Bel {B['telefoon_tonen']}."]
    desc = next(d for d in descs if len(d) <= 160 or d is descs[-1])
    schema = [{
        "@type": "Service", "@id": f"{SITE_URL}/elektricien-{w['slug']}/#service",
        "name": f"Elektricien {naam}", "serviceType": "Elektricien",
        "areaServed": {"@type": "City" if not in_utrecht else "Place", "name": locatie},
        "description": fmt(w["intro"]),
    }]
    return {
        "slug": f"elektricien-{w['slug']}", "nl_slug": f"elektricien-{w['slug']}", "taal": "nl", "title": title, "description": desc, "body": body,
        "nav": "wijken", "schema": schema, "faq": [[fmt(q), fmt(a)] for q, a in w["faq"]],
        "crumbs": [("Werkgebied", "/werkgebied/"), ("Wijken", "/wijken/"), (f"Elektricien {naam}", None)],
        "og_image": "storingsdienst-meting.jpg", "priority": "0.8",
    }


def _wijk_meta_en(w, naam, kort, in_utrecht, locatie, body):
    titles = [f"Electrician {naam} | 24/7 & fixed price | INO",
              f"Electrician {kort} | 24/7 & fixed price | INO",
              f"Electrician {kort} | 24/7 | INO",
              f"Electrician {kort} | INO"]
    title = next(t for t in titles if len(t) <= 60 or t is titles[-1])
    voordeel = "no call-out charge" if in_utrecht else "fair mileage rate"
    descs = [f"Need an electrician in {naam}? Power faults, fuse boxes, Perilex. Fixed price upfront, available 24/7, {voordeel}. Call {B['telefoon_tonen']}.",
             f"Need an electrician in {naam}? Faults, fuse boxes, Perilex. Fixed price upfront and {voordeel}. Call {B['telefoon_tonen']}.",
             f"Need an electrician in {kort}? Faults, fuse boxes, Perilex. Fixed price upfront and {voordeel}. Call {B['telefoon_tonen']}.",
             f"Electrician in {kort}? Faults or fuse box: fixed price upfront, 24/7, {voordeel}. Call {B['telefoon_tonen']}."]
    desc = next(d for d in descs if len(d) <= 160 or d is descs[-1])
    slug = taal.slug_in(f"elektricien-{w['slug']}", "en")
    schema = [{
        "@type": "Service", "@id": f"{SITE_URL}/{slug}/#service",
        "name": f"Electrician {naam}", "serviceType": "Electrician",
        "areaServed": {"@type": "City" if not in_utrecht else "Place", "name": locatie},
        "description": fmt(w["intro"]),
    }]
    return {
        "slug": slug, "nl_slug": f"elektricien-{w['slug']}", "taal": "en",
        "title": title, "description": desc, "body": body,
        "nav": "wijken", "schema": schema, "faq": [[fmt(q), fmt(a)] for q, a in w["faq"]],
        "crumbs": [("Service area", "/en/service-area/"), ("Neighbourhoods", "/en/neighbourhoods/"), (f"Electrician {naam}", None)],
        "og_image": "storingsdienst-meting.jpg", "priority": "0.6",
    }


# --------------------------------------------------------------------------- storingpagina
def storing_pagina(s, alle):
    stappen = "".join(
        f'<li><h3>{escape(t)}</h3><p>{escape(fmt(u))}</p></li>' for t, u in s["stappen"])
    oorzaken = "".join(
        f'<div class="cert-card"><h3>{escape(t)}</h3><p>{escape(fmt(u))}</p></div>' for t, u in s["oorzaken"])
    gerel = {x["slug"]: x for x in alle}
    rel = "".join(f'<a href="{pad("/" + r + "/")}">{gerel[r]["kort"]}</a>' for r in s["gerelateerd"] if r in gerel)
    wa = wa_url(L(f"Hallo INO, ik heb een probleem: {s['kort'].lower()}. Hierbij een foto van mijn meterkast.",
                  f"Hello INO, I have a problem: {s['kort'].lower()}. Here is a photo of my meter cupboard."))
    is_stroomstoring = s['slug'] == 'stroomstoring-utrecht'
    if is_stroomstoring:
        h1_display = L("Geen stroom in huis? Check eerst: Stedin of INO bellen?", "No power at home? First check: call Stedin or INO?")
        intro_display = L("Alles is ineens donker. Voordat je iemand belt: vergelijk direct hieronder of het om een wijkstoring van Stedin gaat of om een storing in jouw eigen installatie waarvoor INO direct kan uitrukken.",
                          "Suddenly everything is dark. Before you call anyone, compare below whether it is a neighbourhood outage for Stedin or a fault in your own installation that INO can come out for straight away.")
        hero_actions_html = ""
        hero_meta_html = ""
        stedin_blok = blok_stedin_checker(toon_kop=False)
    else:
        h1_display = escape(s['h1'])
        intro_display = escape(fmt(s['intro']))
        hero_actions_html = f"""<div class="hero-actions">
      <a class="btn btn-primary btn-lg" href="tel:{B['telefoon_e164']}" data-track="bellen">{ICON_TEL} {L("Direct een elektricien", "Electrician now")}: {B['telefoon_tonen']}</a>
      <a class="btn btn-whatsapp" href="{wa}" target="_blank" rel="noopener" data-track="whatsapp">{ICON_WA} {L("Stuur foto via WhatsApp", "Send a photo via WhatsApp")}</a>
    </div>"""
        hero_meta_html = L("""<div class="meta-row"><span>Direct de monteur aan de lijn</span><span>Vaste prijs vóór we beginnen</span><span>Geen voorrijkosten in Utrecht</span></div>""",
                           """<div class="meta-row"><span>Speak directly to the electrician</span><span>Fixed price before we start</span><span>No call-out charge in Utrecht</span><span>English spoken</span></div>""")
        stedin_blok = ""

    hero_pad = ' style="padding-bottom:12px"' if is_stroomstoring else ""
    body = f"""<section class="lp-hero storing-hero"{hero_pad}>
  <div class="container">
    <div class="badge">{L("24/7 hulp bij storingen in Utrecht e.o.", "24/7 help with power faults in and around Utrecht")}</div>
    <h1>{h1_display}</h1>
    <p>{intro_display}</p>
    {hero_actions_html}
    {hero_meta_html}
  </div>
</section>

{stedin_blok}

<section class="section">
  <div class="container narrow">
    <div class="danger-box" role="note"><strong>{L("Eerst je veiligheid", "Safety first")}</strong><p>{escape(s['gevaar'])}</p></div>
    <h2>{escape(s['stappen_titel'])}</h2>
    <ol class="check-steps">{stappen}</ol>
    <p class="safety-note">{L("Werk nooit zelf aan de groepenkast of aan leidingen onder spanning. Een automaat omhoog of omlaag schakelen en stekkers eruit halen kan veilig; alle verdere reparaties laat je aan een gecertificeerd elektricien over.", "Never work on the fuse box or live wiring yourself. Switching a breaker up or down and unplugging appliances is safe; leave all other repairs to a certified electrician.")}</p>
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
    <div class="section-heading"><h2>{L("Lukt het niet? Heldere tarieven bij spoedhulp", "Not working? Clear emergency rates")}</h2>
    <p>{L("Geen woekertarieven of nare verrassingen: we werken met vaste, eerlijke tarieven. Je spreekt altijd rechtstreeks onze eigen elektromonteur, zonder callcenters.", "No inflated rates or nasty surprises: we work with fixed, fair rates. You always speak directly to our own electrician, never a call centre.")}</p></div>
    {tarief_kaarten()}
  </div>
</section>

{faq_html(s['faq'])}

<section class="section soft">
  <div class="container">
    <h2>{L("Andere veelvoorkomende storingen", "Other common faults")}</h2>
    <div class="link-cloud">{rel}<a href="{pad('/spoed-elektricien-utrecht/')}">{L("Spoed elektricien 24/7", "Emergency electrician 24/7")}</a><a href="{pad('/wijken/')}">{L("Werkgebied per wijk", "Service area by neighbourhood")}</a></div>
  </div>
</section>

{cta_band(L("Kom je er niet uit? Wij komen direct.", "Can't sort it out? We come straight away."), L("Bel of app gerust, ook 's avonds, 's nachts en in het weekend. Je hoort vooraf altijd wat het kost.", "Call or WhatsApp us, also in the evening, at night and at weekends. You always hear the price upfront."))}
"""
    return {
        "slug": taal.slug_in(s["slug"]), "nl_slug": s["slug"], "taal": taal.TAAL,
        "title": s["title"], "description": s["description"], "body": body,
        "nav": s["slug"], "faq": [[fmt(q), fmt(a)] for q, a in s["faq"]],
        "crumbs": [(L("Spoed 24/7", "Emergency 24/7"), pad("/spoed-elektricien-utrecht/")), (s["kort"], None)],
        "og_image": "storingsdienst-meting.jpg", "priority": L("0.8", "0.6"),
        "schema": [{"@type": "Service", "name": L(s["kort"] + " verhelpen", "Fix: " + s["kort"]),
                    "serviceType": L("Storingsdienst elektra", "Electrical emergency service"),
                    "areaServed": {"@type": "City", "name": "Utrecht"}}],
    }


# --------------------------------------------------------------------------- blokken voor content
def blok_storing_kaarten(storingen):
    return '<div class="quick-help quick-help-lg">' + "".join(
        f'<a href="{pad("/" + s["slug"] + "/")}">{s["kort"]}</a>' for s in storingen) + \
        f'<a href="{pad("/spoed-elektricien-utrecht/")}" class="qh-urgent">{L("Iets anders / acuut", "Something else / urgent")}</a></div>'


def blok_wijk_chips(wijken):
    return '<div class="link-cloud">' + "".join(
        f'<a href="{pad("/elektricien-" + w["slug"] + "/")}">{w["naam"]}</a>' for w in wijken) + \
        f'<a href="{pad("/wijken/")}">{L("Alle wijken", "All neighbourhoods")}</a></div>'


def blok_wijken_hub(wijken, overige_utrecht, overige_regio):
    def card(naam, sub, href):
        return (f'<a class="wijk-card" href="{pad(href)}"><div><h3>{L("Elektricien", "Electrician")} {escape(naam)}</h3>'
                f'<p>{escape(sub)}</p></div></a>')
    u = [card(w["naam"], " · ".join(w["buurten"][:3]), f"/elektricien-{w['slug']}/") for w in wijken if w["type"] == "wijk"]
    r = [card(w["naam"], " · ".join(w["buurten"][:3]), f"/elektricien-{w['slug']}/") for w in wijken if w["type"] == "plaats"]
    return (f'<h2 class="wijk-label">{L("Gemeente Utrecht · geen voorrijkosten", "Municipality of Utrecht · no call-out charge")}</h2><div class="wijk-grid">{"".join(u)}</div>'
            f'<h2 class="wijk-label">{L("Regio Utrecht", "Utrecht region")} · € {tv("km_tarief")} per km</h2><div class="wijk-grid">{"".join(r)}</div>')


# --------------------------------------------------------------------------- Google-reviews carrousel (/reviews/)
def blok_reviews_carousel():
    from config import REVIEWS
    from html import escape
    g_svg = ('<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>'
             '<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>'
             '<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>'
             '<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/></svg>')
    star = '<svg width="15" height="15" viewBox="0 0 24 24" fill="#ffb400" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
    sterren = f'<span class="review-stars-wrap" role="img" aria-label="{L("5 van 5 sterren", "5 out of 5 stars")}">{star * 5}</span>'
    kaarten = []
    for r in REVIEWS:
        init = "".join(w[0] for w in r["naam"].split()[:2]).upper()
        kaarten.append(f"""<article class="review-slide-card">
  <div class="review-card-top">
    <div class="review-author-wrap">
      <div class="review-avatar" aria-hidden="true">{escape(init)}</div>
      <div><strong class="review-author-name">{escape(r['naam'])}</strong><span class="review-author-meta">{L("Google-review", "Google review (in Dutch)")}</span></div>
    </div>
    <div class="review-google-badge">{g_svg}</div>
  </div>
  <div class="review-rating-row">{sterren}</div>
  <p class="review-card-text">"{escape(r['tekst'])}"</p>
</article>""")
    kaarten.append(f"""<a class="review-slide-card review-slide-more" href="{B['google_maps']}" target="_blank" rel="noopener">
  <div class="review-card-top"><div class="review-google-badge">{g_svg}</div></div>
  <p class="review-card-text"><strong>{L("Alle", "Read all")} <span data-g="aantal">{B['google_aantal']}</span> {L("reviews lezen", "reviews")}</strong><br>{L("Bekijk alle ervaringen op ons Google-bedrijfsprofiel.", "See every review on our Google Business Profile.")}</p>
  <span class="mini-link">{L("Naar Google →", "Go to Google →")}</span>
</a>""")
    pijlen = ""
    if len(kaarten) > 3:
        pijlen = f"""<div class="carousel-controls">
        <button type="button" class="carousel-arrow-btn" id="reviewsPrevBtn" aria-label="{L("Vorige review", "Previous review")}"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg></button>
        <button type="button" class="carousel-arrow-btn" id="reviewsNextBtn" aria-label="{L("Volgende review", "Next review")}"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg></button>
      </div>"""
    return f"""<section class="section reviews-carousel-section" id="reviews">
  <div class="container">
    <div class="reviews-header-wrap">
      <div>
        <span class="eyebrow">GOOGLE REVIEWS</span>
        <h2>{L("Wat klanten op Google zeggen", "What customers say on Google")}</h2>
        <a class="reviews-score-summary" href="{B['google_maps']}" target="_blank" rel="noopener">
          <span class="score-google-icon">{g_svg}</span>
          <span class="score-number" data-g="score">{L(B['google_score'], taal.getal_en(B['google_score']))}</span>
          {sterren}
          <span class="score-total">{L("uit", "from")} <strong><span data-g="aantal">{B['google_aantal']}</span> {L("Google-reviews", "Google reviews")}</strong></span>
        </a>
      </div>
      {pijlen}
    </div>
    <div class="reviews-carousel-track" id="reviewsTrack" tabindex="0" role="region" aria-label="{L("Google-reviews", "Google reviews")}">
      {"".join(kaarten)}
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------- Rekenhulp storingskosten (alleen /tarieven/)
def blok_storing_rekenhulp():
    """Indicatie arbeidskosten op basis van tijdstip en duur. Alle bedragen uit config.py."""
    def num(v):
        return float(str(v).replace(",", "."))
    data = json.dumps({
        "dag": [T["uur_dag"], num(T["kwartier_dag"])],
        "avond": [T["uur_avond"], num(T["kwartier_avond"])],
        "nacht": [T["uur_nacht"], num(T["kwartier_nacht"])],
    })
    tel, tel_e = B["telefoon_tonen"], B["telefoon_e164"]
    return f"""<section class="section rekenhulp-section" id="rekenhulp">
  <div class="container narrow">
    <div class="section-heading">
      <span class="eyebrow">{L("REKENHULP", "COST CALCULATOR")}</span>
      <h2>{L("Wat kost een storing oplossen?", "What does fixing a fault cost?")}</h2>
      <p>{L("Kies het moment en hoe lang het ongeveer duurt. Je ziet direct de arbeidskosten, inclusief btw.", "Choose when and roughly how long it takes. You instantly see the labour cost, including VAT.")}</p>
    </div>
    <div class="rekenhulp" data-tarieven='{data}'>
      <fieldset>
        <legend>{L("Wanneer?", "When?")}</legend>
        <div class="rh-opties">
          <label><input type="radio" name="rh_moment" value="dag"><span>{L("Overdag<small>ma–vr 08–18 u</small>", "Daytime<small>Mon–Fri 08:00–18:00</small>")}</span></label>
          <label><input type="radio" name="rh_moment" value="avond"><span>{L("Avond<small>ma–vr 18–22 u</small>", "Evening<small>Mon–Fri 18:00–22:00</small>")}</span></label>
          <label><input type="radio" name="rh_moment" value="nacht"><span>{L("Nacht &amp; weekend<small>22–08 u, za, zo, feestdag</small>", "Night &amp; weekend<small>22:00–08:00, Sat, Sun, holidays</small>")}</span></label>
        </div>
        <p class="rh-nu" hidden></p>
      </fieldset>
      <fieldset>
        <legend>{L("Hoe lang ongeveer?", "Roughly how long?")}</legend>
        <div class="rh-opties rh-duur">
          <label><input type="radio" name="rh_duur" value="1" checked><span>{L("1 uur<small>meest voorkomend</small>", "1 hour<small>most common</small>")}</span></label>
          <label><input type="radio" name="rh_duur" value="1.5"><span>{L("1,5 uur", "1.5 hours")}</span></label>
          <label><input type="radio" name="rh_duur" value="2"><span>{L("2 uur", "2 hours")}</span></label>
          <label><input type="radio" name="rh_duur" value="3"><span>{L("3 uur", "3 hours")}</span></label>
        </div>
      </fieldset>
      <div class="rh-uitkomst" aria-live="polite">
        <div><span class="rh-label">{L("Indicatie arbeidskosten", "Estimated labour cost")}</span><strong class="rh-bedrag">€ {T['uur_dag']}</strong><span class="rh-uitleg"></span></div>
        <ul>
          <li>{L("Eerste uur is inclusief diagnose en btw, daarna per kwartier.", "The first hour includes diagnosis and VAT, then per quarter hour.")}</li>
          <li>{L("Gemeente Utrecht: geen voorrijkosten. Daarbuiten", "Municipality of Utrecht: no call-out charge. Outside it")} € {tv('km_tarief')} per km.</li>
          <li>{L("Materiaal komt erbij en bespreken we altijd eerst met je.", "Materials are extra and we always discuss them with you first.")}</li>
        </ul>
        <div class="rh-knoppen">
          <a class="btn btn-primary" href="tel:{tel_e}" data-track="bellen">{L("Bel direct", "Call now")} {tel}</a>
          <a class="btn btn-secondary" href="{pad('/tarieven/')}">{L("Alle tarieven", "All prices")}</a>
        </div>
      </div>
    </div>
  </div>
</section>"""
