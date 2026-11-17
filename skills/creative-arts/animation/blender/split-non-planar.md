---
id: creative-arts.animation.blender.split-non-planar
name: split-non-planar
category: creative-arts
field: animation
product: blender
tags: [blender, split-non-planar, split-concave, mesh-cleanup, ngons, export-prep]
level: practitioner
status: docs-checked
description: "Fix non-planar and concave faces in Blender: Split Non-Planar, Split Concave, Make Planar, find them with the Distortion overlay, then triangulate with Ctrl T or the modifier."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/mesh_analysis.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/triangulate_faces.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/triangulate.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# split-non-planar

Goal: faces that triangulate predictably in engines, renderers and 3D printers.

## The problem

Distorted (non-flat) n-gons have an undefined triangulation, which can cause shading creases and inverted triangles; concave faces are a related problem.

## Tools (Edit Mode > Mesh > Clean Up)

- **Split Non-Planar Faces**: splits selected faces bent beyond *Max Angle*. Use Rotate Edge if you want newly created edges to point another way.
- **Split Concave Faces**: splits concave faces so only convex ones remain.
- **Make Planar Faces**: flattens the selected faces instead of splitting them. *Factor* is the flattening strength per iteration and may need more *Iterations* even at 1.

## Finding them

- Overlays > Mesh Analysis > **Distortion** (Edit Mode, Solid shading) colours faces that are not flat: high values red, low blue, out-of-range gray. Set Minimum/Maximum.
- Select > Select All by Trait > **Faces by Sides** (side count in the redo panel) lists n-gons or triangles.

## Triangulate deliberately

Triangulate Faces (`Ctrl T`, Face menu) or the Triangulate modifier fixes the triangulation. Modifier options: Quad Method (Beauty, Fixed, Fixed Alternate, Shortest Diagonal, Longest Diagonal), N-gon Method (Beauty, Clip) and Minimum Vertices.

## Gotchas

- Splitting faces on a subdivision model changes edge flow; fix the geometry instead where possible.
- Make Planar changes vertex positions; check that curved areas are not flattened unintentionally.
- Mesh Analysis is for 3D printing checks, shows only with deform modifiers and is slow on high-poly meshes while editing.

## Verify

Distortion overlay shows nothing above your threshold; compare the exported mesh's shading in the target application with Blender.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Clean Up, Mesh Analysis, Triangulate Faces, Triangulate Modifier and Select All by Trait pages. Removed the unconfirmed 5-10 degree starting angle, the Beauty/Shortest recommendation, and claims about export seams.
Method: documentation only; no commands were run.
