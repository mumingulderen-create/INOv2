"""
Sjablonen voor pagina's die uit data worden gemaakt (wijken, storingen) en
voor blokken die in content-bestanden kunnen worden gezet met {{BLOK_NAAM}}.
"""
import json
from html import escape
from config import SITE_URL, BEDRIJF as B, TARIEVEN as T, TARIEF_ZIN, VOORRIJ_ZIN, AANRIJTIJD
from layout import wa_url, ICON_TEL, ICON_WA


def fmt(s):
    """Vul {uur_dag}, {km_tarief} enz. in vanuit TARIEVEN."""
    return s.format(**T, **AANRIJTIJD) if "{" in s else s


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


def blok_stedin_checker(toon_kop=True):
    kop_html = """<div class="section-heading" style="text-align:center;margin-left:auto;margin-right:auto">
      <span class="eyebrow">STORING OF STROOMUITVAL?</span>
      <h2>Stedin bellen, of INO bellen?</h2>
      <p style="margin-left:auto;margin-right:auto;max-width:640px">Twijfel je wie je moet inschakelen bij stroomuitval? Bekijk hieronder direct het verschil tussen een netstoring en een storing in jouw eigen installatie.</p>
    </div>""" if toon_kop else """<div class="hp"><h2>Stedin of INO bellen bij stroomuitval</h2></div>"""
    return f"""<section class="section soft" id="stedin-check">
  <div class="container">
    {kop_html}

    <!-- 2 Kolommen Naast Elkaar: Stedin vs INO -->
    <div class="stedin-compare-grid">
      <!-- Kolom 1: Stedin -->
      <div class="stedin-col-card stedin-col-net">
        <div class="stedin-col-header">
          <span class="stedin-col-badge badge-stedin">🏛️ Netbeheerder Stedin</span>
          <h3>Wanneer bel je Stedin?</h3>
          <p class="stedin-col-sub">Bij storingen in het energienetwerk van de wijk of aan de verzegelde hoofdaansluiting.</p>
        </div>
        
        <div class="stedin-col-body">
          <h4 class="stedin-list-title">Herkenbare kenmerken:</h4>
          <ul class="stedin-check-list">
            <li><span>✕</span> <strong>Hele straat of buren</strong> hebben ook geen stroom</li>
            <li><span>✕</span> <strong>Straatverlichting buiten</strong> is uit of knippert</li>
            <li><span>✕</span> <strong>Display van kWh-meter</strong> is compleet zwart/uit</li>
            <li><span>✕</span> <strong>Verzegelde hoofdzekering</strong> onder de meter is uitgevallen</li>
          </ul>
        </div>

        <div class="stedin-col-footer">
          <div class="stedin-action-box">
            <span class="stedin-action-label">Actie: Neem contact op met netbeheerder</span>
            <a class="btn btn-secondary full" href="tel:08009009">📞 Bel Stedin: 0800 9009</a>
            <a class="stedin-official-link" href="https://www.stedin.net/storing-en-onderhoud" target="_blank" rel="noopener">Officiële storingsprocedure op Stedin.net ↗</a>
          </div>
        </div>
      </div>

      <!-- Kolom 2: INO -->
      <div class="stedin-col-card stedin-col-ino">
        <div class="stedin-col-header">
          <span class="stedin-col-badge badge-ino">⚡ INO Elektrotechniek (24/7 Spoed)</span>
          <h3>Wanneer bel je INO?</h3>
          <p class="stedin-col-sub" style="font-weight:600;color:var(--ink);line-height:1.45">
            Vast all-in tarief: <strong>€ {T['uur_dag']}</strong> (08–18u) · <strong>€ {T['uur_avond']}</strong> (18–22u) · <strong>€ {T['uur_nacht']}</strong> (nacht &amp; weekend)
          </p>
        </div>

        <div class="stedin-col-body">
          <h4 class="stedin-list-title">Herkenbare kenmerken:</h4>
          <ul class="stedin-check-list list-ino">
            <li><span>✓</span> <strong>Alleen bij jou thuis</strong> is het donker (buren hebben licht)</li>
            <li><span>✓</span> <strong>Aardlekschakelaar (knop 'T')</strong> klapt steeds omlaag</li>
            <li><span>✓</span> <strong>Groepenschakelaar</strong> springt direct terug bij aanzetten</li>
            <li><span>✓</span> <strong>Knetterend geluid of brandlucht</strong> bij een stopcontact of kast</li>
          </ul>
        </div>

        <div class="stedin-col-footer">
          <div class="stedin-action-box">
            <span class="stedin-action-label">Actie: Direct storingsdienst inschakelen</span>
            <a class="btn btn-primary full" href="tel:{B['telefoon_e164']}" data-track="bellen">📞 Bel direct INO: {B['telefoon_tonen']}</a>
            <span class="stedin-fast-note">⚡ Bij spoed in Utrecht binnen {AANRIJTIJD["aanrijtijd_utrecht"]} min, regio {AANRIJTIJD["aanrijtijd_regio"]} min</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Brede Hulpbalk: Twijfel / WhatsApp Meekijkservice -->
    <div class="stedin-helper-banner">
      <div class="stedin-helper-icon">📸</div>
      <div class="stedin-helper-text">
        <h4>Twijfel je wat je ziet in je meterkast?</h4>
        <p>Je hoeft geen verstand te hebben van groepenkasten. Maak met je mobiel een foto van je meterkast en stuur deze via WhatsApp. Wij kijken binnen 5 minuten gratis mee en vertellen je direct wie je moet bellen!</p>
      </div>
      <div class="stedin-helper-action">
        <a class="btn btn-whatsapp" href="{wa_url('Hallo INO, ik heb een storing en stuur hierbij een foto van mijn meterkast. Kunnen jullie even gratis meekijken?')}" target="_blank" rel="noopener" data-track="whatsapp">💬 Stuur foto via WhatsApp</a>
      </div>
    </div>

  </div>
</section>"""


