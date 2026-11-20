/* Look picker: lets people try a design variant (designs/*.md). "Live design" is the shared DESIGN.md. */
(function () {
  var sel = document.getElementById("look-picker");
  if (!sel) return;
  var root = document.documentElement;
  fetch("designs/variants.json", { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
    if (!d || d.picker === false || !d.variants || !d.variants.length) return;
    var saved = root.getAttribute("data-look") || "";
    var first = document.createElement("option"); first.value = ""; first.textContent = "Live design"; sel.appendChild(first);
    d.variants.forEach(function (v) {
      var o = document.createElement("option"); o.value = v.slug; o.textContent = v.name; if (v.description) o.title = v.description; sel.appendChild(o);
    });
    sel.value = d.variants.some(function (v) { return v.slug === saved; }) ? saved : "";
    if (sel.value === "") root.removeAttribute("data-look");
    sel.hidden = false;
    sel.addEventListener("change", function () {
      var link = document.getElementById("look-css");
      if (sel.value) {
        if (!link) { link = document.createElement("link"); link.rel = "stylesheet"; link.id = "look-css"; document.head.appendChild(link); }
        link.href = "designs/looks/" + sel.value + ".css";
        root.setAttribute("data-look", sel.value);
      } else {
        root.removeAttribute("data-look");
        if (link) link.remove();
      }
      try { if (sel.value) localStorage.setItem("starsi-look", sel.value); else localStorage.removeItem("starsi-look"); } catch (e) {}
    });
  }).catch(function () {});
})();
