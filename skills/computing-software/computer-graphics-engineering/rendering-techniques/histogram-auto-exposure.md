---
id: computing-software.computer-graphics-engineering.rendering-techniques.histogram-auto-exposure
name: histogram-auto-exposure
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, hdr-rendering, auto-exposure, eye-adaptation, luminance-histogram, compute-shader, exposure-compensation, metering]
level: advanced
status: docs-checked
description: "Implement histogram-based auto exposure: luminance histogram in compute, weighted average luminance, EV100 and Lmax exposure from Lagarde and de Rousiers."
sources: ["https://bruop.github.io/exposure/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Histogram auto exposure

Source: the BruOp blog post on automatic exposure on building a luminance histogram in
compute shaders (following Alex Tardif's histogram luminance post) and deriving exposure with
the method of Lagarde and de Rousiers (2014).

## 1. Where it fits
Tone mapping pipeline: render linear HDR, find the average luminance, scale the input luminance
by exposure, apply the tone operator to reach a clamped linear [0, 1], then apply the inverse
EOTF (gamma) for the display. Exposure linearly scales the scene luminance so that the tone
operator maps values as expected. The exposure value (EV) is a logarithmic representation of
luminance: +1 EV doubles the luminance.

## 2. Luminance
`L = 0.2125 R + 0.7154 G + 0.0721 B` on the HDR radiance values (the CIE xyY luminosity
coefficients, as written in the post).

## 3. Exposure from average luminance
With sensor sensitivity S, reflected-light meter calibration constant K, lens and vignetting
attenuation q, average scene luminance Lavg:
```
EV100 = log2(Lavg * S / K)
Lmax  = 78 / (q * S) * 2^EV100          // luminance that saturates the sensor
H     = 1 / Lmax                         // exposure
L'    = H * L
```
The post uses S = 100, K = 12.5 (Canon, Nikon and Sekonic use it, and most engines follow) and
q = 0.65, which simplifies to `Lmax = 9.6 * Lavg`, so `L' = L / (9.6 * Lavg)`. The result is
still not clamped to [0, 1], so clipping can remain.

## 4. Average luminance: geometric mean versus histogram
Two popular ways: a geometric average obtained by repeatedly downsampling the luminance (like a
mip chain), or a histogram over a static luminance range. The geometric average over-represents
extreme values; a histogram gives control over how extremes influence the average (and allows
other statistics such as the median).

## 5. Histogram in compute
- Each work group keeps a shared histogram for its chunk of pixels and adds it into the global
  histogram buffer at the end, avoiding contention on the global buffer per pixel.
- Pixels below a threshold luminance fall in bin 0 and are excluded from the average.
- A second compute pass reads the global histogram, accumulates a weighted count, and also
  resets the global histogram for the next frame. The weighted sum divided by the number of
  pixels contributing any luminance (all except bin 0) gives the average bin, which is mapped back
  from histogram bin space to a luminance by inverting the binning operation.

## Gotchas
- Bin 0 (below threshold) must be excluded from the divisor.

## Verify
- [ ] Walk from interior to exterior: exposure converges smoothly.
- [ ] Reset the global histogram every frame.

## Checked

Method: docs-checked 2026-11-09 against the bruop.github.io exposure post (exposure, luminance, histogram construction and aggregation prose read; the shader listings were skimmed). Dropped the HLSL listings, the percentile filter percentages, the temporal adaptation formula and speeds, centre-weighted metering masks, the Unreal Engine and RTR4 sources, and the 0.1 ms cost claim.
