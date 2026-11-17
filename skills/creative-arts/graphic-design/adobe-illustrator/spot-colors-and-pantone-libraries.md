---
id: creative-arts.graphic-design.adobe-illustrator.spot-colors-and-pantone-libraries
name: spot-colors-and-pantone-libraries
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-color, illustrator-swatches, spot-colors, pantone, pantone-connect, swatch-libraries, separations-preview, spot-tints, white-ink, varnish-plate]
level: practitioner
status: draft
description: "Specify spot colours in Illustrator: Pantone libraries and Connect, coated vs uncoated, spot tints, white/varnish/foil plates, naming and separations checks."
sources:
  - https://helpx.adobe.com/illustrator/using/spot-process-colors.html
  - https://www.pantone.com/pantone-connect
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spot colours and Pantone libraries

**Goal:** logo and packaging artwork that separates onto the correct spot plates with names the printer's RIP recognises.

## Getting Pantone colours
- Swatches panel > Swatch Libraries menu > Color Books > PANTONE+ Solid Coated / Uncoated. In
  current Creative Cloud versions many Pantone books require **Pantone Connect** (a paid extension/
  subscription); older files keep their existing swatch definitions.
- Pick colours from a **physical Pantone guide** under standard light, never from the screen.
- Coated (C) vs Uncoated (U) are the same ink; the swatch's screen/CMYK simulation differs. Use the book
  matching the paper so proofs look right, but keep the ink name consistent with the printer's expectations.

## Spot swatch settings
- Color Type **Spot**; spot swatches are always global. Tints (Color panel slider) print as screens of that one ink.
- Name exactly as the printer and all other files use it (`PANTONE 485 C`). Mismatched names
  (`PANTONE 485 CVC`) create extra plates.
- **Special plates** are also spot swatches: `White` (white ink on clear or kraft), `Varnish`/`Spot UV`,
  `Foil`, `Emboss`, `Dieline`/`CutContour`. Give them a visible but distinct colour, set the objects
  to **Overprint Fill** (Attributes panel) so they do not knock out the artwork beneath. Agree names with the printer.

## Mixing spot with process
- Brand jobs printing CMYK only: convert spots to process with the **Pantone Color Bridge** values
  (CMYK equivalents for the paper), not Illustrator's automatic conversion. Some brands specify their own CMYK.
- Gradients between a spot and white = tint ramp of the spot. Gradients between two spots are allowed
  but check separations.

## Check separations
Window > **Separations Preview** > Overprint Preview: toggle plates. Count plates against the quote.
File > Document Color Mode should be CMYK for print; spot swatches separate independent of the mode.

## Gotchas
- Placed images (PSD duotones, EPS logos) bring their own spot names into the file.
- Transparency effects on spot colours (opacity, blend modes) can flatten into process builds - test with a PDF/X preflight.
- Pantone libraries update; ink formulations for the same number can shift between Pantone versions -
  quote the edition in brand guidelines.

## Verify
- [ ] Separations Preview plate count matches the job spec; no duplicate spot names.
- [ ] Special plates set to overprint and named as the printer requires.
- [ ] Colours approved from a physical guide, not a screen.
