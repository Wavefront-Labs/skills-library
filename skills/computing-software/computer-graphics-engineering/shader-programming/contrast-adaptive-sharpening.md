---
id: computing-software.computer-graphics-engineering.shader-programming.contrast-adaptive-sharpening
name: contrast-adaptive-sharpening
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, post-processing-shaders, contrast-adaptive-sharpening, fidelityfx-cas, sharpening, rcas, taa, upscaling]
level: practitioner
status: docs-checked
description: "Apply AMD FidelityFX CAS or similar sharpening after TAA/upscaling: how the adaptive kernel works, strength settings, placement in the chain and avoiding halos."
sources: ["https://github.com/GPUOpen-Effects/FidelityFX-CAS", "https://github.com/GPUOpen-Effects/FidelityFX-CAS/blob/master/ffx-cas/ffx_cas.h", "https://github.com/GPUOpen-Effects/FidelityFX-FSR/blob/master/ffx-fsr/ffx_fsr1.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contrast Adaptive Sharpening (CAS)

TAA and upscalers soften the image. A sharpen pass restores perceived detail; CAS limits
sharpening where local contrast is already high, so edges don't halo.

## 1. How CAS works
For each pixel, read the 3x3 neighbourhood. The default (faster) path takes the soft min/max over the plus-shaped
cross only; defining `CAS_BETTER_DIAGONALS` in `ffx_cas.h` adds the corners. The per-channel amount is
`sqrt(saturate(min(minRGB, 1 - maxRGB) / maxRGB))` (the diagonal variant uses `2 - maxRGB` because its
sums are doubled): low-contrast areas get more sharpening, already-contrasty areas less. The output is a weighted sum
`(c + w * (n + s + e + w_)) / (1 + 4w)` with negative `w` (a 5-tap unsharp kernel), saturated.

Simplified version:
```glsl
vec3 a = tex(-1,0), b = tex(1,0), c = tex(0,-1), d = tex(0,1), e = tex(0,0);
vec3 mn = min(min(min(a, b), min(c, d)), e);
vec3 mx = max(max(max(a, b), max(c, d)), e);
vec3 amp = sqrt(clamp(min(mn, 1.0 - mx) / mx, 0.0, 1.0));   // inputs in [0,1]
float peak = -1.0 / mix(8.0, 5.0, sharpness);               // sharpness 0..1
vec3 w = amp * peak;
vec3 outc = (e + (a + b + c + d) * w) / (1.0 + 4.0 * w);
```

## 2. Integration
- Use the official FidelityFX CAS header (`ffx_cas.h` in GPUOpen-Effects/FidelityFX-CAS, MIT licence): `CasFilter()` is the
  32-bit form and `CasFilterH()` the packed 16-bit form; it can also upsample.
- FSR 1 applies RCAS (Robust Contrast Adaptive Sharpening, a non-scaling variation on CAS) as a separate pass after EASU.
- Placement: the header recommends running CAS after tonemapping, with input value 1.0 at the peak of the display output;
  running it after compositing UI is fine. Film grain before CAS gets amplified, so reduce it or add grain after CAS.
- Expose strength to users; the setup code maps sharpness 0..1 to a peak of `-1 / lerp(8, 5, sharpness)`.

## Gotchas
- Sharpening amplifies noise and film grain; apply grain after sharpening.
- The adaptive term assumes input scaled so the display peak is 1.0; tonemap first.
- Sharpening twice (engine CAS plus another sharpening pass) can halo.

## Verify
- [ ] A/B with TAA alone: texture detail restored, no white/black halos at high-contrast edges.
- [ ] Temporal stability: no new shimmer in motion.

## Checked

Checked 2026-10-26 against FidelityFX-CAS repository (ffx-cas/ffx_cas.h, MIT, last push 2021-07-15) and FidelityFX-FSR repository (ffx_fsr1.h, last push 2022-05-22). Confirmed: the per-channel `amp` formula and its default (cross) versus `CAS_BETTER_DIAGONALS` (`2.0 - max`) variants, the 5-tap filter shape and `1 + 4w` normalisation, `peak = -1/lerp(8, 5, saturate(sharpness))`, 32-bit and packed 16-bit entry points, tonemap-first and grain guidance from the header comments, MIT licence; RCAS is a non-scaling CAS variation applied after EASU in FSR 1. Corrected: the `2 - max` form only applies with CAS_BETTER_DIAGONALS and the default samples the cross. Removed as unconfirmed: FSR 2/3 sharpness behaviour, driver sharpening product names, the default strength range.

Method: documentation only; no commands were run.
