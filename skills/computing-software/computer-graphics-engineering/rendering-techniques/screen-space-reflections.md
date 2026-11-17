---
id: computing-software.computer-graphics-engineering.rendering-techniques.screen-space-reflections
name: screen-space-reflections
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, ssr, screen-space-reflections, hi-z-tracing, stochastic-ssr, reflection-fallback, edge-fade, roughness-reflections]
level: advanced
status: draft
description: "Implement screen-space reflections: view-space or Hi-Z ray marching, thickness and hit validation, stochastic rough reflections with temporal resolve."
sources: ["https://jcgt.org/published/0003/04/04/paper.pdf", "https://www.ea.com/frostbite/news/stochastic-screen-space-reflections", "https://gpuopen.com/fidelityfx-sssr/", "Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 11.6.5"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screen-space reflections

**Goal:** reflections of on-screen geometry on floors, water and glossy surfaces, blending
seamlessly into probe/sky reflections where screen data runs out (RTR4 §11.6.5).

## 1. Ray setup
Per pixel with low enough roughness (e.g. < 0.6): reflect the view vector about the normal
in view space. For rough surfaces, sample a GGX lobe direction per pixel (stochastic SSR)
instead of the mirror direction.

## 2. Tracing
- **Linear screen-space DDA** (McGuire & Mara, JCGT 2014): march in screen space with
  perspective-correct depth interpolation — uniform pixel steps, no wasted samples.
- **Hi-Z tracing**: march through a min-depth mip pyramid, stepping up levels in empty space,
  down near surfaces — far fewer steps for long rays (AMD FidelityFX SSSR).
Hit test: ray depth behind the depth buffer by less than a **thickness** (e.g. 0.1–0.5 m in
view space, or scaled with distance); otherwise it passed behind an object.

## 3. Shade the hit
Sample last frame's **lit colour** (pre-TAA, reprojected with motion vectors) at the hit UV,
or the current frame's lighting if reflections run after the lighting pass. Weight by
Fresnel and the material's specular term.

## 4. Confidence and fallback
```glsl
float conf = hit ? 1.0 : 0.0;
conf *= 1.0 - smoothstep(0.85, 1.0, max(abs(hitUV.x * 2 - 1), abs(hitUV.y * 2 - 1)));  // screen edge fade
conf *= 1.0 - smoothstep(0.4, 0.9, dot(reflDirView, vec3(0, 0, -1)));                  // rays toward camera
vec3 refl = mix(probeOrSkyReflection, ssrColor, conf);
```
Rays toward the camera leave the screen data almost immediately — fade them.

## 5. Rough reflections
Stochastic SSR: one ray per pixel per frame along sampled GGX directions, then a spatial
resolve reusing neighbours' hits (ratio estimator weighting by BRDF/pdf) and temporal
accumulation. Cheaper alternative: blur the reflection buffer by roughness (cone-traced
mips) — less accurate, more stable.

## Gotchas
- Missing information: anything off-screen or occluded never reflects (classic: reflections
  disappearing as the camera tilts down). Probes/RT must cover it.
- Self-intersection at the start: offset the origin and skip the first steps.
- Thin objects get rays through them; thickness tuning trades leaks vs false hits.
- Water with normal maps: high-frequency normals make SSR noisy — temporal filter and
  limit ray length.

## Verify
- [ ] Puddle/floor test scene: reflections align with objects; no gaps at contact points.
- [ ] Camera tilt: edges fade smoothly to probe reflections (no hard cut-off).
- [ ] Rough-surface reflections stable under motion (temporal resolve working).
