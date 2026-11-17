---
id: creative-arts.animation.blender.vse-scopes
name: vse-scopes
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-scopes, histogram, waveform, vectorscope]
level: practitioner
status: docs-checked
description: "Check exposure and colour in the VSE with scopes: luma waveform, chroma vectorscope and histogram views in the preview, plus legal range and skin-tone line checks."
sources:
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/preview/display/display_mode.html
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/preview/header.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-scopes

Goal: grade and match shots in the edit using objective measurements.

## Scopes in the sequencer preview

Preview header > **Display Mode**: Image Preview, **Luma Waveform**, **RGB Parade**, **Chroma Vectorscope**, **Histogram**. Split the editor into several Preview areas to see the picture and a scope at the same time.

## Reading them

- **Luma Waveform**: horizontal position matches a pixel column of the frame, vertical position is brightness from 0 at the bottom to 1 at the top. A waveform pixel is brighter where more pixels in that column have that brightness. It shows at a glance whether there is enough contrast and whether areas are under- or overexposed.
- **RGB Parade**: three waveforms for the red, green and blue channels instead of one for overall brightness.
- **Chroma Vectorscope**: angle is hue, distance from the centre is saturation, brightness is the number of pixels with that hue and saturation.
- **Histogram**: three overlapping graphs, one per colour channel. X is intensity from 0 (black) to 1, Y is the number of pixels. Use it to balance the tonal range.

## Matching shots

1. Put the two shots side by side (or toggle between them) with a waveform open.
2. Match black and white levels first (Color Balance modifier Lift and Gain, or Curves).
3. Then match the vectorscope cluster positions (hue and saturation).

## Gotchas

- Delivery-specific legal levels depend on the broadcaster or platform specification. Confirm the limits there before clamping.

## Verify

Check a neutral grey card in the footage: its trace sits at the centre of the vectorscope after balancing.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Display Mode entries (Image Preview, Luma Waveform, RGB Parade, Chroma Vectorscope, Histogram), how the waveform, vectorscope and histogram are drawn, Color Balance Lift/Gamma/Gain. Corrected the histogram description (per-channel, not luma) and added RGB Parade; removed the skin-tone line, proxy-resolution and view-transform claims, which the manual does not state.
- Method: documentation only; no commands were run.
