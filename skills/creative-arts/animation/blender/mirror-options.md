---
id: creative-arts.animation.blender.mirror-options
name: mirror-options
category: creative-arts
field: animation
product: blender
tags: [blender, mirror-modifier, modifiers, symmetry, bisect, clipping, merge, uv]
level: practitioner
status: verified
description: "Use Blender's Mirror modifier: axes, Bisect and Flip, Mirror Object, Clipping, Merge distance, Flip UV and UV Offsets, vertex group mirroring, plane positioning."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# mirror-options

Goal: model one half and get a merged symmetrical whole, including UVs and left/right vertex groups.

## Fields

- **Axis** X/Y/Z: the axis perpendicular to the mirror plane, local to the object, across the object origin. One axis gives one mirror, two give four, three give eight.
- **Bisect**: if the mesh already exists on both sides of the plane it is cut there, and only one side (the positive one by default) is kept and mirrored. **Flip** keeps the negative side instead. **Bisect Distance** is the distance from the bisect plane within which vertices are removed.
- **Mirror Object**: an object (usually an Empty) whose position and rotation define the mirror planes instead of the modified object's; animating it moves the axis.
- **Clipping**: stops vertices crossing the mirror plane while editing in Edit Mode. Vertices on the plane cannot move away from it while Clipping is on; disable it to move them along the mirror axis.
- **Merge** + **Merge Distance**: a vertex within that distance of its mirror copy is merged and snapped onto the plane.
- **Data**: *Flip UV* (Mirror U and Mirror V in the 4.5.14 Python API) mirrors UVs around the middle of the image, and Flip U/V Offset moves that flip point away from 0.5; *UV Offsets* (U Offset, V Offset) shifts mirrored UVs on U/V (useful for baking, where overlapping UVs cause artefacts); *Flip UDIM* mirrors around each tile centre; *Vertex Groups* mirrors groups named with left/right suffixes (.L/.R, .left/.right...).

## Vertex group mirroring prerequisites

The group must follow the left/right naming pattern and the opposite-side group must already exist (the manual says it is not created automatically and must be empty). In Blender 4.5.14 an opposite group that already held weights was not a problem: the mirrored copy simply got the .L and .R weights swapped, so verify the result instead of relying on the empty-group rule.

## Positioning the mirror plane

Select the edge on the centre line, snap Cursor to Selected, then Object > Set Origin > Origin to 3D Cursor so the origin (and mirror plane) sits exactly there. Alternative: use an Empty as Mirror Object and move it.

## Applying

Click Apply to make a real mesh, or keep the modifier for future editing.

## Verify

No duplicate loop on the centre line; with Clipping on, centre vertices cannot leave the plane.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Mirror modifier page). Confirmed: axis semantics and count of mirrors, Bisect/Flip, Mirror Object, Clipping behaviour, Merge Distance, Data options (Flip UV, UV Offsets, Flip UDIM, Vertex Groups prerequisites), origin technique. Renamed UI labels (Mirror U/V became Flip UV; Offset became UV Offsets). Removed unconfirmed default merge distance, stack-order, shortcut and normals troubleshooting claims.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Mirror on a cube with Python: Axis X/Y/Z gives 2, 4 and 8 times the vertices; Merge off keeps 16 vertices, Merge on welds the vertices on the plane (12), Merge Distance 1.5 also merges across the cube; Bisect X on a centred cube keeps the positive side (mirrored result spans -2 to 2 after moving the +X vertices out to 2) and Flip keeps the negative side (-1 to 1); Mirror Object at x=3 mirrors a cube about that point (0..2 and 4..6 in world space); Clip defaults off; Bisect Distance, Mirror Vertex Groups, Mirror UDIM and the U/V offset properties exist with the described tooltips; with Mirror Vertex Groups on, .L weights landed in .R on the copy; U Offset 0.25 shifted the mirrored UVs by 0.25. Not run: the origin and 3D cursor positioning steps and Apply (UI operator steps).

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
