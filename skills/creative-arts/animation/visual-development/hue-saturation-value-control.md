---
id: creative-arts.animation.visual-development.hue-saturation-value-control
name: hue-saturation-value-control
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, color-theory, hue-saturation-value, value-control, saturation, color-mixing]
level: intro
status: draft
description: "Control hue, saturation and value independently when painting: value carries form, saturation is spent sparingly, and hue shifts with light temperature."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/HSL_and_HSV
  - https://en.wikipedia.org/wiki/Munsell_color_system
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hue, saturation and value control

Goal: deliberate control of each colour dimension, so colour supports form and focus instead of
fighting them.

## Dimensions
- **Hue**: position on the colour wheel (red, yellow-green...).
- **Saturation/chroma**: intensity, from grey to pure.
- **Value/lightness**: light to dark. Carries the form and the composition; get it right first.

## Practical rules
- Value first: a painting that works in greyscale will work in colour; the reverse is rare.
- HSV "V" and HSL "L" are not perceptual lightness: pure yellow and pure blue at the same V differ
  massively in perceived value. Check with a desaturate/luminosity layer, not by slider numbers.
- Saturation is a budget: keep most of the image moderately saturated and spend high chroma
  at the focal point or on small accents.
- Saturation peaks in the midtones and at the terminator; very light and very dark values
  are naturally lower in chroma.
- Shift hue, not just value, when going into light and shadow (warm light / cool shadow or the reverse).

## Method
1. Paint or check the value structure in greyscale.
2. Choose a dominant hue family and saturation ceiling for the image.
3. Pick colours with an eyedropper-free mindset: decide H, S and V separately.
4. Toggle a luminosity check layer (black fill, Color blend mode) frequently.
5. Mark the single most saturated area; reduce competitors.

## Failure modes
- Colours chosen at full saturation everywhere - garish.
- Value relationships broken by colour choices (yellow and blue reading the same in the design but not in greyscale).
- Shadows made by adding black (dull) instead of shifting hue and value.

## Verify
- [ ] Greyscale check passes.
- [ ] Saturation highest at the focal point.
- [ ] Hue shifts between light and shadow.

Related: `creative-arts.animation.visual-development.value-thumbnails`,
`creative-arts.animation.visual-development.gamut-mapping`.
