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

  // Formulieren via FormSubmit (AJAX) met honeypot tegen spam
  function wire(form, okMsg) {
    if (!form) return;
    if (!form.querySelector('[name="_honey"]')) {
      var hp = document.createElement("input");
      hp.type = "text"; hp.name = "_honey"; hp.tabIndex = -1; hp.autocomplete = "off"; hp.className = "hp"; hp.setAttribute("aria-hidden", "true");
      form.appendChild(hp);
    }
    var submit = form.querySelector("button[type='submit']");
    var label = submit ? submit.textContent : "Versturen";
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      if (data.get("_honey")) return;
      var result = form.querySelector(".form-result") || document.getElementById("formResult");
      if (submit) { submit.disabled = true; submit.textContent = "Versturen…"; }
      fetch("https://formsubmit.co/ajax/d0d9de6bb2a30083d92c3fe4775b9ce6", { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error(); return r.json(); })
        .then(function () {
          track("formulier_verstuurd", { formulier: form.id || "form" });
          if (result) {
            result.hidden = false; result.className = "form-result";
            result.innerHTML = "<strong>Aanvraag verstuurd.</strong><br>Bedankt " + esc(data.get("name") || "") + ", " + okMsg;
            result.scrollIntoView({ behavior: "smooth", block: "center" });
          } else { alert("Verstuurd. " + okMsg); }
          form.reset();
          if (list) list.textContent = "";
        })
        .catch(function () {
          var msg = "<strong>Versturen lukte niet.</strong><br>Bel ons direct op <a href=\"tel:+31628763775\">06 28 76 37 75</a> of probeer het opnieuw.";
          if (result) { result.hidden = false; result.className = "form-result form-result-error"; result.innerHTML = msg; }
          else alert("Versturen lukte niet. Bel ons op 06 28 76 37 75.");
        })
        .finally(function () { if (submit) { submit.disabled = false; submit.textContent = label; } });
    });
  }
  wire(document.getElementById("quoteForm"), "we nemen zo snel mogelijk contact met je op.");
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

  // Klik-meting (bellen / WhatsApp). Werkt automatisch zodra je Google Analytics 4
  // of Google Tag Manager toevoegt; zonder die tools doet dit niets.
  function track(evt, params) {
    try {
      if (window.gtag) window.gtag("event", evt, params || {});
      (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: evt }, params || {}));
    } catch (e) {}
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-track]");
    if (a) track(a.getAttribute("data-track") === "bellen" ? "klik_bellen" : "klik_whatsapp", { pagina: location.pathname });
  });
})();
