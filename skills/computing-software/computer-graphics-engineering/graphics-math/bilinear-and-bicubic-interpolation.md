---
id: computing-software.computer-graphics-engineering.graphics-math.bilinear-and-bicubic-interpolation
name: bilinear-and-bicubic-interpolation
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-encoding, bicubic-interpolation, bilinear-interpolation, catmull-rom, texture-filtering, image-resampling]
level: practitioner
status: draft
description: "Interpolate images and grids: bilinear weights and texel-centre offsets, bicubic kernels (Catmull-Rom, B-spline, Keys a=-0.5), fast bicubic from bilinear taps, ringing."
sources: ["https://doi.org/10.1109/TASSP.1981.1163711", "https://developer.nvidia.com/gpugems/gpugems2/part-iii-high-quality-rendering/chapter-20-fast-third-order-texture-filtering", "https://en.wikipedia.org/wiki/Bicubic_interpolation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bilinear and bicubic interpolation

## Bilinear
```cpp
float sampleBilinear(const Image& I, float u, float v) {      // u, v in pixel units, centres at x.5
    float x = u - 0.5f, y = v - 0.5f;
    int x0 = floor(x), y0 = floor(y); float fx = x - x0, fy = y - y0;
    float a = I(x0, y0), b = I(x0+1, y0), c = I(x0, y0+1), d = I(x0+1, y0+1);
    return lerp(lerp(a, b, fx), lerp(c, d, fx), fy);
}
```
The -0.5 accounts for texel centres; forgetting it shifts the image by half a pixel (a common
off-by-half bug between OpenCV-style integer-centred and GPU-style half-centred conventions).

## Bicubic kernels (4x4 taps)
Mitchell-Netravali family with parameters (B, C):
| Kernel | (B, C) | Character |
|---|---|---|
| Catmull-Rom / Keys a = -0.5 | (0, 0.5) | Interpolating, sharp, slight ringing |
| Keys a = -0.75 (OpenCV `INTER_CUBIC`) | | Sharper, more ringing |
| Mitchell | (1/3, 1/3) | Balanced (ImageMagick default for upsampling) |
| Cubic B-spline | (1, 0) | Smooth, blurry, non-interpolating, no ringing |

Keys kernel: `W(x) = (a+2)|x|^3 - (a+3)|x|^2 + 1` for `|x| <= 1`; `a|x|^3 - 5a|x|^2 + 8a|x| - 4a` for
`1 < |x| < 2`.

## Overshoot
Negative lobes produce values below 0 / above 1 near edges (ringing): clamp results, and beware HDR
data (bright pixels produce dark halos). B-spline has no negative lobes.

## GPU: bicubic from 4 bilinear fetches
Combine weights so each pair of taps becomes one bilinear fetch at an offset position: B-spline
needs 4 fetches instead of 16 (Sigg and Hadwiger, GPU Gems 2 ch. 20); Catmull-Rom can be done with 5 to
9 fetches because its weights change sign.

## Downsampling
Bilinear/bicubic interpolation does not prefilter: shrinking by more than 2x aliases. Use area
averaging (`INTER_AREA`), mipmaps, or a kernel scaled to the output pixel size.

## Verify
Upsample a step edge and a linear ramp: ramp must be reproduced exactly by all interpolating kernels;
measure overshoot at the step.
