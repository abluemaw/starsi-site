#!/usr/bin/env python3
"""Makes a side-by-side review sheet (English | Español | 한국어) for a native speaker.

Run:  python3 tools/translation_review.py [output-folder]
It writes review.html (tick lines off, add notes, export) and review.csv (opens in Google Sheets or Excel).
Lines are listed in the order they appear on the page, grouped by section. Nothing here is published.
"""
import csv, html, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "translation-review")
os.makedirs(OUT, exist_ok=True)

es = json.load(open(os.path.join(HERE, "i18n", "es.json"), encoding="utf-8"))
ko = json.load(open(os.path.join(HERE, "i18n", "ko.json"), encoding="utf-8"))
page = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
body = page.partition("</style>")[2].partition("<script>")[0]

# walk the page in order, remembering which section each line is in
NAMES = {"top": "Header", "welcome": "Welcome (top of page)", "sales": "Sales banner", "demo": "Demo", "success": "What could success look like?",
         "growth": "Grow your profits", "potential": "Calculator", "passion": "Your passion is teaching", "faq": "FAQ", "enroll": "Enrollment form",
         "features": "Features", "benefits": "Benefits", "pricing": "Pricing", "specialized": "Pricing: specialized and extra services", "stories": "Success stories"}
anchors = []
for key, name in NAMES.items():
    for m in re.finditer(r'<[a-z]+ [^>]*\bid="%s"' % key, body):
        anchors.append((m.start(), name))
for m in re.finditer(r"<footer", body):
    anchors.append((m.start(), "Footer"))
for m in re.finditer(r'class="sticky"', body):
    anchors.append((m.start(), "Footer and sticky bar"))
anchors.sort()
rows, seen = [], set()
for m in re.finditer(r'>([^<>]+)<|\b(?:alt|aria-label|title|placeholder)="([^"]*)"', body):
    t = " ".join((m.group(1) or m.group(2) or "").split())
    if t and t in es and t not in seen:
        seen.add(t)
        section = "Header"
        for pos, name in anchors:
            if pos <= m.start():
                section = name
        rows.append((section, t, es[t], ko.get(t, "")))
for t in es:  # anything not found on the page (messages shown by scripts, page title)
    if t not in seen:
        rows.append(("Other (title, messages)", t, es[t], ko.get(t, "")))

with open(os.path.join(OUT, "review.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Section", "English", "Español", "한국어", "OK? (yes / no)", "Corrected Español", "Corrected 한국어", "Notes"])
    w.writerows([list(r) + ["", "", "", ""] for r in rows])

groups = []
for r in rows:
    if not groups or groups[-1][0] != r[0]:
        groups.append((r[0], []))
    groups[-1][1].append(r)

def esc(s): return html.escape(s)
parts = ["""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>StarSI translation review</title><style>
:root{--bg:#0b1230;--card:#121c45;--ink:#f4f6ff;--mut:#a9b3d6;--gold:#ffc61a;--line:#2a3566}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{position:sticky;top:0;z-index:5;background:#0b1230ee;backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:12px 20px;display:flex;gap:16px;flex-wrap:wrap;align-items:center}
h1{font-size:20px;margin:0;color:var(--gold)}.sp{flex:1}button,select{font:inherit;font-weight:700;padding:8px 14px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
button.go{background:var(--gold);color:#1a0f00;border:0}main{max-width:1500px;margin:0 auto;padding:20px}h2{margin:34px 0 10px;font-size:19px;color:var(--gold)}
.row{display:grid;grid-template-columns:28px 1fr 1fr 1fr;gap:12px;padding:12px;border:1px solid var(--line);border-radius:12px;background:var(--card);margin-bottom:8px}
.row.done{opacity:.55}.c small{display:block;color:var(--mut);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:2px}
.c div{white-space:pre-wrap}textarea{grid-column:2/-1;width:100%;min-height:36px;margin-top:4px;padding:8px;border-radius:8px;border:1px solid var(--line);background:#0b1230;color:var(--ink);font:inherit}
input[type=checkbox]{width:20px;height:20px;margin-top:4px}p.note{color:var(--mut);max-width:900px}
@media(max-width:900px){.row{grid-template-columns:28px 1fr}.row .c{grid-column:2}textarea{grid-column:2}}
</style></head><body><header><h1>StarSI translation review</h1><span id="count"></span><span class="sp"></span>
<select id="f"><option value="all">Show all lines</option><option value="todo">Only lines not ticked</option></select>
<button class="go" id="exp">Export my notes</button></header><main>
<p class="note">Read each line in your language. Tick the box when it is right. If it is wrong, write the better wording or a note in the box under the line. Product names (AI Website, U-Bill, HQ Function and so on) stay in English on purpose. Your ticks and notes are saved in this browser; press Export when you finish and send the file back.</p>"""]
n = 0
for name, items in groups:
    parts.append("<h2>%s</h2>" % esc(name))
    for _, en, e, k in items:
        n += 1
        parts.append('<div class="row" data-i="%d"><input type="checkbox" aria-label="OK"><div class="c"><small>English</small><div>%s</div></div><div class="c" lang="es"><small>Español</small><div>%s</div></div><div class="c" lang="ko"><small>한국어</small><div>%s</div></div><textarea placeholder="Better wording or a note (optional)"></textarea></div>' % (n, esc(en), esc(e), esc(k)))
parts.append("""</main><script>
(function(){var rows=[].slice.call(document.querySelectorAll(".row")),KEY="starsi-review-v1";
var st={};try{st=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
function count(){var d=rows.filter(function(r){return r.querySelector("input").checked}).length;document.getElementById("count").textContent=d+" of "+rows.length+" lines ticked"}
function filt(){var only=document.getElementById("f").value==="todo";rows.forEach(function(r){r.hidden=only&&r.querySelector("input").checked})}
rows.forEach(function(r){var i=r.dataset.i,c=r.querySelector("input"),t=r.querySelector("textarea"),s=st[i]||{};c.checked=!!s.ok;t.value=s.note||"";r.classList.toggle("done",c.checked);
c.addEventListener("change",function(){st[i]=st[i]||{};st[i].ok=c.checked;r.classList.toggle("done",c.checked);save();count();filt()});
t.addEventListener("input",function(){st[i]=st[i]||{};st[i].note=t.value;save()})});
document.getElementById("f").addEventListener("change",filt);
document.getElementById("exp").addEventListener("click",function(){var out=["Line,English,Ticked,Note"];rows.forEach(function(r){var s=st[r.dataset.i]||{};var en=r.querySelector(".c div").textContent.replace(/"/g,'""');var n=(s.note||"").replace(/"/g,'""');out.push(r.dataset.i+',"'+en+'",'+(s.ok?"yes":"no")+',"'+n+'"')});
var a=document.createElement("a");a.href=URL.createObjectURL(new Blob(["\\ufeff"+out.join("\\n")],{type:"text/csv"}));a.download="starsi-translation-review-notes.csv";a.click()});
count();filt()})();
</script></body></html>""")
open(os.path.join(OUT, "review.html"), "w", encoding="utf-8").write("".join(parts))
print("Wrote %d lines to %s" % (len(rows), os.path.abspath(OUT)))
