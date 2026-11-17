---
id: creative-arts.animation.blender.retopo-snapping-setup
name: retopo-snapping-setup
category: creative-arts
field: animation
product: blender
tags: [blender, retopo-snapping, retopology-overlay, snap-to-surface, retopology, shrinkwrap]
level: intro
status: docs-checked
description: "Set up Blender for retopology: face project or face nearest snapping, Retopology overlay, a mirror and shrinkwrap stack, and display settings for working over a sculpt."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/controls/snapping.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/shrinkwrap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# retopo-snapping-setup

Goal: every new vertex lands on the high-poly surface and the low poly stays visible on top.

## Objects

1. High poly: `HP_head`. Making it unselectable (Outliner selectable restriction toggle) stops clicks selecting it, but then leave *Exclude Non-Selectable* off, because that option limits snapping to selectable objects.
2. New low poly: start with a single vertex or plane (`Shift A → Mesh → Plane`, delete to one vert in Edit mode), named `LP_head`, at the high poly's location.

## Snapping (header magnet)

- Enable snapping, then under *Snap Target for Individual Elements* choose **Face Project** (snaps each vertex to the face found by projecting along the viewing direction) or **Face Nearest** (snaps to the closest face; unlike Face Project it can reach occluded geometry). Plain *Face* snapping (surface under the mouse cursor) is also described as useful for retopology.
- *Snap Base*: Closest, Center, Median or Active; Closest snaps the vertex nearest the target.
- Edit Mode options: *Include Active* snaps to other elements of the edited mesh (turn it off so new vertices only snap to the high poly), *Include Non-Edited* snaps to objects not in Edit Mode.

## Overlay

Mesh Edit Mode overlays → Shading → **Retopology** on: the edited mesh becomes see-through and, with *Offset* (distance moved toward the camera), is drawn in front of nearby geometry. Alternative: Object Properties → Viewport Display → *In Front*.

## Modifiers on the low poly

```
Mirror (X, Clipping on, Merge)           – work on one half
Shrinkwrap (Target HP_head, Nearest Surface Point or Project, On Cage, Edit Mode)
```
Shrinkwrap keeps vertices on the surface even after sliding or smoothing; apply at the end.

## Gotchas

- Face Project projects along the viewing direction, so from a view where the surface is nearly edge-on vertices can land far away; rotate the view or use Face Nearest.
- Snapping to the low poly itself: with *Include Active* off, new vertices ignore the other elements of the edited mesh.
- Retopology overlay offset too large makes faces appear floating; small values are enough.

## Verify

Extrude and move vertices: they stick to the high poly; from the side the low poly faces sit on the surface with no gaps; Mirror clipping keeps the centre line on X=0.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Snapping, Viewport Overlays, Retopology, Shrinkwrap, Mirror and Outliner pages). Confirmed: Snap Base options; Snap Target for Individual Elements Face Project and Face Nearest; Include Active, Include Non-Edited and Exclude Non-Selectable meanings; Retopology overlay (Mesh Edit Mode overlays, Shading) and its Offset; Object Viewport Display In Front; Shrinkwrap Nearest Surface Point and Project modes; Mirror Clipping and Merge. Corrected: Face Project and Face Nearest are individual-element snap targets (there is no Project Individual Elements checkbox), and Exclude Non-Selectable would stop snapping to an unselectable high poly. Removed: the example overlay offset values.

Method: documentation only; no commands were run.
