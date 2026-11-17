---
id: creative-arts.graphic-design.adobe-illustrator.live-shapes-and-live-corners
name: live-shapes-and-live-corners
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, pen-tool, live-corners, live-shapes, corner-widget, corner-radius, round-corners, chamfer, inverted-round, transform-panel, polygon-sides]
level: practitioner
status: draft
description: "Use Illustrator live shapes and live corners: corner widgets, exact radii, round/inverted/chamfer corners, absolute vs relative rounding, and Scale Corners."
sources:
  - https://helpx.adobe.com/illustrator/using/live-corners.html
  - https://helpx.adobe.com/illustrator/using/draw-simple-lines-shapes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Live shapes and live corners

**Goal:** editable rounded corners and parametric shapes with exact, consistent values.

## Live shapes
Rectangles, rounded rectangles, ellipses, polygons and lines drawn with the shape tools stay
**live**: Properties/Transform panel shows width, height, rotation, corner radii, polygon side
count and pie angles for ellipses. Editing values updates the shape non-destructively.
Polygon: drag the side widget, or type sides; star tool is not live.

## Live corners (any path)
- Select corner points with Direct Selection (A) - a **corner widget** (small circle) appears
  inside each corner. Drag it to round all selected corners at once.
- Double-click a widget (or Transform panel > corner options) for:
  - **Corner type:** Round, **Inverted Round**, **Chamfer**.
  - **Radius** value (exact).
  - **Rounding:** Relative or **Absolute** - absolute gives a true circular arc; relative gives a
    smoother curve that can look softer.
- Alt/Option+click a widget cycles corner types.
- Very small angles cannot take large radii - the corner shows a red path when the radius is limited.
- View > Hide Corner Widget if they get in the way (or set a threshold angle in Preferences).

## Consistency in icons and UI
- Use the same radius set across a system (e.g. 2 px small, 4 px card, 8 px large) and type values
  rather than dragging.
- Scaling: **Preferences > General > Scale Corners** (also in the Transform panel options) decides
  whether radii scale with the object. Off for UI components (fixed radius), on for illustrations scaled as a whole.

## Expanding
Object > Shape > **Expand Shape** converts a live shape to a normal path (needed for some
operations); live corners on a path become regular curves when you edit the path's points
significantly. Keep a copy of the live version.

## Gotchas
- Pathfinder operations expand live shapes - round corners after merging, not before, if you want them editable.
- Corner radius on a stroked shape looks different inside vs outside the stroke; align strokes to inside for UI.

## Verify
- [ ] Corner radii entered as values and consistent across the set.
- [ ] Scale Corners setting correct for the work type.
