---
id: creative-arts.graphic-design.editorial-layout.modular-grid-fields-from-line-count
name: modular-grid-fields-from-line-count
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, grid-system, modular-grid, grid-fields, baseline-grid, muller-brockmann, swiss-style, type-area, indesign-create-guides]
level: advanced
status: draft
description: "Construct a Muller-Brockmann modular grid: derive field heights from whole lines of text, one-line field gaps, cap-height alignment, and set it up with InDesign Create Guides."
sources:
  - https://www.niggli.ch/en/produkt/grid-systems-in-graphic-design/
  - https://helpx.adobe.com/indesign/using/ruler-guides.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modular grid fields from line count

**Goal:** a modular grid whose fields (modules) align exactly with lines of body text, so images, captions
and text tops and bottoms all line up (Muller-Brockmann, Grid Systems in Graphic Design).

## Method
1. **Fix the body text first:** size and leading, e.g. 9/12 pt. The leading (12 pt) is the base unit.
2. **Type area height** must be a whole number of lines: e.g. 59 lines x 12 pt = 708 pt.
3. **Choose fields vertically** (e.g. 4, 6 or 8 rows). Gaps between fields are **one line** (sometimes two).
   Solve: rows x L + (rows - 1) x gap = total lines. 59 lines, 4 rows, gap 1 -> 4L + 3 = 59 -> L = 14 lines
   per field. If it does not divide, adjust total lines (top/bottom margin) until it does.
4. **Columns horizontally:** column count and gutter (gutter often equals the vertical gap or about one
   line height). Fields are then columns x rows rectangles.
5. **Alignment detail:** the top of each field aligns with the **cap height** of the first text line in it
   and the bottom with the **baseline** of the last line. So an image placed in a field lines up with text
   tops and bases next to it. Field top = baseline of first line minus cap height.

## Set up in InDesign
- Document: margins chosen so the type area height = N x leading.
- Preferences > Grids: baseline grid start = top margin (relative to top margin), increment = leading.
- Layout > Margins and Columns: columns and gutter.
- Layout > **Create Guides**: Rows = field count, Gutter = leading (12 pt), Fit Guides to Margins. Then
  check that row guides fall on baselines; nudge the type area or use a script to place guides at cap-height
  offsets for precision.
- Put the grid on the parent page.

## Using fields
- Images occupy 1, 2, 3... whole fields horizontally and vertically, including the gaps.
- Captions start on the first baseline below an image field.
- Headlines sized so their baselines sit on grid lines.

## Gotchas
- Fine grids (8x8+ fields) give flexibility but tempt clutter; coarse grids give calm.
- Fields that do not match line count make images misalign by part of a line, visible across a spread.
- Different leading for captions breaks alignment unless it is a fraction (half) of the base leading.

## Verify
- [ ] Each field top aligns with cap height and bottom with a baseline of adjacent text.
- [ ] Total type area = whole number of lines; parent page holds the guides.
