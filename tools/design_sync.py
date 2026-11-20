#!/usr/bin/env python3
"""Keeps DESIGN.md and the site's design variables in step, both ways.

  DESIGN.md  <->  sections/00-tokens.css

Commands
  python3 tools/design_sync.py auto [base]   decide the direction from what changed since `base`
                                             (default: the commit before HEAD). DESIGN.md wins if both changed.
  python3 tools/design_sync.py to-css        DESIGN.md  -> sections/00-tokens.css
  python3 tools/design_sync.py from-css      sections/00-tokens.css -> DESIGN.md
  python3 tools/design_sync.py page          rebuild design/index.html, designs/looks/*.css and designs/variants.json
  python3 tools/design_sync.py promote NAME  copy designs/NAME.md into DESIGN.md (make that look live)

Only the "design values" are synced: colors, effects, typography fonts, spacing, rounded and themes.
The long written parts of DESIGN.md are never touched.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "DESIGN.md")
CSS = os.path.join(ROOT, "sections", "00-tokens.css")
TEMPLATE = os.path.join(ROOT, "design", "template.html")
PAGE = os.path.join(ROOT, "design", "index.html")
ICONS = os.path.join(ROOT, "icons")

SECTIONS = ["colors", "effects", "typography", "spacing", "rounded", "themes"]
# theme role -> css variable
ROLES = {
    "page": "--page-bg", "pageAlt": "--page-alt", "text": "--page-ink", "textMuted": "--page-muted",
    "cardFill": "--card-bg", "line": "--line-soft", "link": "--link-page", "label": "--kicker",
    "ok": "--ok-page", "okBg": "--ok-bg", "navBg": "--nav-bg", "heroGlow": "--hero-glow",
    "heading": "--heading", "headlineFrom": "--headline-from", "headlineMid": "--headline-mid", "headlineTo": "--headline-to",
}
FONTS = {"display": "--font-display", "body": "--font-body", "mono": "--font-mono"}


def kebab(k):
    return re.sub(r"([a-z])([A-Z0-9])", r"\1-\2", k).lower()


def camel(name):
    parts = name.lstrip("-").split("-")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


# ---------- DESIGN.md front matter ----------
LEAF = re.compile(r'^(\s*)([A-Za-z0-9_]+):\s*(.*?)\s*$')


def parse_md(text):
    lines = text.split("\n")
    assert lines[0] == "---", "DESIGN.md must start with ---"
    end = lines.index("---", 1)
    entries, section, sub, group = [], None, None, ""
    for i in range(1, end):
        raw = lines[i]
        if not raw.strip():
            continue
        if raw.lstrip().startswith("#"):
            if section == "colors":
                group = raw.lstrip()[1:].strip()
            continue
        m = LEAF.match(raw)
        if not m:
            continue
        indent, key, val = len(m.group(1)), m.group(2), m.group(3)
        if indent == 0:
            section, sub = key, None
            continue
        if section not in SECTIONS:
            continue
        if val == "":
            sub = key
            continue
        quoted = len(val) >= 2 and val[0] == '"' and val[-1] == '"'
        v = val[1:-1] if quoted else val
        if indent == 2 and section in ("colors", "effects", "spacing", "rounded"):
            entries.append({"path": (section, key), "line": i, "value": v, "group": group})
        elif section == "typography" and indent == 4 and key == "fontFamily":
            entries.append({"path": (section, sub, key), "line": i, "value": v, "group": ""})
        elif section == "themes" and indent == 4:
            entries.append({"path": (section, sub, key), "line": i, "value": v, "group": ""})
    return lines, end, entries


def var_for(path):
    s = path[0]
    if s in ("colors", "effects"):
        return "--" + kebab(path[1])
    if s == "spacing":
        return "--space-" + path[1]
    if s == "rounded":
        return "--radius-" + path[1]
    if s == "typography":
        return FONTS.get(path[1])
    return None  # themes handled separately


# ---------- md -> css ----------
def gen_css(entries, scope=None):
    blocks = {"colors": [], "effects": [], "typography": [], "spacing": [], "rounded": []}
    themes = {"dark": {}, "light": {}}
    page = {}
    for e in entries:
        p = e["path"]
        if p[0] == "themes":
            var = ROLES.get(p[2])
            if var and p[1] in themes:
                themes[p[1]][var] = e["value"]
        else:
            v = var_for(p)
            if v:
                blocks[p[0]].append("  %s: %s;" % (v, e["value"]))
    root = ":root" if not scope else ':root[data-look="%s"]' % scope
    if scope:
        out = ["/* look: %s */" % scope]
    else:
        out = ["/* GENERATED from DESIGN.md. Edit DESIGN.md, or edit a value here: the sync copies it back to DESIGN.md. */"]
    out.append(root + " {")
    for name in ("colors", "effects", "typography", "spacing", "rounded"):
        out.append("  /* %s */" % name)
        out.extend(blocks[name])
    out.append("}")

    def theme_block(sel, vals, indent=""):
        lines = [indent + sel + " {"]
        for var in ROLES.values():
            if var in vals:
                lines.append("%s  %s: %s;" % (indent, var, vals[var]))
        lines.append("%s  --text-metal: linear-gradient(180deg, var(--headline-from) 0%%, var(--headline-mid) 55%%, var(--headline-to) 100%%);" % indent)
        lines.append("%s  --hero-bg: radial-gradient(ellipse at 50%% 0%%, var(--hero-glow), var(--page-bg) 70%%);" % indent)
        lines.append("%s}" % indent)
        return lines

    out.append("/* theme: dark (default) */")
    out += theme_block(root, themes["dark"])
    out.append("/* theme: light (follows the visitor's device) */")
    out.append("@media (prefers-color-scheme: light) {")
    out += theme_block(root + ':not([data-theme="dark"])', themes["light"], "  ")
    out.append("}")
    out.append("/* theme: light, forced */")
    out += theme_block(root + '[data-theme="light"]', themes["light"])
    if not scope:
        out.append(':root { color-scheme: dark; } :root[data-theme="light"] { color-scheme: light; }')
        out.append("@media (prefers-color-scheme: light) { :root:not([data-theme=\"dark\"]) { color-scheme: light; } }")
    return "\n".join(out) + "\n"


# ---------- css -> md ----------
DECL = re.compile(r"^\s*(--[a-z0-9-]+):\s*(.+?);\s*$")


def parse_css(text):
    """Returns {var: value} for the primitives, plus light/dark role values."""
    prim, light, dark = {}, {}, {}
    mode = "prim"
    in_media = False
    for line in text.split("\n"):
        t = line.strip()
        if t.startswith("/* theme: dark"):
            mode = "dark"
        elif t.startswith("/* theme: light (follows"):
            mode = "light"
        elif t.startswith("/* theme: light, forced"):
            mode = "light-forced"
        m = DECL.match(line)
        if not m:
            continue
        var, val = m.group(1), m.group(2)
        if mode == "prim":
            prim[var] = val
        elif mode == "dark" and var in ROLES.values():
            dark[var] = val
        elif mode == "light" and var in ROLES.values():
            light[var] = val
        elif mode == "light-forced" and var in ROLES.values():
            light.setdefault(var, val)
    return prim, dark, light


def norm(v):
    return re.sub(r"\s+", " ", v.strip().strip('"')).lower()


def css_to_md(md_text, css_text):
    lines, end, entries = parse_md(md_text)
    prim, dark, light = parse_css(css_text)
    by_var = {}
    for e in entries:
        v = var_for(e["path"])
        if v:
            by_var[v] = e
    role_by_var = {v: k for k, v in ROLES.items()}
    changes = []

    def set_value(e, new):
        line = lines[e["line"]]
        m = LEAF.match(line)
        quoted = '"' in m.group(3)[:1]
        key = m.group(2)
        lines[e["line"]] = '%s%s: "%s"' % (m.group(1), key, new) if quoted or True else line
        changes.append("%s: %s -> %s" % ("/".join(e["path"]), e["value"], new))
        e["value"] = new

    # primitives
    adds = {}
    for var, val in prim.items():
        e = by_var.get(var)
        if e is not None:
            if norm(e["value"]) != norm(val):
                set_value(e, val)
        elif re.match(r"^#[0-9a-fA-F]{3,8}$", val) and not var.startswith(("--space", "--radius")):
            adds[var] = val
    # themes
    for mode, vals in (("dark", dark), ("light", light)):
        for var, val in vals.items():
            role = role_by_var[var]
            e = next((x for x in entries if x["path"] == ("themes", mode, role)), None)
            if e and norm(e["value"]) != norm(val):
                set_value(e, val)
    # brand new colour tokens go at the end of the colors block
    if adds:
        last = max(e["line"] for e in entries if e["path"][0] == "colors")
        new_lines = ['  %s: "%s"' % (camel(v), val) for v, val in adds.items()]
        lines[last + 1:last + 1] = new_lines
        changes += ["new colour %s: %s" % (camel(v), val) for v, val in adds.items()]
    return "\n".join(lines), changes



# ---------- icons ----------
def load_icons():
    """Returns [(name, inner_svg)] from icons/*.svg (sorted)."""
    out = []
    if not os.path.isdir(ICONS):
        return out
    for f in sorted(os.listdir(ICONS)):
        if f.endswith(".svg") and f != "sprite.svg":
            m = re.search(r"<svg[^>]*>(.*)</svg>", read(os.path.join(ICONS, f)), re.S)
            if m:
                out.append((f[:-4], m.group(1).strip()))
    return out


def write_sprite(icons):
    syms = "".join('<symbol id="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</symbol>' % (n, b) for n, b in icons)
    write(os.path.join(ICONS, "sprite.svg"), '<svg xmlns="http://www.w3.org/2000/svg">%s</svg>\n' % syms)


def icon_html(icons):
    return "\n".join('      <div class="icon-tile"><svg class="ic"><use href="#icon-%s"/></svg><b>%s</b></div>' % (n, n.replace("-", " ")) for n, _ in icons)


def icon_sprite_inline(icons):
    syms = "".join('<symbol id="icon-%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</symbol>' % (n, b) for n, b in icons)
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">%s</svg>' % syms


# ---------- design variants ----------
DESIGNS = os.path.join(ROOT, "designs")


def variant_files():
    if not os.path.isdir(DESIGNS):
        return []
    return sorted(f for f in os.listdir(DESIGNS) if f.endswith(".md") and f.lower() != "readme.md")


def merge_entries(base, over):
    merged = [dict(e) for e in base]
    index = {e["path"]: e for e in merged}
    for o in over:
        if o["path"] in index:
            index[o["path"]]["value"] = o["value"]
        elif o["path"][0] == "colors":
            n = dict(o)
            merged.append(n)
            index[n["path"]] = n
    return merged


def meta(text, key):
    m = re.search(r'^%s:\s*"?(.*?)"?\s*$' % key, text, re.M)
    return m.group(1) if m else ""


def build_looks():
    """designs/*.md (only the values that differ) -> designs/looks/<name>.css + designs/variants.json"""
    import json
    _, _, base = parse_md(read(MD))
    picker = meta(read(MD), "lookPicker").lower() != "off"
    listing = []
    looks_dir = os.path.join(DESIGNS, "looks")
    os.makedirs(looks_dir, exist_ok=True)
    keep = set()
    for f in variant_files():
        slug = f[:-3]
        text = read(os.path.join(DESIGNS, f))
        _, _, over = parse_md(text)
        merged = merge_entries(base, over)
        fonts, stretch = meta(text, "fontsUrl"), meta(text, "headingStretch")
        css = []
        if fonts:
            css.append('@import url("%s");' % fonts)
        css.append("/* GENERATED from designs/%s.md. Do not edit. */" % slug)
        css.append(gen_css(merged, scope=slug))
        if stretch:
            sel = ",".join(':root[data-look="%s"] %s' % (slug, t) for t in ("h1", "h2", "h3"))
            css.append("%s { font-stretch: %s; }" % (sel, stretch))
        write(os.path.join(looks_dir, slug + ".css"), "\n".join(css) + "\n")
        keep.add(slug + ".css")
        col = {e["path"][1]: e["value"] for e in merged if e["path"][0] == "colors"}
        listing.append({"slug": slug, "name": meta(text, "name") or slug, "description": meta(text, "description"),
                        "swatches": [col.get("gold400", ""), col.get("night", ""), col.get("electric500", "")]})
    for f in os.listdir(looks_dir):
        if f.endswith(".css") and f not in keep:
            os.remove(os.path.join(looks_dir, f))
    old = os.path.join(DESIGNS, "looks.css")
    if os.path.exists(old):
        os.remove(old)
    write(os.path.join(DESIGNS, "variants.json"), json.dumps({"picker": picker, "variants": listing}, indent=1) + "\n")
    return len(listing)


