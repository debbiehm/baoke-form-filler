"""Finds the character boxes on the Great Eastern nomination form.

The form is a flat PDF (no fillable fields). Each row of boxes is drawn as an
outer rectangle plus vertical divider lines, so cells = rectangle edges +
dividers inside it.
"""
from collections import namedtuple

Strip = namedtuple("Strip", "page x0 y0 x1 y1 cells")  # cells = [(x0, x1), ...]


def find_strips(page):
    rects, vlines = [], []
    for dr in page.get_drawings():
        for it in dr["items"]:
            if it[0] == "re":
                r = it[1]
                if 9 < r.height < 22 and r.width > 9:
                    rects.append(r)
            elif it[0] == "l":
                a, b = it[1], it[2]
                if abs(a.x - b.x) < 0.5 and abs(a.y - b.y) > 6:
                    vlines.append((a.x, min(a.y, b.y), max(a.y, b.y)))
    strips, seen = [], set()
    for r in rects:
        key = (round(r.x0), round(r.y0), round(r.x1), round(r.y1))
        if key in seen:
            continue
        seen.add(key)
        mid = (r.y0 + r.y1) / 2
        xs = sorted({round(x, 1) for x, y0, y1 in vlines if r.x0 + 1 < x < r.x1 - 1 and y0 - 1 <= mid <= y1 + 1})
        bounds = [r.x0, *xs, r.x1]
        cells = [(a, b) for a, b in zip(bounds, bounds[1:]) if b - a > 4]
        strips.append(Strip(page.number, r.x0, r.y0, r.x1, r.y1, cells))
    strips.sort(key=lambda s: (s.y0, s.x0))
    return strips


def strip_at(strips, x, y):
    """The smallest strip containing point (x, y), or None (page frames also count as strips)."""
    hits = [s for s in strips if s.x0 - 1 <= x <= s.x1 + 1 and s.y0 - 1 <= y <= s.y1 + 1]
    return min(hits, key=lambda s: (s.x1 - s.x0) * (s.y1 - s.y0)) if hits else None


if __name__ == "__main__":
    import sys
    import pymupdf
    doc = pymupdf.open(sys.argv[1])
    for p in doc:
        if p.number > 4:
            break
        print(f"===== page {p.number + 1}")
        for s in find_strips(p):
            w = (s.x1 - s.x0) / max(len(s.cells), 1)
            print(f"  y {s.y0:6.1f}-{s.y1:6.1f}  x {s.x0:6.1f}-{s.x1:6.1f}  cells={len(s.cells):2d}  w~{w:4.1f}")
