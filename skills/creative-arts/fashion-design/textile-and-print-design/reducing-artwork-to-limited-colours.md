---
id: creative-arts.fashion-design.textile-and-print-design.reducing-artwork-to-limited-colours
name: reducing-artwork-to-limited-colours
category: creative-arts
field: fashion-design
product: textile-and-print-design
tags: [fashion-design, textile-and-print-design, colour-separation, colour-reduction, indexed-colour, posterize, screen-print-colours, spot-colour]
level: practitioner
status: draft
description: "Reduce print artwork to a limited number of flat colours for screen printing: indexed colour, cleaning stray pixels, merging similar colours and assigning a screen per colour."
sources:
  - https://helpx.adobe.com/photoshop/using/converting-color-modes.html
  - https://www.bloomsbury.com/uk/printed-textile-design-9781350076358/
  - https://en.wikipedia.org/wiki/Screen_printing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reducing artwork to a limited colour count

**Goal:** artwork with a fixed number of flat colours (each one a screen), because screen
printing cost and set-up scale with the number of colours.

## Decide the count
- Rotary/flat-bed screen printing: each colour needs a screen; 4-8 colours is common in
  fashion; more raises cost and minimums.
- Overprinting (one transparent colour over another) creates an extra apparent colour
  without an extra screen.

## Photoshop workflow
1. Duplicate the artwork; work on a copy.
2. Simplify: Filter > Noise > Median (small radius) to remove speckles.
3. **Image > Mode > Indexed Color**: Palette "Local (Perceptual)" or "Custom", set number
   of colours, **Dither: None**, Forced: None. Preview and adjust.
4. Inspect the Color Table (Image > Mode > Color Table); merge near-identical colours,
   replace with the palette's Pantone-referenced values.
5. Clean stray pixels with the Pencil tool (aliasing off) at 100-200% zoom.
6. Convert back to RGB/CMYK if needed for separations; keep each colour selectable
   (Select > Color Range at 0 fuzziness).

## Textile CAD
Dedicated software (NedGraphics, AVA CAD/CAM, Lectra Kaledo, EAT DesignScope) does
colour reduction and separation with cleaning tools and colour libraries.

## Gotchas
- Anti-aliased edges create dozens of intermediate colours; remove them.
- Dithering looks fine on screen but can't be engraved as flat screens.
- Fine gradients need halftones; discuss with the printer.

## Verify
- [ ] Colour table shows exactly the planned number of colours.
- [ ] No stray pixels or anti-aliasing at 200% zoom.
- [ ] Each colour referenced to a palette standard.
