---
id: creative-arts.animation.blender.comp-glare-types
name: comp-glare-types
category: creative-arts
field: animation
product: blender
tags: [blender, glare, glare-types, fog-glow, glare-streaks, glare-ghosts, bloom, compositor]
level: practitioner
status: docs-checked
description: "Add bloom and lens glare with the compositor Glare node: Bloom, Fog Glow, Streaks, Ghosts, Simple Star, Sun Beams and Kernel, Threshold, Strength, Quality, and outputs."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/glare.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# comp-glare-types

Goal: believable light bloom and lens artefacts from bright areas.

## Node (Filter > Glare)

**Glare Type**:
- **Bloom**: soft glow around bright areas from light scattering in eyes and lenses.
- **Fog Glow**: a more physically accurate version of Bloom, softer and more realistic at the cost of more computation.
- **Streaks**: bright streaks radiating from highlights. Settings: **Streaks** (count), **Streaks Angle** (angle of the first streak), **Fade**, **Iterations**, **Color Modulation**.
- **Ghosts**: overlapping lens-reflection artefacts, with **Iterations** (number of ghosts) and **Color Modulation**.
- **Simple Star**: simpler star-shaped streaks, with **Fade**, **Iterations** and **Diagonal** (rotates the streaks 45 degrees).
- **Sun Beams**: crepuscular rays, with **Size**, **Sun Position** and **Jitter**.
- **Kernel**: a custom convolution kernel, given as a Float kernel or a Color image (**Kernel Data Type**).

Common settings:
- **Quality**: High, Medium or Low processing resolution; lower is useful for previews.
- Highlights panel: **Threshold** (minimum luminance that contributes; higher restricts glare to the brightest regions), **Smoothness**, and an optional **Clamp** with a **Maximum**.
- Adjust panel: **Strength** (above 1 boosts the glare, below 1 blends it with the original), **Saturation**, **Tint**.
- **Size** (Bloom, Fog Glow, Sun Beams): relative spread, where 1 covers the full image.

Outputs: **Image**, **Glare** (glare only) and **Highlights** (the extracted bright areas).

## Taste rules

- Glow should come from things that are actually bright in the render (lights, sun specular), not from white walls. Use the Threshold rather than a large Strength.
- Keep the look consistent across a sequence.
- Use streaks and ghosts sparingly: anamorphic look, sci-fi, lens flares on specific shots.

## Gotchas

- Glare computed before denoising can amplify fireflies into blobs. Denoise first.
- Size is relative to the image, so it scales with resolution, but check the result at final resolution.

## Verify

Toggle the node and compare. Only light sources and strong highlights should glow, and the mid-tones should not get hazy.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Glare Types (Bloom, Ghosts, Streaks, Fog Glow, Simple Star, Sun Beams, Kernel), Quality levels, Highlights, Adjust and Glare-panel settings, and the three outputs. Removed the Mix slider (replaced by Strength in 5.2), the 4.2+ version note and the remark about EEVEE Bloom.
Method: documentation only; no commands were run.
