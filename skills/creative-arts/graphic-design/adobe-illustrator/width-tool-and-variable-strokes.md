---
id: creative-arts.graphic-design.adobe-illustrator.width-tool-and-variable-strokes
name: width-tool-and-variable-strokes
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, pen-tool, width-tool, variable-width-stroke, width-profiles, tapered-strokes, line-art, outline-stroke, monoline]
level: practitioner
status: draft
description: "Shape strokes with the Illustrator Width tool: width points, asymmetric widths, saved variable width profiles for line art, and outlining strokes for output."
sources:
  - https://helpx.adobe.com/illustrator/using/draw-variable-width-stroke.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Width tool and variable-width strokes

**Goal:** tapered, calligraphic or swelling strokes on any path, adjustable at any time.

## Width tool (Shift+W)
- Hover a stroked path; drag outward from the path to create a **width point** and widen the
  stroke there. Drag inward to thin.
- Drag a width point along the path to move it; Alt/Option+drag a point to copy it.
- **Alt/Option+drag one side** for an **asymmetric** width (thicker on one side - useful for
  ink-like shading on outlines).
- Double-click a width point to type exact Side 1/Side 2 widths; tick "Adjust Adjoining Width Points".
- Select a width point and Delete to remove it. Shift+click to select several.
- Discontinuous width points (two at the same spot) allow abrupt width changes.

## Width profiles
- Stroke panel or Control bar: **Variable Width Profile** drop-down has presets (tapered both ends,
  one end, bulge).
- After shaping a stroke, save it: drop-down > **Add to Profiles**. Apply the profile to other paths
  for consistent line quality; Flip Along/Flip Across fix direction.
- Profiles are stored with the document; reset with "Reset Profiles".

## Line art use
- Draw with the Pen/Pencil/Curvature tool as single paths, apply a uniform stroke, then apply a
  tapered profile to all lines at once - instant hand-inked feel.
- Combine with round caps for soft ends.

## Output
- Variable widths stay live in AI/PDF. For cutting, embroidery, fonts or SVG for some apps:
  **Object > Path > Outline Stroke** (on a copy) converts to filled shapes.
- After outlining, run Pathfinder Unite on overlapping parts if you need one clean shape.

## Gotchas
- Very sharp curves with wide strokes create kinks or self-intersections on the inside of the curve;
  reduce width there or add a point.
- Width tool edits are lost if you apply a different profile to the path.
- Scaling: Scale Strokes & Effects setting decides whether widths scale with the object.

## Verify
- [ ] Strokes taper as intended at all path lengths; no kinks at 400% zoom.
- [ ] Reused shapes come from a saved width profile.
- [ ] Outlined copy for outputs that need filled paths.
