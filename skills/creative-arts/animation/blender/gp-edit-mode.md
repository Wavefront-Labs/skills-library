---
id: creative-arts.animation.blender.gp-edit-mode
name: gp-edit-mode
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-edit-mode, gp-stroke-editing, gp-curve-editing, gp-simplify]
level: practitioner
status: docs-checked
description: "Edit Grease Pencil strokes in Edit mode: selection modes, join, close, simplify, subdivide, set start point, reproject, outline and Bezier curve type editing."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/introduction.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/stroke_menu.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/point_menu.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/selecting.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modes/edit/grease_pencil_menu.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/multiframe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-edit-mode

Goal: clean up and restructure strokes with precise operators.

## Selection (Edit mode)
- Header select mode (keys 1, 2, 3): **Points**, **Strokes**, **Segments** (points between other strokes).
- **Select Linked** (L; Shift-L deselects the linked stroke), **Select Fill** (Ctrl-L, all curves of the active fill region), **Select Similar** (Shift-G; Layer, Material, Vertex Color, Radius, Opacity), **Select Alternated**, **By Stroke Type** (Stroke or Fill), **First/Last**.

## Stroke menu
- **Join** (Ctrl-J) joins selected strokes; **Join and Copy** (Shift-Ctrl-J) does it into a new stroke; **Leave Gaps** skips connecting geometry.
- **Close** (F) and **Toggle Cyclic**: Close All, Open All or Toggle; **Match Point Density** adds points in the new segment.
- **Simplify**: Fixed (Steps), Adaptive (Factor, RDP algorithm), Sample (Length), Merge (Distance).
- **Subdivide** (Number of Cuts) and **Subdivide and Smooth**; **Trim** (to first loop or intersection).
- **Set Start Point** (cyclic strokes) and **Switch Direction**: matter for the Build modifier.
- **Move to Layer** (M), **Assign Material**, **Set as Active Material**.
- **Arrange**: Bring to Front, Bring Forward, Send Backward, Send to Back (draw order inside a 2D layer).
- **Set Caps**, **Set Uniform Thickness**, **Set Uniform Opacity**, **Set Stroke Type** (Stroke, Fill, Both), **Join Fills** (Shift-J), **Separate Fills** (Alt-P).
- **Set Curve Type** (V): Bezier, NURBS, Poly or Catmull Rom, with a Handles option. Bezier handle display is the overlay Handles setting (None, Selected, All).

## Grease Pencil menu (Edit mode)
- **Separate** (P): Selection, By Material or By Layer into new objects.
- **Clean Up**: Delete Loose Points (Limit), Delete Duplicate Frames, Merge by Distance (Merge Distance, Unselected), **Reproject** (Front, Side, Top, View, Surface, Cursor; Keep Original).
- **Outline**, **Mirror** (Ctrl-M), **Split** (V), **Duplicate** (Shift-D), **Delete** (X) variants.

## Point menu
**Extrude** (E; extruding an intermediate point creates a new stroke), **Smooth** (Iterations, Factor, Smooth Endpoints, Keep Shape, Position/Radius/Opacity), **Set Handle Type** (Auto, Vector, Align, Free), **Set Corner Type** (Round, Flat, Sharp).

## Gotchas
- Editing several Grease Pencil objects at once is not supported.
- Operators act on the current frame unless Multiframe is on, and not every operator supports Multiframe.
- Overlay Stroke Direction (Edit) shows start points green and end points red, which helps before Switch Direction or Set Start Point.

## Verify
Select a stroke, run Simplify > Adaptive and confirm fewer points remain in Points select mode with the shape intact.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed from the Stroke, Point, Grease Pencil menu and Selecting pages: shortcuts (Ctrl-J, F, M, L, Ctrl-L, Shift-G, P, V), Simplify modes, Reproject being under Grease Pencil > Clean Up, Set Curve Type options. Removed unconfirmed shortcuts (Alt-C, Ctrl-arrows, Alt-S, Shift-F) and the legacy Curve Editing toggle claim.
Method: documentation only; no commands were run.