def do_promote(name):
    slug = name[:-3] if name.endswith(".md") else name
    path = os.path.join(DESIGNS, slug + ".md")
    if not os.path.exists(path):
        print("No design called '%s' in designs/." % slug)
        return 1
    _, _, base = parse_md(read(MD))
    _, _, over = parse_md(read(path))
    new_md, changes = css_to_md(read(MD), gen_css(merge_entries(base, over)))
    if not changes:
        print("DESIGN.md already matches '%s'." % slug)
    else:
        write(MD, new_md)
        print("Made '%s' the live design:" % slug)
        for c in changes:
            print("  " + c)
    do_to_css()
    return 0


# ---------- design pages (gallery + one full page per design) ----------
def rebase(html, up):
    return re.sub(r'(["\'(])(images|fonts|designs|icons)/', lambda m: m.group(1) + up + m.group(2) + "/", html)


def build_design_pages():
    """designs/index.html (gallery) and designs/<name>/index.html (the full site wearing that look)."""
    import html as H, json
    idx = os.path.join(ROOT, "index.html")
    if not os.path.exists(idx):
        return 0
    site = read(idx)
    data = json.load(open(os.path.join(DESIGNS, "variants.json")))
    # one page per design
    for v in data["variants"]:
        slug, name = v["slug"], v["name"]
        page = site.replace('<html lang="en">', '<html lang="en" data-look="%s">' % slug, 1)
        a = page.find("var q=new URLSearchParams")
        b = page.find("}catch(e){}</script>", a)
        if a != -1 and b != -1:
            page = page[:a] + 'r.setAttribute("data-look","%s");var k=document.createElement("link");k.rel="stylesheet";k.href="designs/looks/%s.css";document.head.appendChild(k)' % (slug, slug) + page[b:]
        page = re.sub(r"<title>(.*?)</title>", lambda m: "<title>%s | %s</title>" % (m.group(1), H.escape(name)), page, 1)
        page = page.replace("</head>", "<style>.look-picker{display:none!important}.look-badge{position:fixed;left:16px;bottom:16px;z-index:40;font:600 13px var(--font-body);color:var(--page-ink);background:var(--card-bg);border:1px solid var(--line-soft);border-radius:var(--radius-md);padding:8px 12px;box-shadow:var(--card-shadow)}.look-badge:hover{border-color:var(--page-muted)}</style>\n</head>", 1)
        page = page.replace("</body>", '<a class="look-badge" href="../">Design: %s &middot; all designs</a>\n</body>' % H.escape(name), 1)
        page = rebase(page, "../../")
        out = os.path.join(DESIGNS, slug)
        os.makedirs(out, exist_ok=True)
        write(os.path.join(out, "index.html"), page)
    # gallery
    tpl = os.path.join(ROOT, "design", "gallery-template.html")
    if os.path.exists(tpl):
        _, _, entries = parse_md(read(MD))
        col = {e["path"][1]: e["value"] for e in entries if e["path"][0] == "colors"}
        cards = []

        def card(slug, name, desc, dots, page, shot, live=False):
            d = "".join('<i style="background:%s"></i>' % c for c in dots if c)
            tag = '<span class="tag">Live design</span>' if live else ""
            return ('    <div class="card%s"><a class="shot" href="%s"><img src="img/%s.jpg" alt="The site in %s" loading="lazy" onerror="this.remove()"></a>'
                    '<div class="body">%s<h2>%s</h2><div class="dots">%s</div><p>%s</p>'
                    '<div class="row"><a class="go" href="%s">Open page</a><a href="%s">Design system</a><a href="../?design=%s">Try on the site</a></div></div></div>'
                    % (" live" if live else "", page, shot, H.escape(name), tag, H.escape(name), d, H.escape(desc), page, ("../design/" if live else slug + "/system/"), slug if not live else "live"))
        cards.append(card("live", "Live design", "The shared design in DESIGN.md that everyone sees right now.", [col.get("gold400"), col.get("night"), col.get("electric500")], "../", "live", True))
        for v in data["variants"]:
            cards.append(card(v["slug"], v["name"], v.get("description", ""), v.get("swatches", []), v["slug"] + "/", v["slug"]))
        html = read(tpl).replace("/*TOKENS*/", gen_css(entries)).replace("<!--CARDS-->", "\n".join(cards))
        write(os.path.join(DESIGNS, "index.html"), html)
    return len(data["variants"])

