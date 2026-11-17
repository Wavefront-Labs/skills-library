---
id: creative-arts.photography-fine-art.conceptual-photography.unifying-colour-and-grain-in-a-composite
name: unifying-colour-and-grain-in-a-composite
category: creative-arts
field: photography-fine-art
product: conceptual-photography
tags: [conceptual-photography, photo-compositing, composite-color-matching, color-grade, grain-matching, atmospheric-depth, lens-blur-match]
level: practitioner
status: draft
description: "Unify a finished composite: global colour grade, matching black levels, depth haze, matched noise/grain and lens effects so elements share one capture."
sources: ["https://helpx.adobe.com/photoshop/using/adjustment-fill-layers.html", "https://helpx.adobe.com/photoshop/using/filter-effects-reference.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unifying colour and grain in a composite

## Order of operations (top of the layer stack)
1. **Black and white points**: each element's darkest and lightest values must sit in the plate's
   range. Use a Threshold adjustment layer temporarily to find darkest points; match with Curves.
2. **Colour**: sample a neutral in each element; correct per element with Curves channels, then apply
   a **global grade** (Color Lookup, Curves, Gradient Map at low opacity) over everything.
3. **Atmosphere**: farther elements get lower contrast and a tint of the sky colour (a Solid Color
   layer masked with a depth gradient).
4. **Focus**: blur elements that sit outside the plate's depth of field (Lens Blur / Field Blur).
5. **Grain/noise**: elements from different ISOs have different noise; first Reduce Noise on the
   noisier, then add uniform grain over the whole image (Filter > Noise > Add Noise on a 50% grey
   overlay layer, or Camera Raw Filter Grain).
6. **Lens character**: global vignette, chromatic aberration consistent with plate.

## Gotchas
- Sharpening elements independently makes them pop out; sharpen once at output.
- Grain must be added after resizing for the final print, not before.

## Verify
- [ ] At print size, elements cannot be distinguished by contrast, colour, noise or sharpness.
