---
id: creative-arts.graphic-design.brand-identity.brand-colour-palette-with-specs
name: brand-colour-palette-with-specs
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, identity-system, brand-colour-palette, brand-colors, pantone, cmyk, rgb, hex, ral, colour-proportions, accessible-colour, visual-identity]
level: practitioner
status: draft
description: "Define a brand colour palette: primary, secondary and neutrals, proportion of use, matched Pantone, CMYK, RGB, HEX and RAL specs, accessible text pairs and proofing."
sources:
  - https://www.w3.org/TR/WCAG22/#contrast-minimum
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brand colour palette with specs

**Goal:** brand colours that look the same (as close as each medium allows) in print, on screen, on
signage and on products, with rules for how much of each to use.

## Structure
- **Primary** (1-2): the recognisable brand colours.
- **Secondary / accent** (2-6): for charts, wayfinding, campaigns, product lines.
- **Neutrals** (2-4): text, backgrounds, UI greys; often a warm or cool tint.
- **Proportions:** show a bar or pie (e.g. 60% white, 25% neutral, 10% primary, 5% accent). Colour
  proportion is as recognisable as hue.

## Specs per colour
| Medium | Spec |
|---|---|
| Print spot | Pantone (PMS) Coated and Uncoated (they look different: choose both visually) |
| Print process | CMYK values for coated and uncoated, from the printer's profile or Pantone Color Bridge |
| Screen | RGB and HEX (sRGB) |
| Paint, signage | RAL, NCS or paint brand code; vinyl codes (3M, Oracal) for vehicles |
| Textile | Pantone TCX for fabrics if merchandise matters |
- Start from the spot colour (or a physical sample), then match each medium visually under ISO 3664 lighting;
  do not just convert numbers.

## Accessibility
- Test text and background pairs: list which combinations pass WCAG AA (4.5:1 normal text, 3:1 large text
  and graphics). Define darker text-safe variants of light brand colours.
- Check colour-blind simulations if colour carries meaning (charts, status).

## Delivery
- Swatch files: ASE (Adobe), CC Library, Figma variables or styles, CSS custom properties.
- Name consistently across files (`Brand Red`, `Brand Red 60%`).

## Gotchas
- Bright RGB greens, oranges and blues cannot be matched in CMYK; pick a spot or accept the shift.
- Uncoated stock dulls colours; the Uncoated Pantone reference shows what to expect.
- Screens vary; HEX values are the reference, not how one monitor shows them.

## Verify
- [ ] Every colour has spot, CMYK, RGB/HEX and paint specs, visually matched and proofed.
- [ ] Accessible text pairs listed; proportions documented.
