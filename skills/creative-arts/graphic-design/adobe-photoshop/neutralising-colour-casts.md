---
id: creative-arts.graphic-design.adobe-photoshop.neutralising-colour-casts
name: neutralising-colour-casts
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, adjustment-layers, tonal-correction, color-cast-correction, gray-point, color-balance, white-balance, info-panel, colour-samplers, average-blur-trick]
level: practitioner
status: draft
description: "Remove colour casts in Photoshop by numbers: find neutrals, set the grey point in Curves, use Info panel samplers, Color Balance by tonal range, and the average-blur invert trick."
sources:
  - https://helpx.adobe.com/photoshop/using/curves-adjustment.html
  - https://helpx.adobe.com/photoshop/using/applying-color-adjustments.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Neutralising colour casts

**Goal:** neutrals that are truly neutral, so products and skin look right and matched images sit together.

## Find something that should be neutral
White shirts, grey concrete, paper, road surfaces, shadows on white walls, a grey card if the
photographer shot one. Place **colour samplers** there (Shift+click with Eyedropper) and watch
the **Info panel** (F8): a neutral has R = G = B.

## Method 1: Curves grey point
1. Curves adjustment layer. Select the **grey eyedropper** (middle).
2. Click a mid-tone neutral. Photoshop shifts the channels so that point becomes R=G=B.
3. If the result is wrong, the point was not neutral - Ctrl/Cmd+Z and try another.
4. Also set black and white eyedroppers on true black/white detail if needed (double-click them
   to set target values, e.g. black 10/10/10, white 245/245/245, to avoid clipping).

## Method 2: per-channel Curves by numbers
In Curves, choose the Red, Green or Blue channel and nudge until the samplers read equal in
highlights, midtones and shadows separately. Casts often differ by tone (warm highlights, blue
shadows) - single-click fixes cannot handle that; per-channel curves can.

## Method 3: Color Balance
Adjustment layer; choose Shadows / Midtones / Highlights; move Cyan-Red, Magenta-Green,
Yellow-Blue sliders. Preserve Luminosity on. Good for gentle global shifts and creative grading.

## Average-blur trick (quick global cast)
Duplicate the layer, Filter > Blur > **Average** (one flat colour = the cast). Invert it
(Ctrl/Cmd+I), set blend mode to **Color**, opacity 20-50%. Cancels the overall cast. Crude but fast.

## Camera Raw
For raw files or JPEGs, Camera Raw's White Balance eyedropper on a neutral is usually best (see Camera Raw filter skill).

## Gotchas
- Not everything should be neutral: sunset light, candlelight and brand-lit scenes are meant to be warm.
  Remove the cast from the subject, keep the mood.
- Monitor not calibrated = you will "fix" casts that are not there. Trust the numbers.

## Verify
- [ ] Info panel shows R, G, B within ~3 points of each other on known neutrals in shadows, mids and highlights.
- [ ] Skin and product colours look natural; images in a set match.