def tarief_kaarten(voorrij=True):
    extra = f'<p class="price-note form-note">{VOORRIJ_ZIN} Een schouw op locatie kost € {T["schouw"]} en verrekenen we volledig als je de klus laat uitvoeren.</p>' if voorrij else ""
    return f"""<div class="price-grid">
  <div class="price-card"><h3>Overdag</h3><div class="price-amount">€ {T['uur_dag']}<span> 1e uur</span></div><p>Ma–vr 08:00–18:00. Daarna € {T['kwartier_dag']} per kwartier.</p></div>
  <div class="price-card"><h3>Avond</h3><div class="price-amount">€ {T['uur_avond']}<span> 1e uur</span></div><p>Ma–vr 18:00–22:00. Daarna € {T['kwartier_avond']} per kwartier.</p></div>
  <div class="price-card highlight"><h3>Nacht &amp; weekend</h3><div class="price-amount">€ {T['uur_nacht']}<span> 1e uur</span></div><p>22:00–08:00, complete zaterdagen, zondagen en feestdagen. Daarna € {T['kwartier_nacht']} per kwartier.</p></div>
</div>
<p class="form-note">Alle bedragen inclusief 21% btw en foutdiagnose. Meer werk of een onderdeel nodig? Dan hoor je eerst de prijs en beslis jij.</p>{extra}"""


