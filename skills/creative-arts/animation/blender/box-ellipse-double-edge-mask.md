---
id: creative-arts.animation.blender.box-ellipse-double-edge-mask
name: box-ellipse-double-edge-mask
category: creative-arts
field: animation
product: blender
tags: [blender, mattes, double-edge-mask, box-mask, ellipse-mask, compositor]
level: practitioner
status: docs-checked
description: "Shape masks in the compositor: Box and Ellipse Mask (Mask Type, Position, Size, Rotation, Value) and Double Edge Mask (Outer, Inner, Images Edges, Only Inside Outer)."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/mask/box_mask.html
  - https://docs.blender.org/manual/en/latest/compositing/types/mask/ellipse_mask.html
  - https://docs.blender.org/manual/en/latest/compositing/types/mask/double_edge_mask.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# box-ellipse-double-edge-mask

Goal: quick shape masks without roto, and controlled gradients between shapes.

## Box Mask and Ellipse Mask nodes (Mask category)

- **Mask Type** (operation against the input mask): **Add** (union; covered areas set to Value), **Subtract**, **Multiply** (intersection) and **Not**. Chain several nodes to combine shapes.
- **Mask**: optional input mask used as the base. **Value**: intensity of the generated mask.
- **Position**: centre as a fraction of the frame (0.5, 0.5 is centred; 0.0, 0.0 is the lower left).
- **Size**: width and height as a fraction of the image width (equal values give a circle on the Ellipse Mask).
- **Rotation** around the centre.
- Output **Mask**, sized to the scene render dimensions. Edges are hard; for soft edges pass the mask through a slight Blur node (a heavy blur for a vignette).
- With the Active Node gizmo enabled, the Ellipse Mask has an interactive gizmo in the node editor: drag edges or corners to resize (hold Shift to keep the aspect ratio), the centre cross to move and the centre dot to rotate.

Uses: vignettes (see comp-vignette), screen inserts, quick grade windows, garbage mattes for static rigs.

## Double Edge Mask node

Creates a gradient between two masks. Inputs: **Outer Mask** (fades from black at its edges to white at the inner mask) and **Inner Mask** (fully white).
- **Images Edges**: when on, the image edges that intersect the outer mask count as edges of the outer mask; when off the outer mask is treated as open-ended.
- **Only Inside Outer**: when on, only inner-mask edges lying inside the outer mask are considered; otherwise all inner edges are.
Output: **Mask**.

Uses: soft-edged falloff and gradient mattes shaped like the subject, transitions between a tight core and a loose outer roto shape.

## Gotchas

- Position and size are fractions of the frame, so they hold at any resolution.
- Judge a Double Edge Mask result with a Viewer; test it on hard-edged (black or white) inputs first.

## Verify

View the mask with a Viewer and sample: inside exactly 1, outside exactly 0, gradient smooth with no banding.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Box and Ellipse Mask Mask Type operations, Position, Size (fraction of image width), Rotation, Value, output size and blur tip, Ellipse gizmo; Double Edge Mask Outer Mask, Inner Mask, Images Edges and Only Inside Outer. Removed the old Inner Edge and Buffer Edge names, the binary-inputs requirement and the keyframing instruction.
Method: documentation only; no commands were run.
