#!/usr/bin/env python3
"""260x200 mm grid template: 20 mm pitch, 1 mm line width.

Line centrelines sit on every 20 mm multiple (0, 20, ... 260 / 0, 20, ... 200),
so cell pitch is exactly 20 mm. Centred strokes on the outer edges lose their
outer half to the canvas boundary: outer lines are 0.5 mm visible, inner ones 1 mm.

Outputs:
  grid_260x200_20mm.png  600 dpi raster (6142 x 4724 px), 4x supersampled
  grid_260x200_20mm.svg  vector, real mm units
"""

from pathlib import Path

from PIL import Image, ImageDraw

WIDTH_MM = 260.0
HEIGHT_MM = 200.0
PITCH_MM = 20.0
LINE_MM = 1.0
DPI = 600
SS = 4  # supersampling factor
INK = (0, 0, 0)
PAPER = (255, 255, 255)

HERE = Path(__file__).resolve().parent
PX_PER_MM = DPI / 25.4
HALF = LINE_MM / 2.0


def positions(total_mm: float) -> list[float]:
    n = round(total_mm / PITCH_MM)
    return [i * PITCH_MM for i in range(n + 1)]


def render_png() -> None:
    w = round(WIDTH_MM * PX_PER_MM)
    h = round(HEIGHT_MM * PX_PER_MM)
    img = Image.new("RGB", (w * SS, h * SS), PAPER)
    draw = ImageDraw.Draw(img)
    s = PX_PER_MM * SS
    W, H = w * SS, h * SS

    def band(centre: float) -> tuple[int, int]:
        return round((centre - HALF) * s), round((centre + HALF) * s)

    for x in positions(WIDTH_MM):
        x0, x1 = band(x)
        draw.rectangle((max(x0, 0), 0, min(x1, W) - 1, H - 1), fill=INK)
    for y in positions(HEIGHT_MM):
        y0, y1 = band(y)
        draw.rectangle((0, max(y0, 0), W - 1, min(y1, H) - 1), fill=INK)

    img = img.resize((w, h), Image.LANCZOS)
    out = HERE / "grid_260x200_20mm.png"
    img.save(out, dpi=(DPI, DPI))
    print(f"{out.name}: {w} x {h} px @ {DPI} dpi")


def render_svg() -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{WIDTH_MM:g}mm" height="{HEIGHT_MM:g}mm" '
            f'viewBox="0 0 {WIDTH_MM:g} {HEIGHT_MM:g}">'
        ),
        f'<rect width="{WIDTH_MM:g}" height="{HEIGHT_MM:g}" fill="#fff"/>',
        f'<g fill="#000">',
    ]
    for x in positions(WIDTH_MM):
        x0 = max(x - HALF, 0.0)
        x1 = min(x + HALF, WIDTH_MM)
        parts.append(
            f'<rect x="{x0:g}" y="0" width="{x1 - x0:g}" height="{HEIGHT_MM:g}"/>'
        )
    for y in positions(HEIGHT_MM):
        y0 = max(y - HALF, 0.0)
        y1 = min(y + HALF, HEIGHT_MM)
        parts.append(
            f'<rect x="0" y="{y0:g}" width="{WIDTH_MM:g}" height="{y1 - y0:g}"/>'
        )
    parts.append("</g></svg>")
    out = HERE / "grid_260x200_20mm.svg"
    out.write_text("\n".join(parts) + "\n")
    print(f"{out.name}: {WIDTH_MM:g} x {HEIGHT_MM:g} mm")


if __name__ == "__main__":
    render_png()
    render_svg()
