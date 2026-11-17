---
id: creative-arts.photography-fine-art.adobe-lightroom.frequency-separation-retouching
name: frequency-separation-retouching
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, frequency-separation, edit-in-photoshop, skin-retouching, apply-image, photoshop]
level: practitioner
status: draft
description: "Retouch skin and surfaces with frequency separation in Photoshop: 16-bit and 8-bit Apply Image settings, Gaussian Blur radius, repairs on each layer and pitfalls."
sources: ["https://helpx.adobe.com/photoshop/user-guide.html (Apply Image; Linear Light blending; Gaussian Blur)", "https://helpx.adobe.com/photoshop/using/blending-modes.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Frequency separation retouching

Splits the image into a **low-frequency** layer (colour and tone) and a **high-frequency** layer (texture), so you can smooth blotches without erasing pores, or fix texture without changing tone.

## Build (16-bit document)
1. Duplicate the background twice: `Low` (lower) and `High` (top).
2. Hide High. On Low: Filter > Blur > **Gaussian Blur** until texture disappears but shapes remain (3-8 px for a head-and-shoulders at 24 MP; larger for big files).
3. Select High. Image > **Apply Image** with Layer = Low and:
   - 16-bit: Invert **ticked**, Blending **Add**, Scale 2, Offset 0.
   - 8-bit: Invert unticked, Blending **Subtract**, Scale 2, Offset 128.
4. Set High to **Linear Light**. The image should look identical to the original; toggle to check.

## Repairs
- **Low layer**: Mixer brush or Lasso + Gaussian Blur on blotchy areas, or a low-opacity brush sampling nearby tone, to even colour transitions. Keep within facial planes.
- **High layer**: Clone Stamp (Sample: Current Layer, hardness 50-100%) or Healing Brush to remove blemishes and replace damaged texture.

## Pitfalls
- Over-smoothing Low creates a plastic look; keep changes at 30-60% via layer opacity.
- Healing across tonal boundaries on High creates smudges; use Clone.
- Choose radius by the size of the defects, not by preset.
- For simple spot work, Healing Brush on a blank layer is faster; reserve FS for tone unevenness.

## Verify
- [ ] Before/after at 100%: pores and fine hair intact, tone transitions even, no halos at edges of the face.
