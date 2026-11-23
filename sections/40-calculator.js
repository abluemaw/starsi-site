/* Income calculator: students x tuition, per month and per year */
(function () {
  var s = document.getElementById("students"), t = document.getElementById("tuition");
  if (!s || !t) return;
  function fmt(v) { return v.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }); }
  function calc() {
    var n = +s.value, p = Math.max(0, +t.value || 0);
    document.getElementById("n").value = n;
    document.getElementById("month").textContent = fmt(n * p);
    document.getElementById("year").textContent = fmt(n * p * 12);
  }
  s.addEventListener("input", calc); t.addEventListener("input", calc); calc();
})();
