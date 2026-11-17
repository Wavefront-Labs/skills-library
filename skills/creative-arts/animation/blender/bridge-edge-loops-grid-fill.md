---
id: creative-arts.animation.blender.bridge-edge-loops-grid-fill
name: bridge-edge-loops-grid-fill
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, bridge-edge-loops, grid-fill, fill-holes, topology, quads]
level: practitioner
status: docs-checked
description: "Connect and cap openings with quads in Blender: Bridge Edge Loops (cuts, twist, interpolation, merge) and Grid Fill (span, offset, simple blending) instead of Fill or ngons."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/bridge_edge_loops.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/grid_fill.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bridge-edge-loops-grid-fill

Goal: join parts and close openings with clean quad topology that subdivides well.

## Bridge Edge Loops (Edge menu)

- Deletes any selected faces, then creates faces between two or more selected edge loops. In Blender an "edge loop" is any chain of connected edges, closed or not.
- Redo panel: **Connect Loops** (Open Loop, Closed Loop, Loop Pairs), **Merge** (merge loops into one instead of creating faces) with **Merge Factor** (0 merges into the first loop, 1 into the last), **Twist** (offsets which target vertex each source vertex connects to, twisting the tube), **Number of Cuts**, **Interpolation** (Linear, Blend Path, Blend Surface), **Smoothness** (for Blend Path and Blend Surface; 0 is like Linear), **Profile Factor** and **Profile Shape**.
- Use: arm to torso, handles on mugs, tubes between pipes, holes cut in two surfaces and connected (selected faces are deleted and their openings bridged).

## Grid Fill (Face menu)

- Input: a roughly rectangular loop of edges (or just two opposing sides of one), or a roughly rectangular patch of faces; the output is a grid of quads.
- Best results when each pair of opposing sides has the same vertex count; this is not required.
- Redo panel: **Span** (number of columns; rows are derived), **Offset** (which vertex is the first corner, by default the active vertex; rotate the layout), **Simple Blending** (simpler interpolation, better on flat surfaces or where preserving curvature is unwanted).

## Fill and Make Edge/Face

- `Alt F` (Face > Fill) fills a closed edge loop with triangles. Make Edge/Face (`F`) fills edges or vertices with a single n-gon.
- Neither gives the quad grid that subdivision and deformation prefer; use Grid Fill or Bridge there.

## Gotchas

- Grid Fill's error "Loops are not connected by wire/boundary edges" means the selected edge chains do not form a closed loop; add edges to close it.
- Fix a skewed grid with Offset in the redo panel rather than reselecting; fix a twisted bridge with Twist.

## Verify

Select > Select All by Trait > Faces by Sides (set the side count in the redo panel) finds no unintended triangles or n-gons; check the area with a Subdivision Surface modifier for pinching.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Bridge Edge Loops, Grid Fill, Fill and Select All by Trait pages: all option names, Merge Factor and Smoothness behaviour, Grid Fill inputs, the real error text, Alt F as triangle fill. Removed the even-vertex-count requirement, the wrong error strings and the unconfirmed claim that mismatched counts always make triangles.
Method: documentation only; no commands were run.
