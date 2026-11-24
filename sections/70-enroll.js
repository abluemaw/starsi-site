/* Enrollment preview: builds a local draft file in the browser. Nothing is sent anywhere. */
(function () {
  var f = document.getElementById("form");
  if (!f) return;
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = {}; new FormData(f).forEach(function (v, k) { data[k] = v; });
    var draft = Object.assign({ status: (window.STARSI_I18N || {})["Nonbinding enrollment draft"] || "Nonbinding enrollment draft" }, data);
    var url = URL.createObjectURL(new Blob([JSON.stringify(draft, null, 2)], { type: "application/json" }));
    var a = document.createElement("a"); a.href = url; a.download = "starsi-enrollment-draft.json"; a.click();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    document.getElementById("result").textContent = (window.STARSI_I18N || {})["Your draft was prepared for download. Nothing has been submitted or signed."] || "Your draft was prepared for download. Nothing has been submitted or signed.";
  });
})();
