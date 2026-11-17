---
id: creative-arts.animation.blender.mask-splines-feather
name: mask-splines-feather
category: creative-arts
field: animation
product: blender
tags: [blender, masking, roto, mask-splines-feather, mask-spline, feather-points, mask-editor]
level: practitioner
status: docs-checked
description: "Draw roto masks in Blender: Ctrl click points, Toggle Cyclic, handle types, feather points and Scale Feather, plus the Feather Offset and Falloff settings in the sidebar."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/editing.html
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/sidebar.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mask-splines-feather

Goal: precise, soft-edged mask shapes for rotoscoping.

## Setup

Open the Movie Clip Editor or the Image Editor and change the mode to **Mask** in the header; this adds the mask tools and panels. Create or pick a Mask data-block.

## Drawing and editing

- **Add Vertex and Slide** (Ctrl LMB): inserts a control point and defines handle orientation with a continued drag; on an existing spline it inserts a point. If the last point was selected, a double-click also closes the curve.
- **Toggle Cyclic** (Alt C): closes or opens the curve by joining the last control point to the first.
- **Set Handle Type** (V): Auto, Vector, Aligned Single, Aligned or Free (the 5.2 enum labels).
- **Add Feather Vertex and Slide** (Shift Ctrl LMB): inserts feather control points that move independently of the main curve. If no feather is in use it creates a basic feather.
- **Scale Feather** (Alt S) scales the feather size; **Clear Feather Weight** (Mask menu) resets feather weight to zero.
- Move, Rotate, Scale work with G, R, S. Mask > Add offers Circle and Square primitives.

## Feather settings

- **Active Spline** panel: **Feather Offset** (*Even* keeps the feather thickness but can loop; *Smooth* gives a smoother shape but can produce a sharp feather on S-shaped segments), **Weight Interpolation** (*Linear* or *Ease*), **Cyclic**, **Fill**, **Self Intersection Check**.
- **Mask Layers** panel: **Falloff** sets the shape of the feather transition (Smooth, Sphere, Root, Inverse Square, Sharp or Linear).
- In the compositor Mask node, **Feather** turns the drawn feather on or off.

## Practice (not from the manual)

Roto complex subjects as several simple shapes with as few points as possible; they are easier to animate than one detailed outline.

## Verify

Connect a Mask node to a Viewer over the plate: edges hug the subject and feathers are soft only where intended.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/masking/editing, movie_clip/masking/sidebar, compositing/types/input/mask) and the 5.2 source (rna_mask.cc handle, offset, interpolation and falloff enums; properties_mask_common.py Add menu). Fixed: the handle-type names, and Feather Offset and Falloff live in the Active Spline and Mask Layers panels, not a Mask Settings panel. Removed unconfirmed claims about feather-line artefacts and motion-blurred edges.
Method: documentation only; no commands were run.
