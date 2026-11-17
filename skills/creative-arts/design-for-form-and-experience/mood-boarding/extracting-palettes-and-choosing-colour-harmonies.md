---
id: creative-arts.design-for-form-and-experience.mood-boarding.extracting-palettes-and-choosing-colour-harmonies
name: extracting-palettes-and-choosing-colour-harmonies
category: creative-arts
field: design-for-form-and-experience
product: mood-boarding
tags: [palette-extraction, color-palette, color-harmony, trend-research, colour-theory, complementary-colors, analogous-colors, color-scheme]
level: practitioner
status: draft
description: "Extract a palette from reference imagery, then shape it with harmony schemes (analogous, complementary, triadic) and proportions, checked for contrast and context."
sources:
  - "Johannes Itten, The Art of Color (1961)"
  - "Adobe Color - extract theme and colour harmony rules (color.adobe.com)"
  - "Josef Albers, Interaction of Color (Yale University Press, 1963)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Palette extraction and colour harmony

**Goal:** a palette drawn from real references and organised into a scheme that works in use.

## Extract
1. Choose 1-3 hero reference images from the mood board (`creative-arts.design-for-form-and-experience.mood-boarding.building-a-mood-board-and-style-tiles`).
2. Sample with a tool: Adobe Color "Extract Theme", Figma/Photoshop eyedropper on posterised or blurred copy (Filter > Pixelate > Mosaic, or Gaussian blur) to get average colours; Coolors image picker; code with k-means (`colorthief`, `node-vibrant`).
3. Pick 5-8 candidates covering light, dark, mid and one accent; discard muddy near-duplicates.
4. Record in HEX, RGB and Lab/OKLCH; note sample location and lighting (photos shift colour).

## Harmony schemes (colour wheel relationships)
- **Monochromatic:** one hue, varied lightness and saturation: calm, cohesive.
- **Analogous:** neighbours on the wheel (30-60 degrees): natural, harmonious; pick one dominant.
- **Complementary:** opposites (180 degrees): high contrast and energy; use one as dominant, the other as accent.
- **Split-complementary** (hue + two neighbours of its complement): contrast with less tension.
- **Triadic** (120 degrees apart) and **tetradic** (two complementary pairs): vibrant, needs strong dominance and muted tints.
- **Neutral-plus-accent:** most brand and interiors work: 60-30-10 proportions (dominant, secondary, accent).

## Shape and test
1. Assign roles: background, surface, text, primary, accent, feedback.
2. Tune by **value** (lightness) first: the palette must work in greyscale; then saturation.
3. Check contrast for text (4.5:1) and against colour-vision deficiency simulators (`creative-arts.design-for-form-and-experience.interaction-design.designing-for-colour-vision-deficiency`).
4. Test in context (mock screens, material swatches under intended lighting), since simultaneous contrast changes perception (Albers).
5. Save as swatch library / tokens (`creative-arts.design-for-form-and-experience.design-systems.building-tonal-colour-ramps-in-oklch`).

## Verify
- [ ] Palette traces to named references with roles and proportions.
- [ ] Works in greyscale and passes contrast.
- [ ] Verified in context, not on a swatch sheet alone.
