---
id: creative-arts.animation.blender.gn-mesh-boolean-dual
name: gn-mesh-boolean-dual
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-mesh-boolean, mesh-boolean-node, gn-dual-mesh, dual-mesh, mesh-to-points, procedural-modeling]
level: practitioner
status: verified
description: "Use the Geometry Nodes Mesh Boolean node (Exact vs Float solver, cutters, Intersecting Edges output) and Dual Mesh / Mesh to Points for procedural cutouts and honeycomb looks."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/mesh/operations/mesh_boolean.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/mesh/operations/dual_mesh.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/mesh/operations/mesh_to_points.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-mesh-boolean-dual

Goal: procedural booleans with many cutters, and topology transformations for stylized structures.

## Mesh Boolean node

- **Operation**: Intersect, Union, Difference (same operations as the Boolean modifier); inputs are Mesh 1 and Mesh 2.
- **Solver**: *Exact* (best with coplanar or overlapping faces, much slower), *Float* (good performance, no support for overlapping geometry), *Manifold* (usually fastest, only for manifold meshes plus Difference with a plane).
- **Self Intersection** and **Hole Tolerant** apply to the Exact solver only.
- Output **Intersecting Edges** (available with the Exact and Manifold solvers; the Float solver has no such output) is a boolean field of the edges created where the inputs meet — use it to bevel or add a trim material along the cut (Set Material with that selection after an edge→face domain conversion, or Extrude Edges).

## Recipes

- **Perforated panel**: Grid → Mesh to Points/Distribute → Instance on Points (small cylinders) → Realize Instances → Mesh Boolean Difference (Exact) from a solidified plate.
- **Window cutouts on a procedural building**: cutter geometry per floor/bay joined into one input; keep the Exact solver.

## Dual Mesh

Turns faces into vertices and vertices into faces; face-domain attributes move to the point domain. It only works on manifold geometry (remesh non-manifold input first). **Keep Boundaries** keeps non-manifold boundaries in place. It pairs well with triangulated meshes such as an Ico Sphere (evenly spaced triangles).

## Mesh to Points

Modes: Vertices, Edges (edge midpoints by default), Faces (average of the face's vertices by default), Corners (placed at the corner's vertex, so they overlap by default). Inputs: Selection, Position, Radius.

## Gotchas

- The Exact solver is much slower than Float; bake the result or use Manifold for closed meshes.
- The Float solver does not support overlapping geometry; switch to Exact for coplanar faces.
- Hole Tolerant costs extra time; enable it only when Exact shows errors on non-manifold input.

## Verify

Spreadsheet face count stable across frames.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Mesh Boolean, Dual Mesh and Mesh to Points pages: solver descriptions, Exact-only options and Intersecting Edges output, Keep Boundaries, manifold-only warning, Mesh to Points modes. Removed unconfirmed claims: multi-input Mesh 2, instance handling, Manifold version gate, UV inheritance, nudge value.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Mesh Boolean operations Intersect, Union, Difference and solvers Exact, Float, Manifold exist; Self Intersection and Hole Tolerant inputs are enabled only for Exact. Evaluated a cube minus an offset cube: Exact and Manifold both flagged 6 Intersecting Edges, Float exposed no Intersecting Edges output (the old text said Exact only). Dual Mesh on an Ico Sphere (12 vertices, 20 faces) gave 20 vertices and 12 faces; Dual Mesh has a Keep Boundaries input. Mesh to Points modes on a cube gave 8, 12, 6 and 24 points for Vertices, Edges, Faces and Corners, with Selection, Position and Radius inputs. Not run (confirmed from the manual only): solver speed and overlap behaviour, the recipes, default placement of edge and face points.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