# ---------- design page ----------
def swatches(entries):
    groups, order = {}, []
    for e in entries:
        if e["path"][0] != "colors":
            continue
        g = e["group"] or "Colours"
        if g not in groups:
            groups[g] = []
            order.append(g)
        groups[g].append(e)
    html = []
    for g in order:
        html.append('    <div class="sw-group"><h3>%s</h3><div class="sw-row">' % g)
        for e in groups[g]:
            html.append('      <div class="sw"><div class="chip" style="background:var(--%s)"></div><div class="meta"><b>%s</b><span data-var="--%s">%s</span></div></div>'
                        % (kebab(e["path"][1]), e["path"][1], kebab(e["path"][1]), e["value"]))
        html.append("    </div></div>")
    return "\n".join(html)


def render_page(entries, icons):
    css = gen_css(entries)
    fam = {e["path"][1]: e["value"].split(",")[0].strip().strip("'\"") for e in entries if e["path"][0] == "typography"}
    return (read(TEMPLATE).replace("<!--FONT-DISPLAY-->", fam.get("display", "")).replace("<!--FONT-BODY-->", fam.get("body", ""))
            .replace("/*TOKENS*/", css).replace("<!--SWATCHES-->", swatches(entries))
            .replace("<!--ICONS-->", icon_html(icons)).replace("<!--ICON-SPRITE-->", icon_sprite_inline(icons)))


