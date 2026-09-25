/* INO – formulieren: Cloudflare Turnstile (botbescherming) en foto's verkleinen.
   Laadt alleen op pagina's met een formulier (front-matter "extra": ["formulier"]).
   script.js (wire) gebruikt window.inoFormulier bij het versturen. */
(function () {
  "use strict";
  var SITEKEY = "";
  var widgets = {}; // form.id -> widgetId

  function renderAlles() {
    document.querySelectorAll("form[data-formulier] .form-turnstile").forEach(function (el) {
      var form = el.closest("form");
      if (!form || widgets[form.id] !== undefined) return;
      widgets[form.id] = window.turnstile.render(el, {
        sitekey: SITEKEY,
        action: form.getAttribute("data-formulier"),
        appearance: "interaction-only",
        language: "nl",
        "refresh-expired": "auto",
      });
    });
  }

  if (SITEKEY && document.querySelector("form[data-formulier]")) {
    window.inoTurnstileKlaar = renderAlles;
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=inoTurnstileKlaar";
    s.async = true; s.defer = true;
    document.head.appendChild(s);
  }

  // Wacht maximaal ~15 s op een token (meestal is het er al bij het laden).
  function token(form) {
    return new Promise(function (resolve) {
      var tries = 0;
      (function poll() {
        var id = widgets[form.id];
        var t = window.turnstile && id !== undefined ? window.turnstile.getResponse(id) : "";
        if (t || tries++ > 60) return resolve(t || "");
        setTimeout(poll, 250);
      })();
    });
  }

  function reset(form) {
    var id = widgets[form.id];
    try { if (window.turnstile && id !== undefined) window.turnstile.reset(id); } catch (e) {}
  }

  // Foto's verkleinen naar max. 2000 px JPEG. Dit haalt ook EXIF/GPS-gegevens
  // weg en houdt de upload klein. Lukt dat niet (oud toestel), dan gaat het
  // origineel mee als het een JPG of PNG is; de server controleert alles opnieuw.
  var MAX_PX = 2000, MAX_FOTOS = 5, MAX_ORIGINEEL = 15 * 1024 * 1024;
  function verklein(file, n) {
    if (!window.createImageBitmap) return Promise.reject();
    return createImageBitmap(file, { imageOrientation: "from-image" }).then(function (bmp) {
      var f = Math.min(1, MAX_PX / Math.max(bmp.width, bmp.height));
      var c = document.createElement("canvas");
      c.width = Math.round(bmp.width * f); c.height = Math.round(bmp.height * f);
      c.getContext("2d").drawImage(bmp, 0, 0, c.width, c.height);
      if (bmp.close) bmp.close();
      return new Promise(function (resolve, reject) {
        c.toBlob(function (b) { b ? resolve(new File([b], "foto-" + n + ".jpg", { type: "image/jpeg" })) : reject(); }, "image/jpeg", 0.82);
      });
    });
  }
  function fotos(lijst) {
    var files = Array.prototype.slice.call(lijst || []).filter(function (f) { return f && f.size > 0; });
    if (files.length > MAX_FOTOS) return Promise.reject(new Error("Je kunt maximaal " + MAX_FOTOS + " foto's meesturen."));
    return Promise.all(files.map(function (f, i) {
      if (f.size > MAX_ORIGINEEL) return Promise.reject(new Error("Een foto is te groot (max. 15 MB)."));
      return verklein(f, i + 1).catch(function () {
        if (/^image\/(jpeg|png)$/.test(f.type)) return f;
        throw new Error("Dit fotoformaat wordt niet ondersteund. Stuur een JPG- of PNG-foto, of app de foto naar ons.");
      });
    }));
  }

  window.inoFormulier = { token: token, reset: reset, fotos: fotos, actief: !!SITEKEY };
})();
