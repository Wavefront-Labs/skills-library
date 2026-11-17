---
id: computing-software.computer-graphics-engineering.rendering-techniques.volumetric-path-tracing-delta-tracking
name: volumetric-path-tracing-delta-tracking
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, delta-tracking, volumetric-path-tracing, ratio-tracking, woodcock-tracking, null-scattering, participating-media]
level: sme
status: draft
description: "Path trace heterogeneous volumes: delta (Woodcock) tracking, ratio tracking for transmittance, majorant grids and the null-scattering formulation."
sources: ["https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering", "https://cs.dartmouth.edu/~wjarosz/publications/miller19null.html", "https://jannovak.info/publications/MonteCarloVolumeRenderingSTARCourse/index.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Volumetric path tracing (delta tracking)

## 1. Free-flight sampling in heterogeneous media
For homogeneous media sample distance analytically: `t = -ln(1 - u) / sigma_t`. For heterogeneous
`sigma_t(x)`, introduce a **majorant** `sigma_maj >= sigma_t(x)` over the region and fictitious
"null" particles with `sigma_n = sigma_maj - sigma_t`.

**Delta (Woodcock) tracking**:
```cpp
float t = tmin;
while (true) {
    t -= log(1 - rnd()) / sigmaMaj;
    if (t >= tmax) return ESCAPED;                       // no collision in the medium
    vec3 x = o + d * t;
    float st = sigmaT(x);
    if (rnd() < st / sigmaMaj) return REAL_COLLISION_AT(x);   // then absorb vs scatter by albedo
    // else null collision: continue
}
```
Unbiased; cost depends on how tight the majorant is.

## 2. Transmittance estimation
- **Ratio tracking** for shadow rays: step with the majorant like delta tracking but multiply
  `T *= 1 - sigma_t(x) / sigma_maj` at each tentative collision instead of terminating; lower
  variance than binary visibility.
- **Residual ratio tracking**: subtract a control variate (homogeneous approximation) for speed.

## 3. Majorant grids
A single global majorant wastes steps in thin regions. Use a coarse grid (or the VDB tree's node
max values) of local majorants, and DDA through it, sampling free flights per cell. PBRT-v4 uses a
`MajorantGrid` (16^3) with `DDAMajorantIterator`.

## 4. Null-scattering path integral (Miller, Georgiev, Jarosz 2019)
Reformulates volume transport so null collisions are explicit path vertices; enables
spectral/chromatic media with a single majorant, MIS between distance sampling strategies, and
unbiased estimators beyond delta tracking. PBRT-v4's volume integrator follows this formulation.

## 5. Integration with the path tracer
At a real collision: with probability albedo scatter (sample phase function, NEE to lights with ratio
tracking transmittance), else absorb (add emission for fire media). Combine with surface
interactions inside/outside media via medium interfaces on surfaces.

## Gotchas
- Majorant smaller than actual sigma_t anywhere -> biased (too transparent); compute majorants
  conservatively including interpolation.
- Spectral (RGB) sigma_t requires a majorant per wavelength or the hero/max channel approach with
  weights.
- Dense media make step counts huge; consider path guiding or approximations for production.

## Verify
- [ ] Homogeneous medium via delta tracking matches the analytic exponential result.
- [ ] Changing the majorant (looser) changes cost only, not the converged image.