def build_page():
    build_looks()
    if not os.path.exists(TEMPLATE):
        return False
    _, _, entries = parse_md(read(MD))
    icons = load_icons()
    write_sprite(icons)
    write(PAGE, render_page(entries, icons))
    return True


def build_variant_system_pages():
    """designs/<name>/system/index.html: the design system page for each variant, built from its merged values."""
    import html as H, json
    if not os.path.exists(TEMPLATE) or not os.path.isdir(DESIGNS):
        return 0
    _, _, base = parse_md(read(MD))
    icons = load_icons()
    n = 0
    for f in variant_files():
        slug = f[:-3]
        text = read(os.path.join(DESIGNS, f))
        name = meta(text, "name") or slug
        _, _, over = parse_md(text)
        page = render_page(merge_entries(base, over), icons)
        page = page.replace("/*FIXED*/false", "true")
        fonts, stretch = meta(text, "fontsUrl"), meta(text, "headingStretch")
        if fonts:
            page = page.replace("</head>", '<link rel="stylesheet" href="%s">\n</head>' % fonts, 1)
        if stretch:
            page = page.replace("</head>", "<style>h1,h2,h3{font-stretch:%s}</style>\n</head>" % stretch, 1)
        page = page.replace("<title>StarSI Gold | Design system</title>", "<title>%s | Design system</title>" % H.escape(name))
        page = page.replace('<div class="kicker">Design system</div>\n    <h1 class="metal-text">StarSI Gold</h1>',
                            '<div class="kicker">Design system &middot; a variant of the live design</div>\n    <h1 class="metal-text">%s</h1>' % H.escape(name))
        page = page.replace("StarSI Gold · built from DESIGN.md", "%s · built from designs/%s.md on top of DESIGN.md" % (H.escape(name), slug))
        page = page.replace("Everything on this page comes from <b>DESIGN.md</b>.", "Everything on this page comes from <b>designs/%s.md</b>, on top of the live <b>DESIGN.md</b>." % slug)
        page = page.replace('<a href="https://github.com/abluemaw/starsi-site/blob/main/DESIGN.md">Open DESIGN.md</a>',
                            '<a href="https://github.com/abluemaw/starsi-site/blob/main/designs/%s.md">Open %s.md</a>' % (slug, slug))
        page = re.sub(r'(["\'(])\.\./', lambda m: m.group(1) + "../../../", page)
        page = page.replace('<a href="../../../">The site</a>', '<a href="../">This design on the site</a> &middot; <a href="../../../">The live site</a>')
        out = os.path.join(DESIGNS, slug, "system")
        os.makedirs(out, exist_ok=True)
        write(os.path.join(out, "index.html"), page)
        n += 1
    return n


