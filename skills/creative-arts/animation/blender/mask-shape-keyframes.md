---
id: creative-arts.animation.blender.mask-shape-keyframes
name: mask-shape-keyframes
category: creative-arts
field: animation
product: blender
tags: [blender, masking, roto, mask-keyframes, mask-shape-key, animation]
level: practitioner
status: docs-checked
description: "Animate Blender roto masks with shape keys: Insert and Clear Shape Key, Re-Key Points, Feather Reset Animation, Dope Sheet Mask mode, and a bisecting keying strategy."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mask-shape-keyframes

Goal: masks that follow motion smoothly with as few keys as possible.

## Keys (Mask > Animation)

- **Insert Shape Key** (I): inserts a shape key for the active mask layer at the current frame. It works on the level of mask layers, so it keyframes all the splines and points in that layer.
- **Clear Shape Key** (Alt I): clears the shape key for the active layer at the current frame.
- **Feather Reset Animation**: resets the feather offset across all animated frames.
- **Re-Key Points of Selected Shapes**: re-interpolates the selected points across the range of keys selected in the Dope Sheet.
- Timing of mask keys is edited in the Dope Sheet's **Mask** mode.

The manual positions shape keys as the tool for when there are not enough good features to track, or the mask is not based on footage. Otherwise parent points or layers to tracks (see `creative-arts.animation.blender.mask-parent-to-track`) and key only the shape changes.

## Strategy (roto practice, not from the manual)

1. Key the first and last frames.
2. Key the middle, then the middle of each half, and so on (bisecting), adding keys only where the shape drifts off.
3. Key at changes of direction first.
4. Avoid keying every frame by hand: frame-by-frame adjustments make edges jitter.

## Feather and motion blur

Feather is a property of the spline points. For motion-blurred edges, the compositor Mask node has Motion Blur settings (Samples and Shutter) that blur an animated mask using the surrounding frames.

## Gotchas

- Keys are per layer, not per point: moving one point and inserting a key keys every spline in the layer.

## Verify

Play the masked plate at full speed: edges follow the subject with no jitter and no slips between keys.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/masking/editing, compositing/types/input/mask) and the 5.2 source keymap (I and Alt I in the mask editor). Confirmed Insert and Clear Shape Key, Feather Reset Animation, Re-Key Points, Dope Sheet Mask mode and Mask node Motion Blur. Corrected the skill-id reference and removed unconfirmed claims about the timeline, feather being part of the key, and adding points after keying.
Method: documentation only; no commands were run.
