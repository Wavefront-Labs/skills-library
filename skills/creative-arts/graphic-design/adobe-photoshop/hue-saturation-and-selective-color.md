---
id: creative-arts.graphic-design.adobe-photoshop.hue-saturation-and-selective-color
name: hue-saturation-and-selective-color
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, adjustment-layers, tonal-correction, hue-saturation, selective-color, vibrance, colorize, recolour-product, colour-range-sliders]
level: practitioner
status: draft
description: "Target and change specific colours with Hue/Saturation ranges, Colorize, Selective Color and Vibrance, for recolouring products and taming saturation."
sources:
  - https://helpx.adobe.com/photoshop/using/adjusting-hue-saturation.html
  - https://helpx.adobe.com/photoshop/using/applying-color-adjustments.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hue/Saturation and Selective Color

**Goal:** change one colour family without disturbing the rest of the image.

## Hue/Saturation (adjustment layer)
- **Master** affects all colours. The drop-down picks a range: Reds, Yellows, Greens, Cyans,
  Blues, Magentas.
- Click the **targeted adjustment tool** (hand) and click on the colour in the image to select its range;
  drag left/right to change saturation (Ctrl/Cmd+drag changes hue).
- Refine the range with the sliders on the colour bars at the bottom: inner bars = full effect,
  outer bars = falloff. Narrow them to avoid touching neighbouring colours (skin when editing orange).
- **Colorize** tints the whole image (or masked area) one hue - quick monochrome/sepia or a
  base for recolouring a white product.

## Recolour a product
1. Select the product (or use Color Range for the colour) and use as the adjustment layer's mask.
2. Shift Hue for similar-lightness targets. If target lightness differs a lot (red to light grey),
   Hue/Saturation struggles: use a **Solid Color fill layer in Color blend mode** plus Curves
   to match lightness, or Replace Color.
3. Check brand colour by sampling a mid-tone area against the target value.

## Selective Color (adjustment layer)
Print-trade style: for each colour range (Reds... plus Whites, Neutrals, Blacks) add/subtract
Cyan, Magenta, Yellow, Black percentages. **Relative** method scales existing amounts; **Absolute**
adds fixed amounts.
- Clean skies: Blues/Cyans, add Cyan, reduce Yellow.
- Warm or cool neutrals: Neutrals range, small Cyan/Yellow moves.
- Deepen blacks: Blacks range, add Black.
Works in RGB documents too (it simulates CMYK adjustments).

## Vibrance
Vibrance boosts low-saturation colours more than already-saturated ones and protects skin tones -
safer than Saturation for overall punch. Use small amounts (+10 to +30).

## Gotchas
- Large hue shifts reveal edge fringes and wrong-coloured reflections; mask and paint them.
- Oversaturated colours fall outside CMYK gamut - check gamut warning before print (see soft proofing).

## Verify
- [ ] Only the target colour changed (toggle the layer and compare neutral and skin areas).
- [ ] Sampled colour of the recoloured product matches the brand/target values.
