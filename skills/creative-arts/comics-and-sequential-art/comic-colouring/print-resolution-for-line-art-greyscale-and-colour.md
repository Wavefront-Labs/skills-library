---
id: creative-arts.comics-and-sequential-art.comic-colouring.print-resolution-for-line-art-greyscale-and-colour
name: print-resolution-for-line-art-greyscale-and-colour
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, print-production, print-specs, print-resolution, ppi, line-art-1200, colour-300-ppi, effective-resolution]
level: practitioner
status: draft
description: "Set resolution correctly for printed comics: 300-400 ppi colour and greyscale, 600-1200 ppi bitmap line art, effective ppi after scaling, and fixing low-res files."
sources:
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
  - https://en.wikipedia.org/wiki/Halftone
  - https://en.wikipedia.org/wiki/Line_art
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print resolution for line art, greyscale and colour

**Goal:** files sharp enough for print without being needlessly huge.

## Targets at final printed size (typical printer requirements)
| Content | Resolution |
|---|---|
| Colour / greyscale art | 300 ppi (some colourists work at 400-600 for safety) |
| 1-bit line art / lettering raster | 600-1200 ppi (1200 preferred for crisp lines) |
| Screentones as bitmap | 600-1200 ppi so the dot pattern doesn't alias |
Lettering in vector (live text/outlines in PDF) is resolution-independent.

## Effective resolution
- What matters is ppi at **printed size**. A 600 ppi image placed at 200% prints at
  300 ppi effective.
- Art drawn at 150% original size at 400 ppi becomes ~600 ppi when reduced to print size.
- Check in InDesign (Links panel: Effective PPI) or Photoshop Image Size with resample
  off.

## Combining line art and colour
- Common approach: colour at 300-400 ppi in a layered file; line art either upsampled
  to match (keep it crisp, use nearest neighbour then threshold) or kept as a separate
  1200 ppi bitmap layer combined in layout.

## Fixing low-res files
- Upscaling can't recover detail; redraw/rescan if possible.
- For line art, upscale then threshold can smooth jaggies slightly; AI upscalers may
  help screen previews but check carefully for artefacts in print.

## Verify
- [ ] Colour/greyscale >= 300 ppi effective at print size.
- [ ] Line art 600-1200 ppi bitmap, or vector.
- [ ] Preflight reports no low-res images.
