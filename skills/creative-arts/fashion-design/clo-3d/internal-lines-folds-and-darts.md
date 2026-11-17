---
id: creative-arts.fashion-design.clo-3d.internal-lines-folds-and-darts
name: internal-lines-folds-and-darts
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-pattern-tools, clo-internal-lines, clo-fold-angle, clo-darts, fold-strength, internal-polygon]
level: practitioner
status: draft
description: "Use CLO internal lines and shapes: drawing internal lines and darts, fold angle and fold strength for creases and pleats, and converting internal lines for sewing."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Internal lines, fold lines and darts in CLO

**Goal:** add creases, pleat lines, darts and seam placements inside patterns so the 3D
garment folds and shapes as designed.

## Drawing
- **Internal Polygon/Line** tool (shortcut G in recent versions) draws lines inside a pattern;
  internal rectangles/circles also available.
- Darts: draw the dart as an internal shape, then either cut it out (making a real dart
  opening to sew) or use the dart tool in versions that provide one; sew the dart legs together.
- Offset lines (e.g. topstitch guides, pocket placements) via **Offset as Internal Line**.

## Fold angle and strength
- Select an internal line, open the **Property Editor**: set **Fold Angle** (e.g. 0-360
  degrees: 180 = flat/no fold; smaller values fold one way, larger the other) and
  **Fold Strength**.
- Use for creases (trouser front creases), pleat folds, collar roll lines, cuff folds.
- Combine with the **Fold Arrangement** tool to pre-fold pieces (e.g. folding a collar)
  before simulation.

## Using internal lines for sewing and cutting
- Internal lines can be sewn to (attach pockets, gathers along a line).
- Cut along internal lines to split a pattern (Cut / Cut & Sew).
- Internal lines in DXF imports become internal lines automatically.

## Gotchas
- Fold angle has no effect at very coarse particle distance; refine mesh near folds.
- Too strong folds on soft fabrics look like hard creases.
- Internal lines crossing pattern edges can't be sewn; keep them inside or on edges.

## Verify
- [ ] Creases and pleats fold in the intended direction after simulation.
- [ ] Darts sewn leg to leg and shaping correctly.
- [ ] Internal lines needed for sewing don't cross edges.
