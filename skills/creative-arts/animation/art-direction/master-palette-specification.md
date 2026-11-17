---
id: creative-arts.animation.art-direction.master-palette-specification
name: master-palette-specification
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, art-bible, palette-spec, color-management, swatches]
level: advanced
status: draft
description: "Specify a show's master palette: named swatches with values and colour space, saturation and value limits, shadow rules, and how palettes are versioned and shipped."
sources:
  - https://animationguild.org/
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Color_management
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Master palette specification

Goal: one source of truth for every colour on the show, precise enough that two studios produce the
same frame.

## 1. Structure
- **Global palette**: 20-60 named swatches (`sky_day_01`, `skin_A_lit`) grouped by family.
- **Character colour models**: per character, lit and shadow values for each region.
- **Environment palettes** per location and lighting state.
- **Limits**: maximum saturation per value band, darkest allowed black (often not 0), brightest white,
  reserved hues (e.g. pure red only for danger).

## 2. Values and colour space
- Record every swatch in the working colour space the pipeline uses (sRGB display-referred for 2D,
  ACEScg or linear sRGB for CG) and say which. Hex for 2D, float RGB for CG.
- Ship a machine-readable file (ASE/ACO for paint apps, JSON/CSV for the pipeline) alongside the PDF.
- State the viewing condition (sRGB, D65 white, roughly 100-120 cd/m2) and require calibrated monitors.

## 3. Shadow and light rules
- Shadow derivation rule: e.g. multiply by a cool violet at 70% rather than just darkening the hue.
- Highlight rule, rim rule, and ambient tint per lighting state.

## 4. Versioning
- Palette files are versioned like code (`palette_v012`); changes logged with reason and approver.
- Retire swatches rather than editing them in place, so old shots stay reproducible.

## Failure modes
- Hex codes only, no colour space: CG and 2D drift apart.
- Palette edited silently: earlier episodes no longer match.

## Verify
- [ ] Machine-readable palette file plus PDF, same version number.
- [ ] Colour space and viewing condition stated.
- [ ] Saturation/value limits and reserved hues documented.

Related: `creative-arts.animation.art-direction.skin-tone-palettes`,
`creative-arts.animation.color.look-development-for-color-pipelines`,
`creative-arts.animation.art-direction.lighting-palette-variants`.
