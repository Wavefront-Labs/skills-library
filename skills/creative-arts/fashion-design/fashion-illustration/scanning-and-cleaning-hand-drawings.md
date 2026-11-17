---
id: creative-arts.fashion-design.fashion-illustration.scanning-and-cleaning-hand-drawings
name: scanning-and-cleaning-hand-drawings
category: creative-arts
field: fashion-design
product: fashion-illustration
tags: [fashion-design, fashion-illustration, scanning-drawings, line-cleanup, digital-fashion-illustration, adobe-photoshop, image-trace]
level: practitioner
status: draft
description: "Scan hand-drawn fashion sketches and clean them for digital colouring or vector flats: scan settings, levels, removing paper tone, isolating line art and image trace."
sources:
  - https://helpx.adobe.com/photoshop/using/levels-adjustment.html
  - https://helpx.adobe.com/illustrator/using/image-trace.html
  - https://en.wikipedia.org/wiki/Image_scanner
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scanning and cleaning hand drawings

## Scan
- Flatbed at **600 dpi** for line art (300 dpi minimum), greyscale for pencil/ink, 24-bit
  colour for painted work. Save TIFF or PNG, not JPEG.
- Keep the paper flat with the lid closed. Phone captures: shoot square-on in daylight and
  use a scanner app to correct perspective.

## Clean line art (Photoshop)
1. Image > Adjustments > **Levels**: move the white input slider left until the paper is
   white, the black slider right until lines are solid; midtone to taste.
2. Remove smudges with a white brush or Select > Color Range > Highlights.
3. Isolate lines: Select > Color Range > Shadows, new layer, fill black; or set the line
   layer to **Multiply** so colour layers can go beneath.
4. Close gaps in outlines that need fills.

## To vector (Illustrator)
- Object > Image Trace with a black-and-white preset; adjust Threshold, Paths and Noise;
  tick Ignore White. Expand, then Object > Path > Simplify.
- For technical flats, trace is a draft; redraw seams with the Pen tool for clean geometry.

## Gotchas
- Blue-pencil underdrawing drops out if you scan in colour and remove the blue channel
  (or use a non-photo-blue filter).
- Aggressive Levels lose pencil shading; keep the original scan.
- Over-traced vectors carry thousands of anchor points; simplify or redraw.

## Verify
- [ ] Paper tone pure white, lines solid.
- [ ] Line art on its own Multiply layer.
- [ ] Original scan archived.
