/* Hide the sticky call-to-action bar while the welcome banner is on screen */
(function () {
  var el = document.getElementById("welcome");
  if (!el || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (e) { document.body.classList.toggle("welcome-active", e[0].isIntersecting); }, { threshold: 0.25 }).observe(el);
})();

/* Respect "reduce motion": show the still poster instead of the looping hero video */
(function () {
  var v = document.querySelector("video.welcome-art");
  if (!v || !window.matchMedia) return;
  var q = window.matchMedia("(prefers-reduced-motion: reduce)");
  function apply() { if (q.matches) { v.removeAttribute("autoplay"); v.pause(); } else { var p = v.play(); if (p && p.catch) p.catch(function () {}); } }
  apply();
  if (q.addEventListener) q.addEventListener("change", apply);
})();
