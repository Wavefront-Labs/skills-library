---
id: creative-arts.animation.blender.degenerate-dissolve
name: degenerate-dissolve
category: creative-arts
field: animation
product: blender
tags: [blender, degenerate-dissolve, delete-loose, mesh-cleanup, merge-by-distance, clean-up]
level: intro
status: docs-checked
description: "Clean imported or boolean-heavy Blender meshes with Mesh > Clean Up: Delete Loose, Degenerate Dissolve, Limited Dissolve, Merge by Distance, Fill Holes, then check Non Manifold."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/delete.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/all_by_trait.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# degenerate-dissolve

Goal: imported or boolean-heavy meshes become manifold-friendly and export-safe.

## Edit Mode > Mesh > Clean Up

| Tool | What it does |
|---|---|
| **Delete Loose** | deletes selected vertices, edges and optionally faces that are not connected to anything |
| **Decimate Geometry** | reduces face count of the selection by *Ratio* (target triangle count ratio), optional vertex group and symmetry |
| **Degenerate Dissolve** | collapses selected edges shorter than *Merge Distance*, which also removes small faces; vertices near each other but not joined by an edge are not merged |
| **Limited Dissolve** (also Mesh > Delete) | dissolves vertices and edges in flattish areas up to *Max Angle*; option All Boundaries and Delimit |
| **Make Planar Faces** | flattens faces (Factor, Iterations) |
| **Split Non-Planar / Split Concave** | see `creative-arts.animation.blender.split-non-planar` |
| **Merge by Distance** | merges vertices closer than *Merge Distance* (Unselected, Sharp Edges options) |
| **Fill Holes** | fills each hole with a face; *Sides* is the maximum hole size, 0 fills all |

## Order for imports (CAD, scans, photogrammetry)

1. Select all, Merge by Distance (set the distance for your model scale; start small).
2. Delete Loose.
3. Degenerate Dissolve (Merge Distance slightly above the import precision).
4. Recalculate normals (`Shift N`).
5. Select All by Trait > Non Manifold to find what remains; fix by hand or with Fill Holes.

## Gotchas

- A merge distance that is too large collapses small details; increase gradually.
- Degenerate Dissolve and Limited Dissolve can leave n-gons; triangulate if exporting needs it.
- These operators are destructive: keep a copy. The Weld modifier merges by distance non-destructively, and the Decimate modifier in Collapse mode is the non-destructive Decimate Geometry.

## Verify

Statistics overlay vertex count drops by the expected duplicates; Non Manifold selection shows only intentional open edges.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Clean Up and Deleting & Dissolving pages. Corrected: Degenerate Dissolve collapses short selected edges (it does not merge unconnected nearby vertices); Delete Loose definition. Removed the unconfirmed 0.0001 m figure, per-element options claim and the 3D Print Toolbox check.
Method: documentation only; no commands were run.
