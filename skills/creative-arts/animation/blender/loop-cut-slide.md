---
id: creative-arts.animation.blender.loop-cut-slide
name: loop-cut-slide
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, loop-cut, loop-cut-slide, offset-edge-slide, subdivide-edges, edge-loops]
level: practitioner
status: docs-checked
description: "Add edge loops in Blender: Loop Cut and Slide (Ctrl R, Even/Flipped), Offset Edge Slide (Shift Ctrl R) for paired loops, and Subdivide options (cuts, smoothness, corner type)."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/loop.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/loopcut_slide.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/offset_edge_slide.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/subdivide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# loop-cut-slide

Goal: add resolution and support loops exactly where needed.

## Loop Cut and Slide (`Ctrl R`, Edge > Loop Cut and Slide)

- Hover an edge that is perpendicular to the cut direction: a yellow line previews the loop (the Loop Cut toolbar tool shows magenta). Scroll the wheel, press `PageUp`/`PageDown`, or type a number to set **Number of Cuts**; `Alt Wheel` changes Smoothness. `LMB` confirms the loop and moves to sliding, `RMB` aborts.
- Sliding: move the mouse, `LMB` creates the cut there, `RMB` creates it at the centre.
- Options (live and in the Adjust Last Operation panel): **Smoothness** (offsets new edges along normals to keep curvature), **Falloff** (shape for Smoothness), **Factor**, **Even** (`E`: even distance to an adjacent loop), **Flipped** (`F`: which neighbour Even follows), **Clamp** (`C` or hold `Alt`), **Mirror Editing** (needs Mesh Symmetry), **Correct UVs**.
- The new loop stops where the face loop ends, at poles (triangles and n-gons).
- The Loop Cut toolbar tool has Number of Cuts and Correct UVs in Tool Settings; its cuts are uniformly distributed in the face loop and their positions are not controllable there; the Loop Cut and Slide options appear in the redo panel afterwards.

## Offset Edge Slide (`Shift Ctrl R`, Edge > Offset Edge Slide)

- Select one or more edges; it creates two new edges surrounding each selected edge. Move the mouse (right increases the distance, left decreases) or type a number. Useful for support loops around a hard edge.
- Options: **Cap Endpoint** (creates triangles at the ends of each edge chain), **Factor**, **Even** (`E`), **Flipped** (`F`), **Clamp** (`Alt`/`C`), **Mirror Editing**, **Correct UVs** (off: new vertices copy the UVs of the originals).

## Subdivide (Edge > Subdivide)

- Options in the redo panel: **Number of Cuts** (1 halves edges, 2 gives thirds), **Smoothness** (displaces to keep approximate curvature), **Create N-Gons** (off forces triangles or quads), **Quad Corner Type** (Inner Vertices, Path, Straight Cut, Fan; for quads with two adjacent selected edges), **Fractal**, **Along Normal**, **Random Seed**.
- Un-Subdivide (Edge > Un-Subdivide, option Iterations) tries to undo a previous subdivide.

## Verify

The new loop runs all the way around the face loop and the count matches the requested cuts.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Loop Cut and Slide, Loop Cut tool, Offset Edge Slide, Subdivide and Un-Subdivide pages. Corrected: the corner type name is Inner Vertices, and Cap Endpoint makes triangles at chain ends. Removed unconfirmed On Cage, Mirror-modifier and seam advice.
Method: documentation only; no commands were run.
