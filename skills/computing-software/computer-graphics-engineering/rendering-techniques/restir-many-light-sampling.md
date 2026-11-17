---
id: computing-software.computer-graphics-engineering.rendering-techniques.restir-many-light-sampling
name: restir-many-light-sampling
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, restir, reservoir-sampling, ris, many-lights, direct-illumination, ray-tracing]
level: sme
status: draft
description: "Implement ReSTIR DI: weighted reservoir sampling with RIS, temporal and spatial reuse, visibility reuse, and bias control for scenes with many lights."
sources: ["https://research.nvidia.com/publication/2020-07_spatiotemporal-reservoir-resampling-real-time-ray-tracing-dynamic-direct", "https://intro-to-restir.cwyman.org/", "https://github.com/NVIDIAGameWorks/RTXDI"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ReSTIR direct illumination

## 1. Reservoir
```hlsl
struct Reservoir { uint y; float wSum; float M; float W; };   // y = chosen light sample
bool update(inout Reservoir r, uint x, float w, float u) {
  r.wSum += w; r.M += 1;
  if (u * r.wSum < w) { r.y = x; return true; }
  return false;
}
```

## 2. Per-pixel pipeline
1. **Initial candidates (RIS)**: draw M=32 lights from a cheap source pdf `p` (power-weighted alias table);
   weight `w = p_hat(x) / p(x)`, `p_hat` = unshadowed contribution `Le * BSDF * G`.
   Finalise `W = wSum / (M * p_hat(y))`.
2. **Visibility reuse**: one shadow ray to `y`; if occluded set `W = 0` so occluded samples do not spread.
3. **Temporal reuse**: merge the reprojected previous reservoir, clamping its `M` to 20x the current one
   (stops stale history dominating).
4. **Spatial reuse**: merge k=5 neighbours within ~30 px; reject neighbours with depth difference > 10% or
   normal dot < 0.9. Merge: `update(r, n.y, p_hat_here(n.y) * n.W * n.M, rand)`, then `r.M += n.M - 1`.
5. Shade with `f(y) * r.W` and one final visibility ray.

## 3. Bias
- Naive spatial reuse is biased (a neighbour's sample may be invisible here). For unbiased results count M
  only from neighbours where `p_hat > 0` (plus visibility), or use MIS weights (pairwise MIS from GRIS).
- Bias appears as darkening near contact shadows; often acceptable in games.

## Gotchas
- Reservoirs need ping-pong buffers; reading and writing one buffer in the spatial pass races.
- Light IDs must be stable across frames for temporal reuse (remap when lights change).
- Emissive triangles: sample by area and convert the pdf to solid angle.

## Verify
- [ ] With 10k+ lights, 1-spp noise is far below plain light sampling; temporal reuse converges in a few frames.
- [ ] Unbiased mode matches a long-run path-traced reference within noise.
