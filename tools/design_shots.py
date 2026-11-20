#!/usr/bin/env python3
"""Takes a picture of the site in every design for the gallery (designs/img/<name>.jpg).

Run after build.py:  python3 tools/design_shots.py
GitHub runs it by itself (see .github/workflows/snapshot.yml).
"""
import functools, http.server, json, os, threading
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "designs", "img")


def main():
    os.makedirs(OUT, exist_ok=True)
    data = json.load(open(os.path.join(ROOT, "designs", "variants.json")))
    pages = [("live", "index.html")] + [(v["slug"], "designs/%s/index.html" % v["slug"]) for v in data["variants"]]
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    handler.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d/" % srv.server_address[1]
    keep = {s + ".jpg" for s, _ in pages}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--no-sandbox"])
            for slug, path in pages:
                ctx = b.new_context(viewport={"width": 1280, "height": 880}, color_scheme="dark")
                page = ctx.new_page()
                page.goto(base + path, wait_until="networkidle")
                page.wait_for_timeout(1200)
                tmp = os.path.join(OUT, slug + ".png")
                page.screenshot(path=tmp)
                im = Image.open(tmp).convert("RGB")
                im = im.resize((480, round(im.size[1] * 480 / im.size[0])), Image.LANCZOS)
                im.save(os.path.join(OUT, slug + ".jpg"), quality=78, optimize=True)
                os.remove(tmp)
                ctx.close()
                print("shot", slug)
            b.close()
    finally:
        srv.shutdown()
    for f in os.listdir(OUT):          # drop pictures of designs that no longer exist
        if f.endswith(".jpg") and f not in keep:
            os.remove(os.path.join(OUT, f))


if __name__ == "__main__":
    main()
