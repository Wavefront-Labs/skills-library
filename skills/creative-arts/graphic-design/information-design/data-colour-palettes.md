---
id: creative-arts.graphic-design.information-design.data-colour-palettes
name: data-colour-palettes
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, chart-design, data-visualisation, sequential-palette, diverging-palette, categorical-palette, colorbrewer, viridis, perceptually-uniform, highlight-colour, cvd-safe]
level: practitioner
status: draft
description: "Choose colour palettes for data: sequential, diverging and categorical schemes, perceptually uniform ramps, highlight-and-grey strategy, CVD-safe choices and print/screen checks."
sources:
  - https://colorbrewer2.org/
  - https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data colour palettes

**Goal:** colour that encodes the data's structure correctly and stays readable for everyone.

## Match palette type to data
| Data | Palette | Example |
|---|---|---|
| Ordered values, low to high (rates, density) | **Sequential**: one hue (or two) light to dark | ColorBrewer Blues, viridis |
| Values above/below a meaningful midpoint (change vs last year, deviation from average, 0) | **Diverging**: two hues meeting at a neutral light middle | ColorBrewer RdBu, PuOr |
| Unordered categories | **Categorical (qualitative)**: distinct hues of similar lightness | ColorBrewer Set2, Okabe-Ito, Tableau 10 |
| One series to emphasise | **Highlight**: one strong colour, everything else grey | |

## Rules
- **Lightness must carry order** in sequential and diverging palettes - check in greyscale. Rainbow/jet palettes have
  uneven lightness and false boundaries; use perceptually uniform ramps (viridis, cividis, ColorBrewer).
- Diverging: put the midpoint (neutral colour) exactly on the meaningful value, not the data average by accident.
- Categorical: no more than ~6-8 colours; beyond that, group, label directly, or use small multiples.
- Number of classes on maps: 4-7; choose breaks (quantiles, natural breaks, round numbers) deliberately and state them.
- Keep the same colour meaning across a report (Europe is always the same blue).

## Colour vision deficiency (CVD) and accessibility
- ~8% of men have red-green CVD. Avoid red/green as the only distinction; use blue/orange, or vary lightness too.
- Test with simulators (Illustrator/Photoshop View > Proof Setup > Color Blindness; Coblis; Figma plugins).
- WCAG 1.4.1: do not use colour alone - add direct labels, patterns or shapes. Non-text contrast (see accessible
  graphics skill) for lines and bars against the background: 3:1.

## Print and screen
Saturated screen palettes dull in CMYK; check categorical colours remain distinct in print proofs. Very light
sequential steps can vanish on uncoated paper (minimum tint, see dot gain skill).

## Verify
- [ ] Palette type matches data type; greyscale check shows correct order.
- [ ] CVD simulation still distinguishes categories; colour not the only encoding.
