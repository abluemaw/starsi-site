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
    out = head + "<style>\n" + css + "</style>\n<link rel=\"stylesheet\" href=\"designs/looks.css\">\n</head>\n<body id=\"top\">\n\n" + body
    if js:
        out += "<script>\n" + js + "</script>\n"
    out += "\n</body>\n</html>\n"
    return out


if __name__ == "__main__":
    out = build()
    target = os.path.join(HERE, "index.html")
    with open(target, "w", encoding="utf-8") as f:
        f.write(out)
    print("Built index.html (%d bytes)" % len(out.encode("utf-8")))
    sys.path.insert(0, os.path.join(HERE, "tools"))
    try:
        import design_sync
        design_sync.build_looks()
        n = design_sync.build_design_pages()
        design_sync.build_variant_system_pages()
        print("Built the designs gallery and %d design page(s)" % n)
    except Exception as e:  # never block the site build on the extras
        print("Design pages skipped:", e)
