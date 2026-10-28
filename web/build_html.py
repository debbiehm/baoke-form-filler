"""Builds the single-file web app 保客填表.html from web/template.html.

Embeds the blank form, the box positions (layout.py + boxes.py, measured from the PDF)
and the JS libraries, so the HTML works offline and no client data leaves the computer.
Run again only if the form PDF or layout.py changes:  python web/build_html.py
"""
import base64
import json
import sys
from pathlib import Path

import pymupdf

WEB = Path(__file__).resolve().parent
sys.path.insert(0, str(WEB.parent))
import layout as L  # noqa: E402
from boxes import find_strips  # noqa: E402

FORM = WEB.parent / "form" / f"{L.FORM_CODE}.pdf"
OUT = WEB.parent / "保客填表.html"
PAGES = WEB.parent / "index.html"
DIST = WEB / "dist"
DIST_OUT = DIST / "baoke-app.html"


def js(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def main():
    doc = pymupdf.open(FORM)
    if L.FORM_CODE not in doc[0].get_text():
        sys.exit(f"{FORM} is not form {L.FORM_CODE}")
    strips = {i + 1: [[round(s.x0, 2), round(s.y0, 2), round(s.x1, 2), round(s.y1, 2),
                       [[round(a, 2), round(b, 2)] for a, b in s.cells]] for s in find_strips(doc[i])]
              for i in range(5)}
    layout = {k: getattr(L, k) for k in ("FORM_CODE", "HEADER", "OWNER", "RELATIONSHIPS", "NOMINEES", "PART1_SIGN",
                                         "WITNESS_P3", "PART2_OPTIONS", "TRUSTEES", "PART2_SIGN", "WITNESS_P5")}
    def read(f):
        # U+FFFD only appears inside the libraries' string literals; the escape keeps the file plain text
        return ((WEB / "vendor" / f).read_text(encoding="utf-8").replace("</script", "<\\/script")
                .replace("�", "\\ufffd"))
    vendor = "\n;\n".join(read(f) for f in ("pdf-lib.min.js", "xlsx.full.min.js", "jszip.min.js", "pdf.min.js"))
    html = (WEB / "template.html").read_text(encoding="utf-8")
    html = (html.replace("/*__VENDOR__*/", vendor)
                .replace("/*__PDF_WORKER__*/", read("pdf.worker.min.js"))
                .replace("/*__LAYOUT__*/null", js(layout))
                .replace("/*__STRIPS__*/null", js(strips))
                .replace("/*__FORM_B64__*/", base64.b64encode(FORM.read_bytes()).decode()))
    OUT.write_text(html, encoding="utf-8")
    # same app, served by GitHub Pages as an installable app (manifest.webmanifest, sw.js, icons/)
    head = "<title>保客填表</title>"
    assert html.count(head) == 1
    PAGES.write_text(html.replace(head, head + "\n" + "\n".join((
        '<link rel="manifest" href="manifest.webmanifest">',
        '<link rel="icon" type="image/png" href="icons/favicon.png">',
        '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">'))), encoding="utf-8")
    print(f"Built {OUT} + {PAGES.name} ({OUT.stat().st_size / 1e6:.1f} MB)")
    # phone link version (claude.ai artifact): the host adds doctype/html/head/body itself
    body = html
    for tag in ("<!doctype html>", '<html lang="zh-CN">', "<head>", '<meta charset="utf-8">',
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
                "</head>", "<body>", "</body>", "</html>"):
        assert body.count(tag + "\n") == 1, tag
        body = body.replace(tag + "\n", "")
    DIST.mkdir(exist_ok=True)
    DIST_OUT.write_text(body, encoding="utf-8")
    print(f"Built {DIST_OUT}")


if __name__ == "__main__":
    main()
