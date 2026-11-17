---
id: creative-arts.animation.color.openexr-render-outputs
name: openexr-render-outputs
category: creative-arts
field: animation
product: color
tags: [openexr, scene-linear, linear-workflow, exr, half-float, piz, dwaa, multipart, aovs, oiiotool, exrheader]
level: advanced
status: draft
description: "Set up OpenEXR render outputs for comp and grade: half vs float, compression (ZIP/PIZ/DWAA), multi-layer vs multi-part, data window, metadata, inspection."
sources:
  - https://openexr.com/en/latest/
  - https://openexr.com/en/latest/TechnicalIntroduction.html
  - https://openimageio.readthedocs.io/en/latest/oiiotool.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenEXR render outputs

**Goal:** EXRs that hold the full linear range, load fast in comp, and are small enough for the
render storage budget.

## Bit depth

- **Half float (16-bit)**: beauty, light AOVs, colour passes. ~3 decimal digits precision, range
  to 65504. Default for colour.
- **Full float (32-bit)**: depth (Z), position (P), world normals at high values, motion vectors
  for large moves, cryptomatte IDs. Half depth values band and break defocus.

## Compression

| Codec | Lossless? | Use |
|---|---|---|
| ZIP (16 scanlines) | yes | good general default, fast read in Nuke |
| ZIPS (1 scanline) | yes | faster random line access, larger |
| PIZ | yes | best for noisy/grainy images |
| DWAA / DWAB | lossy | 3-5x smaller beauty for review/editorial; keep data passes lossless |
| RLE | yes | flat CG mattes |

Never use DWA on data passes (depth, normals, vectors, IDs): lossy error corrupts maths.

## Layers: multi-layer vs multi-part

- Single-part multi-layer: all AOVs in one image as `layer.channel` names. Reading one layer reads
  the whole file.
- Multi-part (EXR 2.0): each AOV a separate part; apps can read only what they need: faster comp.
- Many studios write beauty as one file and utility AOVs as another for that reason.

## Data window and overscan

The data window can be larger than the display window (overscan for lens distortion/camera shake)
or cropped to non-empty pixels (faster). Comp must respect it; check `Format` vs `Bounding box`
in Nuke.

## Metadata

Write camera, frame, render time, version and colour space into the header (`oiio:ColorSpace` or
a custom `ocio:colorspace` attribute). Pipeline checks then do not have to guess.

## Inspect

```bash
exrheader shot010.1001.exr          # OpenEXR tools: channels, compression, windows
oiiotool --info -v shot010.1001.exr  # same plus metadata
oiiotool shot010.1001.exr --stats    # min/max/avg per channel, NaN/Inf counts
```

## Gotchas

- NaNs and Infs from shaders propagate through blurs into black/white blocks; detect with
  `--stats` and clamp at render or comp.
- Premultiplied alpha is the EXR convention; don't unpremult-premult repeatedly
  (`creative-arts.animation.color.premultiplied-alpha`).

## Verify

`oiiotool --stats` on a frame shows expected channels, no NaN/Inf, and max beauty values above
1.0 where there are highlights (proof nothing was clamped or display-encoded).
