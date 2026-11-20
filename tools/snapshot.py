#!/usr/bin/env python3
"""Adds one picture of the site to the version history.

Usage:  python3 tools/snapshot.py <commit code or saved name>
It builds a picture of the site exactly as it was at that commit, saves a small
thumbnail and a full-page image in versions/img/, and lists it in versions/versions.json.
GitHub runs this by itself after every change (see .github/workflows/snapshot.yml).
"""
import functools, http.server, json, os, shutil, subprocess, sys, tempfile, threading
from PIL import Image
from playwright.sync_api import sync_playwright

KEEP = 80          # how many versions to keep pictures of
VDIR = "versions"
JSON = os.path.join(VDIR, "versions.json")


def git(*args, cwd=None):
    return subprocess.check_output(["git", *args], text=True, cwd=cwd).strip()


def main(ref):
    sha = git("rev-parse", ref + "^{commit}")
    short = sha[:7]
    os.makedirs(os.path.join(VDIR, "img"), exist_ok=True)
    data = json.load(open(JSON)) if os.path.exists(JSON) else []
    if any(e["sha"] == sha for e in data):
        print("Already in the history:", short)
        return

    # who changed it, and what they said: skip the automatic "Rebuild" commits
    who, say = "", ""
    for line in git("log", "-8", "--format=%an%x1f%s", sha).splitlines():
        a, s = line.split("\x1f", 1)
        if not s.startswith("Rebuild index.html"):
            who, say = a, s
            break
    date = git("log", "-1", "--format=%cI", sha)

    tmp = tempfile.mkdtemp()
    work = os.path.join(tmp, "site")
    git("worktree", "add", "--detach", work, sha)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=work)
    handler.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/index.html" % srv.server_address[1]
    png = os.path.join(tmp, "full.png")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--no-sandbox"])
            page = b.new_page(viewport={"width": 1280, "height": 800})
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=png, full_page=True)
            b.close()
    finally:
        srv.shutdown()
        git("worktree", "remove", "--force", work)

    im = Image.open(png).convert("RGB")
    w, h = im.size
    full = im.resize((1000, max(1, round(h * 1000 / w))), Image.LANCZOS)
    full.save(os.path.join(VDIR, "img", short + ".jpg"), quality=72, optimize=True)
    top = im.crop((0, 0, w, min(h, round(w * 0.85))))
    top = top.resize((480, max(1, round(top.size[1] * 480 / w))), Image.LANCZOS)
    top.save(os.path.join(VDIR, "img", short + "-thumb.jpg"), quality=78, optimize=True)

    data.append({"sha": sha, "short": short, "date": date, "author": who, "message": say})
    data.sort(key=lambda e: e["date"], reverse=True)
    for old in data[KEEP:]:
        for suffix in (".jpg", "-thumb.jpg"):
            f = os.path.join(VDIR, "img", old["short"] + suffix)
            if os.path.exists(f):
                os.remove(f)
    data = data[:KEEP]
    with open(JSON, "w") as f:
        json.dump(data, f, indent=1)
    print("Added", short, "-", say)


if __name__ == "__main__":
    for r in sys.argv[1:]:
        main(r)
