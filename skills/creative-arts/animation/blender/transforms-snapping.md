---
id: creative-arts.animation.blender.transforms-snapping
name: transforms-snapping
category: creative-arts
field: animation
product: blender
tags: [blender, snapping, pivot-point, proportional-editing, transform, 3d-cursor]
level: practitioner
status: docs-checked
description: "Place things precisely in Blender with snapping targets, pivot point choice and proportional editing falloffs, and know what to switch off before handing a file on."
sources:
  - https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/3dview/controls/snapping.rst
  - https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/3dview/controls/proportional_editing.rst
  - https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/editors/3dview/controls/pivot_point/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# transforms-snapping

Goal: move things exactly where they belong, first try, in Object and Edit mode.

## Snapping

- `Shift Tab` toggles snapping. Holding `Ctrl` during a transform temporarily toggles it the other way.
- Snap targets in the Snap Target menu: Increment, Grid, Origin, Vertex, Edge, Face, Volume, Edge Center, Edge Perpendicular, Face Center. `Shift LMB` enables several targets at once.
- Individual Elements mode offers *Face Project* (each object or vertex snaps to the face found by projecting along the current view direction) and *Face Nearest* (closest face, including occluded geometry).
- *Snap Base* chooses which part of the selection lands on the target: Closest, Center, Median or Active.
- *Align Rotation to Target* rotates the selection so its Z axis matches the target normal. Turn it off when placing cameras or anything that must keep its orientation.
- *Absolute Increment Snap* snaps to the viewport grid instead of moving in grid-cell steps from the start position.
- *Backface Culling* excludes back-facing geometry from snapping; *Exclude Non-Selectable* limits snapping to selectable objects.
- *Snap to Same Target* (with Face Nearest) limits snapping to the object the selection was nearest to before the transform began.

## Pivot point

Transform Pivot Point selector in the 3D Viewport header (key `.`), Object and Edit mode: Median Point (default), Bounding Box Center, 3D Cursor, Individual Origins, Active Element. Check the manual's pages for each option before relying on a behaviour.

## Proportional editing

- `O` toggles it. Falloffs: Constant, Random, Linear, Sharp, Root, Sphere, Smooth, Inverse Square; change from the header icon or with `Shift O` during editing.
- Radius: mouse wheel or `Page Up` / `Page Down` during the transform.
- *Connected Only* (`Alt O`, Edit mode only) spreads the effect along edge connections rather than by radius alone, so it does not leak into unconnected islands.
- *Projected from View* ignores depth along the view when applying the radius.

## Gotchas

- Proportional editing left on explains "why did the whole mesh move".
- Face Project follows the view: rotate the view and the result changes. Face Nearest ignores view direction.

## Verify

- Proportional editing and snapping are off (header icons not highlighted) before handing the file on.
- Objects placed with Face snapping and Align Rotation sit on the surface with matching orientation.

## Checked

2026-11-01. Confirmed against the Blender manual pages for snapping, proportional editing and pivot point (sources above): snap targets and toggles, individual elements modes, snap base names, align rotation, absolute increment snap, culling and selectability options, same-target option, pivot types and the `.` key, falloff names, `O`, `Shift O`, `Alt O`, radius keys. Removed as not stated on those pages: numeric input and expression syntax, transform orientations, the snap base `B` key, per-version remarks, Graph Editor proportional editing, apply-transform and origin advice, delta transforms and edit-mode shortcuts.
Method: documentation only; no commands were run.
