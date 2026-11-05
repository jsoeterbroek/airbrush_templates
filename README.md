# airbrush_templates

## ktemata_grid — 260 × 200 mm grid, white lines on black, white hold margin

Grid area 260 × 200 mm, 20 mm pitch, 1 mm line width (13 × 10 cells), with 25 mm of
plain white margin on all four sides to hold while spraying. Sheet total: 310 × 250 mm.

- `ktemata_grid/grid_260x200_20mm_hold25mm.svg` — vector, real mm units (exact geometry, print/cut from this)
- `ktemata_grid/grid_260x200_20mm_hold25mm.png` — 7323 × 5906 px @ 600 dpi
- `ktemata_grid/grid_260x200_20mm_hold25mm.py` — generator; `python3 ktemata_grid/grid_260x200_20mm_hold25mm.py`

Dimensions and colours are constants at the top of the generator (`GRID_W_MM`, `GRID_H_MM`,
`PITCH_MM`, `LINE_MM`, `HOLD_MM`, `DPI`, `MARGIN`, `FIELD`, `INK`).

Line centrelines sit on every 20 mm multiple of the grid area (25, 45, … 285 mm), so the pitch
is exact. Strokes are confined to the grid rectangle — the 25 mm hold margin is plain white.
Vertical strokes run 201 mm and horizontal strokes 261 mm (0.5 mm past the nominal grid area on
each side) so the border closes square at full 1 mm width.

Because the margin is white and so are the lines, the outer 1 mm border is invisible where it
meets the margin: the visible black field measures 259 × 199 mm (inner face of the border). The
border centrelines are still exactly at 25 and 285 / 225 mm, which is what defines the 260 × 200 mm
grid area.
