---
id: creative-arts.animation.blender.gp-stroke-placement
name: gp-stroke-placement
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-stroke-placement, drawing-plane, gp-surface-offset, 2d-animation]
level: practitioner
status: docs-checked
description: "Control where Grease Pencil strokes land in 3D: Stroke Placement (Origin, 3D Cursor, Surface, Stroke), drawing planes, surface offset and reprojection."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/stroke_placement.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/draw/drawing_planes.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/grease_pencil_menu.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/strokes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-stroke-placement

Goal: strokes end up at a predictable depth, not scattered through 3D space.

## Stroke Placement (Draw mode header)
| Option | New strokes land |
|---|---|
| **Origin** | At the Grease Pencil object origin |
| **3D Cursor** | At the 3D cursor |
| **Surface** | Stuck onto mesh surfaces, with **Offset** (distance from the surface) and **Project Onto Selected** (only selected objects) |
| **Stroke** | Stuck onto other strokes; **Target**: All Points, End Points or First Point |

## Drawing Plane (Draw and Sculpt modes, header)
View (current viewport orientation), Front (X-Z), Side (Y-Z), Top (X-Y), Cursor (3D cursor orientation). Enable the Canvas overlay to see the active plane.

## Drawing on models
Use Surface placement with a small Offset so strokes do not z-fight with the mesh. Combine with Line Art for 3D-2D hybrids (see the Line Art skills).

## Gotchas
- Both selectors affect only new strokes. Move old ones with Grease Pencil menu (Edit mode) > Clean Up > **Reproject** (Front, Side, Top, View, Surface, Cursor; Surface Offset; Keep Original).
- Stroke Depth Order (Object Data > Settings) set to 2D Layers ignores real stroke depth and uses layer order; keep the object mostly flat, since its depth is the midpoint of its bounding box.
- The View plane follows the viewport, so draw flat art from camera or an orthographic view.

## Verify
Orbit after drawing: strokes lie on the intended plane or surface with no stray depths.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed placement options and sub-options, the five Drawing Plane options, Reproject location and types, and Stroke Depth Order notes. The View placement option, numeric Offset values, Surface fallback behaviour and Numpad 0 advice were not in the docs and were removed; View exists only as a Drawing Plane.
Method: documentation only; no commands were run.
