---
id: creative-arts.comics-and-sequential-art.comic-colouring.rgb-to-cmyk-conversion-for-comic-print
name: rgb-to-cmyk-conversion-for-comic-print
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, print-colour, cmyk-comics, cmyk-conversion, icc-profile, rendering-intent, out-of-gamut, line-art-k-only]
level: practitioner
status: draft
description: "Convert coloured comic pages from RGB to CMYK for print: printer ICC profile, rendering intent, keeping black line art 100K only, gamut checks and when to convert."
sources:
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
  - https://en.wikipedia.org/wiki/CMYK_color_model
  - https://helpx.adobe.com/photoshop/using/converting-between-color-modes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RGB to CMYK conversion for comic print

**Goal:** printed colours close to the screen, with crisp single-plate black line art.

## When to convert
- Many colourists work in RGB (wider gamut, smaller files, more filters) and convert
  at delivery; some publishers require CMYK working files. Follow the spec.
- Convert **once**, from the master RGB file, to a copy. Never round-trip
  CMYK -> RGB -> CMYK.

## Steps (Photoshop)
1. Get the **printer's ICC profile** or required standard (e.g. US: a SWOP/GRACoL
   profile; Europe: FOGRA-based such as Coated FOGRA39; uncoated stocks have their own).
2. Soft-proof first (View > Proof Setup > Custom, that profile) and adjust in RGB:
   saturated blues, greens and oranges often dull.
3. Gamut warning (View > Gamut Warning) shows out-of-gamut areas.
4. **Separate line art from colour** before converting: keep LINES as its own layer.
5. Edit > Convert to Profile: destination = the printer profile; intent **Relative
   Colorimetric** with black point compensation (or Perceptual for heavily saturated
   art; test both on a page).
6. **Line art**: after conversion, make the LINES layer pure **0/0/0/100 (K only)**,
   not a four-colour rich black. Methods: put lines in a separate black channel, or
   fill the line layer with K100 and set it to Multiply/overprint.
7. Check total ink limits (see the rich black skill).

## Why K-only lines
Four-colour lines show colour fringes when the press is slightly out of register.
100K lines register on one plate and stay sharp.

## Gotchas
- Converting with the default profile instead of the printer's.
- Rich black body text/lettering: also make lettering 100K.
- Flattening line art into colour before conversion turns lines into CMYK mixes.

## Verify
- [ ] Converted with the printer's profile; soft proof reviewed.
- [ ] Line art and lettering are 0/0/0/100.
- [ ] Out-of-gamut areas adjusted.
