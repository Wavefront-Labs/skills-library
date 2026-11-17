---
id: creative-arts.graphic-design.adobe-illustrator.image-trace-settings
name: image-trace-settings
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, image-trace, image-trace-settings, vectorising, trace-presets, threshold, paths-corners-noise, ignore-white, expand-trace]
level: practitioner
status: draft
description: "Control Illustrator Image Trace: choose a preset, then tune mode, threshold or colours, paths, corners and noise, ignore white, and expand into clean editable paths."
sources:
  - https://helpx.adobe.com/illustrator/using/image-trace.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image Trace settings

**Goal:** a raster (scan, photo, logo bitmap) converted into vectors with the right amount of detail and
the fewest points, not a blobby or over-noded mess.

## Steps
1. Place the image (File > Place) and select it. Window > **Image Trace**.
2. Start with a preset: **Black and White Logo**, **Sketched Art**, **Silhouettes**, **Line Art**,
   **Technical Drawing**, **3 / 6 / 16 Colors**, **Shades of Gray**, High Fidelity / Low Fidelity Photo.
3. Turn on **Preview** only once settings are roughly right (large images retrace slowly).
4. Tune:
   - **Mode:** Black and White (use **Threshold**, default 128), Grayscale, Color (Colors slider or a
     Palette: Limited, Full Tone, or a swatch **Document Library** to trace with brand colours).
   - **Advanced > Paths:** fidelity of the path to the pixels (lower = smoother, fewer points).
   - **Corners:** higher = more sharp corners.
   - **Noise:** pixel area ignored (raise to drop specks; 20-50 px for scans).
   - **Method:** Abutting (cut-out shapes) or Overlapping (stacked shapes, easier to recolour).
   - **Create:** Fills and/or Strokes (strokes for line art only, with max stroke width).
   - **Snap Curves To Lines**, **Ignore White** (drops white areas so the trace sits on any background).
5. Save your tuned settings as a custom preset from the presets menu.
6. Click **Expand** (Object > Image Trace > Expand) to get editable paths; ungroup, then clean up.

## Source preparation (matters more than sliders)
- Scan at 300-600 ppi, clean levels/contrast in Photoshop first, remove dust, crop tight.
- Larger source pixels give smoother curves; upscale a small logo 2-4x (Preserve Details) before tracing.

## After tracing
- Delete stray specks (Select > Same > Fill Color, or Magic Wand), merge shapes with Shape Builder,
  Object > Path > **Simplify** to reduce points.
- For logos, a traced result is a reference; redraw key curves with the Pen tool for professional work.

## Gotchas
- Tracing photos at high fidelity creates thousands of shapes: heavy files, not true vector art.
- Ignore White only applies in some modes; check the result over a coloured rectangle.
- Expanded trace keeps the original image only if you keep a copy; Expand discards the link to settings.

## Verify
- [ ] Point count is sensible (Document Info > Objects); edges look clean at 400% zoom.
- [ ] Trace sits on a coloured background with no white boxes.
