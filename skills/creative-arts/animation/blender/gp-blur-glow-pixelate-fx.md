---
id: creative-arts.animation.blender.gp-blur-glow-pixelate-fx
name: gp-blur-glow-pixelate-fx
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-blur-fx, gp-glow-fx, gp-pixelate-fx, visual-effects]
level: practitioner
status: docs-checked
description: "Apply Grease Pencil visual effects: Blur (incl. depth-of-field mode), Glow (threshold by colour/luminance, blend), and Pixelate, with render cost notes."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/blur.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/glow.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/pixelate.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-blur-glow-pixelate-fx

Goal: per-object 2D effects for Grease Pencil drawings (glows, soft backgrounds, pixel looks).

Properties → **Visual Effects** tab. The effects treat the object as an image, so they affect the whole object and cannot be limited by layer, material or vertex group; unlike modifiers they cannot be applied. The manual says they suit quick viewport visualisation and can be used for final renders, but the Compositor is recommended when you need more precision.

## Blur

Gaussian blur. **Samples** (0 disables the blur), **Size X, Y** (pixels), **Rotation**, **Use Depth of Field** (uses the focal plane distance of the actual camera; only available in camera view).

## Glow

Adds a glowing rim around the object.
- **Mode**: *Luminance* (glow illuminates the entire object) or *Color* (glow affects a single *Select Color*).
- **Threshold** (a value of 1 means no colours are affected), **Glow Color**, **Blend Mode** (Color Blend Modes), **Opacity**, **Size X, Y** (pixels), **Rotation**, **Samples**, **Glow Under** (glow only affects alpha areas).

## Pixelate

**Size X, Y** (size of the final pixels) and **Anti-aliasing**.

## Verify

Render a frame and compare it with the viewport in camera view.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Visual Effects introduction, Blur, Glow and Pixelate pages). Confirmed tab location, option names and semantics. Removed unconfirmed claims about render cost, the viewport toggle, Solid mode visibility, effect ordering versus compositing, and the stated blend mode list and Focus Object requirement.
Method: documentation only; no commands were run.
