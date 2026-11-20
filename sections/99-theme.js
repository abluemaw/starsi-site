/* Light / dark switch: remembers the choice, starts from the device setting */
(function () {
  var btn = document.getElementById("theme-toggle");
  if (!btn) return;
  var root = document.documentElement;
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: light)") : null;
  function current() { return root.getAttribute("data-theme") || (mq && mq.matches ? "light" : "dark"); }
  function paint() { var t = current(); btn.textContent = t === "light" ? "\u263E" : "\u2600"; btn.setAttribute("title", t === "light" ? "Switch to dark mode" : "Switch to light mode"); }
  btn.addEventListener("click", function () {
    var next = current() === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("starsi-theme", next); } catch (e) {}
    paint();
  });
  if (mq && mq.addEventListener) mq.addEventListener("change", paint);
  paint();
})();