def groepenkast_calculator():
    # Alle calculatorprijzen komen uit config.py (TARIEVEN)
    drie_fase_meer = T["calc_meer_3f"]
    start = T["calc_basis_1f"] + drie_fase_meer + T["optie_kookgroep"]
    prijzen = json.dumps({"basis": T["calc_basis_1f"], "driefase": drie_fase_meer, "kookgroep": T["optie_kookgroep"],
                          "kracht": T["optie_kracht_4p"], "pv": T["optie_pv"], "groep": T["optie_automaat"]})
    wa_default = wa_url(f"Hallo INO, via jullie online calculator kom ik uit op een 3-fase groepenkast met 8 groepen (indicatie € {T['groepenkast_3f']}). Hierbij stuur ik een foto van mijn huidige meterkast mee voor een vaste offerte.")
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
      <span class="badge">GROEPENKAST ADVIES</span>
      <h2>Groepenkast &amp; Inductie Berekenen</h2>
      <p>Selecteer je apparaten voor een direct technisch advies (1-fase of 3-fase) en all-in prijsindicatie.</p>
    </div>

    <div class="calc-card">
      <div class="calc-grid">
        <div class="calc-inputs">
          <div class="calc-step-header">
            <span class="calc-step-num">1</span>
            <div>
              <h3>Welke apparaten wil je aansluiten?</h3>
              <p>Selecteer de apparaten die in de woning draaien of bijkomen.</p>
            </div>
          </div>

          <div class="calc-device-grid">
            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="inductie" data-groepen="1" checked>
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>Inductiekookplaat</strong>
                  <span>2x230V kookgroep of 3-fase</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="laadpaal" data-groepen="1">
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>Laadpaal (Wallbox)</strong>
                  <span>Krachtstroom 3-fase / 11 kW</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="zonnepanelen" data-groepen="1">
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>Zonnepanelen (PV)</strong>
                  <span>Aparte PV-aardlekautomaat</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="warmtepomp" data-groepen="1">
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>Warmtepomp of Airco</strong>
                  <span>Zware groep / 3-fase kracht</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="quooker" data-groepen="1">
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>Quooker / Keukenboiler</strong>
                  <span>Aparte 230V groep (2200W)</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="wasmachine" data-groepen="2" checked>
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>Wasmachine &amp; Droger</strong>
                  <span>Twee aparte zware groepen</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="keuken" data-groepen="2" checked>
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>Oven &amp; Vaatwasser</strong>
                  <span>Twee aparte keukengroepen</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>

            <label class="calc-item">
              <input type="checkbox" name="calc_device" value="basis" data-groepen="3" checked>
              <div class="calc-box">
                <div class="calc-item-text">
                  <strong>Woonkamer, slaapkamers &amp; licht</strong>
                  <span>Drie basis licht-/wandgroepen</span>
                </div>
                <div class="calc-check"></div>
              </div>
            </label>
          </div>

          <div class="calc-step-header" style="margin-top:28px">
            <span class="calc-step-num">2</span>
            <div>
              <h3>Wat voor meterkast en aansluiting heb je nu?</h3>
              <p>Kies je huidige situatie voor een passend advies en plan van aanpak.</p>
            </div>
          </div>

          <div class="calc-sub-label">Huidige netaansluiting (hoofdschakelaar/meter):</div>
          <div class="calc-radio-group" style="margin-bottom:18px">
            <label class="calc-radio-item">
              <input type="radio" name="calc_aansluiting" value="1fase" checked>
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>1-fase aansluiting (230V)</strong>
                  <span>Standaard aansluiting (1x25A of 1x35A op de meter)</span>
                </div>
              </div>
            </label>

            <label class="calc-radio-item">
              <input type="radio" name="calc_aansluiting" value="3fase">
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>3-fase aansluiting (400V)</strong>
                  <span>Krachtstroom al aanwezig (3x25A op de meter)</span>
                </div>
              </div>
            </label>

            <label class="calc-radio-item">
              <input type="radio" name="calc_aansluiting" value="onbekend">
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>Weet ik niet zeker</strong>
                  <span>Ik stuur een foto mee van de hoofdmeter</span>
                </div>
              </div>
            </label>
          </div>

          <div class="calc-sub-label">Type groepenkast:</div>
          <div class="calc-radio-group">
            <label class="calc-radio-item">
              <input type="radio" name="calc_huidig" value="stoppen" checked>
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>Oude stoppenkast</strong>
                  <span>Draaizekeringen met smeltpatronen (volledige vervanging)</span>
                </div>
              </div>
            </label>

            <label class="calc-radio-item">
              <input type="radio" name="calc_huidig" value="automaat">
              <div class="calc-radio-box">
                <div class="calc-radio-circle"></div>
                <div class="calc-radio-text">
                  <strong>Bestaande automatenkast</strong>
                  <span>Schakelaars met hendeltjes (vervangen of uitbreiden)</span>
                </div>
              </div>
            </label>
          </div>
        </div>

        <div class="calc-summary">
          <div class="calc-summary-card">
            <div class="calc-badge">BEREKEND ADVIES</div>
            
            <div class="calc-kpi-row">
              <div class="calc-kpi">
                <span class="calc-kpi-label">Benodigde groepen</span>
                <strong id="calcGroepen">8 groepen</strong>
              </div>
              <div class="calc-kpi">
                <span class="calc-kpi-label">Geadviseerde fase</span>
                <strong id="calcFase">3-fase (400V)</strong>
              </div>
            </div>

            <div class="calc-explanation">
              <div class="calc-explain-title" id="calcTitel">Aanbevolen: 3-fase Hager of ABB Groepenkast</div>
              <p id="calcUitleg">Door de combinatie van apparaten adviseren we een 3-fase groepenkast voor een optimale belastingverdeling conform NEN 1010.</p>
            </div>

            <div class="calc-stedin-notice" id="calcStedinBox">
              <div class="calc-stedin-title">
                <strong>Verzwaring via Stedin naar 3-fase</strong>
              </div>
              <p>Je woning heeft nu 1-fase, maar je apparaten vragen om 3-fase (kracht). Vraag de netaansluiting-verzwaring aan bij Stedin via mijnaansluiting.nl.</p>
              <div class="calc-stedin-role">
                <strong>Hoe INO Techniek dit oplost:</strong>
                Wij monteren en bedraden je nieuwe groepenkast alvast 100% 3-fase voorbereid (met 4-polige hoofdschakelaar). Zodra de Stedin-monteur langskomt, kan deze de fasen direct aansluiten zonder extra ombouwwerk!
              </div>
            </div>

            <div class="calc-breakdown">
              <div class="calc-breakdown-title">Transparante Prijsopbouw</div>
              <ul class="calc-breakdown-list" id="calcBreakdown">
                <li class="calc-breakdown-item"><span>1-fase basiskast (tot 8 gr.)</span><span>€ {T['calc_basis_1f']},-</span></li>
                <li class="calc-breakdown-item"><span>3-fase uitvoering &amp; kamrail voorbereiding</span><span>+ € {drie_fase_meer},-</span></li>
                <li class="calc-breakdown-item"><span>Inductie kookgroep (incl. kamrail &amp; aansluiting)</span><span>+ € {T['optie_kookgroep']},-</span></li>
              </ul>
            </div>

            <div class="calc-price-box">
              <span class="calc-price-label">Indicatieve all-in investering</span>
              <div class="calc-price-val" id="calcPrijs">€ {start},- <span>all-in</span></div>
              <span class="calc-price-sub">Inclusief A-merk kast, kamrails, klein montagemateriaal, montage, 21% btw en 12 mnd garantie</span>
            </div>

            <div class="calc-actions">
              <a href="/offerte/" id="calcOfferteBtn" class="btn btn-primary full">Offerte aanvragen met deze berekening</a>
              <a href="{wa_default}" id="calcWaBtn" target="_blank" rel="noopener" class="btn btn-whatsapp full">
                {ICON_WA} WhatsApp deze berekening + foto
              </a>
            </div>

            <div class="calc-guarantee-note">
              <span>Bindende vaste all-in prijs vooraf</span>
              <span>Geen voorrijkosten binnen de gemeente Utrecht</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""


