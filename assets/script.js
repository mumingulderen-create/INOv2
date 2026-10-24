// Veilige cross-origin foutafhandeling
window.addEventListener('error', function (e) {
  if (e && e.message === 'Script error.') {
    // Cross-origin script error (bijv. Google Analytics / Tag Manager in iframe preview)
    e.preventDefault && e.preventDefault();
    return true;
  }
});
/* INO Elektra – script.js (v2)
   Klein, zonder frameworks. Wordt met `defer` geladen, blokkeert de pagina dus niet. */
(function () {
  "use strict";

  // Oude .html-URL's netjes maken in de adresbalk
  var p = location.pathname;
  if (/(\/index)?\.html$/.test(p)) {
    var clean = p.replace(/\/index\.html$/, "/").replace(/\.html$/, "") || "/";
    history.replaceState(null, "", clean + location.search + location.hash);
  }

  // Mobiel menu
  var btn = document.getElementById("menuBtn"), nav = document.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.focus(); }
    });
  }

  // FAQ-accordeon (toegankelijk). Het +/− teken staat altijd in het LAATSTE <span>.
  document.querySelectorAll(".faq-q").forEach(function (q, i) {
    var a = q.nextElementSibling;
    if (!a) return;
    var id = a.id || "faq-a-" + i;
    a.id = id;
    q.setAttribute("aria-controls", id);
    q.setAttribute("aria-expanded", "false");
    if (!q.getAttribute("type")) q.setAttribute("type", "button");
    q.addEventListener("click", function () {
      var open = a.classList.toggle("open");
      q.setAttribute("aria-expanded", open ? "true" : "false");
      var spans = q.querySelectorAll("span");
      var icon = spans[spans.length - 1];
      if (icon && spans.length) icon.textContent = open ? "−" : "+";
    });
  });

  // Kaart vergroten (werkgebied)
  var mb = document.getElementById("mapEnlargeBtn"), mm = document.getElementById("mapModal"), mc = document.getElementById("mapModalClose");
  if (mb && mm) {
    var close = function () { mm.classList.remove("open"); mb.focus(); };
    mb.addEventListener("click", function () { mm.classList.add("open"); if (mc) mc.focus(); });
    if (mc) mc.addEventListener("click", close);
    mm.addEventListener("click", function (e) { if (e.target === mm) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && mm.classList.contains("open")) close(); });
  }

  // Foto-upload: toon gekozen bestanden
  var photos = document.getElementById("photos"), list = document.getElementById("photoList");
  if (photos && list) photos.addEventListener("change", function () {
    var f = Array.prototype.slice.call(photos.files);
    list.textContent = f.length ? f.length + " bestand(en): " + f.map(function (x) { return x.name; }).join(", ") : "";
  });

  var d = document.getElementById("date");
  if (d) d.min = new Date().toISOString().split("T")[0];

  function esc(v) { return String(v).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[c]; }); }

  // Formulieren → eigen beveiligd endpoint (Cloudflare Worker, zie worker/).
  // Honeypot + Turnstile tegen spam; de server controleert alles opnieuw.
  var VELDNAMEN = { name: "naam", phone: "telefoonnummer", email: "e-mailadres", message: "omschrijving", postcode: "postcode",
    number: "huisnummer", datum: "datum", tijd: "tijd", akkoord: "toestemming", photos: "foto's" };
  function wire(form, okMsg) {
    if (!form) return;
    if (!form.querySelector('[name="_honey"]')) {
      var hp = document.createElement("input");
      hp.type = "text"; hp.name = "_honey"; hp.tabIndex = -1; hp.autocomplete = "off"; hp.className = "hp"; hp.setAttribute("aria-hidden", "true");
      form.appendChild(hp);
    }
    var submit = form.querySelector("button[type='submit']");
    var label = submit ? submit.innerHTML : "Versturen";
    var bezig = false;
    function toon(result, cls, html) {
      if (result) { result.hidden = false; result.className = cls; result.innerHTML = html; result.scrollIntoView({ behavior: "smooth", block: "center" }); }
      else alert(html.replace(/<[^>]+>/g, " "));
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (bezig) return; // geen dubbele inzending
      var result = form.querySelector(".form-result") || document.getElementById("formResult");
      var data = new FormData(form);
      if (data.get("_honey")) return;
      form.querySelectorAll("[aria-invalid]").forEach(function (el) { el.removeAttribute("aria-invalid"); });
      var hulp = window.inoFormulier;
      var fout = "<strong>Er ging iets mis bij het verzenden van je aanvraag.</strong><br>Probeer het opnieuw of bel ons direct op <a href=\"tel:__TEL_E164__\">__TEL__</a>.";
      if (!"__FORM_ENDPOINT__" || !hulp || !hulp.actief) { toon(result, "form-result form-result-error", fout); return; }
      bezig = true;
      if (submit) { submit.disabled = true; submit.textContent = "Versturen…"; }
      var fotoVeld = form.querySelector("input[type='file'][name='photos']");
      (fotoVeld && fotoVeld.files.length ? hulp.fotos(fotoVeld.files) : Promise.resolve([]))
        .then(function (fotos) {
          data.delete("photos");
          fotos.forEach(function (f, i) { data.append("photos", f, f.name || "foto-" + (i + 1) + ".jpg"); });
          return hulp.token(form);
        }, function (err) { throw { bericht: err.message, veld: "photos" }; })
        .then(function (t) {
          if (!t) throw { bericht: "De beveiligingscontrole is nog niet klaar. Wacht even en probeer het opnieuw." };
          data.set("cf-turnstile-response", t);
          data.set("formulier", form.getAttribute("data-formulier"));
          return fetch("__FORM_ENDPOINT__", { method: "POST", body: data, mode: "cors", credentials: "omit", headers: { Accept: "application/json" } });
        })
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (j) {
            if (r.ok && j.ok) return j;
            if (r.status === 422 && j.velden) {
              var namen = Object.keys(j.velden);
              namen.forEach(function (n) { var el = form.querySelector("[name='" + n + "']"); if (el) el.setAttribute("aria-invalid", "true"); });
              throw { bericht: "Controleer de ingevulde gegevens en probeer het opnieuw:<br>" + namen.map(function (n) { return esc((VELDNAMEN[n] || n) + " – " + j.velden[n]); }).join("<br>"), veld: namen[0] };
            }
            if (r.status === 429) throw { bericht: "Je hebt net al iets verstuurd. Wacht een minuut of bel ons direct op <a href=\"tel:__TEL_E164__\">__TEL__</a>." };
            if (r.status === 403) throw { bericht: "We konden je aanvraag niet verifiëren. Probeer het opnieuw of bel ons op <a href=\"tel:__TEL_E164__\">__TEL__</a>." };
            if (r.status === 413) throw { bericht: "De foto's zijn te groot. Stuur minder of kleinere foto's.", veld: "photos" };
            throw {};
          });
        })
        .then(function () {
          track("formulier_verstuurd", { formulier: form.id || "form" });
          track("generate_lead", { formulier: form.id || "form", currency: "EUR" });
          toon(result, "form-result", "<strong>Je aanvraag is succesvol verzonden.</strong><br>Bedankt " + esc(data.get("name") || "") + ", " + okMsg);
          form.reset();
          if (list) list.textContent = "";
        })
        .catch(function (err) {
          toon(result, "form-result form-result-error", err && err.bericht ? "<strong>Je aanvraag is niet verzonden.</strong><br>" + err.bericht : fout);
        })
        .finally(function () {
          bezig = false;
          hulp.reset(form); // Turnstile-token is eenmalig; nieuw token voor een volgende poging
          if (submit) { submit.disabled = false; submit.innerHTML = label; }
        });
    });
  }
  wire(document.getElementById("quoteForm"), "we nemen zo snel mogelijk contact met je op. Je ontvangt ook een bevestiging per e-mail.");
  wire(document.getElementById("spoedForm"), "we bellen je zo snel mogelijk terug.");
  wire(document.getElementById("appointmentForm"), "we bevestigen de afspraak persoonlijk.");

  // ?wijk=... voorinvullen op offerte
  var wijk = new URLSearchParams(location.search).get("wijk");
  if (wijk) {
    var ta = document.querySelector("#quoteForm textarea[name='message']");
    var naam = wijk.replace(/-/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    if (ta && !ta.value) ta.value = "Klus in " + naam + ":\n\n";
    var hid = document.createElement("input");
    hid.type = "hidden"; hid.name = "wijk"; hid.value = naam;
    var qf = document.getElementById("quoteForm"); if (qf) qf.appendChild(hid);
  }

  // Interactieve Groepenkast & Inductie Calculator
  function initCalculator() {
    var deviceInputs = document.querySelectorAll("input[name='calc_device']");
    var huidigInputs = document.querySelectorAll("input[name='calc_huidig']");
    var aansluitingInputs = document.querySelectorAll("input[name='calc_aansluiting']");
    var elGroepen = document.getElementById("calcGroepen");
    var elFase = document.getElementById("calcFase");
    var elTitel = document.getElementById("calcTitel");
    var elUitleg = document.getElementById("calcUitleg");
    var elPrijs = document.getElementById("calcPrijs");
    var P = { basis: 695, driefase: 120, kookgroep: 85, kracht: 185, pv: 95, groep: 45 };
    try { var sec = document.getElementById("keuzehulp"); if (sec && sec.dataset.prijzen) P = JSON.parse(sec.dataset.prijzen); } catch (e) {}
    var elOfferte = document.getElementById("calcOfferteBtn");
    var elWa = document.getElementById("calcWaBtn");
    var elBreakdown = document.getElementById("calcBreakdown");
    var elStedinBox = document.getElementById("calcStedinBox");

    if (!deviceInputs.length || !elGroepen) return;

    function bereken() {
      var groepen = 0;
      var hasLaadpaal = false;
      var hasWarmtepomp = false;
      var hasInductie = false;
      var hasPV = false;
      var hasQuooker = false;

      deviceInputs.forEach(function (inp) {
        if (inp.checked) {
          var val = inp.value;
          var g = parseInt(inp.getAttribute("data-groepen") || "1", 10);
          groepen += g;
          if (val === "laadpaal") hasLaadpaal = true;
          if (val === "warmtepomp") hasWarmtepomp = true;
          if (val === "inductie") hasInductie = true;
          if (val === "zonnepanelen") hasPV = true;
          if (val === "quooker") hasQuooker = true;
        }
      });

      // Minimum 4 basisgroepen
      if (groepen < 4) groepen = 4;

      var currentAansluiting = "1fase";
      aansluitingInputs.forEach(function (r) {
        if (r.checked) currentAansluiting = r.value;
      });

      // Fase advies bepalen
      var advise3Fase = false;
      if (currentAansluiting === "3fase") {
        advise3Fase = true;
      } else if (hasLaadpaal || hasWarmtepomp) {
        advise3Fase = true;
      } else if (hasInductie && groepen >= 7) {
        advise3Fase = true;
      } else if (groepen > 8) {
        advise3Fase = true;
      }

      // Prijsberekening en transparante specificatie
      var breakdownItems = [];
      var basisPrijs = P.basis; // 1-fase basiskast tot 8 groepen (prijs uit config.py)
      breakdownItems.push({ naam: "Basiskast 1-fase (tot 8 gr.)", prijs: "€ " + P.basis + ",-" });

      var extraKosten = 0;

      if (advise3Fase) {
        extraKosten += P.driefase;
        breakdownItems.push({ naam: "3-fase uitvoering & kamrail voorbereiding", prijs: "+ € " + P.driefase + ",-" });
      }

      if (hasInductie) {
        extraKosten += P.kookgroep;
        breakdownItems.push({ naam: "Inductie kookgroep (incl. kamrail & aansluiting)", prijs: "+ € " + P.kookgroep + ",-" });
      }

      if (hasLaadpaal) {
        var laadKosten = advise3Fase ? P.kracht : P.kookgroep;
        extraKosten += laadKosten;
        breakdownItems.push({ 
          naam: advise3Fase ? "Laadpaal (4P aardlekautomaat B16 + kracht kamrail)" : "Laadpaal (2P aardlekautomaat)", 
          prijs: "+ € " + laadKosten + ",-" 
        });
      }

      if (hasWarmtepomp) {
        var wpKosten = advise3Fase ? P.kracht : P.kookgroep;
        extraKosten += wpKosten;
        breakdownItems.push({ 
          naam: advise3Fase ? "Warmtepomp (4P aardlekautomaat + kracht kamrail)" : "Warmtepomp (2P aardlekautomaat)", 
          prijs: "+ € " + wpKosten + ",-" 
        });
      }

      if (hasPV) {
        extraKosten += P.pv;
        breakdownItems.push({ naam: "Zonnepanelen (PV-aardlekautomaat & afzekering)", prijs: "+ € " + P.pv + ",-" });
      }

      if (hasQuooker) {
        extraKosten += P.groep;
        breakdownItems.push({ naam: "Quooker/boiler (aparte groep + kamrail)", prijs: "+ € " + P.groep + ",-" });
      }

      var extraGroepenBovenAcht = Math.max(0, groepen - 8);
      if (extraGroepenBovenAcht > 0) {
        var extraGrKosten = extraGroepenBovenAcht * P.groep;
        extraKosten += extraGrKosten;
        breakdownItems.push({ 
          naam: extraGroepenBovenAcht + "x Extra groep (" + extraGroepenBovenAcht + "× € " + P.groep + ")", 
          prijs: "+ € " + extraGrKosten + ",-" 
        });
      }

      var totaalPrijs = basisPrijs + extraKosten;

      // Update UI
      elGroepen.textContent = groepen + " groepen";
      elFase.textContent = advise3Fase ? "3-fase (400V)" : "1-fase (230V)";

      if (advise3Fase) {
        elTitel.textContent = "Aanbevolen: 3-fase Hager of ABB Groepenkast";
        if (hasLaadpaal || hasWarmtepomp) {
          elUitleg.textContent = "Door zware verbruikers (zoals je laadpaal of warmtepomp) is een 3-fase aansluiting noodzakelijk om veilig en op vol vermogen te draaien.";
        } else if (hasInductie) {
          elUitleg.textContent = "Met koken op inductie en meerdere keukenapparaten biedt 3-fase een optimale verdeling over de fasen zonder dat de hoofdzekering overbelast raakt.";
        } else {
          elUitleg.textContent = "Bij meer dan 8 groepen adviseren we conform NEN 1010 een 3-fase verdeelkast voor een evenwichtige stroomverdeling over de woning.";
        }
      } else {
        elTitel.textContent = "Aanbevolen: 1-fase Hager of ABB Groepenkast";
        elUitleg.textContent = "Ideaal voor jouw appartement of standaard eengezinswoning met 2 aardlekschakelaars en NEN 1010 opleveringskeuring.";
      }

      // Stedin toelichting tonen of verbergen
      if (elStedinBox) {
        if (advise3Fase && currentAansluiting !== "3fase") {
          elStedinBox.style.display = "block";
        } else {
          elStedinBox.style.display = "none";
        }
      }

      // Prijsopbouw bijwerken
      if (elBreakdown) {
        var bHtml = "";
        breakdownItems.forEach(function (it) {
          bHtml += '<li class="calc-breakdown-item"><span>' + it.naam + '</span><span>' + it.prijs + '</span></li>';
        });
        elBreakdown.innerHTML = bHtml;
      }

      elPrijs.innerHTML = "€ " + totaalPrijs + ",- <span>all-in</span>";

      // Dynamische links
      var params = "?groepen=" + groepen + "&fase=" + (advise3Fase ? "3-fase" : "1-fase") + "&prijs=" + totaalPrijs;
      if (elOfferte) elOfferte.href = "/offerte/" + params;

      if (elWa) {
        var msg = "Hallo INO, via de online calculator kom ik uit op een " +
                  (advise3Fase ? "3-fase" : "1-fase") + " groepenkast met " + groepen +
                  " groepen (berekende all-in indicatie € " + totaalPrijs + "). " +
                  (advise3Fase && currentAansluiting !== "3fase" ? "Ik wil graag advies over Stedin verzwaring en het voorbereiden van de kast. " : "") +
                  "Hierbij stuur ik een foto van mijn huidige meterkast mee voor een bindende offerte.";
        elWa.href = "https://wa.me/31628763775?text=" + encodeURIComponent(msg);
      }
    }

    deviceInputs.forEach(function (inp) { 
      inp.addEventListener("change", bereken); 
      inp.addEventListener("input", bereken); 
      inp.addEventListener("click", bereken); 
    });
    huidigInputs.forEach(function (inp) { 
      inp.addEventListener("change", bereken); 
      inp.addEventListener("click", bereken); 
    });
    aansluitingInputs.forEach(function (inp) { 
      inp.addEventListener("change", bereken); 
      inp.addEventListener("click", bereken); 
    });
    bereken();
  }
  initCalculator();


  // Klik- en conversiemeting (bellen / WhatsApp / formulieren).
  // Werkt automatisch en naadloos met Google Analytics 4 (GA4) en Google Ads.
  function track(evt, params) {
    try {
      if (!window.inoGA4geladen) return; // geen toestemming = niets meten
      if (window.gtag) window.gtag("event", evt, params || {});
    } catch (e) {}
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    var isTel = href.indexOf("tel:") === 0 || a.getAttribute("data-track") === "bellen";
    var isWa = href.indexOf("wa.me") !== -1 || a.getAttribute("data-track") === "whatsapp";

    if (isTel) {
      track("klik_bellen", { pagina: location.pathname });
      track("contact", { method: "phone", pagina: location.pathname });
    } else if (isWa) {
      track("klik_whatsapp", { pagina: location.pathname });
      track("contact", { method: "whatsapp", pagina: location.pathname });
    }
  });

  // Slimme, pagina-specifieke WhatsApp links (voor-ingevulde berichten)
  function initSmartWhatsApp() {
    var p = (location.pathname || "").toLowerCase();
    var msg = "Hallo INO Techniek, ik heb een vraag over een elektra klus in Utrecht. Kan ik een foto sturen voor advies?";
    if (p.indexOf("extra-groep") !== -1) {
      msg = "Hallo INO, ik wil graag een extra groep laten plaatsen in mijn meterkast in Utrecht. Hierbij stuur ik een foto van mijn huidige kast mee.";
    } else if (p.indexOf("groepenkast") !== -1) {
      msg = "Hallo INO, ik wil graag advies of een offerte voor het vervangen/uitbreiden van mijn groepenkast. Hierbij stuur ik een foto van mijn huidige meterkast mee.";
    } else if (p.indexOf("perilex") !== -1) {
      msg = "Hallo INO, ik wil een inductiekookplaat of Perilex aansluiting laten aanleggen. Hierbij een foto van mijn situatie.";
    } else if (p.indexOf("laadpaal") !== -1) {
      msg = "Hallo INO, ik wil graag een laadpaal laten installeren aan huis. Wat zijn de mogelijkheden en kosten?";
    } else if (p.indexOf("thuisbatterij") !== -1) {
      msg = "Hallo INO, ik wil graag advies of een offerte voor het aansluiten van een thuisbatterij. Hierbij stuur ik een foto van mijn meterkast mee.";
    } else if (p.indexOf("krachtstroom") !== -1) {
      msg = "Hallo INO, ik heb krachtstroom (3-fase) nodig in mijn woning of bedrijfspand. Graag ontvang ik advies en een richtprijs.";
    } else if (p.indexOf("spoed") !== -1 || p.indexOf("storing") !== -1 || p.indexOf("kortsluiting") !== -1 || p.indexOf("aardlek") !== -1) {
      msg = "Hallo INO, ik heb met spoed een elektricien nodig in Utrecht in verband met een storing. Hierbij een foto van de meterkast.";
    } else if (p.indexOf("frezen") !== -1 || p.indexOf("stopcontact") !== -1) {
      msg = "Hallo INO, ik wil graag stopcontacten laten verplaatsen/infrezen. Kan ik foto's sturen voor een richtprijs?";
    } else if (p.indexOf("tuinverlichting") !== -1) {
      msg = "Hallo INO, ik wil graag tuinverlichting of buitenelektra laten aanleggen. Wat zijn de mogelijkheden?";
    } else if (p.indexOf("tarieven") !== -1) {
      msg = "Hallo INO, ik heb gekeken naar jullie transparante tarieven en wil graag een indicatie voor mijn klus. Hierbij een foto.";
    } else if (p.indexOf("elektricien-") !== -1) {
      var h1 = document.querySelector("h1");
      var title = h1 ? h1.textContent.trim() : "de regio Utrecht";
      msg = "Hallo INO Techniek, ik zoek een betrouwbare elektricien voor een klus (" + title + "). Hierbij stuur ik foto's van de situatie mee.";
    }

    var waHref = "https://wa.me/31628763775?text=" + encodeURIComponent(msg);

    // Update floating WhatsApp widget en mobiele WhatsApp-knop
    var floatingBtn = document.getElementById("floatingWa");
    if (floatingBtn) floatingBtn.href = waHref;

    document.querySelectorAll(".mobile-btn-whatsapp, .m-btn-whatsapp").forEach(function (btn) {
      btn.href = waHref;
    });
  }
  initSmartWhatsApp();
  // Cookiemelding: Google Analytics alleen na akkoord (AVG / Telecommunicatiewet).
  function initCookies() {
    if (typeof window.inoGA4 !== "function") return;
    var KEY = "ino_cookies", KEY_DATUM = "ino_cookies_datum", GELDIG_DAGEN = 365;
    function lees() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
    function datum() { try { return parseInt(localStorage.getItem(KEY_DATUM) || "0", 10); } catch (e) { return 0; } }
    function bewaar(v) { try { localStorage.setItem(KEY, v); localStorage.setItem(KEY_DATUM, String(Date.now())); } catch (e) {} }
    var box, stat, details, vorigeFocus;
    function sluit() { box.hidden = true; if (vorigeFocus && vorigeFocus !== document.body && vorigeFocus.focus) vorigeFocus.focus({ preventScroll: true }); }
    function kies(v) {
      var oud = lees();
      bewaar(v);
      sluit();
      if (v === "ja") { var h = location.hostname || ""; if (h.indexOf("ino-elektra.nl") !== -1 && typeof window.inoGA4 === "function") window.inoGA4(); }
      else if (oud === "ja") location.reload(); // intrekken: pagina zonder GA opnieuw laden
    }
    function bouw() {
      box = document.createElement("div");
      box.className = "consent";
      box.setAttribute("role", "dialog");
      box.setAttribute("aria-modal", "false");
      box.setAttribute("aria-labelledby", "consentTitel");
      box.setAttribute("aria-describedby", "consentTekst");
      box.innerHTML =
        '<div class="consent-kop"><span class="consent-icoon" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg></span>' +
        '<h2 id="consentTitel">Jouw privacy</h2></div>' +
        '<p id="consentTekst">We gebruiken alleen wat nodig is om de site te laten werken. Met jouw toestemming meten we ook hoe de site gebruikt wordt, zodat we hem kunnen verbeteren. Geen advertenties, geen verkoop van gegevens. <a href="/privacy/">Privacyverklaring</a></p>' +
        '<div class="consent-details" hidden>' +
          '<div class="consent-rij"><div><strong>Noodzakelijk</strong><span>Onthoudt je cookiekeuze en beschermt formulieren tegen spam. Altijd aan.</span></div>' +
            '<label class="consent-schakel is-vast"><input type="checkbox" checked disabled><span class="consent-slider" aria-hidden="true"></span><span class="sr-only">Noodzakelijk, altijd aan</span></label></div>' +
          '<div class="consent-rij"><div><strong>Statistieken</strong><span>Google Analytics: welke pagina’s bekeken worden. Geanonimiseerd, niet voor advertenties.</span></div>' +
            '<label class="consent-schakel"><input type="checkbox" data-consent-stat><span class="consent-slider" aria-hidden="true"></span><span class="sr-only">Statistieken toestaan</span></label></div>' +
        '</div>' +
        '<div class="consent-knoppen">' +
          '<button type="button" class="consent-btn consent-btn-link" data-consent="voorkeuren" aria-expanded="false">Voorkeuren</button>' +
          '<button type="button" class="consent-btn consent-btn-link" data-consent="opslaan" hidden>Keuze opslaan</button>' +
          '<button type="button" class="consent-btn consent-btn-sec" data-consent="nee">Alleen noodzakelijk</button>' +
          '<button type="button" class="consent-btn consent-btn-pri" data-consent="ja">Alles accepteren</button>' +
        '</div>';
      stat = box.querySelector("[data-consent-stat]");
      details = box.querySelector(".consent-details");
      box.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest("[data-consent]");
        if (!b) return;
        var actie = b.getAttribute("data-consent");
        if (actie === "voorkeuren") { toonDetails(true); stat.focus(); return; }
        if (actie === "opslaan") { kies(stat.checked ? "ja" : "nee"); return; }
        kies(actie);
      });
      document.body.appendChild(box);
    }
    function toonDetails(aan) {
      details.hidden = !aan;
      box.classList.toggle("is-open", aan);
      box.querySelector('[data-consent="voorkeuren"]').hidden = aan;
      box.querySelector('[data-consent="voorkeuren"]').setAttribute("aria-expanded", aan ? "true" : "false");
      box.querySelector('[data-consent="opslaan"]').hidden = !aan;
    }
    function toon(metDetails, focus) {
      vorigeFocus = document.activeElement;
      if (!box) bouw();
      stat.checked = lees() === "ja";
      toonDetails(!!metDetails);
      box.hidden = false;
      var eerste = box.querySelector(metDetails ? "[data-consent-stat]" : '[data-consent="ja"]');
      if (focus && eerste) setTimeout(function () { eerste.focus({ preventScroll: true }); }, 50);
    }
    var keuze = lees();
    var verlopen = keuze && datum() && (Date.now() - datum() > GELDIG_DAGEN * 864e5);
    if (!keuze || verlopen) toon(false);
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("[data-cookie-instellingen]");
      if (a) { e.preventDefault(); toon(true, true); }
    });
  }
  initCookies();
})();


