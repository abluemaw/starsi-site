/* Hide the sticky call-to-action bar while the welcome banner is on screen */
(function () {
  var el = document.getElementById("welcome");
  if (!el || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (e) { document.body.classList.toggle("welcome-active", e[0].isIntersecting); }, { threshold: 0.25 }).observe(el);
})();

/* Run all of the hero's camera and dissolve animations on one shared timeline. */
(function () {
  var banner = document.querySelector(".welcome-banner[data-welcome-step]");
  if (!banner) return;

  var button = banner.querySelector(".welcome-motion-control");
  var labels = button.querySelectorAll("[data-welcome-control]");
  var motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var observer;

  function showControl(state) {
    labels.forEach(function (label) {
      label.hidden = label.dataset.welcomeControl !== state;
    });
    button.hidden = false;
  }

  function finish() {
    banner.dataset.welcomeStep = "classroom";
    delete banner.dataset.welcomePaused;
    showControl("replay");
  }

  function play() {
    if (observer) observer.disconnect();
    banner.dataset.welcomeStep = "playing";
    delete banner.dataset.welcomePaused;
    showControl("pause");
  }

  button.addEventListener("click", function () {
    if (banner.dataset.welcomeStep !== "playing") {
      play();
    } else if ("welcomePaused" in banner.dataset) {
      delete banner.dataset.welcomePaused;
      showControl("pause");
    } else {
      banner.dataset.welcomePaused = "";
      showControl("resume");
    }
  });

  banner.addEventListener("animationend", function (event) {
    if (event.animationName === "welcome-title-reveal") finish();
  });

  motion.addEventListener("change", function (event) {
    if (event.matches) finish();
  });

  if (motion.matches) {
    finish();
  } else if (!("IntersectionObserver" in window)) {
    play();
  } else {
    observer = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      if (banner.dataset.welcomeStep === "welcome" && !motion.matches) play();
      else observer.disconnect();
    }, { threshold: 0.25 });
    observer.observe(banner);
  }
})();
