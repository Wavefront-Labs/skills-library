---
id: creative-arts.animation.blender.boolean-edit-mode
name: boolean-edit-mode
category: creative-arts
field: animation
product: blender
tags: [blender, boolean-edit-mode, intersect-knife, intersect-boolean, mesh-editing, knife-project]
level: practitioner
status: docs-checked
description: "Run booleans inside Edit mode: Face Intersect Boolean between selected and unselected, Intersect Knife for cut lines, separate modes, solver choice and follow-up clean-up."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/intersect_boolean.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/intersect_knife.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# boolean-edit-mode

Goal: quick destructive booleans or intersection cuts within one mesh, without extra objects and modifiers.

## Setup

Join the cutter into the base mesh (or model it inside the same object). In Edit mode select the cutter's geometry (`L` over it); the rest stays unselected.

## Intersect (Boolean)

*Face → Intersect (Boolean)*:
- *Boolean*: Difference / Union / Intersect, with the selected part as the cutter and the unselected part as the base.
- *Solver*: Float or Exact (Exact handles overlapping geometry but is slower; Float adds a *Merge Threshold*). *Swap* (with Difference) cuts the unselected geometry out of the selected geometry instead. *Self Intersection* handles self-intersecting geometry at a performance cost.

## Intersect (Knife)

*Face → Intersect (Knife)*: adds edges where faces intersect, without removing anything.
- *Source*: Self Intersect (selected faces with other selected faces) or Selected/Unselected.
- *Separate Mode*: All (disconnect all faces at each intersection edge), Cut (with Selected/Unselected, only disconnect the selected faces from the unselected ones; otherwise same as All), Merge (connect all faces at each intersection edge).
- *Solver*: Float or Exact.
Use it to get cut lines, then delete or separate parts manually: e.g. split a mesh where a plane intersects it.

## Related

*Knife Project* (`creative-arts.animation.blender.knife-project-bisect`) cuts by a silhouette from the view; *Bisect* cuts by a plane.

## Gotchas

- Unselected geometry that should not participate must be hidden (`H`) first.
- Results are destructive: undo or keep a duplicate.

## Verify

After Intersect (Boolean) Difference, the cutter geometry is gone and the hole is closed (no non-manifold edges); after Intersect (Knife), new edges lie exactly along the intersection line.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST, Intersect (Boolean) and Intersect (Knife) pages). Confirmed: menu paths Face > Intersect (Boolean) and Face > Intersect (Knife); Boolean Operation Intersect/Union/Difference; Swap; Self Intersection; Source and Separate Mode options; H hides geometry to exclude it. Corrected: the solver is Float or Exact (not Fast); Hole Tolerant belongs to the Boolean modifier, not this operator; Separate Mode Cut only separates selected from unselected faces. Removed: the unconfirmed cutter-normals gotcha.

Method: documentation only; no commands were run.
