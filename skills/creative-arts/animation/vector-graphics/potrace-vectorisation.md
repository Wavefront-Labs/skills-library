---
id: creative-arts.animation.vector-graphics.potrace-vectorisation
name: potrace-vectorisation
category: creative-arts
field: animation
product: vector-graphics
tags: [potrace, vectorization, image-trace, trace-bitmap, inkscape, bitmap-to-svg, turdsize, alphamax, line-art-tracing]
level: practitioner
status: docs-checked
description: "Vectorise raster line art with Potrace (CLI) or Inkscape Trace Bitmap: black-and-white input first, turdsize/alphamax/opttolerance tuning, checking results."
sources:
  - https://potrace.sourceforge.net/potrace.1.html
  - https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vectorising with Potrace

**Goal:** clean vector shapes from raster line art, logos or silhouettes (scanned drawings, legacy bitmap assets),
usable for scaling, colouring in vector tools, or motion graphics.

## Prepare the bitmap

Potrace reads PBM, PGM, PPM (PNM) and BMP files. The input should use only black and white; other pixel values are
converted with a simple threshold. For better detail preservation threshold the image yourself first: the
`mkbitmap` tool distributed with Potrace can scale and interpolate the image before thresholding. Clean dust and
paper texture out of the scan before thresholding.

## Trace

```bash
potrace scan.pbm -s -o scan.svg --turdsize 4 --alphamax 1.0 --opttolerance 0.2
```
| Option | Effect |
|---|---|
| `-s` / `--svg` | SVG backend. Unless `-r` is given the input resolution is assumed to be 72 dpi. Other backends: `-b pdf`, `-b eps` (the default backend), `-b ps`, `dxf`, `geojson`, `pgm`, `gimppath`, `xfig` |
| `--turdsize N` (`-t`) | suppress speckles of up to N pixels |
| `--alphamax A` (`-a`) | corner threshold, default 1: smaller gives more sharp corners; 0 means no smoothing (polygon output); above 4/3 all corners are suppressed |
| `--opttolerance T` (`-O`) | curve optimisation tolerance, default 0.2: larger values join more consecutive Bezier segments at the expense of accuracy |
| `--longcurve` (`-n`) | turn off curve optimisation (larger files) |
| `--invert` (`-i`) | invert the input bitmap before processing |
| `--turnpolicy` (`-z`) | how to resolve ambiguities in path decomposition (black, white, right, left, minority, majority, random; default minority) |

## Inkscape Trace Bitmap

Import the bitmap, select it, Path > Trace Bitmap, use Update to refresh the preview, then Ok. The result is placed exactly over the picture. Single scan modes: **Brightness cutoff** (the most frequently used; a silhouette-like path following the shape), **Edge detection** (contours only), **Color quantization** (traces borders between colours), **Autotrace** and **Centerline tracing (autotrace)**. **Multiple scans** gives a more detailed result but creates a separate object for each scan.

## What brightness-cutoff tracing gives you

Silhouette outlines (filled shapes), not centrelines. For single open-path lines from handwriting or line drawings use Inkscape's Centerline tracing (autotrace), which reduces a shape to an open path.

## Gotchas

- Over-smoothing rounds intended sharp corners on lettering; lower alphamax for type and logos.
- Raising opttolerance trades accuracy for fewer segments; clean the bitmap rather than relying on it for noisy scans.
- Colour artwork: use Multiple scans or quantisation and expect manual cleanup (each scan is a separate object).

## Verify

Overlay the SVG on the source at 200%: edges follow the drawing within a pixel or two, no specks, corners sharp
where the artist drew them.

## Checked

2026-11-09. Confirmed against the potrace(1) man page (potrace.sourceforge.net/potrace.1.html) and the Inkscape manual "Tracing an image" page: input formats and thresholding, backend list, option meanings and defaults (alphamax 1, opttolerance 0.2, turnpolicy minority), 72 dpi SVG assumption, Inkscape modes and workflow. Removed unconfirmed claims: the ImageMagick threshold command, the 600 dpi scan advice, the statement that Inkscape's Trace Bitmap uses Potrace with the same smoothing options, node-count checks, and the claim that `--invert` traces white on black (the page says it inverts the input bitmap).
Method: documentation only; no commands were run.
