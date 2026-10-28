"""Draws the home-screen icons for the 保客填表 web app into icons/.

A cream form sheet with 保 and two ticked boxes on deep green.
Run once (or after changing the design):  python web/make_icons.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "icons"
GREEN, CREAM, INK, TICK = "#1F4E3D", "#F6F1E7", "#1F4E3D", "#2F8A5E"
FONT = "C:/Windows/Fonts/msyhbd.ttc"
S = 1024  # drawn large, then scaled down


def draw(scale):
    """scale = share of the canvas the sheet may use (maskable icons need a safe zone)."""
    img = Image.new("RGB", (S, S), GREEN)
    d = ImageDraw.Draw(img)
    w, h = S * 0.62 * scale, S * 0.76 * scale
    x0, y0 = (S - w) / 2, (S - h) / 2
    r = w * 0.08
    d.rounded_rectangle((x0 + w * 0.03, y0 + w * 0.04, x0 + w * 1.03, y0 + h + w * 0.04), r, fill="#163A2D")  # shadow
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), r, fill=CREAM)
    font = ImageFont.truetype(FONT, int(w * 0.56))
    d.text((S / 2, y0 + h * 0.33), "保", font=font, fill=INK, anchor="mm")
    # two ticked boxes with lines, like the form's checkboxes
    b = w * 0.13
    for i in range(2):
        by = y0 + h * (0.64 + i * 0.17)
        bx = x0 + w * 0.14
        d.rounded_rectangle((bx, by, bx + b, by + b), b * 0.18, outline=INK, width=max(3, int(b * 0.12)))
        d.line([(bx + b * 0.2, by + b * 0.52), (bx + b * 0.42, by + b * 0.76), (bx + b * 0.86, by + b * 0.22)],
               fill=TICK, width=max(4, int(b * 0.18)), joint="curve")
        d.rounded_rectangle((bx + b * 1.45, by + b * 0.36, x0 + w * 0.86, by + b * 0.64), b * 0.14, fill="#C9BFA9")
    return img


def main():
    OUT.mkdir(exist_ok=True)
    full, safe = draw(1.0), draw(0.78)
    for size in (512, 192):
        full.resize((size, size), Image.LANCZOS).save(OUT / f"icon-{size}.png")
        safe.resize((size, size), Image.LANCZOS).save(OUT / f"maskable-{size}.png")
    full.resize((180, 180), Image.LANCZOS).save(OUT / "apple-touch-icon.png")
    full.resize((64, 64), Image.LANCZOS).save(OUT / "favicon.png")
    print("icons written to", OUT)


if __name__ == "__main__":
    main()
