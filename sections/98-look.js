/* Look picker: lets people try a design variant (designs/*.md). "Live design" is the shared DESIGN.md. */
(function () {
  var sel = document.getElementById("look-picker");
  if (!sel) return;
  var root = document.documentElement;
  fetch((document.documentElement.getAttribute("data-root") || "") + "designs/variants.json", { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
    if (!d || d.picker === false || !d.variants || !d.variants.length) return;
    var darkImg = document.querySelector(".logo-dark"), lightImg = document.querySelector(".logo-light");
    var base = window.SITE_ROOT || document.documentElement.getAttribute("data-root") || "";
    var liveLogo = (d.live && d.live.logo) || (darkImg && darkImg.getAttribute("src"));
    function setLogo(slug) {
      if (!darkImg) return;
      var v = d.variants.filter(function (x) { return x.slug === slug; })[0];
      var dark = (v && v.logo) || liveLogo, light = (v && v.logoLight) || (!v && d.live && d.live.logoLight) || "";
      if (dark && darkImg.getAttribute("src") !== base + dark) darkImg.setAttribute("src", base + dark);
      if (lightImg) { if (light) { lightImg.setAttribute("src", base + light); lightImg.removeAttribute("hidden"); root.setAttribute("data-logo-light", ""); } else { root.removeAttribute("data-logo-light"); } }
    }
    var saved = root.getAttribute("data-look") || "";
    var first = document.createElement("option"); first.value = ""; first.textContent = "Live design"; sel.appendChild(first);
    d.variants.forEach(function (v) {
      var o = document.createElement("option"); o.value = v.slug; o.textContent = v.name; if (v.description) o.title = v.description; sel.appendChild(o);
    });
    sel.value = d.variants.some(function (v) { return v.slug === saved; }) ? saved : "";
    if (sel.value === "") root.removeAttribute("data-look");
    sel.hidden = false;
    setLogo(sel.value);
    sel.addEventListener("change", function () {
      var link = document.getElementById("look-css");
      if (sel.value) {
        if (!link) { link = document.createElement("link"); link.rel = "stylesheet"; link.id = "look-css"; document.head.appendChild(link); }
        link.href = (document.documentElement.getAttribute("data-root") || "") + "designs/looks/" + sel.value + ".css";
        root.setAttribute("data-look", sel.value);
      } else {
        root.removeAttribute("data-look");
        if (link) link.remove();
      }
      setLogo(sel.value);
      try { if (sel.value) localStorage.setItem("starsi-look", sel.value); else localStorage.removeItem("starsi-look"); } catch (e) {}
    });
  }).catch(function () {});
})();
