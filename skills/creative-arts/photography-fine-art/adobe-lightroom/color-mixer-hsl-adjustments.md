---
id: creative-arts.photography-fine-art.adobe-lightroom.color-mixer-hsl-adjustments
name: color-mixer-hsl-adjustments
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, color-mixer, lightroom-color, hsl, targeted-adjustment-tool, lightroom-classic]
level: practitioner
status: draft
description: "Control individual hues in the Lightroom Classic Color Mixer (HSL): hue, saturation and luminance per colour band, the targeted tool and fine-art use cases."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (HSL / Color panel)", "https://helpx.adobe.com/lightroom-classic/help/apply-develop-settings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Color Mixer (HSL) adjustments

Eight bands: Red, Orange, Yellow, Green, Aqua, Blue, Purple, Magenta. Each has Hue, Saturation and Luminance. Switch between **HSL** (grouped by property) and **Color** (grouped by band) views; "All" shows everything.

## Use the Targeted Adjustment Tool
Click the target icon, choose H, S or L, then drag up/down **on the subject** in the photo. Lightroom moves every band that colour belongs to (a sky is usually Blue + Aqua), which is more accurate than guessing bands.

## Typical fine-art moves
- **Skies**: Blue Luminance -10 to -30 darkens without a polariser look; Aqua Hue toward blue cleans cyan skies.
- **Foliage**: Yellow Hue + toward green and Green Saturation down calms garish greens; Yellow/Green Luminance up adds glow.
- **Skin**: Orange is the skin band. Orange Luminance up brightens skin; Orange Saturation down 5-15 removes ruddiness; Red Hue + slightly toward orange evens blotches.
- **Colour harmony**: reduce saturation of distracting accent hues so the palette stays restrained.

## Gotchas
- Large Luminance changes on a band cause blotchy edges and noise (especially Blue in skies with JPEGs); keep under about +/-40 on raws.
- HSL affects the whole image; for one object use a mask's Color Range or AI mask instead.
- With a Monochrome profile, the panel becomes the B&W Mix.

## Verify
- [ ] At 100%, transitions in skies and skin show no banding or halo where a band boundary lies.
