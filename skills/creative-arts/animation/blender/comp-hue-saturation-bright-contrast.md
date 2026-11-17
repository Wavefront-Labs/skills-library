---
id: creative-arts.animation.blender.comp-hue-saturation-bright-contrast
name: comp-hue-saturation-bright-contrast
category: creative-arts
field: animation
product: blender
tags: [blender, color-grade, hue-saturation-node, bright-contrast, compositor]
level: practitioner
status: docs-checked
description: "Quick colour tweaks in the compositor: Hue/Saturation/Value ranges, Brightness/Contrast and clamping their output, Hue Correct for secondaries, and linear-render alternatives."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/color/adjust/hue_saturation.html
  - https://docs.blender.org/manual/en/latest/compositing/types/color/adjust/bright_contrast.html
  - https://docs.blender.org/manual/en/latest/compositing/types/color/adjust/hue_correct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# comp-hue-saturation-bright-contrast

Goal: quick saturation, hue shifts and contrast adjustments.

## Hue/Saturation/Value node (Color > Adjust)

- **Hue**: rotation offset from 0 (-180 degrees) to 1 (+180 degrees); 0 and 1 give the same result, so 0.5 is no change.
- **Saturation**: 0 removes colour, above 1 increases saturation.
- **Value**: 0 makes the colour black, 1 keeps it the same, higher is brighter.
- **Factor**: amount of influence; connect a matte for local changes.
- A greyscale image has no hue, so Hue and Saturation do nothing to it; add colour with a Mix node instead.

## Brightness/Contrast node (Color > Adjust)

- **Brightness**: an additive factor; negative darkens.
- **Contrast**: a scaling factor that makes brighter pixels brighter while keeping darker pixels dark; negative lowers contrast.
- The output can go beyond 0 to 1. Before mixing with images in the normal range, clamp with a Map Value node (Min and Max enabled) or a Color Ramp node.

## Alternatives for linear renders

- Contrast: an RGB Curves node or the Color Balance node (see comp-color-balance).
- Brightness in stops: the Exposure node (see comp-tonemap-exposure).

## Secondary corrections

- Desaturate only the background: an inverted matte into Factor of a Hue/Saturation/Value node.
- Shift the colour of one object: Hue on its matte.
- **Hue Correct** node: curves per hue range, for precise secondaries.

## Gotchas

- Order matters: saturation after a contrast increase looks different than before.
- Boosting saturation on very bright values can push colours out of gamut; check the result through the view transform.

## Verify

Mute the node to compare before and after. Check skin tones and neutral greys by sampling them in the viewer.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Hue range 0 to 1 mapped to -180 to +180 degrees, Saturation and Value behaviour, Factor, greyscale having no hue, Brightness/Contrast descriptions and the clamping advice. Removed the Convert Premultiplied option (not in 5.2), the fixed-pivot contrast claim, the AgX gamut claim and the vectorscope check.
Method: documentation only; no commands were run.
