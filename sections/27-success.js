/* What could success look like: school size tabs, English / Español / 한국어, video boxes.
   To add a video, put the file in the video folder and write its path in VIDEOS below (one per size and language).
   Leave "" to show the "coming soon" box. The words in TEXT are translations to be reviewed by a native speaker. */
(function () {
  var root = document.getElementById("success");
  if (!root) return;

  var VIDEOS = {
    small: { en: "", es: "", ko: "" },
    mid:   { en: "", es: "", ko: "" },
    big:   { en: "", es: "", ko: "" }
  };

  var TEXT = {
    en: {
      title: "What could success look like?",
      small: "Small school", mid: "Midsize school", big: "Big school",
      soon: "Success story video coming soon",
      "alt-small": "A small martial arts school with students training together",
      "alt-mid": "A midsize martial arts school with a full class training",
      "alt-big": "A big martial arts academy with a huge class training in unison"
    },
    es: {
      title: "¿Cómo podría verse el éxito?",
      small: "Escuela pequeña", mid: "Escuela mediana", big: "Escuela grande",
      soon: "Video de historia de éxito próximamente",
      "alt-small": "Una escuela pequeña de artes marciales con alumnos entrenando juntos",
      "alt-mid": "Una escuela mediana de artes marciales con una clase completa entrenando",
      "alt-big": "Una gran academia de artes marciales con una clase enorme entrenando al unísono"
    },
    ko: {
      title: "성공은 어떤 모습일까요?",
      small: "소규모 도장", mid: "중간 규모 도장", big: "대규모 도장",
      soon: "성공 사례 영상 준비 중",
      "alt-small": "수련생들이 함께 훈련하는 소규모 무술 도장",
      "alt-mid": "한 반 가득 훈련하는 중간 규모 무술 도장",
      "alt-big": "대규모 수련생이 한 몸처럼 훈련하는 대형 무술 아카데미"
    }
  };

  var lang = "en", size = "small";
  var pageLang = (document.documentElement.getAttribute("lang") || "en").slice(0, 2);
  if (TEXT[pageLang]) lang = pageLang;

  function box(sz) { return root.querySelector('.success-video[data-size="' + sz + '"]'); }
  function poster(sz) { var i = root.querySelector('.success-panel[data-size="' + sz + '"] img'); return i ? i.getAttribute("src") : ""; }

  function renderVideo(sz) {
    var b = box(sz), url = VIDEOS[sz][lang];
    b.textContent = "";
    if (url) {
      var v = document.createElement("video");
      v.controls = true; v.preload = "none"; v.playsInline = true; v.poster = poster(sz); v.src = url;
      b.appendChild(v);
    } else {
      var p = document.createElement("div"); p.className = "success-poster"; p.style.backgroundImage = 'url("' + poster(sz) + '")';
      var play = document.createElement("span"); play.className = "success-play"; play.setAttribute("aria-hidden", "true");
      var soon = document.createElement("div"); soon.className = "success-soon"; soon.textContent = TEXT[lang].soon;
      b.appendChild(p); b.appendChild(play); b.appendChild(soon);
    }
  }

  function applyLang() {
    root.setAttribute("lang", lang); root.setAttribute("data-lang", lang);
    var t = TEXT[lang];
    root.querySelectorAll("[data-i18n]").forEach(function (el) { el.textContent = t[el.getAttribute("data-i18n")]; });
    root.querySelectorAll("[data-i18n-alt]").forEach(function (el) { el.setAttribute("alt", t[el.getAttribute("data-i18n-alt")]); });
    root.querySelectorAll(".success-chip").forEach(function (c) {
      var on = c.getAttribute("data-lang") === lang; c.classList.toggle("is-on", on); c.setAttribute("aria-pressed", on ? "true" : "false");
    });
    ["small", "mid", "big"].forEach(renderVideo);
  }

  function applySize(next, focus) {
    size = next;
    root.querySelectorAll(".success-tab").forEach(function (t) {
      var on = t.getAttribute("data-size") === size;
      t.classList.toggle("is-on", on); t.setAttribute("aria-selected", on ? "true" : "false"); t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    root.querySelectorAll(".success-panel").forEach(function (p) { p.hidden = p.getAttribute("data-size") !== size; });
  }

  root.querySelectorAll(".success-chip").forEach(function (c) {
    c.addEventListener("click", function () {
      lang = c.getAttribute("data-lang"); try { localStorage.setItem("starsi-success-lang", lang); } catch (e) {}
      applyLang();
    });
  });
  var order = ["small", "mid", "big"];
  root.querySelectorAll(".success-tab").forEach(function (t) {
    t.addEventListener("click", function () { applySize(t.getAttribute("data-size")); });
    t.addEventListener("keydown", function (e) {
      var i = order.indexOf(size);
      if (e.key === "ArrowRight") { e.preventDefault(); applySize(order[(i + 1) % 3], true); }
      if (e.key === "ArrowLeft") { e.preventDefault(); applySize(order[(i + 2) % 3], true); }
    });
  });

  applyLang(); applySize("small");
})();
