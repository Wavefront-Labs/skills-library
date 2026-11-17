---
id: computing-software.computer-graphics-engineering.rendering-techniques.local-tone-mapping
name: local-tone-mapping
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, hdr-tonemapping, local-tone-mapping, exposure-fusion, bilateral-grid, local-exposure, detail-preservation]
level: advanced
status: docs-checked
description: "Apply local tone mapping with exposure fusion (Mertens, Wronski): synthetic exposures, Laplacian pyramid blending, why per-pixel, Gaussian and bilateral blends fail."
sources: ["https://bartwronski.com/2022/02/28/exposure-fusion-local-tonemapping-for-real-time-rendering/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local tone mapping

Source: Bart Wronski, "Exposure fusion: local tonemapping for real-time rendering" (2022), which
revisits the local tonemapping problem for games using Mertens, Kautz and Van Reeth's exposure
fusion.

## 1. The problem
A physically based pipeline gives an HDR scene; to display it you pick an exposure and tonemap.
With a high-dynamic-range scene (for example a day scene with harsh sunlight and shadowed
areas), one exposure cannot show all details: exposing for midtones is "reasonable", and reducing
contrast globally reveals details but looks washed out. The aim is to keep the punchy look and
still see the relevant details; in games, visuals often have to serve gameplay, so important
detail cannot be invisible. The author's earlier hacked solution for God of War helped in some
scenes but pushing it caused ugly halo artefacts.

Other fixes are artistic: lighting (fill lights, character lights), albedo changes. The post
advises doing as much as possible there rather than fighting the tonemapper.

## 2. Ways to blend exposures, and their failures
Starting from several exposures (the post uses three), decide per region which to use:
- **Per-pixel blending:** does not work well; even a dark region has some bright pixels, and
  bringing them down instead of up reduces contrast, giving washed-out, oversaturated "toxic
  HDR" results.
- **Gaussian blending:** blur the pixel luminance a lot before choosing the exposure. Bright
  regions leak onto medium and dark regions and vice versa; acceptable in a still image but
  visible and distracting with a moving game camera.
- **Bilateral blending:** edge-stopping prevents bleeding but brings gradient reversals and edge
  ringing; one proposed mitigation blends bilateral with Gaussian.
- **Guided filter blending:** transferring the exposure from a low-resolution blended image to
  full resolution was tried and is flawed.

## 3. Exposure fusion
Observation: at sharp edges the blend should occur over a small area to avoid halos, over flat
regions over a large area so it is imperceptible. Mertens et al. achieve this by building
Laplacian pyramids for each exposure and blending the Laplacians, with each level's blending radius
proportional to its Laplacian radius, constructed by a Gaussian pyramid of the weights.

Steps (from the post):
1. Create synthetic exposures by tonemapping with different exposure settings; three is a good
   start, allowing separate control of shadows and highlights.
2. Compute a lightness image for each (the demo uses gamma-mapped luminance, called a crude
   approximation).
3. Build a Laplacian pyramid of each lightness image up to some level; the last level is a
   Gaussian-blurred low-resolution version.
4. Assign each full-resolution lightness image a per-pixel weight. The paper uses contrast,
   saturation and exposure (closeness to grey); to avoid an over-saturated, over-contrasty look
   the author recommends using just exposure.
5. Build a Gaussian pyramid of the weights.
6. At a coarse level (for example the 5th or 6th mip), blend the coarsest Gaussian lightness mips
   with the Gaussian weights.
7. Go towards finer levels, blending the Laplacians at each level using that level's Gaussian
   weights and adding to the accumulated result.
8. Transfer the lightness to the full image, then do the rest of tonemapping and colour grading.

Optional local contrast boost: include Laplacian magnitudes in the blending weights (the
effective weight is the Gaussian weight times the absolute magnitude, chosen separately per
scale). It reduces the flat look any local tonemapper can produce; Lightroom's Clarity slider
has a similar effect.

## Gotchas
- Getting this to look good in many conditions needs tricks and tuning; the result is an artistic
  choice and can be pushed to an unnatural look.

## Verify
- [ ] High-contrast scene shows detail in both shadows and highlights without halos or washout.

## Checked

Method: docs-checked 2026-11-09 against the Wronski exposure fusion post (problem statement, blending alternatives, exposure fusion and algorithm details read; implementation tricks and extreme settings not read). Dropped the base/detail log-luminance recipe and its constants, the Unreal Engine local exposure claims, the bilateral grid paper (not read), the temporal stability and eye adaptation advice, and the colour-grading ordering claim.
