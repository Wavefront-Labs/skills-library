---
id: creative-arts.animation.blender.shrink-fatten-smooth-randomize
name: shrink-fatten-smooth-randomize
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, shrink-fatten, smooth-vertices, randomize-vertices, laplacian-smooth, vertex-tools]
level: practitioner
status: docs-checked
description: "Inflate, relax or roughen Blender mesh parts: Shrink/Fatten (Alt S), Smooth Vertices, Laplacian smooth and Randomize, with Offset Even, Uniform and Normal options."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/shrink-fatten.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/smooth_vertices.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/laplacian_smooth.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/laplacian_smooth.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/randomize.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# shrink-fatten-smooth-randomize

Goal: inflate, relax or roughen parts of a mesh without sculpting.

## Shrink/Fatten (`Alt S`, Mesh > Transform > Shrink/Fatten)

- Moves the selected vertices inward or outward along their normals, all by the same distance. Move the mouse down to shrink and up to fatten, or type a distance; `LMB`/`Return` confirms.
- Redo panel: **Offset**; **Offset Even** (off: each vertex moves the same distance; on: each edge is offset the same distance; toggle with `S` or hold `Alt`); **Mirror Editing** (needs Mesh Symmetry); **Proportional Editing**.
- Toolbar tool with Push/Pull in the same group.

## Smooth Vertices (Vertex > Smooth Vertices, or the context menu)

- Redo options: **Smoothing** (factor), **Repeat** (iterations), **Axes** (limit the effect to some axes).
- If the mesh is too coarse and stays blocky, subdivide first. The Smooth modifier does this non-destructively. Smooth Faces (Shade Smooth) is unrelated: it only changes normals.

## Smooth Vertices (Laplacian)

- Vertex > Smooth Vertices (Laplacian) uses the Smooth Laplacian algorithm. The modifier reduces noise with minimal changes to shape; its options are **Repeat**, **Axis**, **Lambda Factor** (negative exaggerates shape), **Lambda Border** (border edges are smoothed separately), **Preserve Volume** (reduces shrinkage from large Factor or Repeat) and **Normalized**. Meshes with more than 10,000 vertices can take minutes; test on a small portion.

## Randomize (Mesh > Transform > Randomize)

- Moves selected vertices in random directions. **Amount** (maximum distance), **Uniform** (0: random distance between 0 and Amount; 1: exactly Amount; direction stays random), **Normal** (0: fully random direction; 1: along the normal or its opposite), **Random Seed**.
- Object Mode has a separate Randomize Transform for objects.

## Gotchas

- Use Select > Select Loops > Boundary Loops to find boundary vertices when you want to exclude them from smoothing, then deselect them.
- Run Recalculate Normals first if some faces are flipped, since Shrink/Fatten follows normals.

## Verify

Compare with `Ctrl Z` / `Shift Ctrl Z`; check the dimensions in the Sidebar Item tab or Statistics overlay to judge volume loss.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Shrink/Fatten, Smooth Vertices, Smooth Vertices (Laplacian), Smooth Laplacian Modifier and Randomize pages (Edit Mode and Object Mode). Corrected: Offset Even is per edge when on; Uniform and Normal semantics; Laplacian options belong to the modifier page the operator refers to. Removed unconfirmed flat-bottom, volume-shrink and Mirror-modifier remarks.
Method: documentation only; no commands were run.
