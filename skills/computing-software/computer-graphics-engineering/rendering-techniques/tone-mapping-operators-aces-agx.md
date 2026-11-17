---
id: computing-software.computer-graphics-engineering.rendering-techniques.tone-mapping-operators-aces-agx
name: tone-mapping-operators-aces-agx
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, hdr-rendering, tone-mapping, aces, khronos-pbr-neutral, filmic]
level: practitioner
status: docs-checked
description: "Implement HDR-to-SDR tone mapping: the Narkowicz ACES fit and the Khronos PBR Neutral operator, with exact constants and behaviour."
sources: ["https://knarkowicz.wordpress.com/2016/01/06/aces-filmic-tone-mapping-curve/", "https://github.com/KhronosGroup/ToneMapping/blob/main/PBR_Neutral/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tone mapping operators: ACES fit and PBR Neutral

**Goal:** turn scene-referred HDR values into displayable LDR. Both operators below are applied
to linear values.

## 1. ACES filmic fit (Narkowicz, 2016)
Narkowicz sampled the ACES ODT(RRT(x)) transform from the reference images (using Rec709 D65 with
the 2.4 gamma removed, since no linear D65 ODT exists) and manually fitted a simple curve
(maximum fit error 0.0138), weighted toward precision in the blacks because a gamma is applied
afterwards. The data was pre-exposed so 1 on input maps to about 0.8 on output; for the original
ACES curve multiply the input by 0.6. Source code is CC0 or MIT:
```hlsl
float3 ACESFilm(float3 x)
{
    float a = 2.51f, b = 0.03f, c = 2.43f, d = 0.59f, e = 0.14f;
    return saturate((x * (a * x + b)) / (x * (c * x + d) + e));
}
```
The author's own update: this is a luminance-only fit that over-saturates brights (consistent
with their art direction); for more realistic rendering use a more complex fit such as Stephen
Hill's (BakingLab ACES.hlsl).

## 2. Khronos PBR Neutral
Designed to reproduce base colours faithfully. Input is non-negative linear Rec. 709 colour; it
supports sRGB output only and does no gamut mapping. Constants: F90 = 0.04, Ks = 0.8 - F90
(where highlight compression starts), Kd = 0.15 (speed of desaturation).
```
x  = min(R, G, B)
f  = (x <= 2*F90) ? x - x*x / (4*F90) : F90
p  = max(R - f, G - f, B - f)
pn = 1 - (1 - Ks)^2 / (p + 1 - 2*Ks)
g  = 1 / (Kd * (p - pn) + 1)
out = (p <= Ks) ? c - f : (c - f) * (pn / p) * g + pn * (1 - g)     // pn added to all channels
```
Properties stated by Khronos: `out = in - F90` for all channels in [0.08, 0.8], so base colours
are exactly reproduced for a shiny dielectric facing the camera under unit white lighting; no
hue shifts (changes stay in the plane of the input colour and the white axis); derivatives are
continuous; the mapping is 1:1 and analytically invertible. Reference files in the repository:
pbrNeutral.glsl, an OpenColorIO config and LUT.

## Gotchas
- Applying tone mapping more than once (for example renderer and post pass) double tone maps.
- Colour grading LUTs authored for one operator do not transfer to another.

## Verify
- [ ] Single tone-map application verified in a frame capture.
- [ ] A saturated bright-light test scene is free of objectionable hue shifts with the chosen operator.

## Checked

Method: docs-checked 2026-11-09 against Narkowicz's ACES post (curve, fit and update note) and the Khronos PBR Neutral README (specification and notes), both read in full. Dropped Reinhard, AgX (Sobotka repository and iolite page not readable), Blender and three.js defaults, hue-skew claims about per-channel curves, HDR display advice, mid-grey validation numbers and the RTR4 reference.
