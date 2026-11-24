/* Hide the sticky call-to-action bar while the welcome banner is on screen */
(function () {
  var el = document.getElementById("welcome");
  if (!el || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (e) { document.body.classList.toggle("welcome-active", e[0].isIntersecting); }, { threshold: 0.25 }).observe(el);
})();

/* Play the hero once, then show the still in the same position. */
(function () {
  var video = document.querySelector("video.welcome-art");
  if (!video) return;

  var still = new Image(video.width, video.height);
  still.className = video.className;
  still.alt = "";
  still.src = video.poster;

  function showStill() {
    video.pause();
    if (still.complete && still.naturalWidth) {
      video.replaceWith(still);
    } else {
      still.addEventListener("load", function () { video.replaceWith(still); }, { once: true });
    }
  }

  video.addEventListener("ended", showStill, { once: true });

  var motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (motion.matches) {
    showStill();
    return;
  }

  motion.addEventListener("change", function (event) {
    if (event.matches && video.isConnected) showStill();
  });
  video.play().catch(showStill);
})();
