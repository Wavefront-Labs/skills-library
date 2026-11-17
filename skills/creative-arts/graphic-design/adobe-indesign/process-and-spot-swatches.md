---
id: creative-arts.graphic-design.adobe-indesign.process-and-spot-swatches
name: process-and-spot-swatches
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-swatches, process-vs-spot, mixed-ink, spot-colour, pantone-swatches, ink-manager, separations-preview, cmyk, swatch-naming]
level: practitioner
status: draft
description: "Define InDesign swatches as process or spot, name them, use mixed inks, and control plates with Ink Manager and Separations Preview to match the quote."
sources:
  - https://helpx.adobe.com/indesign/using/swatches.html
  - https://helpx.adobe.com/indesign/using/spot-process-colors.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Process and spot swatches

**Goal:** colours that separate onto exactly the plates the job is paying for.

## Process vs spot
- **Process (CMYK):** built from cyan, magenta, yellow, black dots. Use for full-colour jobs.
- **Spot:** a premixed ink (Pantone, a brand ink, metallic, fluorescent, white for clear
  substrates, varnish). Each spot = **one extra plate** and extra cost.
- A 4-colour job with one Pantone logo = 5 plates. If the budget is 4, convert the spot to
  process (with Pantone's CMYK bridge values) and accept the shift.

## Create swatches (Window > Color > Swatches)
- New Color Swatch: Color Type **Process** or **Spot**, Color Mode CMYK or a Pantone library
  (e.g. PANTONE+ Solid Coated / Uncoated - choose the one matching the paper).
- Untick "Name with Color Value" and name by role for process brand colours
  (`Brand Blue`), but **never rename Pantone swatches** - the printer's RIP matches by name.
- Same spot from Illustrator and InDesign must have identical names (`PANTONE 286 C`, not
  `PANTONE 286 CV`), or you get two plates.

## Mixed inks
Swatches panel menu > New Mixed Ink Swatch: combine a spot with process inks (e.g. spot +
black tints) for two-colour jobs with more tonal range. Mixed Ink Groups generate a grid of
combinations.

## Control plates
- **Window > Output > Separations Preview** (View: Separations): toggle each plate; see the
  real plate count.
- **Ink Manager** (Swatches panel menu or Export > Output): **Ink Alias** a duplicate spot to
  the correct one; tick **All Spots to Process** to convert at output without touching swatches.
- Delete unused swatches (panel menu > Select All Unused).

## Gotchas
- Placed Illustrator/PSD files bring their own spot colours in; check Separations Preview after placing.
- Pantone Coated vs Uncoated are the same ink with different screen simulation - use the one
  for the paper so proofs look right.
- RGB swatches in a print doc convert at export, unpredictably for saturated colours.

## Verify
- [ ] Separations Preview shows only the plates the quote includes.
- [ ] Spot names identical across all placed files; no RGB swatches in use.
