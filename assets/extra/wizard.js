/* Offerte-wizard (alleen geladen op /offerte/). Overgenomen uit v1, zonder externe afhankelijkheden. */
(function () {
  function esc(v) { return String(v).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[c]; }); }
  function track(evt, params) {
    try { if (window.inoGA4geladen && window.gtag) window.gtag("event", evt, params || {}); } catch (e) {}
  }
  function initKlusWizard() {
    var wizard = document.getElementById("quoteWizard");
    if (!wizard) return;

    var currentStep = 1;
    var totalSteps = 3;
    var serviceInput = document.getElementById("wizardService");
    var termijnInput = document.getElementById("wizardTermijn");
    var messageBox = document.getElementById("message");
    var progressBar = document.getElementById("wizardProgressBar");
    var stepIndicators = wizard.querySelectorAll(".wizard-progress-step");
    var stepContents = wizard.querySelectorAll(".wizard-step-content");
    var tiles = wizard.querySelectorAll(".wizard-tile");
    var pills = wizard.querySelectorAll(".wizard-pill");
    var dropzone = document.getElementById("wizardDropzone");
    var photoInput = document.getElementById("photos");
    var photoList = document.getElementById("photoList");

    function goToStep(step, geenScroll) {
      if (step < 1 || step > totalSteps) return;
      currentStep = step;

      // Update progress bar
      if (progressBar) {
        var pct = step === 1 ? 0 : step === 2 ? 50 : 100;
        progressBar.style.width = pct + "%";
      }

      // Update step circles & labels
      stepIndicators.forEach(function (ind) {
        var s = parseInt(ind.dataset.step, 10);
        ind.classList.remove("active", "completed");
        if (s === currentStep) {
          ind.classList.add("active");
        } else if (s < currentStep) {
          ind.classList.add("completed");
        }
      });

      // Show/hide step contents
      stepContents.forEach(function (content) {
        var s = parseInt(content.dataset.step, 10);
        if (s === currentStep) {
          content.hidden = false;
        } else {
          content.hidden = true;
        }
      });

      // Smooth scroll into view
      if (!geenScroll) wizard.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    var countBadge = document.getElementById("wizardStep1Count");
    var step1NextBtn = document.getElementById("wizardStep1Next");

    function getSelectedServices() {
      var arr = [];
      wizard.querySelectorAll(".wizard-tile.selected").forEach(function (t) {
        if (t.dataset.service) arr.push(t.dataset.service);
      });
      return arr;
    }

    function updateSelectionUI() {
      var sel = getSelectedServices();
      var count = sel.length;
      if (serviceInput) serviceInput.value = sel.join(", ");

      if (countBadge) {
        if (count === 0) {
          countBadge.textContent = "Kies minimaal 1 klus";
          countBadge.style.color = "#b91c1c";
          countBadge.style.background = "#fee2e2";
        } else if (count === 1) {
          countBadge.textContent = "1 klus geselecteerd";
          countBadge.style.color = "var(--green-dark)";
          countBadge.style.background = "#eef8ec";
        } else {
          countBadge.textContent = count + " klussen gecombineerd";
          countBadge.style.color = "var(--green-dark)";
          countBadge.style.background = "#eef8ec";
        }
      }

      if (step1NextBtn) {
        if (count > 1) {
          step1NextBtn.innerHTML = "Volgende: Toelichting (" + count + " klussen) →";
        } else {
          step1NextBtn.innerHTML = "Volgende: Toelichting &amp; Foto's →";
        }
      }

      // Dynamic placeholder for message textarea
      if (messageBox) {
        if (count === 0) {
          messageBox.placeholder = "Beschrijf kort je situatie en wat er moet gebeuren...";
        } else if (count === 1) {
          var s = sel[0];
          if (s.indexOf("Meterkast") !== -1) {
            messageBox.placeholder = "Bijv: Mijn groepenkast is verouderd met stoppen. Ik wil graag een nieuwe 1- of 3-fase kast met aardlekschakelaars.";
          } else if (s.indexOf("Extra groep") !== -1) {
            messageBox.placeholder = "Bijv: Ik krijg een Quooker en combi-oven en wil 1 of 2 extra groepen laten bijplaatsen.";
          } else if (s.indexOf("Kookgroep") !== -1 || s.indexOf("Perilex") !== -1) {
            messageBox.placeholder = "Bijv: We gaan koken op inductie. Er ligt nog geen Perilex stopcontact / kookgroep.";
          } else if (s.indexOf("Laadpaal") !== -1) {
            messageBox.placeholder = "Bijv: Ik wil een 11kW Wallbox laten monteren bij de oprit, incl. load balancing.";
          } else {
            messageBox.placeholder = "Beschrijf kort wat er moet gebeuren voor " + s + "...";
          }
        } else {
          messageBox.placeholder = "Licht de situatie kort toe voor: " + sel.join(" + ") + "...";
        }
      }
    }

    // Tile multi-selection (Step 1)
    tiles.forEach(function (tile) {
      tile.addEventListener("click", function () {
        tile.classList.toggle("selected");
        updateSelectionUI();
      });
    });
    updateSelectionUI();

    // Pill selection (termijn in Step 2)
    pills.forEach(function (pill) {
      pill.addEventListener("click", function () {
        pills.forEach(function (p) { p.classList.remove("selected"); });
        pill.classList.add("selected");
        if (termijnInput) termijnInput.value = pill.dataset.val || pill.textContent.trim();
      });
    });

    // Next / Previous buttons
    wizard.addEventListener("click", function (e) {
      var nextBtn = e.target.closest("[data-wizard-next]");
      var prevBtn = e.target.closest("[data-wizard-prev]");

      if (nextBtn) {
        e.preventDefault();
        if (currentStep === 1) {
          var sel = getSelectedServices();
          if (sel.length === 0) {
            if (countBadge) {
              countBadge.textContent = "Kies minimaal 1 optie om door te gaan!";
              countBadge.style.color = "#b91c1c";
              countBadge.style.background = "#fee2e2";
            }
            tiles.forEach(function (t) {
              t.style.borderColor = "#e53e3e";
              setTimeout(function () { t.style.borderColor = ""; }, 1500);
            });
            return;
          }
          goToStep(2);
        } else if (currentStep === 2) {
          // Check if message is filled
          if (messageBox && !messageBox.value.trim()) {
            messageBox.focus();
            messageBox.style.borderColor = "#e53e3e";
            setTimeout(function () { messageBox.style.borderColor = ""; }, 2500);
            return;
          }
          goToStep(3);
        }
      } else if (prevBtn) {
        e.preventDefault();
        goToStep(currentStep - 1);
      }
    });

    // Dropzone drag-and-drop
    if (dropzone && photoInput) {
      ["dragenter", "dragover"].forEach(function (ename) {
        dropzone.addEventListener(ename, function (e) {
          e.preventDefault();
          dropzone.classList.add("dragover");
        });
      });
      ["dragleave", "drop"].forEach(function (ename) {
        dropzone.addEventListener(ename, function (e) {
          e.preventDefault();
          dropzone.classList.remove("dragover");
        });
      });
      dropzone.addEventListener("drop", function (e) {
        if (e.dataTransfer && e.dataTransfer.files) {
          photoInput.files = e.dataTransfer.files;
          updatePhotoDisplay();
        }
      });
      photoInput.addEventListener("change", updatePhotoDisplay);
    }

    // Na succesvol versturen (form.reset in script.js) terug naar stap 1
    var formEl = document.getElementById("quoteForm");
    if (formEl) formEl.addEventListener("reset", function () {
      setTimeout(function () { goToStep(1, true); updatePhotoDisplay(); }, 0);
    });

    function updatePhotoDisplay() {
      if (!photoInput || !photoList) return;
      var f = Array.prototype.slice.call(photoInput.files || []);
      if (!f.length) {
        photoList.innerHTML = "";
        return;
      }
      var html = '<div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:8px;">';
      f.forEach(function (file) {
        html += '<span style="background:#eef8ec;color:#185315;padding:5px 12px;border-radius:8px;font-size:12px;font-weight:700;display:inline-flex;align-items:center;gap:6px;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg> ' + esc(file.name) + '</span>';
      });
      html += '</div>';
      photoList.innerHTML = html;
    }

    // Direct versturen via WhatsApp knop in Stap 3
    var btnSendWhatsApp = document.getElementById("btnSendWhatsApp");
    if (btnSendWhatsApp) {
      btnSendWhatsApp.addEventListener("click", function (e) {
        e.preventDefault();
        var form = document.getElementById("quoteForm");
        var nameField = form ? form.querySelector("input[name='name']") : null;
        var phoneField = form ? form.querySelector("input[name='phone']") : null;
        var postcodeField = form ? form.querySelector("input[name='postcode']") : null;
        var numberField = form ? form.querySelector("input[name='number']") : null;

        var nameVal = (nameField && nameField.value || "").trim();
        var phoneVal = (phoneField && phoneField.value || "").trim();
        var postcodeVal = (postcodeField && postcodeField.value || "").trim();
        var numberVal = (numberField && numberField.value || "").trim();
        var servicesVal = (serviceInput && serviceInput.value || "").trim() || "Elektra klus";
        var termijnVal = (termijnInput && termijnInput.value || "").trim();
        var msgVal = (messageBox && messageBox.value || "").trim();

        if (!nameVal) {
          if (nameField) {
            nameField.focus();
            nameField.style.borderColor = "#e53e3e";
            setTimeout(function () { nameField.style.borderColor = ""; }, 2000);
          }
          return;
        }

        var lines = [
          "Hallo INO Techniek, ik heb via de offerte-wizard op de website een aanvraag samengesteld:",
          "- Klus(sen): " + servicesVal,
          "- Gewenste termijn: " + (termijnVal || "In overleg"),
          "- Toelichting: " + (msgVal || "(geen extra toelichting)"),
          "- Mijn naam: " + nameVal
        ];
        if (phoneVal) lines.push("- Tel: " + phoneVal);
        if (postcodeVal || numberVal) lines.push("- Adres/postcode: " + (postcodeVal + " " + numberVal).trim());
        lines.push("\nIk stuur foto's van mijn situatie mee.");

        var waUrl = "https://wa.me/__WHATSAPP__?text=" + encodeURIComponent(lines.join("\n"));
        track("formulier_verstuurd", { formulier: "quoteForm", method: "whatsapp_wizard" });
        track("generate_lead", { formulier: "quoteForm", method: "whatsapp_wizard", currency: "EUR" });
        window.open(waUrl, "_blank", "noopener");
      });
    }
  }
  initKlusWizard();
})();
