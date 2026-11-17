---
id: creative-arts.animation.blender.gp-guides-canvas
name: gp-guides-canvas
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-guides, drawing-guides, gp-canvas, perspective-drawing]
level: practitioner
status: docs-checked
description: "Keep Grease Pencil strokes on a known plane: Drawing Plane options, the Canvas grid overlay, line/arc/curve tools and stroke stabilisation."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/introduction.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/drawing_planes.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/tools/curve.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/brushes/draw.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-guides-canvas

Goal: keep new strokes on a known plane and use the line and curve tools for straight and arc-shaped work.

## Canvas grid
Viewport Overlays > Grease Pencil > **Canvas** shows a grid over the Grease Pencil drawing plane. Settings: Canvas Grid Opacity, **Canvas X-Ray** (objects drawn behind the grid), Subdivisions, Grid Color, Scale X/Y, Offset X/Y.

## Choose the drawing plane
Header **Drawing Plane** (Draw and Sculpt modes): View, Front (X-Z), Side (Y-Z), Top (X-Y) or Cursor (3D cursor orientation). It affects new strokes only. Turn on Canvas to see which plane is active. See gp-stroke-placement for location (Stroke Placement).

## Line and curve tools (Draw mode toolbar)
Line, Polyline, Arc, Curve, Box and Circle tools draw primitives with the Draw brushes. The Curve tool: drag start and end, tweak two Bezier manipulators, confirm with Return or MMB, cancel with Esc or RMB; Shift uses one manipulator, Alt makes an arc from a centre, NumpadPlus/NumpadMinus or the wheel change the point count, E extrudes the end point. Tool settings include **Subdivisions** and a **Thickness Profile** curve.

## Freehand smoothing
Brush > Advanced **Active Smooth** (iterations while drawing) and the **Stabilize Stroke** section (Radius, Factor) steady freehand lines; Post-Processing > Smooth runs after the stroke ends.

## Gotchas
- Drawing Plane and Stroke Placement only affect new strokes; reproject old ones from Grease Pencil > Clean Up > Reproject.
- With the View plane, strokes follow the current viewport angle, so draw from camera or an orthographic view for flat art.
- Drawing guides (ruler-style radial, grid or perspective guides) are not documented in the current manual; do not rely on them.

## Verify
Enable Canvas, pick Front, draw: strokes sit on the grid plane when orbited.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed: Drawing Plane options, Canvas overlay settings, Curve tool controls, Stabilize Stroke Radius/Factor and Active Smooth. The previous guide types, spacing and reference point claims and the Shift-to-constrain claim were not found anywhere in the 5.2 manual and were removed.
Method: documentation only; no commands were run.
