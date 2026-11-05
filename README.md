# airbrush_templates

## ktemata_grid — 260 × 200 mm grid, white on black, 25 mm hold margin

Grid area 260 × 200 mm, 20 mm pitch, 1 mm line width (13 × 10 cells), with 25 mm of
plain margin on all four sides to hold while spraying. Sheet total: 310 × 250 mm.

- `ktemata_grid/grid_260x200_20mm_hold25mm.svg` — vector, real mm units (exact geometry, print/cut from this)
- `ktemata_grid/grid_260x200_20mm_hold25mm.png` — 7323 × 5906 px @ 600 dpi, inked lines on black
- `ktemata_grid/grid_260x200_20mm_hold25mm.py` — generator; `python3 ktemata_grid/grid_260x200_20mm_hold25mm.py`

Dimensions and colours are constants at the top of the generator (`GRID_W_MM`, `GRID_H_MM`,
`PITCH_MM`, `LINE_MM`, `HOLD_MM`, `DPI`, `PAPER`, `INK`).

Line centrelines sit on every 20 mm multiple of the grid area (25, 45, … 285 mm), so the pitch
is exact. Strokes are clipped to the grid rectangle — the 25 mm hold margin is plain background.
Vertical strokes run 201 mm and horizontal strokes 261 mm (0.5 mm past the nominal grid area on
each side) so the outer border closes square at full 1 mm width.
