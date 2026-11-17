---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.gradient-tones-in-csp
name: gradient-tones-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-tones, csp-gradient-tone, gradient-tool, gradation-tone, tone-layer, dot-gradient]
level: practitioner
status: draft
description: "Make gradient (gradation) screentones in Clip Studio Paint: gradient tool with tone effect, gradient layers, dot shape and frequency, editing direction, avoiding print banding."
sources:
  - https://deleter-mangashop.com/en/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradient tones

## Method A: gradient fill + tone effect
1. Select the area.
2. **Gradient** tool, gradient set "Foreground to transparent" (draws dots fading out) or a custom
   black-to-white.
3. Create as **Gradient layer** (Tool property: Create gradient layer) so it stays editable, or draw on a
   raster layer.
4. Layer property > Effect > **Tone**; set frequency and dot type; dots now scale from large to small.

## Method B: gradient tone material
- Material palette > Monochromatic pattern > Gradation: drag onto the selection; the material comes in
  with preset direction and lpi. Rotate with Object tool.

## Editing
- Object tool on a gradient layer moves start/end points; you can change curve and colours.
- Reverse direction or add midpoints for glows.
- Mask with the layer mask for soft edges (scrape with soft eraser for highlights).

## Print settings
- Match the frequency of other tones on the page (e.g. 60 lpi) so they read as one system.
- Very light ends: the smallest dots may drop out in print; start the gradient a little darker than 0%.
- Check at final output resolution (600 dpi monochrome).

## Gotchas
- Applying tone effect to a gradient on a colour-expression layer exports colour pixels; set the page
  expression to monochrome or greyscale.
- Gradient with smoothing curve too steep causes visible bands of dot sizes.

## Verify
- [ ] Monochrome 2-tone export shows smooth dot transition with no banding.
