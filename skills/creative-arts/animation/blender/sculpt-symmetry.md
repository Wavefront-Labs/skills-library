---
id: creative-arts.animation.blender.sculpt-symmetry
name: sculpt-symmetry
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, sculpt-symmetry, radial-symmetry, sculpt-tiling, symmetrize, mirror-sculpt]
level: practitioner
status: docs-checked
description: "Use Blender sculpt symmetry properly: mirror in local axes, lock axes, radial counts, tiling and feather, Symmetrize direction and merge distance, and fixing an off-centre origin."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/symmetry.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/origin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# sculpt-symmetry

Goal: symmetric strokes where you want them, deliberate asymmetry afterwards.

## Options (Toolbar > Tool > Symmetry)

- **Mirror** X/Y/Z: mirror strokes across the selected local axes. To change the direction the axes point, rotate the model in Edit Mode, not Object Mode.
- **Lock** X/Y/Z: block any modification or deformation along the selected local axes while sculpting.
- **Tiling** X/Y/Z: seamlessly tile strokes along the axes to create repeating patterns. **Tile Offset** changes the tile size per axis; the default tile size is one unit.
- **Radial** X/Y/Z: repeat the stroke that many times within 360 degrees around the axis.
- **Feather**: reduces stroke strength where it overlaps the planes of symmetry.
- **Symmetrize** with **Direction** and **Merge Distance** (distance within which symmetrical vertices are merged): mirrors one side onto the other. The manual points to it for Dyntopo, which can leave a mesh asymmetric.

## Off-centre origin

Mirroring uses the object's local axes, so set the origin where you want the mirror plane. Object > Set Origin offers Origin to Geometry (moves the origin to the centre of the object) and Origin to 3D Cursor (place the cursor first).

## Asymmetry pass

Finish with symmetry off for life: weight shift, slight lip and eye differences, wrinkles. Do this late, or on a copy, so you can go back to the symmetric version.

## Gotchas

- Axes follow the mesh's local orientation, so an object rotated in Object Mode still mirrors in its local axes.
- Symmetrize after Dyntopo work and before rigging, so the topology stays symmetric.

## Verify

Stroke near the centre line: no seam and no double-strength ridge (Feather helps); a front view looks mirrored.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/tool_settings/symmetry and scene_layout/object/origin: panel location, Mirror, Lock, Tiling, Tile Offset default, Radial, Feather, Symmetrize options and Dyntopo remark, Set Origin entries. Removed unconfirmed claims: default mirror axis, header butterfly icon, behaviour of Symmetrize on Multires, and topology mirror weights.
Method: documentation only; no commands were run.
