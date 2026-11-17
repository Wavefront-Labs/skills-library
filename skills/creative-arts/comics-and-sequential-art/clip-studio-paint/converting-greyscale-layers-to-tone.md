---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.converting-greyscale-layers-to-tone
name: converting-greyscale-layers-to-tone
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-tones, csp-convert-to-tone, layer-property-tone, screentone, frequency-lpi, monochrome-output]
level: practitioner
status: draft
description: "Turn painted grey shading into printable dot screentone in Clip Studio Paint via Layer property > Tone: frequency, density source, dot type and angle, and output checks."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://en.wikipedia.org/wiki/Screentone
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Converting greyscale layers to tone

**Goal:** shade freely in grey, then output true halftone dots that print cleanly in
black-and-white books.

## Steps
1. Paint shading on a raster layer in greys (soft brushes, gradients fine).
2. Layer property palette > **Effect: Tone** (the tone button).
3. Set:
   - **Frequency** (lines per inch): book default, e.g. ~60 LPI (see the manga LPI skill).
   - **Density**: "Use image brightness" so lighter greys become smaller dots, or a
     fixed density.
   - **Dot type**: circle (standard), line, noise, etc.
   - **Angle**: 45 degrees typical.
4. Optionally "Posterize by density" for clearer stepped tones.
5. Display colour may show as grey on screen; the output becomes dots in Monochrome
   export.

## Alternatives
- New tone from a selection (selection launcher > New tone) creates a tone layer with a
  fixed density.
- Tone materials (patterns/gradations) from the Material palette.

## Output
- Export in Monochrome (2-tone) at 600-1200 dpi for print; tones render as crisp dots.
- Exporting Gray at low dpi turns dots to mush or moire.

## Gotchas
- Mixing different frequencies on overlapping layers causes moire.
- Resizing the canvas after converting changes dot size relative to the page; set
  frequency based on final size.

## Verify
- [ ] Tone layers share the book's frequency and angle.
- [ ] Monochrome test export at print dpi shows clean dots.