KLUS_LINKS = [
    (("groepenkast", "kast"), "/groepenkast/"),
    (("perilex", "kookgroep", "inductie", "koken"), "/perilex/"),
    (("laadpaal",), "/laadpaal-installeren/"),
    (("krachtstroom", "400v"), "/krachtstroom-aanleggen/"),
    (("stopcontact", "frezen", "verbouwing", "keuken"), "/frezen-stopcontacten-verleggen/"),
    (("tuin", "buiten", "schuur"), "/tuinverlichting-buitenelektra/"),
    (("aardlek",), "/aardlekschakelaar-springt-eruit/"),
    (("groep valt", "uitval"), "/kortsluiting-utrecht/"),
    (("storing", "doormeten", "bedrading"), "/stroomstoring-utrecht/"),
]


def klus_link(titel):
    t = titel.lower()
    for keys, href in KLUS_LINKS:
        if any(k in t for k in keys):
            return href
    return "/diensten/"


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
    aanrij = f'<span>Bij spoed: {fmt(w["aanrijtijd"])}</span>' if w["aanrijtijd"] else '<span>Bij spoed: bel voor de actuele aanrijtijd</span>'
    # Alleen buren (lijst staat ruwweg geografisch): minder gedeelde tekst per pagina, de footer/hub linkt de rest
    i = next(n for n, x in enumerate(alle) if x["slug"] == w["slug"])
    andere = [x for x in (alle[max(0, i - 3):i] + alle[i + 1:i + 4]) if x["slug"] != w["slug"]]
    # Echte praktijkvoorbeelden (door eigenaar in te vullen in wijken.py: "praktijk": [["titel", "tekst"], ...])
    praktijk = w.get("praktijk") or []
    praktijk_html = (f'''<section class="section">
  <div class="container">
    <h2>Recent in {escape(naam)}</h2>
    <div class="service-grid">{"".join(f'<article class="service-card"><h3>{escape(fmt(t))}</h3><p>{escape(fmt(x))}</p></article>' for t, x in praktijk)}</div>
  </div>
</section>

''') if praktijk else ""
    andere_links = "".join(f'<a href="/elektricien-{x["slug"]}/">Elektricien {x["naam"]}</a>' for x in andere)
    tarief_voorrij = (f"Binnen de gemeente Utrecht, en dus ook in {naam}, rekenen we geen voorrijkosten."
                      if in_utrecht else
                      f"{naam} ligt buiten de gemeente Utrecht. Voorrijden kost € {T['km_tarief']} per km; dat bedrag hoor je altijd vooraf.")
    wa = wa_url(f"Hallo INO, ik woon in {naam} en heb een vraag. Hierbij een foto.")
    body = f"""<section class="lp-hero">
  <div class="container">
    <div class="badge">Elektricien {escape(locatie)}</div>
    <h1>Elektricien in {escape(naam)} nodig?</h1>
    <p>{escape(fmt(w['intro']))}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="tel:{B['telefoon_e164']}" data-track="bellen">{ICON_TEL} Bel {B['telefoon_tonen']}</a>
      <a class="btn btn-whatsapp" href="{wa}" target="_blank" rel="noopener" data-track="whatsapp">{ICON_WA} WhatsApp een foto</a>
      <a class="btn btn-secondary" href="/offerte/?wijk={w['slug']}">Offerte aanvragen</a>
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
        <li>Overdag (08:00–18:00): € {T['uur_dag']} (1e uur, incl. btw)</li>
        <li>Avond (ma–vr 18:00–22:00): € {T['uur_avond']}</li>
        <li>Nacht (22:00–08:00), za, zo en feestdagen: € {T['uur_nacht']}</li>
        <li>Groepenkast 1-fase: vanaf € {T['groepenkast_1f']} all-in</li>
        <li>Perilex aansluiten: € {T['perilex_aansluiten']}</li>
      </ul>
      <p class="form-note">{escape(tarief_voorrij)}</p>
      <a class="mini-link" href="/tarieven/">Alle tarieven bekijken</a>
    </aside>
  </div>
</section>

<section class="section soft">
  <div class="container">
    <div class="section-heading"><h2>Veelgevraagde klussen in {escape(naam)}</h2>
    <p>Dit doen we het vaakst voor bewoners in {escape(naam)}. Staat jouw klus er niet tussen? Bekijk <a class="mini-link" href="/diensten/">alle diensten</a>.</p></div>
    <div class="service-grid">{klussen}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <a class="alert-banner" href="/spoed-elektricien-utrecht/">
      <div><strong>Nu een storing in {escape(naam)}?</strong>
      <span>Geen stroom, een aardlek die blijft uitvallen of brandlucht? Bel {B['telefoon_tonen']}, ook 's nachts en in het weekend.</span></div>
      <span class="arrow" aria-hidden="true">→</span>
    </a>
    <div class="quick-help">
      <a href="/stroomstoring-utrecht/">Geen stroom in huis</a>
      <a href="/aardlekschakelaar-springt-eruit/">Aardlek springt eruit</a>
      <a href="/kortsluiting-utrecht/">Groep valt steeds uit</a>
      <a href="/stopcontact-werkt-niet/">Stopcontact werkt niet</a>
    </div>
  </div>
</section>

{faq_html(w['faq'], f"Vragen van bewoners uit {escape(naam)}")}

{praktijk_html}<section class="section soft">
  <div class="container">
    <h2>Ook actief in de buurt</h2>
    <div class="link-cloud">{andere_links}<a href="/wijken/">Alle wijken en plaatsen</a></div>
  </div>
</section>

{cta_band(f"Elektricien nodig in {escape(naam)}?", wijk=w['slug'])}
"""
    # Title max 60 tekens, description 120–160 (zie CLAUDE.md): kies de eerste variant die past
    kort = w.get("naam_kort") or naam
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
        "slug": f"elektricien-{w['slug']}", "title": title, "description": desc, "body": body,
        "nav": "wijken", "schema": schema, "faq": [[fmt(q), fmt(a)] for q, a in w["faq"]],
        "crumbs": [("Werkgebied", "/werkgebied/"), ("Wijken", "/wijken/"), (f"Elektricien {naam}", None)],
        "og_image": "storingsdienst-meting.jpg", "priority": "0.8",
    }


