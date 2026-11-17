---
id: creative-arts.animation.blender.vse-color-mix-blend
name: vse-color-mix-blend
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-color-mix, color-mix-strip, blend-modes]
level: practitioner
status: docs-checked
description: "Combine strips with blend modes in the VSE: per-strip Blend and Opacity, the Color Mix effect strip with its Blend modes and Opacity, and when to use each."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/effects/color_mix.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html#compositing
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# vse-color-mix-blend

Goal: overlays, light leaks, textures and stylised blends in an edit.

## Per-strip blending (simplest)

Sidebar > Strip > Compositing: **Blend** (how the strip blends with strips in lower channels; see the Blend Modes glossary entry in the manual for each mode) and **Opacity** (the strip's alpha; when animated it is drawn as an overlay on the strip, which the Animation Curves overlay can hide).

## Color Mix effect (Add > Effect Strip > Color Mix, with two strips selected)

- Mixes two input strips pixel by pixel. Options: **Blend** and **Opacity** (how much of the second image is composed onto the first).
- Blend choices in the manual: Add, Subtract, Multiply, Screen, Divide, Difference, Darken, Lighten, Overlay, Color Dodge, Color Burn, Hue, Saturation, Value, Color, Soft Light, Linear Light.
- It can do the same as the Add, Subtract and Multiply effect strips, plus the other modes.
- Use it when the blend must apply between two specific strips only, not everything below.

## Uses

- Light leak footage: Screen or Add at partial opacity over the clip.
- Film grain or paper texture: Overlay or Soft Light at low opacity.
- Titles with knockout effects: Subtract or Difference.

## Gotchas

- Blend results depend on the Sequencer colour space (Color Management > Sequencer; see sequencer-color-space): different spaces give different results for colour correction, crossfades and other operations.

## Verify

Toggle the blend strip's mute (H) and compare the frame: the effect should be visible and as strong as intended.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Color Mix options (Blend, Opacity), its mode list and two-input behaviour, menu name Add > Effect Strip, per-strip Blend and Opacity location, colour-space dependence of results. Removed the explicit per-strip mode list and the Factor option name, which the 5.2 manual does not give.
- Method: documentation only; no commands were run.
