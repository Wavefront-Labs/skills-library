---
id: creative-arts.graphic-design.adobe-photoshop.frequency-separation
name: frequency-separation
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photo-retouching, image-repair, frequency-separation, skin-retouching, apply-image, high-frequency, low-frequency, linear-light, beauty-retouching]
level: advanced
status: draft
description: "Retouch skin with frequency separation: split texture and tone with Apply Image (8-bit and 16-bit settings), then fix tone and blemishes without plastic skin."
sources:
  - https://helpx.adobe.com/photoshop/using/apply-image-calculations.html
  - https://helpx.adobe.com/photoshop/using/retouching-repairing-images.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Frequency separation

**Goal:** even out skin tone and remove blemishes while keeping real pore texture.

## Build it
1. Do spot healing of obvious blemishes first on a separate layer (see spot healing skill), then
   make a merged copy (Ctrl/Cmd+Alt/Option+Shift+E) or work on duplicates of the base.
2. Duplicate twice: name them **Low** (bottom) and **High** (top).
3. **Low:** Filter > Blur > Gaussian Blur until pores just disappear but shape remains
   (typically 4-10 px for a head-and-shoulders portrait at 24 MP).
4. **High:** select it, Image > **Apply Image**:
   - Layer: Low, Blending: **Subtract**, Scale **2**, Offset **128** (8-bit document).
   - 16-bit document: Layer: Low, **Invert** ticked, Blending: **Add**, Scale **2**, Offset **0**.
5. Set High's blend mode to **Linear Light**. The image should look identical to the original
   (toggle to check). Group both (`FS`).

## Retouch
- **Low layer (colour and tone):** use a lasso selection with 15-30 px feather + Gaussian Blur on
  blotchy areas, or a soft brush at 10-20% opacity sampling nearby tones, or Mixer Brush. Even out
  redness and shadows under eyes - lightly.
- **High layer (texture):** Clone Stamp at 100% hardness, **Sample: Current Layer**, to replace
  blemishes, stray hairs and wrinkles with clean pore texture from nearby. Do not blur this layer.

## Keep it believable
- Lower the group's effect where needed (mask, or reduce work); skin needs some variation.
- Avoid heavy blur on Low across edges (jawline, nose) - it causes halos; select within areas.
- Combine with dodge and burn (see that skill) for shape; frequency separation is not for sculpting.
- Many retouchers now prefer dodge and burn plus healing for high-end work; FS is a tool for problem
  skin, not the default for every portrait.

## Gotchas
- Wrong Apply Image settings (8-bit settings in 16-bit file) give a slightly off result - check
  that toggling the group shows no change before you start.
- Over-blurring Low = plastic skin. Pore texture must look continuous at 100%.

## Verify
- [ ] Before retouching, the FS group is pixel-identical to the original (Difference check = black).
- [ ] At 100%: pores intact, tone even but varied, no halos on edges.
