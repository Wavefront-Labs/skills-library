---
id: creative-arts.animation.blender.multires-subdivide-reshape
name: multires-subdivide-reshape
category: creative-arts
field: animation
product: blender
tags: [blender, multiresolution, multires-subdivide, linear-subdivide, apply-base, multires-unsubdivide, rebuild-subdivisions, multires-reshape, sculpting]
level: practitioner
status: docs-checked
description: "Drive Blender's Multires modifier: Subdivide, Simple, Linear, Unsubdivide, Rebuild Subdivisions, Apply Base, Conform Base, Reshape and Delete Higher."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# multires-subdivide-reshape

Goal: build and manage multiresolution sculpt levels: add them correctly, recover them from a dense import, and push detail back to the base cage.

## Adding levels (Subdivision section)

- **Subdivide**: a smooth level using the default Catmull-Clark algorithm. The usual sculpt route.
- **Simple**: a level with unsmoothed base mesh edges (simple interpolation, no smoothing).
- **Linear**: a completely unsmoothed level using linear interpolation of the current sculpted displacement.
- Level fields: **Levels Viewport**, **Sculpt**, **Render**. In Sculpt Mode Alt-1 lowers and Alt-2 raises the sculpt level.

## Recovering levels from a dense mesh

- **Unsubdivide**: rebuilds a lower subdivision level of the current base mesh.
- **Rebuild Subdivisions** (Generate section): rebuilds all possible subdivision levels to generate a lower-resolution base, to make an optimized Multires version of an existing sculpt. Only available when no subdivision level has been created through the modifier.
- If a dense sculpt cannot be reduced this way, rebuild a clean base with retopology or Quadriflow remesh first.

## Push detail to the base

- **Apply Base**: modifies the unsubdivided mesh to match the form of the subdivided mesh, using a heuristic that assumes a Subdivision Surface modifier will be added to the mesh.
- **Conform Base**: also matches the subdivided form, but the resulting base vertex positions equal their subdivided positions.
- **Reshape**: copies the shape of another object onto the multires levels by copying vertex coordinates. Select the other mesh (matching topology and vertex indices) first, then Shift-select the multires object and click Reshape.
- **Delete Higher**: deletes all levels above the current one.
- **Save External** writes displacements to an external `.btx` file.

## Modifier notes

- Multires cannot be placed after modifiers that change geometry; deform modifiers after it act on the multires levels. Reshape with a Shrinkwrap modifier (wrap method Project, snap mode Above Surface, Negative on) is the documented way to re-project details from another sculpt.
- Advanced panel: **Quality**, **UV Smooth**, **Boundary Smooth**, **Use Creases**, **Use Custom Normals**. **Optimal Display** is in the main options, not the Advanced panel.

## Gotchas

- Changing the base topology once levels exist corrupts the subdivision details; finalize topology first.
- Voxel and Quadriflow remeshing do not work on objects with a Multires modifier (tested in 4.5.14: both operators' poll fails with "The remesher cannot run with a Multires modifier in the modifier stack" once the modifier has subdivision levels).

## Verify

Step through levels with the Sculpt level field: detail appears progressively. After Apply Base the level 0 cage hugs the sculpt more closely.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against modeling/modifiers/generate/multiresolution and meshes/retopology: Subdivide, Simple and Linear meanings, Unsubdivide, Rebuild Subdivisions availability, Apply Base heuristic, Conform Base, Reshape selection order, Delete Higher, Save External, Alt-1 and Alt-2, Optimal Display location, remesh restriction. Removed the unsupported Ctrl-number level keys and the quoted error message for failed Unsubdivide, and the claim that a Subdivision Surface modifier before Multires doubles subdivision.
Run note, 2026-11-01, Blender 4.5.14 LTS headless: `multires_subdivide` modes CATMULL_CLARK, SIMPLE and LINEAR each added one level (`levels`, `sculpt_levels`, `render_levels` followed `total_levels`); setting `levels` above `total_levels` was clamped to it; the operators `multires_unsubdivide`, `multires_rebuild_subdiv`, `multires_base_apply` (Apply Base), `multires_reshape`, `multires_higher_levels_delete`, `multires_external_save` and `multires_external_pack` exist, with no separate Conform Base operator in 4.5.14; Unsubdivide on a UV sphere raised "No valid subdivisions found to rebuild a lower level"; Quality, UV Smooth, Boundary Smooth, Use Creases and Use Custom Normals are modifier properties.
Method: documentation checked against the manual and API pages; part of the claims were run headless in Blender 4.5.14 (see the run note), but other claims describe Blender 5.x features that 4.5.14 does not have, so the status stays docs-checked.
