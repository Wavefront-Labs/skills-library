---
id: creative-arts.graphic-design.lettering-and-calligraphy.vectorising-hand-lettering
name: vectorising-hand-lettering
category: creative-arts
field: graphic-design
product: lettering-and-calligraphy
tags: [graphic-design, lettering-and-calligraphy, lettering-digitising, type-design, vectorising-lettering, bezier-drawing, extrema, image-trace, pen-tool, hand-lettering, illustrator]
level: practitioner
status: draft
description: "Turn lettering sketches into clean vectors: trace vs drawn beziers, points on extrema, horizontal/vertical handles, smooth curves and keeping hand character."
sources:
  - https://helpx.adobe.com/illustrator/using/drawing-pen-curvature-or-pencil-tool.html
  - https://glyphsapp.com/learn/drawing-good-paths
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vectorising hand lettering

**Goal:** vector letters as smooth and controlled as a font, without losing the character
of the hand-drawn original.

## 1. Get a good source
- Refine the sketch on tracing paper first: fix slant, weight and spacing on paper; vectorising
  does not fix a bad drawing.
- Scan at 600 ppi greyscale (or photograph square-on in even light), Levels to black/white.

## 2. Trace or draw?
- **Image Trace** (Illustrator, see image trace skill) suits textured brush lettering where
  the rough edge is the point. Result: many points, organic edges.
- **Hand-drawn beziers** for clean script, logotypes and anything that will be scaled large
  or refined later. Professional lettering is drawn point by point.

## 3. Bezier rules (the lettering/type designer's way)
- **Points on extrema:** put anchor points at the top, bottom, leftmost and rightmost points of
  every curve. Hold Shift to keep handles **horizontal or vertical**.
- **As few points as possible:** extrema plus points at real corners or inflections; no extra
  points mid-curve.
- **Handle balance:** the two handles of a curve segment roughly balanced (neither collapsed nor
  overlong) - the "tangent rule" gives smooth, tension-even curves.
- **Smooth points** (handles colinear) for curves, **corner points** only where the letter has a corner.
- Draw outlines of the strokes (closed shapes), not centre-lines with a stroke - weight
  control is better and output is predictable. For monoline scripts you may draw centre-lines,
  apply a stroke, then Outline Stroke and clean up.

## 4. Build and refine
- Draw letters as overlapping shapes, then Pathfinder Unite (or Shape Builder) at the end.
- Check overshoot: round letters slightly beyond baseline/x-height.
- Compare with the sketch at small size and large size; keep intentional irregularity, remove accidental wobble.
- Apply a consistent slant by shearing only after drawing upright if the style allows.

## 5. Clean output
Remove stray points, unite overlaps, check for self-intersections, and ensure compound paths
for counters (Object > Compound Path > Make).

## Verify
- [ ] Every curve has points at extrema with horizontal/vertical handles.
- [ ] Outline mode (Ctrl/Cmd+Y) shows minimal, evenly spaced points; no kinks at 800% zoom.
- [ ] Final art is a clean compound path with no overlaps.
