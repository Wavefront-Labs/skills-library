---
id: creative-arts.graphic-design.information-design.icon-grid-and-keylines
name: icon-grid-and-keylines
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, icon-design, accessible-graphics, icon-grid, keylines, pixel-snapping, live-area, padding, stroke-weight, 24px-grid, material-icons, optical-balance]
level: practitioner
status: draft
description: "Draw icons on a proper grid: canvas and live-area padding, keyline shapes for optical balance, consistent stroke weights and corner radii, and pixel snapping for crisp small sizes."
sources:
  - https://m2.material.io/design/iconography/system-icons.html
  - https://developer.apple.com/design/human-interface-guidelines/icons
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Icon grid and keylines

**Goal:** icons that look the same size and weight as each other and stay crisp at 16-24 px.

## The canvas
- Pick a base size: **24 x 24 px** (Material, most UI sets), 20 or 16 for dense UI, 32/48 for
  marketing. Draw at 1x on a pixel grid, not scaled from a big drawing.
- **Live area / padding:** 2 px trim on a 24 grid (live area 20 x 20). Only rare elements
  (a tail, a sparkle) may enter the padding.

## Keyline shapes (optical sizing)
Shapes of equal width look different in size. Keylines on the grid (Material system icons):
- **Square** ~18 x 18, **circle** ~20 diameter, **portrait rectangle** 16 x 20,
  **landscape rectangle** 20 x 16.
A circle must be larger than a square to look the same size; triangles larger still. Fit each
icon's dominant form to the matching keyline, then judge by eye.

## Consistency rules (write them down)
- **Stroke weight:** one value (2 px at 24 is common; 1.5 px for lighter sets). Interior
  details use the same stroke.
- **Corner radius:** e.g. 2 px outer, 0-1 px inner; consistent terminal caps (round or butt).
- Angles: prefer 45 and 90 degrees; other angles alias at small sizes.
- Gaps between elements >= stroke width so they do not fill in.
- Filled vs outlined: decide per set; do not mix inside one UI context (filled for selected states is fine).

## Pixel snapping (Illustrator / Figma)
- Illustrator: View > Pixel Preview; **Snap to Pixel / Align to Pixel Grid** (Transform panel
  "Align to pixel grid" on new objects). Odd-width strokes (1 px) on whole-pixel coordinates
  blur - centre them on the half-pixel or use even strokes.
- Figma: use whole-pixel positions, check at 1x; enable pixel grid and snap to pixel grid.
- Outline strokes and union shapes before export so SVGs are single compound paths (see SVG export skill).

## Verify
- [ ] Set viewed together at 1x: no icon looks bigger, bolder or lighter than its neighbours.
- [ ] 16 and 24 px renders crisp (no grey half-pixel edges on straight lines).
- [ ] Grid, keylines and rules documented in the icon set spec.
