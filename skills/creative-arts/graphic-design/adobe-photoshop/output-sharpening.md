---
id: creative-arts.graphic-design.adobe-photoshop.output-sharpening
name: output-sharpening
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, smart-filters, smart-sharpen, high-pass-sharpening, unsharp-mask, output-sharpening]
level: practitioner
status: draft
description: "Sharpen for final output with Smart Sharpen or High Pass: amount and radius by output size, luminosity-only sharpening, halo control and print vs screen."
sources:
  - https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Output sharpening

**Goal:** crisp detail at the final size and medium, without halos or noise.

## When
Sharpen **last**, after resizing to final pixel dimensions, as a smart filter or on a merged
copy (Ctrl/Cmd+Alt+Shift+E). Different outputs (web, print) get different sharpening.

## Smart Sharpen (Filter > Sharpen > Smart Sharpen)
- **Remove: Lens Blur** (better edges than Gaussian).
- Screen: Amount 80-150%, Radius 0.3-0.6 px.
- Print (300 ppi): Radius 0.8-1.5 px, Amount 100-200% - print softens, so it looks too sharp on screen at 100%.
- Reduce Noise 10-20% to avoid sharpening grain; Shadows/Highlights fade to stop halos.

## High Pass
1. Duplicate layer (or merged copy), Filter > Other > **High Pass**, radius 1-3 px (just until edges appear).
2. Blend mode **Overlay** (strong) or **Soft Light** (gentle); lower opacity to taste.
3. Mask to apply only to eyes/product edges.

## Avoid colour artefacts
- Set the sharpening layer/filter blending to **Luminosity** mode (Edit > Fade or smart filter
  blending options) so colour fringes are not exaggerated.

## Gotchas
- Never sharpen then downsize; never sharpen JPEG artefacts.
- Halos: bright outlines along dark edges at 100% = radius/amount too high.
- Judge print sharpening at 50% zoom, screen at 100%.

## Verify
- [ ] No halos or noisy skies at 100%.
- [ ] Print proof looks crisp, not crunchy.
