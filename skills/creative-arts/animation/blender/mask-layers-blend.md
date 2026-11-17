---
id: creative-arts.animation.blender.mask-layers-blend
name: mask-layers-blend
category: creative-arts
field: animation
product: blender
tags: [blender, masking, mask-layers-blend, mask-layer, roto]
level: practitioner
status: docs-checked
description: "Organise Blender masks with layers: Opacity, Invert, Blend modes (Merge Add, Merge Subtract and others), Falloff, Move to Layer and per-layer restrict toggles."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/sidebar.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mask-layers-blend

Goal: combine several mask shapes into one clean matte, with some shapes cutting holes or behaving differently.

## Mask Layers panel (Sidebar > Mask tab)

A Mask data-block holds layers; a layer holds one or several splines. Layers group splines so they can be animated or parented together (for example one motion-tracked point can drive a whole layer). Per layer:

- **Opacity** and **Invert** (inverts the values in the layer).
- **Blend**: Merge Add, Merge Subtract, Add, Subtract, Lighten, Darken, Multiply, Replace, Difference. The manual says *Merge Add* and *Merge Subtract* give better results than plain add and subtract when a *Feather* is used on overlapping masks.
- **Falloff**: the shape of the feather transition between black and white.
- **Holes**, **Overlap**, **Fill Solver**: see `creative-arts.animation.blender.mask-holes-overlap`.
- **Move to Layer** (M): moves the active spline to another layer or creates a new layer.
- The layer list rows carry Restrict View, Restrict Select and Restrict Render toggles (Blender's `hide`, `hide_select`, `hide_render` layer properties).

## Layer strategy

- One layer per independent subject or motion (the manual's example: two unwanted people crossing in footage get one layer each in a single mask data-block, so where they meet the shapes add rather than making a hole).
- Use a Subtract (or Merge Subtract) layer for a gap that should be cut out.
- Use Restrict Select on finished layers so points are not moved by accident.

## Using the mask elsewhere

The compositor **Mask** node selects a Mask data-block. Its outputs are the black and white *Mask*; it has Feather, Size Source and Motion Blur settings. Use a separate Mask data-block when a different matte is needed.

## Verify

Connect a Mask node to a Viewer: overlapping shapes form one even white matte and subtracted areas are black.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/masking/sidebar, compositing/types/input/mask) and the 5.2 source (rna_mask.cc blend enum, restrict properties; properties_mask_common.py layer panel). Confirmed the Blend list, Opacity, Invert, Falloff, Move to Layer (M) and the Mask node. Removed unconfirmed claims about layer ordering, density with plain Add, and a lock toggle (the list has Restrict View, Select and Render).
Method: documentation only; no commands were run.
