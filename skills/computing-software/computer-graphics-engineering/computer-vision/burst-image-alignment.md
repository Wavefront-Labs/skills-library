---
id: computing-software.computer-graphics-engineering.computer-vision.burst-image-alignment
name: burst-image-alignment
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, alignment-stitching, burst-alignment, burst-photography, tile-alignment, multi-frame-denoising, hdr-plus]
level: advanced
status: gated
description: "Align bursts of handheld frames for denoising, HDR or super-resolution: reference selection, coarse-to-fine tile alignment, subpixel refinement, robust merge, ghost rejection."
sources: ["https://hdrplusdata.org/hdrplus.pdf", "https://www.ipol.im/pub/art/2021/336/", "https://arxiv.org/abs/1905.03277"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Burst image alignment

## Pipeline (HDR+ style, checked against Hasinoff et al., SIGGRAPH Asia 2016)
1. **Reference**: pick the sharpest frame in a subset of the burst near the start (a gradient metric on the
   green channel of the raw input; the paper calls this lucky imaging).
2. **Pyramid**: build a 4-level Gaussian pyramid of the downsampled-to-grey raw input (the paper aligns
   3 Mpix grey images instead of 12 Mpix raw).
3. **Tile search**: per tile, search for the offset minimising a residual, initialised from the coarser
   level (try the upsampled offsets of the 3 nearest coarse tiles and keep the one with the smallest
   L1 residual). **The norm differs by scale**: at coarse scales the paper minimises **L2** with a
   sub-pixel result and a large search radius; at the finest scale it minimises **L1** at pixel level
   with a small radius. (The reverse of what is often assumed.)
4. **Subpixel**: at the coarse scales, fit a quadratic to the residual surface around the integer minimum
   and take its minimum (for a 1D parabola through costs 4.0, 1.0, 2.25 the offset is +0.206 px,
   computed); only pixel-level alignment is used at the finest scale because the merge cannot use more.
5. **Merge**: per tile (16x16 tiles of the Bayer colour planes, 32x32 for very dark scenes) in the
   frequency domain with shrinkage by the noise level; overlapping tiles use a modified raised-cosine
   window `1/2 - 1/2 cos(2 pi (x + 1/2) / n)` whose overlapped copies (half-tile overlap) sum to one.

## Robustness
- Motion that cannot be explained by tile offsets (people, leaves) must be down-weighted: compare
  aligned tile to reference against the noise model (from sensor noise calibration) and reduce
  weight where the difference exceeds k sigma.
- Use a fixed exposure across the burst (or normalise exposure) and work in linear raw space.

## OpenCV building blocks
- Global alignment: `cv2.findTransformECC` (affine/homography) or `cv2.calcOpticalFlowFarneback`,
  DIS optical flow (`cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM).calc(a, b, None)`)
  for dense flow. Tested on a photo shifted by (3.4, -2.2) px: ECC translation gave (3.45, -2.22) and
  the median DIS flow (3.41, -2.18).
- `cv2.createAlignMTB()` for exposure brackets (translation only, exposure-invariant): `calculateShift`
  takes two single-channel images of the same type and returned the shift that aligns the second to
  the first for a copy darkened to 40% (a 3-channel input raises an assertion).

## Super-resolution variant
Handheld multi-frame SR (Wronski et al.) uses sub-pixel offsets from natural hand tremor to fill
Bayer gaps; requires accurate subpixel alignment and kernel-regression merge (gated: unconfirmed, source is paywalled or blocked); the Wronski et al. paper was not fetched here.

## Verify
Aligned difference images against the reference should look like noise except in moving regions;
PSNR of merged output vs a tripod long-exposure ground truth.
