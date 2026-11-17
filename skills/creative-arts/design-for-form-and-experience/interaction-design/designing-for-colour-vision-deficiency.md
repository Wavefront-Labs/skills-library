---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-for-colour-vision-deficiency
name: designing-for-colour-vision-deficiency
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [color-vision-deficiency, colour-blindness, color-blindness, deuteranopia, protanopia, accessibility, ui-color]
level: practitioner
status: draft
description: "Design for colour vision deficiency: avoid red-green-only encoding, add redundant cues, use blue-orange palettes, and test with simulators and greyscale."
sources:
  - "WCAG 2.2 SC 1.4.1 Use of Color and 1.4.11 Non-text Contrast (w3.org/TR/WCAG22)"
  - "Color Universal Design Organization (CUDO) - Color Universal Design guidelines and palette (jfly.uni-koeln.de/color)"
  - "Colorblind Awareness (colourblindawareness.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing for colour vision deficiency (CVD)

**Goal:** information is available to the roughly 1 in 12 men and 1 in 200 women with CVD.

## Facts
Most common: **deuteranomaly/deuteranopia** (reduced green), **protanomaly/protanopia** (reduced red) cause confusion of reds, greens, browns and oranges; **tritan** (blue-yellow) is rare. Lightness differences remain visible.

## Rules
1. **Redundant encoding:** add shape, icon, label, pattern, position or text with every colour meaning (line charts: direct labels and different dashes/markers; status: icon plus word).
2. **Avoid red-green-only pairs,** and red on black or green on red text. If you must use them, vary **lightness** strongly.
3. **Prefer colour-safe palettes:** blue and orange as main contrast pair; the Okabe-Ito palette (black, orange, sky blue, bluish green, yellow, blue, vermilion, reddish purple) for categorical charts.
4. **Differentiate by luminance** as well as hue; check ratio of at least 3:1 between adjacent encoded elements.
5. Links need non-colour cue (underline) in body text unless 3:1 contrast with surrounding text plus another indication.
6. Heatmaps: use viridis-like sequential palettes instead of rainbow or red-green diverging; use blue-orange diverging.
7. Form validation: icon plus message, not just a red border.

## Test
- Greyscale view; Figma plugins (Stark, Color Blind), Chrome DevTools Rendering - Emulate vision deficiencies, Color Oracle.
- Test with users with CVD when possible.

## Verify
- [ ] Every colour meaning has a second cue.
- [ ] Charts use a CVD-safe palette and direct labels.
- [ ] Passes simulator and greyscale checks.