/* Live Google-score: de vaste score staat al in de HTML; dit werkt hem bij via onze
   eigen Worker (geen Google-scripts, geen cookies). Op /reviews/ ook de nieuwste reviews. */
(function () {
  try {
    var url = "__REVIEWS_ENDPOINT__";
    if (!url || url === "" || !window.fetch || !document.querySelector("[data-g]")) return;
    function maak(tag, cls, tekst) { var e = document.createElement(tag); if (cls) e.className = cls; if (tekst != null) e.textContent = tekst; return e; }
    function kaarten(d) {
      var track = document.getElementById("reviewsTrack");
      if (!track || !d.reviews || !d.reviews.length) return;
      var badge = track.querySelector(".review-google-badge"), ster = track.querySelector(".review-stars-wrap svg");
      var oud = track.querySelectorAll("article.review-slide-card"), plek = track.querySelector(".review-slide-more");
      for (var i = 0; i < oud.length; i++) oud[i].remove();
      d.reviews.forEach(function (r) {
        var a = maak("article", "review-slide-card"), top = maak("div", "review-card-top"), wrap = maak("div", "review-author-wrap");
        var init = r.naam.split(/\s+/).slice(0, 2).map(function (w) { return w.charAt(0); }).join("").toUpperCase();
        var av = maak("div", "review-avatar", init); av.setAttribute("aria-hidden", "true");
        var info = maak("div"); info.appendChild(maak("strong", "review-author-name", r.naam));
        info.appendChild(maak("span", "review-author-meta", "Google-review" + (r.wanneer ? " · " + r.wanneer : "")));
        wrap.appendChild(av); wrap.appendChild(info); top.appendChild(wrap);
        if (badge) top.appendChild(badge.cloneNode(true));
        var rij = maak("div", "review-rating-row"), st = maak("span", "review-stars-wrap");
        st.setAttribute("role", "img"); st.setAttribute("aria-label", r.sterren + " van 5 sterren");
        for (var s = 0; s < r.sterren && ster; s++) st.appendChild(ster.cloneNode(true));
        rij.appendChild(st);
        a.appendChild(top); a.appendChild(rij); a.appendChild(maak("p", "review-card-text", "“" + r.tekst + "”"));
        track.insertBefore(a, plek);
      });
    }
    function zet(d) {
      var nl = function (n, dec) { return Number(n).toLocaleString("nl-NL", { minimumFractionDigits: dec, maximumFractionDigits: dec }); };
      document.querySelectorAll("[data-g]").forEach(function (e) {
        var k = e.getAttribute("data-g");
        if (k === "score" && d.score) e.textContent = nl(d.score, 1);
        if (k === "aantal" && d.aantal) e.textContent = nl(d.aantal, 0);
      });
      kaarten(d);
    }
    var bewaard = null;
    try { bewaard = JSON.parse(sessionStorage.getItem("inoReviews") || "null"); } catch (e) {}
    if (bewaard && bewaard.t > Date.now() - 36e5) { zet(bewaard.d); return; }
    fetch(url, { mode: "cors", credentials: "omit", headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || !d.ok) return;
        zet(d);
        try { sessionStorage.setItem("inoReviews", JSON.stringify({ t: Date.now(), d: d })); } catch (e) {}
      })
      .catch(function () {});
  } catch (err) {}
})();
