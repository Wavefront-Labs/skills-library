---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.correct-line-tools-for-vector-lines
name: correct-line-tools-for-vector-lines
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-vector-layer, csp-correct-line, simplify-vector-line, redraw-line-width, connect-vector-line, vector-inking]
level: practitioner
status: draft
description: "Fix vector lines with Clip Studio Paint's Correct line tools: control point, pinch, simplify, connect, redraw line and redraw line width, adjust line width, plus when to use each."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Correct line tools

Work only on **vector layers**. The **Correct line** tool group contains:
| Sub tool | Use |
|---|---|
| **Control point** | move, add, delete control points; change width or opacity at a point; cut a line at a point |
| **Pinch vector line** | drag part of a line to reshape it smoothly (adjust pinch range in Tool property) |
| **Simplify vector line** | reduce control points on a shaky stroke for a smoother curve |
| **Connect vector line** | join two line ends that nearly touch, closing gaps for fills |
| **Redraw vector line** | trace over a line to replace its path while keeping its properties |
| **Redraw vector line width** | trace over a line to change its width profile (adding taper or thickness) |
| **Adjust line width** | thicken or thin an area of lines with a brush-like stroke (fatten/narrow, scale) |

## Workflow
1. Ink on a vector layer (Vector layer with stabilisation set to taste).
2. Erase overshoots with the vector eraser "up to intersection".
3. Use Simplify to calm wobbly long curves.
4. Add weight with Adjust line width on the shadow side, or Redraw vector line width for tapered ends.
5. Connect vector line where colour fills leak.

## Gotchas
- Tools have no effect on raster layers; check the layer type icon.
- Over-simplifying removes intentional detail; use small strokes.
- Adjust line width on very dense hatching thickens neighbours; select first.

## Verify
- [ ] Fills (with Refer other layers + close gap) no longer leak.
- [ ] Line weight hierarchy consistent across the page.
