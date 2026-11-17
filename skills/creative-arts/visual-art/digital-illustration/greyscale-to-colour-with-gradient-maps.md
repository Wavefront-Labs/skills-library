---
id: creative-arts.visual-art.digital-illustration.greyscale-to-colour-with-gradient-maps
name: greyscale-to-colour-with-gradient-maps
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, digital-painting, digital-painting-process, greyscale-to-colour, gradient-map, color-blend-mode, overlay-mode, value-painting, grisaille]
level: practitioner
status: draft
description: "Paint in greyscale for values, then colourise: gradient map adjustment layers, Color and Overlay blend modes, why naive colourising looks muddy, and when to paint over in colour."
sources: ["https://helpx.adobe.com/photoshop/using/applying-gradient-map.html", "https://docs.krita.org/en/reference_manual/filters/map.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Greyscale to colour with gradient maps

The digital version of grisaille: solve **values** in greyscale first, then add colour. Works when the values are correct; colour can't fix bad values.

## 1. Greyscale painting
- Use a limited value scale (e.g. 5-7 values); keep lights and shadows as clearly separated families.
- Flatten to a single layer (or keep the stack) and duplicate for safety.

## 2. Gradient map
- Add a **Gradient Map** adjustment layer (Photoshop: Layer > New Adjustment Layer; Krita: filter layer or Filter > Map > Gradient Map; Clip Studio: Layer > New Correction Layer > Gradient Map).
- The gradient maps dark values to one colour and light to another: e.g. dark blue-violet -> warm mid brown -> pale warm yellow. Hue should shift through the range (cool shadows, warm lights, or the reverse) and saturation usually peaks in the mid-tones.
- Try several presets; lower opacity or mask per area.

## 3. Colour blend modes
- **Color** mode layer: applies hue and saturation, keeps underlying luminance; good for local colour (skin, clothes) on top of the gradient map.
- **Overlay / Soft Light**: tints and increases contrast; can blow out darks and lights.
- **Multiply** for shadow colour; **Screen / Add (Linear Dodge)** for glow.

## 4. Paint over in colour
- Colourised greyscale looks **muddy or dead** because of uniform saturation and missing hue variation: real colour changes hue and chroma with light (warm light / cool shadow, saturated terminator, reflected colour).
- Merge a copy, then paint opaque colour on top - edges, highlights, reflected lights, saturated transitions near the terminator.
- Check values by toggling a black-and-white adjustment layer on top: colour shouldn't change the values you solved.

## Gotchas
- Color mode on near-black or near-white does almost nothing - darks stay grey.
- Yellow is inherently light: a yellow object painted in mid grey goes olive. Paint it lighter in greyscale.
- Over-reliance gives a "filter" look; finish by hand.

## Verify
- [ ] Values read correctly in greyscale first.
- [ ] Hue shifts across the value range.
- [ ] Final painted pass on top; luminance check with B/W layer.
