#!/usr/bin/env python3
"""Builds index.html from the files in sections/.

Run:  python3 build.py
Nobody has to run this by hand: GitHub runs it after every change.

How the page is put together
  sections/NN-name.html   the words and layout of one section
  sections/NN-name.css    the styling for that section
  sections/NN-name.js     optional script for that section
Files are joined in number order. Numbers 10 to 89 go inside <main>.
00 is the top of the page (title, description, shared colours and fonts),
01 is the header, 90 is the footer.
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.join(HERE, "sections")


def files(ext):
    return sorted(glob.glob(os.path.join(SEC, "*." + ext)))


def num(path):
    return int(re.match(r"(\d+)-", os.path.basename(path)).group(1))


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def build():
    head = read(os.path.join(SEC, "00-head.html"))
    css = "".join(read(p) for p in files("css"))
    body = ""
    main_open = False
    for p in files("html"):
        n = num(p)
        if n == 0:
            continue
        if 10 <= n <= 89 and not main_open:
            body += "<main>\n\n"
            main_open = True
        if n >= 90 and main_open:
            body += "</main>\n\n"
            main_open = False
        body += read(p)
    if main_open:
        body += "</main>\n\n"
    js = "".join(read(p) for p in files("js"))
    fonts_link = ""
    try:
        import re as _re
        m = _re.search(r'^fontsUrl:\s*"?(.*?)"?\s*$', read(os.path.join(HERE, "DESIGN.md")), _re.M)
        if m and m.group(1):
            fonts_link = '<link rel="stylesheet" href="%s">\n' % m.group(1)
    except Exception:
        pass
    out = head + "<style>\n" + css + "</style>\n" + fonts_link + "</head>\n<body id=\"top\">\n\n" + body
    # header logo comes from DESIGN.md (logo / logoLight)
    try:
        import re as _re2
        md = read(os.path.join(HERE, "DESIGN.md"))
        def _m(k):
            m = _re2.search(r'^%s:\s*"?(.*?)"?\s*$' % k, md, _re2.M)
            return m.group(1) if m else ""
        logo, logo_light = _m("logo"), _m("logoLight")
        if logo:
            out = _re2.sub(r'(<img class="nav-logo logo-dark" src=")[^"]*(")', lambda m: m.group(1) + logo + m.group(2), out, 1)
        if logo and logo_light:
            out = out.replace('<img class="nav-logo logo-light" src="" alt="" hidden>', '<img class="nav-logo logo-light" src="%s" alt="StarSI AI">' % logo_light, 1)
            out = out.replace('<html lang="en">', '<html lang="en" data-logo-light>', 1)
    except Exception:
        pass
    # version the icon sheet's address so a changed sheet is never served from an old cache
    try:
        import hashlib
        sp = os.path.join(HERE, "icons", "sprite.svg")
        if os.path.exists(sp):
            v = hashlib.md5(open(sp, "rb").read()).hexdigest()[:8]
            out = out.replace("icons/sprite.svg#", "icons/sprite.svg?v=%s#" % v)
    except Exception:
        pass
    if js:
        out += "<script>\n" + js + "</script>\n"
    out += "\n</body>\n</html>\n"
    return out


LANGS = {
    "en": {"name": "English", "flag": "us", "dir": ""},
    "es": {"name": "Español", "flag": "es", "dir": "es"},
    "ko": {"name": "한국어", "flag": "kr", "dir": "ko"},
}


def localise(out, code):
    """Fill the language menu for one page and (for es / ko) swap in the translated lines."""
    import json
    info = LANGS[code]
    root = "" if code == "en" else "../"
    out = out.replace("{{ROOT}}", root).replace("{{FLAG}}", info["flag"]).replace("{{LANGNAME}}", info["name"])
    for c in LANGS:
        out = out.replace("{{CUR_%s}}" % c.upper(), ' aria-current="true"' if c == code else "")
    if code == "en":
        return out, []
    out = out.replace('<html lang="en"', '<html lang="%s" data-root="../"' % code, 1)
    path = os.path.join(HERE, "i18n", code + ".json")
    stale = []
    if os.path.exists(path):
        tr = json.load(open(path, encoding="utf-8"))
        used = set()

        def swap_text(m):
            t = " ".join(m.group(1).split())
            if t in tr:
                used.add(t)
                lead = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
                trail = m.group(1)[len(m.group(1).rstrip()):]
                return ">" + lead + tr[t] + trail + "<"
            return m.group(0)

        def swap_attr(m):
            t = m.group(2).strip()
            if t in tr:
                used.add(t)
                return '%s="%s"' % (m.group(1), tr[t].replace('"', "&quot;"))
            return m.group(0)

        def swap_meta(m):
            t = m.group(2).strip()
            if t in tr:
                used.add(t)
                return '%s"%s"' % (m.group(1), tr[t].replace('"', "&quot;"))
            return m.group(0)

        # head (title and description), then body text and attributes; never the style or script blocks
        pre, s1, _rest = out.partition("<style>")
        pre = re.sub(r"(<title>)([^<]*)(?=</title>)", lambda m: m.group(1) + tr.get(m.group(2).strip(), m.group(2)), pre)
        for k in list(tr):
            if "<title>" + k + "</title>" in out:
                used.add(k)
        pre = re.sub(r'(<meta (?:name|property)="(?:description|og:description|og:title|twitter:description|twitter:title)" content=)"([^"]*)"', swap_meta, pre)
        css = out.partition("</style>")[0][len(pre) + len(s1):]
        e1 = "</style>"
        body_all = out.partition("</style>")[2]
        body, s3, tail = body_all.partition("<script>")
        body = re.sub(r">([^<>]+)<", swap_text, body)
        body = re.sub(r'\b(alt|aria-label|placeholder|title)="([^"]*)"', swap_attr, body)
        i18n_js = {k: tr[k] for k in ("Your draft was prepared for download. Nothing has been submitted or signed.", "Nonbinding enrollment draft") if k in tr}
        inject = "<script>window.STARSI_I18N = %s;</script>\n" % json.dumps(i18n_js, ensure_ascii=False)
        out = pre + s1 + css + e1 + body + inject + s3 + tail
        stale = [k for k in tr if k not in used and k not in i18n_js]
    # the page lives one folder down, so asset addresses need to climb back up
    out = re.sub(r'((?:src|href|poster)=")(images|video|icons|designs|fonts)/', r"\1../\2/", out)
    out = re.sub(r'(url\(["\']?)(images|video|icons|fonts)/', r"\1../\2/", out)
    return out, stale


if __name__ == "__main__":
    out = build()
    page_en, _ = localise(out, "en")
    target = os.path.join(HERE, "index.html")
    with open(target, "w", encoding="utf-8") as f:
        f.write(page_en)
    print("Built index.html (%d bytes)" % len(page_en.encode("utf-8")))
    for code in ("es", "ko"):
        page, stale = localise(out, code)
        d = os.path.join(HERE, LANGS[code]["dir"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print("Built %s/index.html (%s)" % (LANGS[code]["dir"], LANGS[code]["name"]))
        for en in stale:
            print("  warning: the English line below changed or is gone, so its %s translation is not used:\n    %s" % (LANGS[code]["name"], en))
    sys.path.insert(0, os.path.join(HERE, "tools"))
    try:
        import design_sync
        design_sync.build_looks()
        n = design_sync.build_design_pages()
        design_sync.build_variant_system_pages()
        print("Built the designs gallery and %d design page(s)" % n)
    except Exception as e:  # never block the site build on the extras
        print("Design pages skipped:", e)
