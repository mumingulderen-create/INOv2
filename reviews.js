/* Reviews-carrousel (alleen geladen op /reviews/): pijltjes scrollen één kaart verder. */
(function () {
  var track = document.getElementById("reviewsTrack");
  var prev = document.getElementById("reviewsPrevBtn");
  var next = document.getElementById("reviewsNextBtn");
  if (!track || !prev || !next) return;
  function stap() { return track.firstElementChild ? track.firstElementChild.offsetWidth + 20 : 340; }
  prev.addEventListener("click", function () { track.scrollBy({ left: -stap(), behavior: "smooth" }); });
  next.addEventListener("click", function () { track.scrollBy({ left: stap(), behavior: "smooth" }); });
})();
