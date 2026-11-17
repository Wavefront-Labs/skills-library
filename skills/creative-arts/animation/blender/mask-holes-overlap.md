---
id: creative-arts.animation.blender.mask-holes-overlap
name: mask-holes-overlap
category: creative-arts
field: animation
product: blender
tags: [blender, masking, mask-holes, mask-overlap, mask-layer, roto]
level: practitioner
status: docs-checked
description: "Control how overlapping mask splines fill in Blender: Holes and Overlap on a layer, Fill Solver, spline Fill and Self Intersection Check, and separate layers."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/sidebar.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mask-holes-overlap

Goal: predictable fill when mask shapes overlap or intersect.

## Settings

Mask editor (Movie Clip Editor or Image Editor in Mask mode), Sidebar > Mask tab.

- **Mask Layers** panel, per layer: **Holes** (overlapping splines from the same layer generate holes in the mask) and **Overlap** (fills self-intersecting areas). Next to them is **Fill Solver**: *Sweep Line* is fast but has no support for self-intersection, *Delaunay* is robust with support for self-intersections. The Overlap option only applies to the Sweep Line solver (the panel greys it out for Delaunay).
- **Active Spline** panel, per spline: **Fill** (a filled area; when off, Blender makes a curve with thickness, for thin objects such as wires or hair) and **Self Intersection Check** (stops the *feather*, not the curve itself, from intersecting itself).
- **Blend** on a layer (for example Subtract or Merge Subtract) cuts one layer out of the layers it combines with. See `creative-arts.animation.blender.mask-layers-blend`.

## When to use which

| Need | Setting |
|---|---|
| A ring or window frame from two splines | Both splines on one layer, Holes on |
| Two shapes that should add together where they cross | Put them on separate layers (the manual's example: two people crossing paths, one layer each, so the shapes add together instead of creating a hole) |
| A shape whose outline crosses itself | Overlap on (Sweep Line) or switch Fill Solver to Delaunay |
| A feather that loops over itself | Self Intersection Check on the spline |

## Verify

View the mask through a Mask node into a Viewer (white on black) and scrub the shot: no unexpected holes or filled gaps on any frame.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch, movie_clip/masking/sidebar) and the 5.2 source (rna_mask.cc, properties_mask_common.py). Confirmed: Holes and Overlap on the Mask Layers panel, Fill Solver items and the Overlap restriction to Sweep Line, Fill and Self Intersection Check on Active Spline and what they do, and the two-layer crossing example. Removed unconfirmed claims about thin dark lines and flicker.
Method: documentation only; no commands were run.
