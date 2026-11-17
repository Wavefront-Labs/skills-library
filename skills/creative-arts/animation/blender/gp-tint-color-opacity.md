---
id: creative-arts.animation.blender.gp-tint-color-opacity
name: gp-tint-color-opacity
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-tint-modifier, gp-color-modifier, gp-opacity-modifier, gp-modifiers]
level: practitioner
status: docs-checked
description: "Recolour and fade Grease Pencil non-destructively: Tint (uniform or gradient from an object), Hue/Saturation colour modifier, Opacity modifier and their filters."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/color/tint.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/color/hue_saturation.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/color/opacity.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-tint-color-opacity

Goal: colour scripts, atmospheric fades and variations without repainting.

## Tint modifier

- **Mode**: Stroke & Fill, Stroke or Fill.
- **Strength**: 0 keeps the original colour, 1.0 fully replaces it with the tint; above 1.0 also makes point alpha less transparent (2.0 is fully opaque).
- **Tint Type** *Uniform*: a single *Color*. *Gradient*: a *Color Ramp* centred on an *Object* (usually an empty; its position and rotation define the centre) with *Radius* as the maximum distance of the effect.

## Hue/Saturation modifier

*Mode* (Stroke & Fill, Stroke, Fill), *Hue* (360 degrees map to 0..1; 0 and 1 give the same result), *Saturation* (0 gives grayscale, above 1 increases saturation) and *Value* (brightness).

## Opacity modifier

- **Mode**: Stroke & Fill, Stroke, Fill, or Hardness (opacity affects transparency from the stroke centre to its border).
- **Opacity Factor**: 1.0 keeps original alpha, below 1.0 more transparent, above 1.0 more opaque (2.0 is fully opaque).
- **Uniform Opacity**: one absolute *Strength* for all points.

## Filters

Layer, layer pass, material, material pass, vertex group and custom curve (availability varies by modifier). Pass indices let one modifier affect a set of materials or layers.

## Verify

Keyframe Strength or Opacity Factor from 0 to 1 and confirm the colour or fade animates in viewport and render.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Tint, Hue/Saturation and Opacity modifier pages and influence filters). Confirmed modes, Strength semantics, Tint Type, Gradient fields, Hue/Saturation/Value behaviour, Opacity Factor, Uniform Opacity and Hardness mode. Removed the unconfirmed "Factor" naming (the Tint field is Strength), the 4.x Hardness note, render-cost remarks, mixing-order claims and the compositing advice.
Method: documentation only; no commands were run.
