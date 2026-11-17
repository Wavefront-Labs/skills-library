---
id: creative-arts.animation.blender.vse-glow-blur-effects
name: vse-glow-blur-effects
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-effects, vse-glow, gaussian-blur-strip]
level: practitioner
status: docs-checked
description: "Use VSE Glow and Gaussian Blur effect strips: threshold, clamp, boost, blur distance and quality, size, animated blurs, and adjustment-layer use."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/effects/glow.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/effects/blur.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/adjustment.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# vse-glow-blur-effects

Goal: soft glows and blurs in an edit (dreamy looks, blurred backgrounds behind titles, transitions).

## Glow (Add > Effect Strip > Glow, with one strip selected)

Areas brighter than the threshold are blurred and superimposed on the base image.

- **Threshold**: areas brighter than this are blurred.
- **Clamp**: the maximum luminosity that is added.
- **Boost Factor**: multiplier of the brightness.
- **Blur Distance**: the size of the blur.
- **Quality**: smoother results but slower.
- **Only Boost**: show only the modified (glow) version without the base image.
- To animate the glow, mix it with the base image using the Gamma Cross effect.

## Gaussian Blur (Add > Effect Strip > Gaussian Blur)

- **Size X / Y**: the distance of the blur on each axis.
- Used to blur a background or to blur a transition strip.

## Recipes

- Blurred background behind a title: duplicate the clip on a higher channel, add Gaussian Blur on it, put the text above.
- Apply to many clips: place an **Adjustment Layer** strip above them. It takes all strips below it as its input, so an effect or modifier on it applies to all of them.

## Gotchas

- Single-input effects need exactly one strip selected when added. The available effect types depend on how many strips are selected (none: generators, one: single-input, two: dual-input).
- Large blurs are slow on high-resolution footage. Check with proxies and a test render.

## Verify

Render frames with the effect and check edges and clipping of the glow.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Glow options (Threshold, Clamp, Boost Factor, Blur Distance, Quality, Only Boost), Gaussian Blur Size X/Y, Gamma Cross suggestion for animating glow, effect availability by number of selected strips, Adjustment Layer takes all strips below as input. Removed the blur-size number, the Screen/50 percent recipe and the effect-length-follows-input claim, which no page states.
- Method: documentation only; no commands were run.
