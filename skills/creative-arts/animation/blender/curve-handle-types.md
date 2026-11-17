---
id: creative-arts.animation.blender.curve-handle-types
name: curve-handle-types
category: creative-arts
field: animation
product: blender
tags: [blender, bezier, curve-object, curve-handle-types, handle-types, vector-handle, auto-handle, aligned-handle]
level: practitioner
status: docs-checked
description: "Control Bezier curve shape in Blender with handle types: Automatic, Vector, Aligned, Free (V menu), Toggle Free/Align, Recalculate Handles and sharp corners."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/curves/structure.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/editing/control_points.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/curve_display.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# curve-handle-types

Goal: smooth curves where wanted, crisp corners where wanted, with the fewest control points.

## Types (Edit mode, select points, `V` > Set Handle Type)

| Type | Colour (default) | Behaviour |
|---|---|---|
| Automatic | yellow | Blender adjusts handle length and direction for the smoothest curve. Converts to Aligned when moved. |
| Vector | green | Handles point at the adjacent control points: straight lines and sharp corners. Converts to Free when moved. |
| Aligned | purple | Handles stay on a straight line: smooth, continuous curve. |
| Free | black | Handles move independently: asymmetric curves and cusps. |

- A selected point's handles are drawn red, so a selected Vector handle looks yellow and can be confused with Automatic. The colours can be changed in Preferences > Themes > 3D Viewport > Active Spline.
- Set Handle Type has a **Toggle Free/Align** option that switches the selected handles between Free and Aligned.
- **Recalculate Handles** (`Shift N`, Control Points menu) rotates the selected handles to be tangential to the curve; its *Length* option makes all handle lengths equal.

## Curve Pen shortcuts for handle types

- Double-click a handle: toggle Vector/Auto (Toggle Vector). Double-click a control point: cycle all handle types (Cycle Handle Type).
- Hold `Left Shift` while dragging a handle: switch between Free and Align.
- Extrude Handle Type (tool preference) sets new points to Vector or Auto.

## Practical recipes

- Logo outline with corners: draw, select the corner points, `V` > Vector; set the curved points to Aligned and tweak.
- Smooth camera path: keep Automatic on all points.
- Teardrop: one point Free (cusp), the rest Aligned.

## Handle display

Curve Edit Mode Overlays > **Handles**: None, Selected or All.

## Gotchas

- Automatic handles change when neighbours move; for precise profiles use Aligned or Vector.
- Vector handles all round a closed shape give a polygon look.

## Verify

Set Handles to All in the overlay; check the colours match intent; zoom in on corners for unwanted rounding.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (curve structure, control points, Curve Pen, curve display pages). Confirmed: the four handle types, their colours and conversion on move, selected-handle red note, Toggle Free/Align, Recalculate Handles shortcut and Length option, Curve Pen double-click and Shift gestures, Handles overlay options. Corrected: Aligned handles are purple (not pink) and Free are black (not black/red); the Ctrl-click handle-selection note and the Graph Editor comparison were removed as unconfirmed.
Method: documentation only; no commands were run.