# --------------------------------------------------------------------------- storingpagina
def storing_pagina(s, alle):
    stappen = "".join(
        f'<li><h3>{escape(t)}</h3><p>{escape(fmt(u))}</p></li>' for t, u in s["stappen"])
    oorzaken = "".join(
        f'<div class="cert-card"><h3>{escape(t)}</h3><p>{escape(fmt(u))}</p></div>' for t, u in s["oorzaken"])
    gerel = {x["slug"]: x for x in alle}
    rel = "".join(f'<a href="/{r}/">{gerel[r]["kort"]}</a>' for r in s["gerelateerd"] if r in gerel)
    wa = wa_url(f"Hallo INO, ik heb een probleem: {s['kort'].lower()}. Hierbij een foto van mijn meterkast.")
    is_stroomstoring = s['slug'] == 'stroomstoring-utrecht'
    if is_stroomstoring:
        h1_display = "Geen stroom in huis? Check eerst: Stedin of INO bellen?"
        intro_display = "Alles is ineens donker. Voordat je iemand belt: vergelijk direct hieronder of het om een wijkstoring van Stedin gaat of om een storing in jouw eigen installatie waarvoor INO direct kan uitrukken."
        hero_actions_html = ""
        hero_meta_html = ""
        stedin_blok = blok_stedin_checker(toon_kop=False)
    else:
        h1_display = escape(s['h1'])
        intro_display = escape(fmt(s['intro']))
        hero_actions_html = f"""<div class="hero-actions">
      <a class="btn btn-primary btn-lg" href="tel:{B['telefoon_e164']}" data-track="bellen">{ICON_TEL} Direct een elektricien: {B['telefoon_tonen']}</a>
      <a class="btn btn-whatsapp" href="{wa}" target="_blank" rel="noopener" data-track="whatsapp">{ICON_WA} Stuur foto via WhatsApp</a>
    </div>"""
        hero_meta_html = """<div class="meta-row"><span>Direct de monteur aan de lijn</span><span>Vaste prijs vóór we beginnen</span><span>Geen voorrijkosten in Utrecht</span></div>"""
        stedin_blok = ""

    hero_pad = ' style="padding-bottom:12px"' if is_stroomstoring else ""
    body = f"""<section class="lp-hero storing-hero"{hero_pad}>
  <div class="container">
    <div class="badge">24/7 hulp bij storingen in Utrecht e.o.</div>
    <h1>{h1_display}</h1>
    <p>{intro_display}</p>
    {hero_actions_html}
    {hero_meta_html}
  </div>
</section>

{stedin_blok}

<section class="section">
  <div class="container narrow">
    <div class="danger-box" role="note"><strong>Eerst je veiligheid</strong><p>{escape(s['gevaar'])}</p></div>
    <h2>{escape(s['stappen_titel'])}</h2>
    <ol class="check-steps">{stappen}</ol>
    <p class="safety-note">Werk nooit zelf aan de groepenkast of aan leidingen onder spanning. Een automaat omhoog of omlaag schakelen en stekkers eruit halen kan veilig; alle verdere reparaties laat je aan een gecertificeerd elektricien over.</p>
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
    <div class="section-heading"><h2>Lukt het niet? Heldere tarieven bij spoedhulp</h2>
    <p>Geen woekertarieven of nare verrassingen: we werken met vaste, eerlijke tarieven. Je spreekt altijd rechtstreeks onze eigen elektromonteur, zonder callcenters.</p></div>
    {tarief_kaarten()}
  </div>
</section>

{faq_html(s['faq'])}

<section class="section soft">
  <div class="container">
    <h2>Andere veelvoorkomende storingen</h2>
    <div class="link-cloud">{rel}<a href="/spoed-elektricien-utrecht/">Spoed elektricien 24/7</a><a href="/wijken/">Werkgebied per wijk</a></div>
  </div>
</section>

{cta_band("Kom je er niet uit? Wij komen direct.", "Bel of app gerust, ook 's avonds, 's nachts en in het weekend. Je hoort vooraf altijd wat het kost.")}
"""
    return {
        "slug": s["slug"], "title": s["title"], "description": s["description"], "body": body,
        "nav": s["slug"], "faq": [[fmt(q), fmt(a)] for q, a in s["faq"]],
        "crumbs": [("Spoed 24/7", "/spoed-elektricien-utrecht/"), (s["kort"], None)],
        "og_image": "storingsdienst-meting.jpg", "priority": "0.8",
        "schema": [{"@type": "Service", "name": s["kort"] + " verhelpen", "serviceType": "Storingsdienst elektra",
                    "areaServed": {"@type": "City", "name": "Utrecht"}}],
    }


