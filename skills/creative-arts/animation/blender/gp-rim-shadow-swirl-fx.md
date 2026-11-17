---
id: creative-arts.animation.blender.gp-rim-shadow-swirl-fx
name: gp-rim-shadow-swirl-fx
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-rim-fx, gp-shadow-fx, gp-swirl-fx, visual-effects]
level: practitioner
status: docs-checked
description: "Use Grease Pencil Rim, Shadow, Swirl, Wave Distortion, Colorize and Flip visual effects: rim light offsets, shadows with wave, swirl around an object."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/rim.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/shadow.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/swirl.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/colorize.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/wave_distortion.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/visual_effects/flip.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-rim-shadow-swirl-fx

Goal: cheap 2D lighting and distortion looks on Grease Pencil objects (Properties → Visual Effects).

## Rim

A masked colour silhouette of the object is displaced horizontally and/or vertically to simulate a rim light.
- **Rim Color**, **Mask Color** (a colour to keep unaltered), **Blend Mode** (Color Blend Modes), **Offset X, Y** (pixels).
- **Blur**: *Blur X, Y* (pixels) and *Samples* (0 disables the blur).

## Shadow

A colour silhouette is displaced behind the object.
- **Shadow Color**, **Offset X, Y** (pixels), **Scale X, Y**, **Rotation** (around the object centre, or around another object when *Object Pivot* / Use Object As Pivot is on).
- **Blur** (*Blur X, Z*, *Samples*).
- **Wave Effect**: *Orientation*, *Amplitude*, *Period*, *Phase* applied to the shadow.

## Swirl

*Object* (centre of the swirl), *Radius* (external radius) and *Angle* (0 shows no swirl).

## Wave Distortion, Colorize, Flip

- **Wave Distortion**: *Orientation*, *Amplitude*, *Period*, *Phase* applied to the object.
- **Colorize**: *Mode* Grayscale, Sepia, Duotone (Low Color, High Color), Transparent or Custom (Color), with *Factor* as the mix value.
- **Flip**: *Axis* Horizontal and/or Vertical.

## Gotchas

- Offsets, radius and blur sizes are in pixels, so check them at final resolution.
- Visual effects affect the whole object and cannot be filtered by layer, material or vertex group.

## Verify

Render at final resolution and compare rim and shadow offsets with the camera view.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Visual Effects: Rim, Shadow, Swirl, Wave Distortion, Colorize, Flip). Confirmed option names and semantics. Removed unconfirmed claims about resolution percentage scaling, example numeric offsets, effect-stack ordering, the specific rim blend mode list and the Rim "needs strokes visible against the mask" remark.
Method: documentation only; no commands were run.
