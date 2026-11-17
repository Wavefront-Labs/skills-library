---
id: creative-arts.graphic-design.adobe-photoshop.image-size-and-resampling
name: image-size-and-resampling
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-document-setup, image-size-resampling, preserve-details-upscale, super-resolution, bicubic-sharper, resample, upscaling, downsampling, ppi]
level: practitioner
status: draft
description: "Resize images in Photoshop without damage: resample on vs off, Bicubic Sharper vs Preserve Details 2.0, Super Resolution, and the limits of upscaling."
sources:
  - https://helpx.adobe.com/photoshop/using/resizing-image.html
  - https://helpx.adobe.com/photoshop/using/image-size-resolution.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image size and resampling

**Goal:** the right pixel count for the output with the least visible loss.

## Image > Image Size (Alt+Ctrl+I / Opt+Cmd+I)
- **Resample unchecked:** changing ppi changes print size only; pixel count is fixed. Use this to
  see how big a file can print at 300 ppi.
- **Resample checked:** Photoshop creates or discards pixels. Choose the method:
| Method | Use |
|---|---|
| **Automatic** | picks Bicubic Sharper for down, Preserve Details for up |
| **Bicubic Sharper (reduction)** | downsizing photos; keeps crispness |
| Bicubic Smoother (enlargement) | modest upscaling of smooth images |
| **Preserve Details 2.0** | upscaling with AI; set Reduce Noise 10-30% |
| Nearest Neighbor (hard edges) | pixel art, screenshots with hard UI edges at integer scales |
| Bilinear | rarely |

## Upscaling a too-small image
1. Try **Camera Raw > Enhance > Super Resolution** (doubles width and height, 4x pixels) on raw
   or JPEG files - usually the best result.
2. Or Image Size with **Preserve Details 2.0**, up to ~200%.
3. Beyond 2-3x, detail is invented; ask for a larger original or a vector version.
   For logos never upscale raster - redraw or get the vector.

## Downsizing for web
Resize to final display size (x2 for high-density screens), then sharpen lightly (see output
sharpening skill), then Export As. Resizing in Export As is fine for simple cases.

## Smart objects
Scaling a smart object layer resamples from the original every time, so you can scale freely.
Image Size on a document with smart objects resamples their display, not their contents.

## Gotchas
- Never resample a file repeatedly (shrink, enlarge, shrink) - work from the original.
- Changing only ppi with resample on for print "to 300" multiplies pixels without adding detail.
- Width/height chain link must be on or the image distorts.

## Verify
- [ ] Final pixel dimensions match the target exactly.
- [ ] At 100% zoom: no halos from over-sharpening, no mush from aggressive upscaling.
- [ ] Original file kept unresampled.
