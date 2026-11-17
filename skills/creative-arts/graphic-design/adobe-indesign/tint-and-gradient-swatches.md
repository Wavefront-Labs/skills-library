---
id: creative-arts.graphic-design.adobe-indesign.tint-and-gradient-swatches
name: tint-and-gradient-swatches
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, tint-swatches, gradient-swatches, indesign-swatches, spot-tints, gradient-feather, swatch-options, print-colour]
level: practitioner
status: draft
description: "Make InDesign tint and gradient swatches from base colours: tints that follow the parent swatch, gradient stops and types, spot gradients, and gradient feather."
sources:
  - https://helpx.adobe.com/indesign/using/tints.html
  - https://helpx.adobe.com/indesign/using/gradients.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tint and gradient swatches

**Goal:** lighter shades and gradients built from the document's brand swatches, so changing a base
colour updates everything derived from it.

## Tints
- Select a swatch, set **Tint** in the Swatches panel (e.g. 40%), then the New Swatch button: a tint swatch
  named `Brand Blue 40%` appears under its parent.
- Tints of a **spot** colour print as a screen of that one ink; tints of a process colour scale each
  CMYK value.
- Editing the parent swatch updates all its tints. Do not create a separate CMYK swatch for each shade.
- Tints below ~5% may not hold on press (highlight dot loss); above ~90% may fill in. Check with the
  printer for uncoated stock.

## Gradients
- Swatches panel menu > **New Gradient Swatch**: Type **Linear** or **Radial**, stops picked from
  existing swatches (Stop Color: Swatches), midpoint location.
- Apply with the Gradient panel or Gradient tool (G) to set angle and length per object; the swatch stores
  colours, not angle.
- Fade to transparent: use **Gradient Feather** effect (Object > Effects) rather than a gradient to Paper,
  which is white, not transparent.

## Spot colours in gradients
- Spot-to-spot or spot-to-Paper gradients separate cleanly on their plates; spot-to-process gradients
  produce mixed separations - fine for PDF/X-4 workflows, but check Separations Preview.
- Gradients between two spots whose angles share a screen can create moire; ask the printer.

## Gotchas
- Banding in long gradients: avoid very long gradients with small value changes; add noise in Photoshop for
  smooth photographic gradients if needed.
- Deleting a parent swatch asks for a replacement; tints follow the replacement.
- Unnamed colours (mixed directly in the Color panel) bypass all of this: Swatches panel menu > Add
  Unnamed Colors, then clean up.

## Verify
- [ ] Separations Preview shows tints on the intended plates only.
- [ ] Changing the base swatch updates every tint and gradient.
