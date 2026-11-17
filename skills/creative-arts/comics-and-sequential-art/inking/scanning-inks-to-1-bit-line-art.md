---
id: creative-arts.comics-and-sequential-art.inking.scanning-inks-to-1-bit-line-art
name: scanning-inks-to-1-bit-line-art
category: creative-arts
field: comics-and-sequential-art
product: inking
tags: [inking, ink-corrections, line-art-prep, line-art-scan, bitmap-line-art, 1200-dpi, threshold, photoshop-bitmap-mode]
level: practitioner
status: draft
description: "Scan inked pages for print: greyscale capture at 600-1200 dpi, threshold to 1-bit bitmap, clean-up, and why bitmap line art at high resolution prints crisper than greyscale."
sources:
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
  - https://helpx.adobe.com/photoshop/using/converting-between-color-modes.html
  - https://en.wikipedia.org/wiki/Line_art
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scanning inks to 1-bit line art

**Goal:** razor-sharp black-and-white line art files for colouring and print.

## Why bitmap
Line art is pure black and white. A 1-bit (bitmap) file at high resolution (600-1200
ppi at print size) prints crisper than greyscale at 300 ppi and is small on disk.
Printers typically ask for line art at 600 ppi minimum, often 1200 (check spec).

## Workflow (Photoshop; similar in other editors)
1. **Scan in greyscale**, 600 ppi at original art size (more if the art is small or
   will be enlarged). Turn off auto-sharpen/descreen.
2. Straighten and crop to the bleed marks.
3. **Levels/Threshold**: Image > Adjustments > Threshold; slide until lines are solid
   and fine hatching survives without filling in (typically around 128-180; judge by
   eye at 100% zoom).
4. Clean dust specks and stray marks (pencil/eraser residue) with a hard 100% white
   pencil tool.
5. **Resize** to final print size at 1200 ppi (if your source supports it), using a
   sharp resampling method; or convert at the target size.
6. Convert: Image > Mode > Bitmap, method **50% Threshold** (not diffusion dither, which
   creates noise), output 1200 ppi.
7. Save as TIFF (LZW or Group 4 compression).

## For colourists
Colourists usually need the line art as a layer in an RGB/CMYK file: convert bitmap ->
greyscale -> colour mode at the working resolution, set the line layer to Multiply.
Ask what they want.

## Gotchas
- Thresholding too high: fine lines and hatching fill in; too low: lines break up.
- Bitmap at 300 ppi shows jaggies in print.
- Blue pencil traces left in: drop them before thresholding (see non-photo blue removal).

## Verify
- [ ] 1-bit TIFF at the required ppi; correct trim + bleed size.
- [ ] Fine lines intact and no specks at 100% zoom.
