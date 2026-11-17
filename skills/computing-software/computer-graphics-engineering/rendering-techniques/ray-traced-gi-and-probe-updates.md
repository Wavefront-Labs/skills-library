---
id: computing-software.computer-graphics-engineering.rendering-techniques.ray-traced-gi-and-probe-updates
name: ray-traced-gi-and-probe-updates
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, rtgi, ray-traced-gi, ddgi, probe-updates, denoising, dxr, vulkan-ray-tracing]
level: advanced
status: draft
description: "Build ray-traced diffuse GI: per-pixel RT with denoising vs ray-traced probe updates (DDGI), ray budgets, hit shading via probes/radiance cache, and performance tiers."
sources: ["https://jcgt.org/published/0008/02/01/", "https://github.com/NVIDIAGameWorks/RTXGI-DDGI", "https://developer.nvidia.com/rtx/ray-tracing/rtxgi"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ray-traced GI and probe updates

## 1. Two families
| | Per-pixel RTGI | Ray-traced probes (DDGI) |
|---|---|---|
| Rays | 0.25-1 per pixel per frame | ~100-300 per probe per frame, thousands of probes |
| Detail | contact-level indirect, sharp | low frequency, grid resolution |
| Cost scales with | resolution | probe count |
| Needs | strong denoiser (ReBLUR, SVGF) | temporal hysteresis only |

Most shipping engines combine both: probes or a radiance cache for multi-bounce, per-pixel or
screen-space for near-field detail.

## 2. DDGI (Majercik et al. 2019)
- Grid of probes; each frame every probe traces N rays (random rotation per frame).
- Hit shading: direct light at hit (shadow ray or shadow map) + previous frame's probe irradiance at
  the hit (infinite bounces over time).
- Update octahedral irradiance (8x8 texels per probe) and distance moments (16x16, mean and
  mean^2) textures with hysteresis (~0.97).
- Sampling uses Chebyshev visibility from distance moments to avoid leaks through walls.
- Probe relocation (move out of geometry) and classification (disable probes inside walls or in
  empty space) are essential.

## 3. Per-pixel RTGI
1. Trace 1 ray per pixel (or per 2x2) cosine/BRDF sampled, half-res.
2. Shade hits cheaply: use the probe/radiance cache at the hit instead of recursive tracing.
3. Denoise: temporal accumulation + spatial filtering (NRD ReBLUR/ReLAX), demodulate albedo first.
4. ReSTIR GI for reuse of paths across pixels and frames improves quality per ray.

## 4. Budgets
- Console/mid PC: probes only (DDGI) or half-res 0.25 rpp.
- High-end: 1 rpp + ReSTIR GI + denoiser.
- Use inline ray queries (`RayQuery` in compute) for simple hit shading; pipelines with hit shaders
  when material evaluation is complex.

## Gotchas
- Shading hits with full materials is the hidden cost; use simplified hit materials (albedo +
  emissive from a lightweight table).
- Probe grids in large worlds need cascades/scrolling volumes.
- Denoisers need correct motion vectors, normals, roughness and hit distance inputs.

## Verify
- [ ] GI converges within ~0.5 s after a light change without flicker.
- [ ] No leaking through walls in indoor test scenes; GPU time within budget per tier.
