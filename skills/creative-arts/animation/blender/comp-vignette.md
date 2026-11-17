---
id: creative-arts.animation.blender.comp-vignette
name: comp-vignette
category: creative-arts
field: animation
product: blender
tags: [blender, vignette, vignette-mask, vignette-ellipse, compositor, color-grade]
level: practitioner
status: docs-checked
description: "Add a vignette in the compositor: the Vignette node (Factor, Feather, Corner Roundness, Scale, Offset, Angle, Mask output) or an Ellipse Mask with heavy blur and Multiply."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/camera_lens_effects/vignette.html
  - https://docs.blender.org/manual/en/latest/compositing/types/mask/ellipse_mask.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# comp-vignette

Goal: a subtle, lens-like darkening toward the corners.

## Vignette node (Camera Lens Effects category)

Inputs: **Image**, **Factor** (overall strength; 0 disables), **Feather** (softness of the transition), and the Transform settings **Corner Roundness** (0 square, 1 fully circular), **Scale** (smaller is tighter around the centre), **Offset** (moves the centre in X and Y) and **Angle** (rotates the mask).
Outputs: **Image** and **Mask** (the vignette mask as greyscale, usable to apply the effect selectively through mix nodes).

## Manual alternative with an Ellipse Mask

The **Ellipse Mask** node creates a mask sized to the scene render dimensions. **Position** is a fraction of the frame (0.5, 0.5 is centred), **Size** is a fraction of the image width (equal width and height give a circle) and **Rotation** rotates it. The manual's tip: for a vignette pass the mask through a heavy Blur, then combine it with the image in a Mix Color node set to Multiply.

## Variants

- Off-centre vignette to guide the eye: use Offset (or the mask Position) toward the subject.
- Coloured vignette: mix a tint through the Mask output for stylised looks.
- Put it in a shared node group for the show with Factor and Feather exposed.

## Gotchas

- A vignette applied before a glare darkens the glow sources at the edges. Decide the order deliberately.
- Leave the vignette off EXR outputs intended for handoff to another compositing package, which will add its own.

## Verify

Sample the centre and the corners of a flat grey frame: the centre stays unchanged and the corners darken by the intended amount, with no visible edge to the vignette shape.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: the 5.2 Vignette node and its Factor, Feather, Corner Roundness, Scale, Offset, Angle inputs and Mask output; Ellipse Mask Position, Size, Rotation and the heavy-blur vignette tip. Removed the old hand-built graph values (Map Range 0.6 to 1.0, blur percentages) and the linear-multiply rationale, which no page states.
Method: documentation only; no commands were run.