# ---------- commands ----------
def changed_files(base):
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"], text=True, cwd=ROOT)
    except subprocess.CalledProcessError:
        out = ""
    return set(out.split())


def do_to_css():
    _, _, entries = parse_md(read(MD))
    new = gen_css(entries)
    old = read(CSS) if os.path.exists(CSS) else ""
    if new != old:
        write(CSS, new)
        print("DESIGN.md -> sections/00-tokens.css (updated)")
        return True
    print("sections/00-tokens.css already matches DESIGN.md")
    return False


def do_from_css():
    new_md, changes = css_to_md(read(MD), read(CSS))
    if changes:
        write(MD, new_md)
        print("sections/00-tokens.css -> DESIGN.md:")
        for c in changes:
            print("  " + c)
    else:
        print("DESIGN.md already matches sections/00-tokens.css")
    do_to_css()   # normalise the css file from the updated DESIGN.md
    return bool(changes)


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "auto"
    if cmd == "to-css":
        do_to_css()
    elif cmd == "from-css":
        do_from_css()
    elif cmd == "page":
        pass
    elif cmd == "promote":
        if len(argv) < 3:
            print("Usage: design_sync.py promote <name>")
            return 1
        rc = do_promote(argv[2])
        if rc:
            return rc
    elif cmd == "auto":
        base = argv[2] if len(argv) > 2 else "HEAD~1"
        files = changed_files(base)
        md_changed = "DESIGN.md" in files
        css_changed = "sections/00-tokens.css" in files
        if not os.path.exists(CSS) or md_changed:
            if css_changed:
                print("Both changed: DESIGN.md wins.")
            do_to_css()
        elif css_changed:
            do_from_css()
        else:
            print("No design change.")
    else:
        print(__doc__)
        return 1
    if build_page():
        print("design/index.html rebuilt")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
