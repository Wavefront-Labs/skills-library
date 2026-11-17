---
id: creative-arts.photography-fine-art.adobe-lightroom.raw-details-and-super-resolution
name: raw-details-and-super-resolution
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, super-resolution, lightroom-detail, raw-details, enhance, upscaling, lightroom-classic]
level: practitioner
status: draft
description: "Use Lightroom Classic Enhance for Raw Details and Super Resolution to double linear resolution for large prints, with limits, file outputs and checks."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/enhance-details.html", "https://helpx.adobe.com/camera-raw/using/enhance-details.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Raw Details and Super Resolution

Both live in Photo > **Enhance** (Ctrl/Cmd+Alt/Option+I) alongside Denoise.

## Raw Details
- Re-demosaics the raw with a machine-learning model for finer edge detail and fewer artefacts (false colour, maze patterns on X-Trans).
- Same pixel dimensions. Output: DNG with `-Enhanced-RD` suffix.
- Useful for very fine textures to be printed large.

## Super Resolution
- Doubles width and height (4x pixel count): a 24 MP raw becomes ~96 MP. Raw and non-raw input (JPEG, TIFF, PNG) are supported.
- Output: DNG with `-Enhanced-SR` suffix; raw input stays a raw-like linear DNG with edits preserved.
- Limits: the source cannot exceed 128 MP or 32,500 px on either side.
- Enhance can run once per file; Denoise and Super Resolution can be ticked together in one pass.

## When to use
- Large prints from a heavily cropped frame or an older low-resolution camera, when print size would otherwise need less than about 180 ppi.
- Not needed for a moderate enlargement: Lightroom's own print resampling handles up to about 1.5x well.

## Gotchas
- Output files are large (a 96 MP DNG can exceed 300 MB); keep them only for images going to print.
- Upscaling enlarges noise: denoise in the same pass.
- Check fine repeating detail (fabric, brick) for invented texture at 100%.

## Verify
- [ ] Compare a 100% crop of the original upsampled in Photoshop (Preserve Details 2.0) against the SR file; keep the SR file only if visibly better.
