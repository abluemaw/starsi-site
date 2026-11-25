/* Hide the sticky call-to-action bar while the welcome banner is on screen */
(function () {
  var el = document.getElementById("welcome");
  if (!el || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (e) { document.body.classList.toggle("welcome-active", e[0].isIntersecting); }, { threshold: 0.25 }).observe(el);
})();
