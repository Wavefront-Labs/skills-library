---
id: creative-arts.animation.blender.mask-in-compositor-vse
name: mask-in-compositor-vse
category: creative-arts
field: animation
product: blender
tags: [blender, masking, mask-in-compositor, mask-vse, mask-node, sequencer]
level: practitioner
status: docs-checked
description: "Use roto masks downstream: Mask node in the compositor, mask strips and modifier masks in the Video Sequence Editor, resolution matching and motion blur."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/input/mask.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/mask.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/modifiers/mask.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# mask-in-compositor-vse

Goal: apply roto to grades, effects and edits.

## Compositor

The **Mask** node selects a Mask data-block and outputs its black-and-white mask. It can feed other nodes, for example Invert, Multiply or Mix, or be used as a factor input.
- **Feather**: use or ignore the spline feather points.
- **Size Source**: Scene Size (the render resolution, scaling with it), Fixed (pixels) or Fixed/Scene (pixels that still scale with the resolution percentage).
- **Motion Blur** for animated masks: **Samples** (more is smoother but slower) and **Shutter** (duration in seconds).

## Video Sequence Editor

- **Mask strip**: generates a mask image from a Mask data-block made in the Movie Clip Editor, always at the render resolution (it scales with proxy levels). It works like the Mask node without the finer controls.
- **Mask modifier**: affects the alpha of the strip it is on, with Mask Input Type Strip (the grayscale of another strip) or Mask (a Mask data-block).
- Most strip modifiers (Color Balance, Curves, Hue Correct, Brightness/Contrast, White Balance, Tone Map, Compositor) have a **Mask Input** with the same Type choice, so a grade can apply only inside a shape.
- **Mask Time**: Relative offsets the mask animation to the start of the strip; Absolute keeps it in sync with the scene frame. Use this when strips are moved in time.

## Verify

Play the edit or render a few frames: the grade appears only inside the shape and follows the subject.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Mask node purpose and options (Feather, Size Source variants, Motion Blur Samples and Shutter), Mask strip behaviour at render resolution, Mask modifier input types, Mask Input on other modifiers, Mask Time Relative and Absolute. Removed the claims about normalised coordinates, VSE masks lacking motion blur and the Set Alpha, Keying and garbage-matte uses, which these pages do not state.
- Method: documentation only; no commands were run.
