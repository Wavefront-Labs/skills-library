---
id: creative-arts.fashion-design.collection-design.pantone-and-colour-standards
name: pantone-and-colour-standards
category: creative-arts
field: fashion-design
product: collection-design
tags: [fashion-design, collection-design, colour-story, pantone-fashion-system, colour-standards, pantone-tcx, pantone-tpg, colour-approval, d65, light-booth]
level: practitioner
status: draft
description: "Reference and communicate colour with Pantone FHI (TCX cotton, TPG paper) and physical standards, approve under D65 in a light booth, and avoid screen-colour errors."
sources:
  - https://www.xrite.com/categories/light-booths
  - https://www.aatcc.org/test-methods/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pantone references and colour standards

**Goal:** make sure the colour you chose is the colour the mill dyes, with one physical
reference everyone approves against.

## Pantone Fashion, Home + Interiors (FHI) system
- Codes like **19-4052 TCX**: first two digits = lightness (11 light ... 19 dark),
  next two = hue, last two = chroma.
- **TCX** = dyed cotton swatch (use for textiles), **TPG** = printed paper (use for
  print/digital artwork), **TN** = nylon. Same code, slightly different appearance by medium.
- Buy current guides; old swatch cards fade. Pantone suggests replacing frequently-used
  guides roughly every 12-18 months.

## Physical standards
- Send mills a physical standard (TCX swatch, a fabric cutting, or a yarn), not a screen
  value. Keep an identical retained standard in-house.
- Label: colour name, code, season, date, approval light source.

## Approving colour
- View in a **light booth** under **D65** (artificial daylight) as the primary illuminant,
  and check secondaries (TL84/F11 store lighting, Illuminant A/incandescent) for
  **metamerism** (two colours matching in one light, not another).
- Instrumental check with a spectrophotometer: delta E (CMC 2:1) tolerance often around
  1.0 for approval; set the value with the mill.

## Screen colour
Monitors show sRGB approximations; label all on-screen chips "for reference only". For
digital print, convert the standard to Lab and work through the printer's ICC profile.

## Gotchas
- Approving under office fluorescent light = surprises in daylight.
- Different fibres take dye differently; standards per fabric may be necessary.

## Verify
- [ ] Every palette colour has a code and physical standard.
- [ ] Approvals logged with illuminant and delta E.
- [ ] Metamerism checked under at least two light sources.
