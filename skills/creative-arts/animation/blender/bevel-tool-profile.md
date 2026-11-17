---
id: creative-arts.animation.blender.bevel-tool-profile
name: bevel-tool-profile
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, bevel, bevel-profile, bevel-segments, harden-normals, clamp-overlap, miter]
level: practitioner
status: docs-checked
description: "Master Blender's Bevel tool (Ctrl B / Shift Ctrl B): width types, segments, profile shape and custom profiles, clamp overlap, loop slide, miters, harden normals and face strength."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/bevel.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bevel-tool-profile

Goal: chamfers and rounds that catch highlights, with clean topology and normals.

## Invoke

- Edit Mode: `Ctrl B` (Bevel Edges) or `Shift Ctrl B` (Bevel Vertices); menus Edge > Bevel Edges and Vertex > Bevel Vertices. Move the mouse for width and roll the wheel for segment density; `LMB`/`Return` confirms, `RMB`/`Esc` cancels.
- While the tool is active the settings show at the top of the 3D Viewport and in the status bar. Hold `Shift` for finer steps or `Ctrl` for coarse snapping. After confirming, every setting stays editable in the Adjust Last Operation panel.
- Keys: `V` Affect (Vertices or Edges), `M` Width Type, `A` Width, `S` Segments, `P` Profile Shape, `H` Harden Normals, `C` Clamp Overlap, `U` Mark Seams, `K` Mark Sharp, `O` Miter Outer, `I` Miter Inner, `N` Intersection Type, `Z` Profile Type.

## Redo panel

- **Affect**: Vertices bevels only the selected vertices; Edges bevels the selected edges plus vertices where three or more edges meet.
- **Width Type**: Offset, Width, Depth, Percent or Absolute; it sets the meaning of **Width**. With several edges the tool compromises where widths conflict; turning off Loop Slide can help it match the requested width.
- **Segments**: density of new geometry. **Profile Shape**: a value between 0 and 1 shaping the side view of each beveled edge; it also shapes the miters when a miter is Arc.
- **Profile Type**: *Superellipse* (from Profile Shape) or *Custom* (curve widget in the panel; the Support Loops and Steps presets are built from the segment count, so re-apply a preset after changing Segments). Custom also offers *Sample Straight Edges* and *Sample Even Lengths*.
- **Clamp Overlap**: stops beveled edges overshooting their neighbouring faces.
- **Loop Slide**: whether new inner edges are perpendicular to the beveled edge or follow the existing inner edges.
- **Harden Normals**: assigns custom split normals to the new faces so they look smooth without changing the rest of the mesh.
- **Mark**: Seams (new edges between two seam edges meeting at a beveled vertex become seams) and Sharp (same for sharp edges).
- **Miter Outer** (Sharp, Patch, Arc), **Miter Inner** (Sharp, Arc) and **Spread** (inner Arc size) control corners where three or more beveled edges meet.
- **Intersection Type**: Grid Fill or Cutoff where beveled edges meet.
- **Material Index**: 0-based slot for the new faces; -1 inherits from neighbours.
- **Face Strength**: None, New, Affected or All, for use with a Weighted Normal modifier that has Face Influence on.

## Gotchas

- Bevel is destructive; the Bevel modifier does the same non-destructively.
- Adjust Segments before applying a Custom profile preset.

## Verify

Matcap or studio lighting highlights read evenly along the new faces; Select > Select All by Trait > Non Manifold selects nothing new.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Bevel page: menus, shortcuts, per-option key hints, Width Type list, Profile Shape range, Profile Type and presets, Loop Slide, Harden Normals, Mark, miters, Intersection Type, Face Strength and Material Index. Removed unconfirmed defaults, shape-value meanings and generic gotchas.
Method: documentation only; no commands were run.
