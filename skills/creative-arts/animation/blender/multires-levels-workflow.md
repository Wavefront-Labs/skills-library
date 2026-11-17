---
id: creative-arts.animation.blender.multires-levels-workflow
name: multires-levels-workflow
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, multires-levels-workflow, sculpt-level, multires-levels, multires-apply-base, base-mesh-edit, multiresolution]
level: practitioner
status: docs-checked
description: "Sculpt across Multiresolution levels in Blender: Sculpt, Viewport and Render levels, Alt-1 and Alt-2 stepping, Sculpt Base Mesh, and base mesh limits."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/adaptive.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# multires-levels-workflow

Goal: big forms on low levels, details on high levels, so changes propagate cleanly. Adding and recovering levels is covered in `creative-arts.animation.blender.multires-subdivide-reshape`.

## Level plan

The manual's example: sculpt general proportions at subdivision level 1, add high-resolution detail at level 4, then switch back to level 1 to correct the shape further. Sculpting on lower levels gives broad changes; higher levels hold fine detail.

## Level controls (Multiresolution modifier)

- **Levels Viewport**: level shown in the viewport. **Sculpt**: level used in Sculpt Mode. **Render**: level used for rendering. Keep Viewport low in layout and animation files.
- In Sculpt Mode, **Alt-1** decreases the sculpt level and **Alt-2** increases it.
- **Sculpt Base Mesh**: deforms the unsubdivided base mesh instead of the higher levels while previewing the current level. This allows broad changes in the context of the high-resolution detail without surface noise.

## Base mesh care

- The base mesh should be a clean, mostly quad topology with no non-manifold faces and no poles with two connected edges. Quadriflow remesh can build such a base automatically.
- Do not change the topology once subdivided: edits to the base mesh corrupt the subdivision details.
- **Apply Base** moves the base mesh to match the sculpted surface (see `creative-arts.animation.blender.multires-subdivide-reshape`).
- Remeshing (voxel or Quadriflow) is not possible on an object with a Multires modifier.
- More than five subdivisions give worse performance and slower level switching. If more resolution is needed locally, the Slide Relax brush moves topology to where it is needed.

## Gotchas

- Multires cannot sit after modifiers that change geometry; modifiers that generate or change geometry cannot come before it.
- Deform modifiers placed after Multires are applied to the multires levels instead of the base mesh.

## Verify

Step down to level 1 with Alt-1, make a large Grab change, then step up with Alt-2: the detail moves with the form.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against modifiers/generate/multiresolution and sculpt_paint/sculpting/introduction/adaptive: Alt-1 and Alt-2 level shortcuts (the previous Page Up, Page Down and Ctrl-number keys are not documented), Levels Viewport, Sculpt and Render, Sculpt Base Mesh, topology advice, more than 5 subdivisions note, modifier order rules, no remeshing with Multires. Removed the character-head level numbering, symmetry-on-base claim and the claim that base vertices may be moved freely.
Method: documentation only; no commands were run.
