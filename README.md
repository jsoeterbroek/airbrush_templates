# airbrush_templates

## ktemata_grid — 260 × 200 mm calibration grid

20 mm pitch, 1 mm line width, line centrelines on every 20 mm multiple (13 × 10 cells).

- `ktemata_grid/grid_260x200_20mm.svg` — vector, real mm units (exact geometry, print/cut from this)
- `ktemata_grid/grid_260x200_20mm.png` — 6142 × 4724 px @ 600 dpi
- `ktemata_grid/grid_260x200_20mm.py` — generator; regenerate with `python3 ktemata_grid/grid_260x200_20mm.py` (Pillow only)

Outer lines are clipped by the canvas edge, so they show 0.5 mm; all interior lines are 1 mm and pitch is exact to ±0.003 mm.
