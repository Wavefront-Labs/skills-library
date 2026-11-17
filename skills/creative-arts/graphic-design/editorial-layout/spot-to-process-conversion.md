---
id: creative-arts.graphic-design.editorial-layout.spot-to-process-conversion
name: spot-to-process-conversion
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, print-colour, iso-12647, spot-to-process, pantone-color-bridge, pantone-cmyk, brand-colour-builds, ink-manager, gamut, colour-shift]
level: practitioner
status: draft
description: "Convert spot colours to CMYK for four-colour jobs: Pantone Color Bridge vs software conversion, brand builds, out-of-gamut shifts, converting at output."
sources:
  - https://helpx.adobe.com/indesign/using/spot-process-colors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spot to process conversion

**Goal:** brand spot colours reproduced as closely as CMYK allows, consistently across every file and printer.

## Decide the CMYK build once
1. **Brand guidelines first:** many brands specify their own CMYK build per Pantone (tuned on press). Use it.
2. Otherwise use **Pantone Color Bridge** (PANTONE+ CMYK equivalents for coated/uncoated) - the printed guide shows
   spot and CMYK side by side so you can judge the match.
3. Software conversion (Lab -> CMYK through the document's CMYK profile) is profile-dependent; acceptable when
   documented and consistent, but values differ by profile and app version.
Record the chosen build in the guidelines and swatch libraries.

## Gamut reality
Many Pantones fall outside CMYK: oranges (e.g. 021), vivid greens, bright blues (Reflex Blue, 072), purples, fluorescents
and all metallics. Expect visible shifts. Show the client a Color Bridge comparison before committing to a 4-colour-only job.
If the colour matters, budget a 5th plate.

## Doing the conversion
- **In the swatch:** change Color Type to Process and enter the build (InDesign/Illustrator) - affects all uses, simplest
  for permanent 4-colour jobs. Rename appropriately (`Brand Orange CMYK`) so nobody mistakes it for the spot.
- **At output only:** InDesign Ink Manager > **All Spots to Process** (or per ink) - keeps spots in the file for other
  versions, converts on export. Conversion then uses software values unless swatches are defined with builds.
- Placed files (AI, PDF, PSD) with spots: convert them too, or Ink Manager handles them at output; check in Separations Preview.

## Tints and gradients
Tints of a converted spot become tints of the CMYK build - fine. Gradients spot-to-white keep smooth if built from the swatch.

## Verify
- [ ] Separations Preview shows only CMYK plates.
- [ ] Builds match the brand guidelines or Color Bridge, documented and consistent across files.
- [ ] Client has seen a printed comparison for critical brand colours.