# --------------------------------------------------------------------------- blokken voor content
def blok_storing_kaarten(storingen):
    return '<div class="quick-help quick-help-lg">' + "".join(
        f'<a href="/{s["slug"]}/">{s["kort"]}</a>' for s in storingen) + \
        '<a href="/spoed-elektricien-utrecht/" class="qh-urgent">Iets anders / acuut</a></div>'


def blok_wijk_chips(wijken):
    return '<div class="link-cloud">' + "".join(
        f'<a href="/elektricien-{w["slug"]}/">{w["naam"]}</a>' for w in wijken) + \
        '<a href="/wijken/">Alle wijken</a></div>'


def blok_wijken_hub(wijken, overige_utrecht, overige_regio):
    def card(naam, sub, href):
        return (f'<a class="wijk-card" href="{href}"><div><h3>Elektricien {escape(naam)}</h3>'
                f'<p>{escape(sub)}</p></div></a>')
    u = [card(w["naam"], " · ".join(w["buurten"][:3]), f"/elektricien-{w['slug']}/") for w in wijken if w["type"] == "wijk"]
    r = [card(w["naam"], " · ".join(w["buurten"][:3]), f"/elektricien-{w['slug']}/") for w in wijken if w["type"] == "plaats"]
    return (f'<h2 class="wijk-label">Gemeente Utrecht · geen voorrijkosten</h2><div class="wijk-grid">{"".join(u)}</div>'
            f'<h2 class="wijk-label">Regio Utrecht · € {T["km_tarief"]} per km</h2><div class="wijk-grid">{"".join(r)}</div>')
