#!/usr/bin/env python3
"""Airbrush holding grid: 260 x 200 mm grid area, 20 mm pitch, 1 mm lines,
white on black, surrounded by HOLD_MM of plain margin on all four sides.

Line centrelines sit on every 20 mm multiple of the grid area, so cell pitch is
exactly 20 mm. The margin is plain background: grid lines are clipped to the
grid rectangle, which the outer strokes close off, so the inked grid measures
261 x 201 mm (0.5 mm of stroke past the nominal 260 x 200 mm on each side).

Raster is drawn with analytic per-pixel coverage (no supersampling): each pixel
column/row gets its exact overlap with the line band, so 1 mm stays 1 mm at any
DPI instead of snapping to whole pixels.

Outputs:
  grid_260x200_20mm_hold25mm.svg  vector, real mm units
  grid_260x200_20mm_hold25mm.png  600 dpi raster
"""

from pathlib import Path

import numpy as np
from PIL import Image

GRID_W_MM = 260.0
GRID_H_MM = 200.0
PITCH_MM = 20.0
LINE_MM = 1.0
HOLD_MM = 25.0
DPI = 600

PAPER = (0, 0, 0)  # background
INK = (255, 255, 255)  # grid lines

HERE = Path(__file__).resolve().parent
WIDTH_MM = GRID_W_MM + 2 * HOLD_MM
HEIGHT_MM = GRID_H_MM + 2 * HOLD_MM
NAME = f"grid_{GRID_W_MM:g}x{GRID_H_MM:g}_{PITCH_MM:g}mm_hold{HOLD_MM:g}mm"
HALF = LINE_MM / 2.0

# Inked grid rectangle: nominal grid area grown by half a stroke so the corners
# close square. Everything outside this box stays background (the hold margin).
INK_X0, INK_X1 = HOLD_MM - HALF, HOLD_MM + GRID_W_MM + HALF
INK_Y0, INK_Y1 = HOLD_MM - HALF, HOLD_MM + GRID_H_MM + HALF


def centre_lines(span_mm: float) -> list[float]:
    n = round(span_mm / PITCH_MM)
    return [HOLD_MM + i * PITCH_MM for i in range(n + 1)]


def band_coverage(lo_mm: float, hi_mm: float, n_px: int, s: float) -> np.ndarray:
    """Fraction of each pixel covered by the mm interval [lo_mm, hi_mm)."""
    lo = (np.arange(n_px) / s)[:, None]  # pixel left edge, mm
    hi = lo + 1.0 / s
    overlap = np.clip(np.minimum(hi, hi_mm) - np.maximum(lo, lo_mm), 0.0, 1.0 / s)
    return np.clip(overlap[:, 0] * s, 0.0, 1.0)


def coverage(centres: list[float], n_px: int, s: float) -> np.ndarray:
    """Fraction of each pixel covered by the union of 1 mm bands centred on `centres`."""
    bands = [band_coverage(c - HALF, c + HALF, n_px, s) for c in centres]
    return np.clip(np.max(bands, axis=0), 0.0, 1.0)


def render_png() -> None:
    s = DPI / 25.4
    w, h = round(WIDTH_MM * s), round(HEIGHT_MM * s)
    v = coverage(centre_lines(GRID_W_MM), w, s).astype(np.float32)  # per column
    hz = coverage(centre_lines(GRID_H_MM), h, s).astype(np.float32)  # per row
    # Each stroke is bounded by the grid rectangle, so the hold margin stays plain.
    xext = band_coverage(INK_X0, INK_X1, w, s).astype(np.float32)
    yext = band_coverage(INK_Y0, INK_Y1, h, s).astype(np.float32)
    alpha = np.outer(yext, v)
    np.maximum(alpha, np.outer(hz, xext), out=alpha)  # union of both stroke sets
    grey = np.rint(np.float32(PAPER[0]) + np.float32(INK[0] - PAPER[0]) * alpha)
    img = Image.fromarray(grey.astype(np.uint8)).convert("RGB")
    out = HERE / f"{NAME}.png"
    img.save(out, dpi=(DPI, DPI))
    print(f"{out.name}: {w} x {h} px @ {DPI} dpi, {WIDTH_MM:g} x {HEIGHT_MM:g} mm")


def render_svg() -> None:
    rects = []
    for x in centre_lines(GRID_W_MM):
        rects.append(
            f'<rect x="{x - HALF:g}" y="{INK_Y0:g}" width="{LINE_MM:g}" '
            f'height="{INK_Y1 - INK_Y0:g}"/>'
        )
    for y in centre_lines(GRID_H_MM):
        rects.append(
            f'<rect x="{INK_X0:g}" y="{y - HALF:g}" width="{INK_X1 - INK_X0:g}" '
            f'height="{LINE_MM:g}"/>'
        )
    svg = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{WIDTH_MM:g}mm" height="{HEIGHT_MM:g}mm" '
                f'viewBox="0 0 {WIDTH_MM:g} {HEIGHT_MM:g}">'
            ),
            f'<rect width="{WIDTH_MM:g}" height="{HEIGHT_MM:g}" fill="#000"/>',
            f'<g fill="#fff">',
            *rects,
            "</g></svg>",
        ]
    )
    out = HERE / f"{NAME}.svg"
    out.write_text(svg + "\n")
    print(f"{out.name}: {WIDTH_MM:g} x {HEIGHT_MM:g} mm")


if __name__ == "__main__":
    render_png()
    render_svg()
