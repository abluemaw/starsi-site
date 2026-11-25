/* Hide the sticky call-to-action bar while the welcome banner is on screen */
(function () {
  var el = document.getElementById("welcome");
  if (!el || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (e) { document.body.classList.toggle("welcome-active", e[0].isIntersecting); }, { threshold: 0.25 }).observe(el);
})();

/* Play the welcome sequence once on entry, with pause and replay controls. */
(function () {
  var banner = document.querySelector(".welcome-banner[data-welcome-step]");
  if (!banner) return;

  var button = banner.querySelector(".welcome-motion-control");
  var labels = button.querySelectorAll("[data-welcome-control]");
  var motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var steps = [
    ["welcome", 1450],
    ["master", 1850],
    ["zoom", 1150],
    ["monitor", 4600],
    ["classroom", 0]
  ];
  var step = steps.length - 1;
  var timer;
  var startedAt;
  var remaining;

  function showControl(state) {
    labels.forEach(function (label) {
      label.hidden = label.dataset.welcomeControl !== state;
    });
    button.hidden = false;
  }

  function showStep(index) {
    clearTimeout(timer);
    timer = undefined;
    step = index;
    banner.dataset.welcomeStep = steps[index][0];
    remaining = steps[index][1];

    if (remaining === 0) {
      showControl("replay");
    } else {
      resume();
    }
  }

  function resume() {
    showControl("pause");
    startedAt = performance.now();
    timer = setTimeout(function () { showStep(step + 1); }, remaining);
  }

  function pause() {
    clearTimeout(timer);
    timer = undefined;
    remaining = Math.max(0, remaining - (performance.now() - startedAt));
    showControl("resume");
  }

  button.addEventListener("click", function () {
    if (step === steps.length - 1) {
      showStep(0);
    } else if (timer !== undefined) {
      pause();
    } else {
      resume();
    }
  });

  showControl("replay");
  if (motion.matches) {
    showStep(steps.length - 1);
    return;
  }

  if (!("IntersectionObserver" in window)) {
    showStep(0);
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    if (!entries[0].isIntersecting) return;
    observer.disconnect();
    if (step === steps.length - 1 && !motion.matches) showStep(0);
  }, { threshold: 0.25 });
  observer.observe(banner);
})();
