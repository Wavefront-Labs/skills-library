---
id: computing-software.computer-graphics-engineering.shader-programming.raymarch-performance-optimisation
name: raymarch-performance-optimisation
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, sdf-raymarching, raymarch-optimization, sphere-tracing, over-relaxation, cone-marching, bounding-volumes, shader-optimisation]
level: advanced
status: draft
description: "Speed up SDF ray marching: bounding volumes, over-relaxed sphere tracing, adaptive epsilon, step and distance limits, cone marching, and half-resolution passes."
sources: ["https://erleuchtet.org/~cupe/permanent/enhanced_sphere_tracing.pdf", "https://iquilezles.org/articles/raymarchingdf/", "https://www.fulcrum-demo.org/wp-content/uploads/2012/04/Cone_Marching_Mandelbox_by_Seven_Fulcrum_LongVersion.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ray marching performance

Cost = pixels x steps x cost(map). Attack each factor.

## 1. Cheaper map
- **Bounding volumes**: wrap expensive sub-objects in a cheap sphere/box SDF; only evaluate the
  detailed SDF if the ray is within the bound:
```glsl
float dB = sdSphere(p - c, R);
float d = dB > 0.5 ? dB : detailedSDF(p);   // margin keeps the field conservative
```
- Bounding volume hierarchies of SDFs for scenes with many objects; or cull objects per tile in a
  compute pre-pass and march only the tile's list.
- Analytic ray intersection for the bounds first: start the march at the bound's entry `t` and end
  at the exit `t`.

## 2. Fewer steps
- **Over-relaxation (Keinert et al. 2014)**: step `omega * d` with omega ~ 1.2-1.6; if the new
  sphere does not overlap the previous one (`d_prev + d_new < step`), back off to omega = 1.
```glsl
float t = tmin, omega = 1.4, prevR = 0.0, stepLen = 0.0;
for (int i = 0; i < MAX_STEPS && t < tmax; i++) {
    float r = map(ro + rd * t);
    bool fail = omega > 1.0 && (abs(r) + prevR) < stepLen;
    if (fail) { stepLen -= omega * stepLen; omega = 1.0; }      // undo and fall back
    else      { stepLen = r * omega; }
    prevR = abs(r);
    if (!fail && abs(r) < eps * t) break;
    t += stepLen;
}
```
- **Adaptive epsilon**: `eps * t` (pixel footprint grows with distance) stops early on far
  surfaces.
- **Max distance and max steps**: cap both; return "miss" colour/fog when exhausted.

## 3. Fewer rays
- **Cone marching**: march low-res tiles with a cone radius equal to the tile footprint; store the
  safe distance; full-res rays start there. 2-4x speedups on complex fractals.
- Half or quarter resolution march + depth-aware upsample; TAA to hide noise.
- Reproject last frame's depth as the starting `t` (with a safety margin).

## 4. Shading
- Normals with the tetrahedron technique: 4 map evaluations instead of 6.
- Soft shadows and AO are extra marches; lower their step counts, use larger steps.

## Gotchas
- Over-relaxation with non-Lipschitz SDFs (twists, noise displacement) causes holes; reduce
  omega or the base step factor.
- Loops with data-dependent exits diverge per warp; neighbouring rays that need very different step
  counts waste lanes. Visualise step count heatmaps.

## Verify
- [ ] Step-count heatmap before/after; average steps reduced with no visual holes.
- [ ] GPU time per pass measured at target resolution.
