---
id: creative-arts.animation.blender.edge-vertex-slide
name: edge-vertex-slide
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, edge-slide, vertex-slide, gg, even-mode, topology-tweaks]
level: practitioner
status: docs-checked
description: "Move topology along the surface in Blender: Edge Slide and Slide Vertices (G G / Shift V), Even and Flipped, Clamp, Mirror Editing and Correct UVs to keep textures in place."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/edge_slide.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/slide_vertices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# edge-vertex-slide

Goal: adjust edge flow without changing the silhouette.

## Edge Slide

- Edit Mode: select one or more edges (Select > Select Loops helps) and press `G` twice, or use Edge > Edge Slide. The edges move across their neighbouring faces; click `LMB` to confirm, `RMB` to cancel.
- By default every vertex moves the same percentage toward its neighbour. **Even** (`E`) keeps all vertices at the same absolute distance from a neighbouring vertex; **Flipped** (`F`) picks the other neighbour while Even is on.
- **Factor**: direction and amount; -1 and 1 move the edges fully to one neighbour. **Clamp** (`Alt` or `C`) keeps edges inside their neighbouring faces. **Mirror Editing** also slides matching edges across the mesh (needs Mesh Symmetry enabled). **Correct UVs** adjusts UVs of moved vertices to avoid texture distortion.

## Slide Vertices

- Vertex > Slide Vertices, `G` twice, or `Shift V`: each selected vertex moves along one of its adjacent edges; move the mouse along the wanted edge, then click.
- Redo panel: Factor, Even (`E`), Flipped (`F`, only with Even), Clamp (`Alt`/`C`; off lets vertices leave their edge), Mirror Editing, Correct UVs.

## Uses

- Tighten support loops toward an edge for sharper subdivision corners.
- Re-space retopology loops.
- Move a loop along a surface without changing the silhouette.

## Gotchas

- Even and Flipped are relative to the Factor: Factor is still a relative number.
- Select clean edge chains; slide is defined by neighbouring faces.

## Verify

Silhouette unchanged (compare in wireframe or X-ray from the front); UV editor shows no texture shift when Correct UVs is on.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Edge Slide and Slide Vertices pages: shortcuts, Even/Flipped/Clamp keys, Factor range, Mirror Editing, Correct UVs. Removed the unconfirmed default for Correct UVs, Mirror-modifier clipping and snapping claims.
Method: documentation only; no commands were run.
