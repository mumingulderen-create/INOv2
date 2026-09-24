/* Rekenhulp storingskosten (alleen op /tarieven/). */
(function () {
  var el = document.querySelector(".rekenhulp");
  if (!el) return;
  var t = JSON.parse(el.getAttribute("data-tarieven"));
  var bedrag = el.querySelector(".rh-bedrag"), uitleg = el.querySelector(".rh-uitleg"), nu = el.querySelector(".rh-nu");
  function euro(n) { return "€ " + (Math.round(n * 100) / 100).toFixed(2).replace(".", ",").replace(",00", ",-"); }
  // Huidig tarief bepalen (feestdagen kan de site niet weten: die vallen onder nacht & weekend)
  var d = new Date(), dag = d.getDay(), uur = d.getHours();
  var moment = (dag === 0 || dag === 6 || uur < 8 || uur >= 22) ? "nacht" : (uur >= 18 ? "avond" : "dag");
  var namen = { dag: "overdagtarief", avond: "avondtarief", nacht: "nacht- en weekendtarief" };
  el.querySelector('input[name="rh_moment"][value="' + moment + '"]').checked = true;
  nu.textContent = "Nu geldt het " + namen[moment] + ".";
  nu.hidden = false;
  function reken() {
    var m = el.querySelector('input[name="rh_moment"]:checked').value;
    var u = parseFloat(el.querySelector('input[name="rh_duur"]:checked').value);
    var extraKw = Math.round((u - 1) * 4);
    var totaal = t[m][0] + extraKw * t[m][1];
    bedrag.textContent = euro(totaal);
    uitleg.textContent = extraKw ? "1e uur " + euro(t[m][0]) + " + " + extraKw + " × kwartier à " + euro(t[m][1]) : "1e uur, incl. diagnose en btw";
  }
  el.addEventListener("change", reken);
  reken();
})();
