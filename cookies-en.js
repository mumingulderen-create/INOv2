/* INO Elektra – cookiemelding.
   Laadt alleen als er nog geen geldige keuze is, of na een klik op "Cookie-instellingen" (initCookies in assets/script.js).
   Twee aparte keuzes, nooit vooraf aangevinkt: statistieken (Google Analytics) en advertentiemeting (Google Ads).
   Opslaan, verlopen na 365 dagen, Consent Mode v2 en het laden van Google: bouw/layout.py (window.inoKeuze / window.inoGA4). */
(function () {
  "use strict";
  var K = "ino_cookies", KD = "ino_cookies_datum";
  var box, stat, ads, details, vorigeFocus;

  function bewaar(k) {
    try {
      localStorage.setItem(K, JSON.stringify({ stat: !!k.stat, ads: !!k.ads }));
      localStorage.setItem(KD, String(Date.now()));
    } catch (e) {}
  }

  // Eerder geplaatste Google-cookies weghalen, op dit domein en op het hoofddomein (.ino-elektra.nl).
  function wisCookies(begin) {
    try {
      var h = location.hostname || "", delen = h.split("."), domeinen = ["", h, "." + h];
      if (delen.length > 2) { var hoofd = delen.slice(-2).join("."); domeinen.push(hoofd, "." + hoofd); }
      (document.cookie || "").split(";").forEach(function (c) {
        var naam = c.split("=")[0].trim();
        if (!naam || !begin.some(function (b) { return naam.indexOf(b) === 0; })) return;
        domeinen.forEach(function (d) {
          document.cookie = naam + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + (d ? "; domain=" + d : "");
        });
      });
    } catch (e) {}
  }

  function kies(k) {
    var oud = window.inoKeuze() || { stat: false, ads: false };
    k = { stat: !!k.stat, ads: !!k.ads };
    bewaar(k);
    sluit();
    // Uitgezet = meteen stoppen met meten en cookies weghalen.
    if (!k.stat) { window.inoStat = false; wisCookies(["_ga"]); }
    if (!k.ads) { window.inoAds = ""; wisCookies(["_gcl_"]); }
    var h = location.hostname || "";
    if (h === "ino-elektra.nl" || h === "www.ino-elektra.nl") window.inoGA4(k); // Consent Mode-update en zo nodig Google laden
    // Google-script al geladen en iets ingetrokken: opnieuw laden zonder dat script.
    if (window.inoGA4geladen && ((oud.stat && !k.stat) || (oud.ads && !k.ads))) location.reload();
  }

  function rij(titel, uitleg, invoer, label) {
    return '<div class="consent-rij"><div><strong>' + titel + '</strong><span>' + uitleg + '</span></div>' +
      '<label class="consent-schakel' + (invoer ? '' : ' is-vast') + '"><input type="checkbox" ' + (invoer || 'checked disabled') + '>' +
      '<span class="consent-slider" aria-hidden="true"></span><span class="sr-only">' + label + '</span></label></div>';
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
      '<p id="consentTekst">We only use what is needed to make the site work. With your consent we also use Google Analytics (statistics) and Google Ads (measuring whether an advert leads to a call, WhatsApp message or request). Under Preferences you choose them separately. No personalised advertising, no selling of data. <a href="/en/privacy/">Privacy statement</a></p>' +
      '<div class="consent-details" hidden>' +
        rij("Necessary", "Remembers your cookie choice and display mode and protects forms against spam. Always on.", "", "Necessary, always on") +
        rij("Statistics (Google Analytics)", "Which pages are viewed and how often call, WhatsApp or form buttons are used.", "data-consent-stat", "Allow statistics") +
        rij("Ad measurement (Google Ads)", "Whether a click on our Google advert leads to a call, WhatsApp message or request. For this, Google receives data about your visit and the ad click. No personalised advertising.", "data-consent-ads", "Allow ad measurement") +
      '</div>' +
      '<div class="consent-knoppen">' +
        '<button type="button" class="consent-btn consent-btn-link" data-consent="voorkeuren" aria-expanded="false">Preferences</button>' +
        '<button type="button" class="consent-btn consent-btn-link" data-consent="opslaan" hidden>Save choice</button>' +
        '<button type="button" class="consent-btn consent-btn-sec" data-consent="nee">Necessary only</button>' +
        '<button type="button" class="consent-btn consent-btn-pri" data-consent="ja">Accept all</button>' +
      '</div>';
    stat = box.querySelector("[data-consent-stat]");
    ads = box.querySelector("[data-consent-ads]");
    details = box.querySelector(".consent-details");
    box.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-consent]");
      if (!b) return;
      var actie = b.getAttribute("data-consent");
      if (actie === "voorkeuren") { toonDetails(true); stat.focus(); }
      else if (actie === "opslaan") kies({ stat: stat.checked, ads: ads.checked });
      else kies({ stat: actie === "ja", ads: actie === "ja" });
    });
    document.body.appendChild(box);
  }

  function toonDetails(aan) {
    var v = box.querySelector('[data-consent="voorkeuren"]');
    details.hidden = !aan;
    box.classList.toggle("is-open", aan);
    v.hidden = aan;
    v.setAttribute("aria-expanded", aan ? "true" : "false");
    box.querySelector('[data-consent="opslaan"]').hidden = !aan;
  }

  function sluit() {
    box.hidden = true;
    if (vorigeFocus && vorigeFocus !== document.body && vorigeFocus.focus) vorigeFocus.focus({ preventScroll: true });
  }

  function toon(metDetails, focus) {
    vorigeFocus = document.activeElement;
    if (!box) bouw();
    var k = window.inoKeuze() || { stat: false, ads: false };
    stat.checked = k.stat;
    ads.checked = k.ads;
    toonDetails(!!metDetails);
    box.hidden = false;
    var eerste = box.querySelector(metDetails ? "[data-consent-stat]" : '[data-consent="nee"]');
    if (focus && eerste) setTimeout(function () { eerste.focus({ preventScroll: true }); }, 50);
  }

  window.inoCookieMelding = toon;
})();
