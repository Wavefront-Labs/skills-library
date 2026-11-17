---
id: creative-arts.animation.vector-graphics.multi-colour-trace-and-quantisation
name: multi-colour-trace-and-quantisation
category: creative-arts
field: animation
product: vector-graphics
tags: [colour-trace, color-trace, colour-quantisation, image-trace, vectorization, posterize, trace-bitmap]
level: practitioner
status: docs-checked
description: "Trace coloured artwork to stacked vector shapes: palette reduction first, then Inkscape colour quantization or multiple scans, and clean-up."
sources:
  - https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html
  - https://potrace.sourceforge.net/potrace.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-colour trace and quantisation

Potrace itself is a bilevel tracer: its input should use only black and white, and other pixel values are converted with a simple threshold (potrace(1) man page). Colour tracing therefore works by splitting the image into colour layers, then tracing each.

## Preparation (most of the quality)
1. Work from the largest, cleanest source; avoid JPEG artefacts.
2. **Reduce the palette first**: posterise or index the image to the number of colours you want. A tight palette gives cleaner shapes than letting the tracer decide.
3. Remove noise and dithering before tracing.

## Inkscape (Path > Trace Bitmap)
- Import the bitmap, select it, open Path > Trace Bitmap, use Update to refresh the preview, then Ok. The result is placed exactly above your picture.
- **Single scan** tab: *Color quantization* traces along borders between different colours; *Brightness cutoff* gives a silhouette; *Edge detection* vectorizes contours only.
- **Multiple scans** gives a more detailed result but creates a separate object for each scan (the manual's example is the Colors option with 10 scans: 10 stacked objects in the result, which can be moved after ungrouping).
- Preview before applying; the result is a stack of objects, not one shape.

## After tracing
Clean up (`trace-cleanup-and-node-reduction.md`), merge near-duplicate colours, and name layers by colour or region.

## Verify
- [ ] Compare against the original at 100% and 400%.
- [ ] Palette count matches the design palette.
- [ ] No hairline gaps between neighbouring shapes at the final output size.

## Checked

2026-11-09. Confirmed against the Inkscape manual "Tracing an image" page and the potrace(1) man page: bilevel input and thresholding, Trace Bitmap workflow, Single scan modes, Multiple scans producing a separate object per scan. Removed unconfirmed claims: suggested colour counts, "Stack scans" and "Remove background" options, the whole Illustrator Image Trace section (Adobe pages not checkable here), and the VTracer note.
Method: documentation only; no commands were run.
