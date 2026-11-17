---
id: creative-arts.graphic-design.adobe-illustrator.perspective-grid-and-mockup-placement
name: perspective-grid-and-mockup-placement
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, perspective-grid, perspective-selection-tool, one-point-perspective, two-point-perspective, mockup, signage-mockup, packaging-mockup]
level: practitioner
status: draft
description: "Draw and attach artwork in perspective with Illustrator's Perspective Grid: set 1, 2 or 3-point grids, place flat art on planes, and build quick signage and packaging mockups."
sources:
  - https://helpx.adobe.com/illustrator/using/perspective-drawing.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Perspective grid and mockup placement

**Goal:** flat logos, signs and labels shown on building walls, boxes and vehicles in believable
perspective, still editable as vectors.

## Set up the grid
- **Perspective Grid tool** (Shift+P) or View > Perspective Grid > Show Grid (Ctrl/Cmd+Shift+I).
- View > Perspective Grid > **One Point / Two Point / Three Point** preset; Define Grid sets viewing
  angle, viewing distance, horizon height and units.
- Drag the on-canvas widgets: vanishing points, horizon line, ground level, grid extent.
- To match a photo: place the photo on a locked bottom layer, then align the vanishing points to the
  photo's converging lines (window edges, kerbs).

## Draw and attach
- The **plane switching widget** (cube, top-left) selects Left (1), Horizontal (2), Right (3) plane, or none (4).
- Draw shapes with rectangle or other tools while the grid is visible: they draw on the active plane.
- **Perspective Selection tool** (Shift+V): drag flat artwork onto the grid to attach it to the active plane;
  press 1/2/3 while dragging to change plane. Hold 5 while dragging to move a plane with its objects.
- Edit attached artwork: double-click a text or symbol in perspective to edit it flat, then it returns
  in perspective. Object > Perspective > **Release with Perspective** detaches it.

## Mockups
- Box: logo and panels on Left and Right planes, lid on the Horizontal plane.
- Signage: two-point grid matched to the photo; attach the sign art; add a subtle shadow with a darker
  shape in Multiply.
- For photo-real packaging, Photoshop smart-object mockups or the 3D and Materials panel may be faster; the
  grid is best for vector illustrations and architectural signage visuals.

## Gotchas
- Raster images, gradients mesh and some effects cannot be attached to the grid; outline or use symbols.
- Live type can be attached, but complex effects on it may not distort correctly.
- Hide the grid (Ctrl/Cmd+Shift+I) before export; otherwise it is easy to forget its state.

## Verify
- [ ] Artwork lines converge to the same vanishing points as the photo.
- [ ] Text is still editable; exported mockup has no grid visible.
