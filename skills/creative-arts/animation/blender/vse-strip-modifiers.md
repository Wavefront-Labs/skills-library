---
id: creative-arts.animation.blender.vse-strip-modifiers
name: vse-strip-modifiers
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-color-modifiers, strip-modifiers, strip-color-balance, color-grade]
level: practitioner
status: docs-checked
description: "Grade in the VSE with strip modifiers: Color Balance, Curves, Hue Correct, Bright/Contrast, White Balance, Tone Map and Mask, modifier masks and adjustment-layer grading."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/modifiers/index.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/modifiers/color_balance.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/modifiers/mask.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/modifiers/compositor.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/adjustment.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# vse-strip-modifiers

Goal: colour-correct clips inside the edit without a separate compositing setup.

## Adding (Properties Editor > Strip Modifiers > Add)

Image modifiers in the 5.2 manual (Blender 4.5.14 has only Brightness/Contrast, Color Balance, Curves, Hue Correct, Mask, Tone Map, White Balance and Sound Equalizer through `strip.modifiers.new`, so the Compositor, Camera Lens Effects and Creative modifiers and the Echo and Pitch sound modifiers need 5.x): **Brightness/Contrast**, **Color Balance**, **Compositor**, **Curves**, **Hue Correct**, **Mask**, **Tone Map**, **White Balance**, plus the groups **Camera Lens Effects** (Chromatic Aberration, Film Grain, Sensor Noise, Vignette) and **Creative** (Sepia, Split Toning, Tune Image, Unsharp Mask). Sound modifiers: Echo, Pitch and Sound Equalizer.

- **Color Balance**: Lift/Gamma/Gain or Offset/Power/Slope (ASC-CDL), applied in the sequencer colour space; works like the Color Balance node.
- **Curves** works like the RGB Curves node, **Hue Correct** like the Hue Correct node, **Tone Map** like the Tone Map node.
- **White Balance**: choose the colour that should be white.
- **Mask modifier**: affects the strip's alpha using another strip's grayscale or a Mask data-block (Mask Time Relative or Absolute for masks).
- **Compositor modifier**: runs a compositor node group (sequencer node tree type). Compositor node groups marked as assets appear in the Add menu as modifiers.

Most image modifiers have a **Mask Input**: Type Strip (another strip's grayscale) or Mask (a Mask data-block), so a grade can be local.

## Stack controls

Each modifier header has Viewport and Render toggles and an Extras menu: Duplicate (Shift D), **Copy to Selected** (copies the modifier from the active strip to all selected strips), Move to First/Last, Show Node Group (Compositor). Modifiers evaluate top to bottom, so order matters; drag to reorder.

## Grade many clips at once

Put an **Adjustment Layer** strip above the clips and add modifiers to it: it takes all strips below as its input.

## Gotchas

- Modifier maths runs in the sequencer colour space (see sequencer-color-space).
- Many modifiers on high-resolution strips slow playback. Use proxies (see vse-proxy-setup).

## Verify

Use the waveform and vectorscope (see vse-scopes) with the modifier toggled: shots should match after the grade.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Modifier list and groups, panel location (Properties Editor > Strip Modifiers), Color Balance methods and colour space, node equivalents for Curves, Hue Correct and Tone Map, Mask modifier options, Compositor modifier and asset use, Mask Input options, header and Extras controls including Copy to Selected, top to bottom evaluation, Adjustment Layer input. Removed the Reinhard description, the typical-order advice and the 5.0 version gate, which the manual does not state.
- Run note, 2026-11-01, Blender 4.5.14 LTS headless: `StripModifier.type` items are BRIGHT_CONTRAST, COLOR_BALANCE, CURVES, HUE_CORRECT, MASK, TONEMAP, WHITE_BALANCE and SOUND_EQUALIZER; modifiers have `input_mask_type` (STRIP or ID), `input_mask_strip`, `input_mask_id`, `mask_time`; Color Balance has `correction_method`, lift, gamma, gain, slope, offset and power.
Method: documentation checked against the manual and API pages; part of the claims were run headless in Blender 4.5.14 (see the run note), but other claims describe Blender 5.x features that 4.5.14 does not have, so the status stays docs-checked.
