---
id: creative-arts.design-for-form-and-experience.design-systems.choosing-a-modular-scale-ratio
name: choosing-a-modular-scale-ratio
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [modular-scale-ratio, modular-scale, type-scale-ratio, type-scale, typographic-scale, type-system]
level: practitioner
status: draft
description: "Choose a modular type scale: pick a base size and ratio, generate steps, trim to the sizes you use, and test on real screens and breakpoints."
sources:
  - "Tim Brown, More Meaningful Typography, A List Apart (alistapart.com)"
  - "Robert Bringhurst, The Elements of Typographic Style"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Modular scale selection

A modular scale multiplies a base size by a constant ratio to produce harmonious sizes. Tim Brown popularised the idea for the web.

## Common ratios
Minor second 1.067, major second 1.125, minor third 1.2, major third 1.25, perfect fourth 1.333, augmented fourth 1.414, perfect fifth 1.5, golden ratio 1.618.

## Choose
1. **Base size:** body text, commonly 16 px (1 rem) on the web; check legibility for your font.
2. **Ratio by density:** data-heavy UIs need small ratios (about 1.125-1.2) so sizes stay close; marketing and editorial pages can use larger ratios (1.25-1.5) for dramatic headings.
3. **Generate steps:** size(n) = base x ratio^n. At base 16 and ratio 1.25: 12.8, 16, 20, 25, 31.25, 39.06.
4. **Trim:** keep only the sizes you use (for example five or six) and name them (step -1, 0, 1, 2, 3 or text-sm, text-base, text-lg).
5. **Round** to whole pixels or to your spacing grid.
6. **Pair with line height** per step (see `...design-systems.setting-a-baseline-grid-and-vertical-rhythm`).
7. **Test** on real devices and with longest headings; reduce the ratio on small screens (see `...design-systems.setting-fluid-typography-with-clamp`).

## Gotchas
- A ratio that suits desktop makes headings huge on mobile.
- Do not add sizes outside the scale.

## Verify
- [ ] The type styles in design match the scale values.
- [ ] Headings still fit on a narrow phone.
- [ ] The scale is stored as tokens (see `...design-systems.design-tokens-and-a-modular-type-scale`).
