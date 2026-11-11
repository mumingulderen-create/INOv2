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
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
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
    list.textContent = f.length ? f.length + " file(s): " + f.map(function (x) { return x.name; }).join(", ") : "";
  });

  var d = document.getElementById("date");
  if (d) d.min = new Date().toISOString().split("T")[0];

  function esc(v) { return String(v).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[c]; }); }

  // Formulieren → eigen beveiligd endpoint (Cloudflare Worker, zie worker/).
  // Honeypot + Turnstile tegen spam; de server controleert alles opnieuw.
  var VELDNAMEN = { name: "name", phone: "phone number", email: "email address", message: "description", postcode: "postcode",
    number: "house number", datum: "date", tijd: "time", akkoord: "consent", photos: "photos" };
  function wire(form, okMsg) {
    if (!form) return;
    if (!form.querySelector('[name="_honey"]')) {
      var hp = document.createElement("input");
      hp.type = "text"; hp.name = "_honey"; hp.tabIndex = -1; hp.autocomplete = "off"; hp.className = "hp"; hp.setAttribute("aria-hidden", "true");
      form.appendChild(hp);
    }
    var submit = form.querySelector("button[type='submit']");
    var label = submit ? submit.innerHTML : "Send";
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
      var fout = "<strong>Something went wrong while sending your request.</strong><br>Please try again or call us directly on <a href=\"tel:+31628763775\">06 28 76 37 75</a>.";
      if (!"https://api.ino-elektra.nl/api/form" || !hulp || !hulp.actief) { toon(result, "form-result form-result-error", fout); return; }
      bezig = true;
      if (submit) { submit.disabled = true; submit.textContent = "Sending…"; }
      var fotoVeld = form.querySelector("input[type='file'][name='photos']");
      (fotoVeld && fotoVeld.files.length ? hulp.fotos(fotoVeld.files) : Promise.resolve([]))
        .then(function (fotos) {
          data.delete("photos");
          fotos.forEach(function (f, i) { data.append("photos", f, f.name || "foto-" + (i + 1) + ".jpg"); });
          return hulp.token(form);
        }, function (err) { throw { bericht: err.message, veld: "photos" }; })
        .then(function (t) {
          if (!t) throw { bericht: "The security check is not ready yet. Please wait a moment and try again." };
          data.set("cf-turnstile-response", t);
          data.set("formulier", form.getAttribute("data-formulier")); data.set("taal", "en");
          return fetch("https://api.ino-elektra.nl/api/form", { method: "POST", body: data, mode: "cors", credentials: "omit", headers: { Accept: "application/json" } });
        })
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (j) {
            if (r.ok && j.ok) return j;
            if (r.status === 422 && j.velden) {
              var namen = Object.keys(j.velden);
              namen.forEach(function (n) { var el = form.querySelector("[name='" + n + "']"); if (el) el.setAttribute("aria-invalid", "true"); });
              throw { bericht: "Please check the details you entered and try again:<br>" + namen.map(function (n) { return esc((VELDNAMEN[n] || n) + " – " + j.velden[n]); }).join("<br>"), veld: namen[0] };
            }
            if (r.status === 429) throw { bericht: "You have just sent something. Please wait a minute or call us directly on <a href=\"tel:+31628763775\">06 28 76 37 75</a>." };
            if (r.status === 403) throw { bericht: "We could not verify your request. Please try again or call us on <a href=\"tel:+31628763775\">06 28 76 37 75</a>." };
            if (r.status === 413) throw { bericht: "The photos are too large. Please send fewer or smaller photos.", veld: "photos" };
            throw {};
          });
        })
        .then(function () {
          track("formulier_verstuurd", { formulier: form.id || "form" });
          track("generate_lead", { formulier: form.id || "form", currency: "EUR" });
          if (window.inoAds) track("conversion", { send_to: window.inoAds });
          toon(result, "form-result", "<strong>Your request has been sent.</strong><br>Thank you " + esc(data.get("name") || "") + ", " + okMsg);
          form.reset();
          if (list) list.textContent = "";
        })
        .catch(function (err) {
          toon(result, "form-result form-result-error", err && err.bericht ? "<strong>Your request has not been sent.</strong><br>" + err.bericht : fout);
        })
        .finally(function () {
          bezig = false;
          hulp.reset(form); // Turnstile-token is eenmalig; nieuw token voor een volgende poging
          if (submit) { submit.disabled = false; submit.innerHTML = label; }
        });
    });
  }
  wire(document.getElementById("quoteForm"), "we will contact you as soon as possible. You will also receive a confirmation by email.");
  wire(document.getElementById("spoedForm"), "we will call you back as soon as possible.");
  wire(document.getElementById("appointmentForm"), "we will confirm the appointment personally.");

  // ?wijk=... voorinvullen op offerte
  var wijk = new URLSearchParams(location.search).get("wijk");
  if (wijk) {
    var ta = document.querySelector("#quoteForm textarea[name='message']");
    var naam = wijk.replace(/-/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    if (ta && !ta.value) ta.value = "Job in " + naam + ":\n\n";
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
      breakdownItems.push({ naam: "Single-phase base unit (up to 8 circuits)", prijs: "€ " + P.basis + "" });

      var extraKosten = 0;

      if (advise3Fase) {
        extraKosten += P.driefase;
        breakdownItems.push({ naam: "Three-phase version & busbar preparation", prijs: "+ € " + P.driefase + "" });
      }

      if (hasInductie) {
        extraKosten += P.kookgroep;
        breakdownItems.push({ naam: "Induction cooking circuit (incl. busbar & connection)", prijs: "+ € " + P.kookgroep + "" });
      }

      if (hasLaadpaal) {
        var laadKosten = advise3Fase ? P.kracht : P.kookgroep;
        extraKosten += laadKosten;
        breakdownItems.push({ 
          naam: advise3Fase ? "EV charger (4P RCBO B16 + three-phase busbar)" : "EV charger (2P RCBO)", 
          prijs: "+ € " + laadKosten + "" 
        });
      }

      if (hasWarmtepomp) {
        var wpKosten = advise3Fase ? P.kracht : P.kookgroep;
        extraKosten += wpKosten;
        breakdownItems.push({ 
          naam: advise3Fase ? "Heat pump (4P RCBO + three-phase busbar)" : "Heat pump (2P RCBO)", 
          prijs: "+ € " + wpKosten + "" 
        });
      }

      if (hasPV) {
        extraKosten += P.pv;
        breakdownItems.push({ naam: "Solar panels (PV RCBO & protection)", prijs: "+ € " + P.pv + "" });
      }

      if (hasQuooker) {
        extraKosten += P.groep;
        breakdownItems.push({ naam: "Quooker/water heater (separate circuit + busbar)", prijs: "+ € " + P.groep + "" });
      }

      var extraGroepenBovenAcht = Math.max(0, groepen - 8);
      if (extraGroepenBovenAcht > 0) {
        var extraGrKosten = extraGroepenBovenAcht * P.groep;
        extraKosten += extraGrKosten;
        breakdownItems.push({ 
          naam: extraGroepenBovenAcht + "x extra circuit (" + extraGroepenBovenAcht + "× € " + P.groep + ")", 
          prijs: "+ € " + extraGrKosten + "" 
        });
      }

      var totaalPrijs = basisPrijs + extraKosten;

      // Update UI
      elGroepen.textContent = groepen + " circuits";
      elFase.textContent = advise3Fase ? "Three-phase (400V)" : "Single-phase (230V)";

      if (advise3Fase) {
        elTitel.textContent = "Recommended: three-phase Hager or ABB fuse box";
        if (hasLaadpaal || hasWarmtepomp) {
          elUitleg.textContent = "Heavy appliances (such as your EV charger or heat pump) need a three-phase connection to run safely at full power.";
        } else if (hasInductie) {
          elUitleg.textContent = "With induction cooking and several kitchen appliances, three-phase spreads the load across the phases without overloading the main fuse.";
        } else {
          elUitleg.textContent = "With more than 8 circuits we recommend a three-phase board in line with NEN 1010, for an even load across the home.";
        }
      } else {
        elTitel.textContent = "Recommended: single-phase Hager or ABB fuse box";
        elUitleg.textContent = "Ideal for your flat or standard family home, with 2 RCDs and a NEN 1010 completion test.";
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

      elPrijs.innerHTML = "€ " + totaalPrijs + " <span>all-in</span>";

      // Dynamische links
      var params = "?groepen=" + groepen + "&fase=" + (advise3Fase ? "3-fase" : "1-fase") + "&prijs=" + totaalPrijs;
      if (elOfferte) elOfferte.href = "/en/quote/" + params;

      if (elWa) {
        var msg = "Hello INO, the online calculator suggests a " +
                  (advise3Fase ? "three-phase" : "single-phase") + " fuse box with " + groepen +
                  " circuits (calculated all-in estimate € " + totaalPrijs + "). " +
                  (advise3Fase && currentAansluiting !== "3fase" ? "I would like advice on the Stedin upgrade and preparing the fuse box. " : "") +
                  "I am sending a photo of my current meter cupboard for a binding quote.";
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
      if (window.inoAds) track("conversion", { send_to: window.inoAds });
    } else if (isWa) {
      track("klik_whatsapp", { pagina: location.pathname });
      track("contact", { method: "whatsapp", pagina: location.pathname });
    }
  });

  // Slimme, pagina-specifieke WhatsApp links (voor-ingevulde berichten)
  function initSmartWhatsApp() {
    var p = (location.pathname || "").toLowerCase();
    var msg = "Hello INO Techniek, I have a question about an electrical job in Utrecht. Can I send a photo for advice?";
    if (p.indexOf("extra-circuit") !== -1) {
      msg = "Hello INO, I would like an extra circuit added to my fuse box in Utrecht. Here is a photo of my current fuse box.";
    } else if (p.indexOf("fuse-box") !== -1) {
      msg = "Hello INO, I would like advice or a quote for replacing/extending my fuse box. Here is a photo of my current meter cupboard.";
    } else if (p.indexOf("perilex") !== -1) {
      msg = "Hello INO, I would like an induction hob or Perilex connection installed. Here is a photo of my situation.";
    } else if (p.indexOf("ev-charger") !== -1) {
      msg = "Hello INO, I would like an EV charger installed at home. What are the options and costs?";
    } else if (p.indexOf("home-battery") !== -1) {
      msg = "Hello INO, I would like advice or a quote for connecting a home battery. Here is a photo of my meter cupboard.";
    } else if (p.indexOf("three-phase") !== -1) {
      msg = "Hello INO, I need three-phase power in my home or business premises. I would like advice and a price estimate.";
    } else if (p.indexOf("emergency") !== -1 || p.indexOf("outage") !== -1 || p.indexOf("short-circuit") !== -1 || p.indexOf("rcd") !== -1) {
      msg = "Hello INO, I urgently need an electrician in Utrecht because of a power fault. Here is a photo of the meter cupboard.";
    } else if (p.indexOf("sockets") !== -1 || p.indexOf("socket") !== -1) {
      msg = "Hello INO, I would like sockets moved or recessed into the wall. Can I send photos for a price estimate?";
    } else if (p.indexOf("garden") !== -1) {
      msg = "Hello INO, I would like garden lighting or outdoor electrics installed. What are the options?";
    } else if (p.indexOf("prices") !== -1) {
      msg = "Hello INO, I have looked at your prices and would like an estimate for my job. Here is a photo.";
    } else if (p.indexOf("electrician-") !== -1) {
      var h1 = document.querySelector("h1");
      var title = h1 ? h1.textContent.trim() : "the Utrecht region";
      msg = "Hello INO Techniek, I am looking for a reliable electrician for a job (" + title + "). I am sending photos of the situation.";
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
        '<h2 id="consentTitel">Your privacy</h2></div>' +
        '<p id="consentTekst">We only use what is needed to make the site work. With your consent we also measure how the site is used, so we can improve it. No advertising, no selling of data. <a href="/en/privacy/">Privacy statement</a></p>' +
        '<div class="consent-details" hidden>' +
          '<div class="consent-rij"><div><strong>Necessary</strong><span>Remembers your cookie choice and protects forms against spam. Always on.</span></div>' +
            '<label class="consent-schakel is-vast"><input type="checkbox" checked disabled><span class="consent-slider" aria-hidden="true"></span><span class="sr-only">Necessary, always on</span></label></div>' +
          '<div class="consent-rij"><div><strong>Statistics and ad measurement</strong><span>Google Analytics: which pages are viewed. Google Ads: whether an advert leads to a call or request.</span></div>' +
            '<label class="consent-schakel"><input type="checkbox" data-consent-stat><span class="consent-slider" aria-hidden="true"></span><span class="sr-only">Allow statistics</span></label></div>' +
        '</div>' +
        '<div class="consent-knoppen">' +
          '<button type="button" class="consent-btn consent-btn-link" data-consent="voorkeuren" aria-expanded="false">Preferences</button>' +
          '<button type="button" class="consent-btn consent-btn-link" data-consent="opslaan" hidden>Save choice</button>' +
          '<button type="button" class="consent-btn consent-btn-sec" data-consent="nee">Necessary only</button>' +
          '<button type="button" class="consent-btn consent-btn-pri" data-consent="ja">Accept all</button>' +
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
    var url = "https://api.ino-elektra.nl/api/reviews";
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
        info.appendChild(maak("span", "review-author-meta", "Google review" + (r.wanneer ? " · " + r.wanneer : "")));
        wrap.appendChild(av); wrap.appendChild(info); top.appendChild(wrap);
        if (badge) top.appendChild(badge.cloneNode(true));
        var rij = maak("div", "review-rating-row"), st = maak("span", "review-stars-wrap");
        st.setAttribute("role", "img"); st.setAttribute("aria-label", r.sterren + " out of 5 stars");
        for (var s = 0; s < r.sterren && ster; s++) st.appendChild(ster.cloneNode(true));
        rij.appendChild(st);
        a.appendChild(top); a.appendChild(rij); a.appendChild(maak("p", "review-card-text", "“" + r.tekst + "”"));
        track.insertBefore(a, plek);
      });
    }
    function zet(d) {
      var nl = function (n, dec) { return Number(n).toLocaleString("en-GB", { minimumFractionDigits: dec, maximumFractionDigits: dec }); };
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

/* Themaknop: wisselt licht/donker en onthoudt de keuze; zonder keuze volgt de site het toestel. */
(function () {
  var k = document.querySelector("[data-thema]"), l = document.getElementById("donkerCss");
  if (!k || !l) return;
  k.addEventListener("click", function () {
    var donker = l.media === "all" || (l.media !== "not all" && window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches);
    l.media = donker ? "not all" : "all";
    try { localStorage.setItem("ino_thema", donker ? "licht" : "donker"); } catch (e) {}
  });
})();
