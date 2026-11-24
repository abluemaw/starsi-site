/* Hide the sticky call-to-action bar while the welcome banner is on screen */
(function () {
  var el = document.getElementById("welcome");
  if (!el || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (e) { document.body.classList.toggle("welcome-active", e[0].isIntersecting); }, { threshold: 0.25 }).observe(el);
})();

/* Preload the final still and crossfade over the video's last frame. */
(function () {
  var v = document.querySelector("video.welcome-art");
  if (!v) return;
  v.loop = false;
  var still = new Image();
  still.className = "welcome-art welcome-final";
  still.alt = "Martial arts school owner using the StarSI.AI command center";
  still.width = 1648;
  still.height = 928;
  var finished = false;
  var q = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  function finish() {
    if (finished) return;
    finished = true;
    v.pause();
    function swap() {
      if (!v.parentNode) return;
      var parent = v.parentNode;
      parent.insertBefore(still, v.nextSibling);
      still.getBoundingClientRect();
      parent.classList.add("welcome-final-visible");
      var remove = function () { v.style.visibility = "hidden"; v.setAttribute("aria-hidden", "true"); };
      if (q && q.matches) remove();
      else setTimeout(remove, 1250);
    }
    if (still.complete && still.naturalWidth) swap();
    else still.addEventListener("load", swap, { once: true });
  }
  still.src = "images/StarSI.AI%20Business%20Command%20Center.png";
  if (still.decode) still.decode().catch(function () {});
  v.addEventListener("ended", finish, { once: true });
  v.addEventListener("error", finish, { once: true });
  if (q && q.matches || v.ended || v.error) finish();
  else {
    var p = v.play();
    if (p && p.catch) p.catch(finish);
  }
  if (q && q.addEventListener) q.addEventListener("change", function () { if (q.matches) finish(); });
})();
