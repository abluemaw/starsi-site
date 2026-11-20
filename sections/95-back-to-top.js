/* Back to top: shows after scrolling one screen down */
(function () {
  var b = document.getElementById("to-top");
  if (!b) return;
  function check() { b.classList.toggle("show", (window.scrollY || document.documentElement.scrollTop) > 600); }
  window.addEventListener("scroll", check, { passive: true });
  check();
})();
