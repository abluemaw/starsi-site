/* Hide the sticky call-to-action bar while the welcome banner is on screen */
(function () {
  var el = document.getElementById("welcome");
  if (!el || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (e) { document.body.classList.toggle("welcome-active", e[0].isIntersecting); }, { threshold: 0.25 }).observe(el);
})();

/* Play the welcome video once, then display the uploaded still. */
(function () {
  var v = document.querySelector("video.welcome-art");
  if (!v) return;
  v.loop = false;
  var still = new Image();
  still.className = v.className;
  still.alt = "Martial arts school owner using the StarSI.AI command center";
  still.width = v.width;
  still.height = v.height;
  var finished = false;
  function finish() {
    if (finished) return;
    finished = true;
    v.pause();
    function swap() { if (v.parentNode) v.parentNode.replaceChild(still, v); }
    if (still.complete && still.naturalWidth) swap();
    else still.addEventListener("load", swap, { once: true });
  }
  still.src = "images/StarSI.AI%20Martial%20Arts%20Command%20Center.png";
  v.addEventListener("ended", finish, { once: true });
  v.addEventListener("error", finish, { once: true });
  var q = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  if (q && q.matches || v.ended || v.error) finish();
  else {
    var p = v.play();
    if (p && p.catch) p.catch(finish);
  }
  if (q && q.addEventListener) q.addEventListener("change", function () { if (q.matches) finish(); });
})();
