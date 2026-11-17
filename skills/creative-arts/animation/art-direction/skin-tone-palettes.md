---
id: creative-arts.animation.art-direction.skin-tone-palettes
name: skin-tone-palettes
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, color-styling, skin-tone-palette, representation, color-models]
level: advanced
status: draft
description: "Build skin tone palettes that render a diverse cast well: undertone, value and saturation ranges, shadow and blush colours, lighting variants, and avoiding greyed or ashy shadows."
sources:
  - https://animationguild.org/
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Human_skin_color
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Skin tone palettes

Goal: every skin tone in the cast looks alive and specific in every lighting state.

## 1. Build each tone as a set, not a single swatch
For each character: base (lit), shadow, core-shadow accent, blush/warm zones (cheeks, nose, ears, knuckles),
highlight, lip, and inner-mouth colour.

## 2. Undertone and value
- Choose an undertone (warm/golden, neutral, cool/red-pink, olive) and keep it consistent across the set.
- Space the cast in value so characters read apart, but don't use skin value alone to separate them.
- Darker skin: keep saturation and warmth in the shadows (red-brown, deep warm violets); greyed shadows
  look ashy. Highlights can carry cool skylight reflection, which models the form well.
- Lighter skin: shadows shift warm-red (subsurface), not grey; avoid making the base too pink.

## 3. Shadow derivation
- Do not just multiply by grey. Shadow = shift hue slightly toward red/orange (warm subsurface) and
  lower value, keeping or raising saturation.
- In stylised cel shading, test the single shadow tone at small sizes; it must not read as dirt.

## 4. Lighting variants
- Check each tone in every state (night, tungsten, neon). Night/blue light kills warmth fastest; add back
  a little saturation in the shadow.

## 5. Review
- Review the whole cast lined up on neutral grey and on representative BGs; involve people who share the
  characters' backgrounds in review where possible.

## Verify
- [ ] Each character's skin set has shadow, blush, highlight, lip swatches.
- [ ] No grey or ashy shadows on darker tones.
- [ ] Cast line-up checked in every lighting state.

Related: `creative-arts.animation.art-direction.lighting-palette-variants`,
`creative-arts.animation.storywriting.cultural-research-authenticity`.
