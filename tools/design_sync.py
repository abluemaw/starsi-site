#!/usr/bin/env python3
"""Keeps DESIGN.md and the site's design variables in step, both ways.

  DESIGN.md  <->  sections/00-tokens.css

Commands
  python3 tools/design_sync.py auto [base]   decide the direction from what changed since `base`
                                             (default: the commit before HEAD). DESIGN.md wins if both changed.
  python3 tools/design_sync.py to-css        DESIGN.md  -> sections/00-tokens.css
  python3 tools/design_sync.py from-css      sections/00-tokens.css -> DESIGN.md
  python3 tools/design_sync.py page          rebuild design/index.html from DESIGN.md

Only the "design values" are synced: colors, effects, typography fonts, spacing, rounded and themes.
The long written parts of DESIGN.md are never touched.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "DESIGN.md")
CSS = os.path.join(ROOT, "sections", "00-tokens.css")
TEMPLATE = os.path.join(ROOT, "design", "template.html")
PAGE = os.path.join(ROOT, "design", "index.html")

SECTIONS = ["colors", "effects", "typography", "spacing", "rounded", "themes"]
# theme role -> css variable
ROLES = {
    "page": "--page-bg", "pageAlt": "--page-alt", "text": "--page-ink", "textMuted": "--page-muted",
    "cardFill": "--card-bg", "line": "--line-soft", "link": "--link-page", "label": "--kicker",
    "ok": "--ok-page", "okBg": "--ok-bg", "navBg": "--nav-bg", "heroGlow": "--hero-glow",
    "headlineFrom": "--headline-from", "headlineMid": "--headline-mid", "headlineTo": "--headline-to",
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
def gen_css(entries):
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
    out = ["/* GENERATED from DESIGN.md. Edit DESIGN.md, or edit a value here: the sync copies it back to DESIGN.md. */"]
    out.append(":root {")
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
    out += theme_block(":root", themes["dark"])
    out.append("/* theme: light (follows the visitor's device) */")
    out.append("@media (prefers-color-scheme: light) {")
    out += theme_block(':root:not([data-theme="dark"])', themes["light"], "  ")
    out.append("}")
    out.append("/* theme: light, forced */")
    out += theme_block(':root[data-theme="light"]', themes["light"])
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
            html.append('      <div class="sw"><div class="chip" style="background:%s"></div><div class="meta"><b>%s</b><span>%s</span></div></div>'
                        % (e["value"], e["path"][1], e["value"]))
        html.append("    </div></div>")
    return "\n".join(html)


def build_page():
    if not os.path.exists(TEMPLATE):
        return False
    _, _, entries = parse_md(read(MD))
    css = gen_css(entries)
    page = read(TEMPLATE).replace("/*TOKENS*/", css).replace("<!--SWATCHES-->", swatches(entries))
    write(PAGE, page)
    return True


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
