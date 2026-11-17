---
id: creative-arts.animation.blender.mesh-filter
name: mesh-filter
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, mesh-filter, sculpt-filter, color-filter, sharpen, enhance-details, random-filter]
level: practitioner
status: docs-checked
description: "Apply Blender sculpt Mesh Filter and Color Filter to whole or masked meshes: smooth, inflate, sphere, random, relax, sharpen, enhance details, erase displacement."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/mesh_filter.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/color_filter.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/mask.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mesh-filter

Goal: global or mask-limited operations without brushing. Pick the filter in the Toolbar, then click and drag left to right (or right to left for a negative effect) in the viewport.

## Mesh Filter

Deforms all vertices at once; masking, auto-masking and visibility are taken into account.

Filter Type:
- **Smooth**: polishes surfaces or removes volume; useful for voxel remesher artifacts.
- **Scale**, **Inflate** (uniform along the normal), **Sphere** (morph progressively to a sphere), **Random** (random movement along the vertex normal).
- **Relax**: evens out the quad distribution without deforming the volume. **Relax Face Sets**: removes jagged lines on face set borders.
- **Surface Smooth**: evens out vertex positions while preserving volume; options Shape Preservation and Per-Vertex Displacement.
- **Sharpen**: pinches hard edges and polishes flat surfaces by curvature; options Smooth Ratio, Intensify Details, Curvature Smooth Iterations.
- **Enhance Details**: intensifies high-frequency detail.
- **Erase Displacement**: deletes Multires displacement, resetting to the regular subdivision result; useful after a Shrinkwrap. Negative strokes intensify the displacement.
- Common settings: **Strength** (adjust at unusual object scales), **Deformation Axis**, and **Orientation** (Local, World, View) to limit displacement.

## Color Filter

Applies colour corrections to the active color attribute on all vertices at once. Filter types: Fill, Hue, Saturation, Value, Brightness, Contrast, Smooth, Red, Green, Blue. LMB applies at the tool strength, LMB-drag sets strength interactively, Ctrl-LMB fills with the secondary colour, Ctrl-X applies a full-strength fill. **Fill Color** and **Strength** are tool settings.

## Recipes

- Thicken one part: mask everything else (Invert Mask from the A pie or Ctrl-I), then Inflate.
- Rock breakup: Random, then Surface Smooth.
- Tidy face set borders before extracting: Relax Face Sets.

## Gotchas

- Drag small amounts and repeat; adjust Strength if the effect is too strong or weak for the object scale.
- Check the masked area is unchanged after applying (undo and redo to compare).

## Verify

Undo and redo to compare before and after; masked areas stay unchanged.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/tools/mesh_filter, color_filter and editing/mask: filter type names (the type is called Relax, not Relax Topology), per-filter options, Erase Displacement behaviour, Color Filter types and mouse usage, Ctrl-I invert. Removed unconfirmed sample strength numbers and the claim about Sphere with an off-centre origin.
Method: documentation only; no commands were run.
