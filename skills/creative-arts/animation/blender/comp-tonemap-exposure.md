---
id: creative-arts.animation.blender.comp-tonemap-exposure
name: comp-tonemap-exposure
category: creative-arts
field: animation
product: blender
tags: [blender, tonemap-node, tonemap, exposure-node, compositor, color-grade]
level: practitioner
status: docs-checked
description: "Control brightness and range in the compositor: Exposure node, the legacy Tone Map node (Rh Simple, R/D Photoreceptor) and why view transforms are recommended instead."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/color/adjust/exposure.html
  - https://docs.blender.org/manual/en/latest/compositing/types/color/adjust/tone_map.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# comp-tonemap-exposure

Goal: control image brightness and dynamic range in the compositor.

## Exposure node (Color > Adjust)

Adjusts the brightness of an image using a camera exposure parameter: inputs **Image** and **Exposure** (a scalar). The scene's Colour Management panel offers a separate exposure setting (see the manual's Color Management page). Use a matte to brighten only a region, for example a window.

## Tone Map node (Color > Adjust), legacy

Maps high dynamic range colours into the limited range supported by a display. The manual calls it a legacy node and recommends view transforms in the colour management settings instead, outputting linear HDR images from the compositor. **Type**:
- **Rh Simple** (simplified Reinhard using the image's average luminance): **Key** (value the average luminance maps to), **Balance** (normally 1), **Gamma** (1 if unused).
- **R/D Photoreceptor**: **Intensity** (below zero darkens), **Contrast** (0 uses an estimate from the input), **Light Adaptation** (0 global, 1 based on pixel intensity), **Chromatic Adaptation** (0 same for all channels, 1 each independent).

The output is a low dynamic range image.

## Recommended approach

Keep the compositor linear and let the Colour Management view transform do the display mapping. Using the Tone Map node on top of a view transform means tone mapping twice; if you use it, check the view transform setting so the two do not stack.

## Gotchas

- Tone Map output is low dynamic range, so put it at the end of the chain, not before further linear compositing.
- Exposure applied to individual passes before recombining changes their balance; apply it to the final image unless you intend the change.

## Verify

Compare the image with and without the node. For Tone Map, check that the brightest light source is no longer clipped and midtones are not grey.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Exposure node inputs and its Color Management counterpart; Tone Map is a legacy node, its Rh Simple and R/D Photoreceptor options and defaults, and LDR output. Removed the 2^Exposure formula, the claim about EXR output, the AgX flattening claim and the Standard view-transform instruction, which the page does not state.
Method: documentation only; no commands were run.
