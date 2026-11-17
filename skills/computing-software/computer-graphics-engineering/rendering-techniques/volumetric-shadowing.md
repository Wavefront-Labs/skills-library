---
id: computing-software.computer-graphics-engineering.rendering-techniques.volumetric-shadowing
name: volumetric-shadowing
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, volumetrics, volumetric-shadows, transmittance-map, deep-shadow-maps, opacity-shadow-maps, froxels, light-shafts]
level: advanced
status: draft
description: "Shadow participating media: shadow-map sampling per froxel, self-shadowing via transmittance volumes, deep/opacity shadow maps and temporal filtering."
sources: ["https://www.ea.com/frostbite/news/physically-based-unified-volumetric-rendering-in-frostbite", "https://graphics.pixar.com/library/DeepShadows/paper.pdf", "https://advances.realtimerendering.com/s2014/wronski/bwronski_volumetric_fog_siggraph2014.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Volumetric shadowing

Two separate problems: (a) media receiving shadows from opaque geometry (light shafts), and (b)
media shadowing themselves and other objects (smoke casting shadows).

## 1. Opaque shadows into media
For every froxel or ray-march sample, sample the light's shadow map (cascade selection by depth):
```glsl
float vis = shadowCascades(samplePos);     // 1 = lit
vec3 inscatter = sigmaS * phase * vis * lightColor;
```
- Use a few PCF taps or a pre-blurred ESM/VSM version of the shadow map to reduce noise; volumetric
  shadows don't need sharp edges.
- Jitter sample positions per frame (blue noise in depth) and use temporal reprojection of the froxel
  volume (Wronski 2014) to remove banding.

## 2. Self-shadowing of media
- **Ray marching toward the light** from each sample: accurate but O(N*M); use few, large steps
  (4-6) with increasing length; common for clouds.
- **Transmittance volume / light-space 3D texture**: precompute transmittance from the light through
  the media into a low-res volume aligned to the light; samples look it up (Frostbite "volumetric
  shadow maps").
- **Opacity shadow maps / deep shadow maps**: store transmittance as a function of depth per shadow
  texel (several slices, or a compressed curve - Pixar deep shadow maps); also lets smoke and hair
  shadow opaque geometry.
- **Fourier/moment opacity maps** compress the function into a few coefficients.

## 3. Media shadowing opaque surfaces
Opaque shading samples the transmittance volume or deep shadow map at the surface position and
multiplies the light. Particles: render particle optical depth into a light-space "particle shadow
map" with additive blending of extinction and convert with `exp(-x)`.

## 4. Performance
- Froxel grid ~160x90x64 for fog: shadow sampling cost is per froxel, not per pixel.
- Update self-shadow volumes at lower rate or resolution than the main march.

## Gotchas
- Cascade transitions show as discontinuities in fog shafts; blend cascades or sample a single
  coarse cascade for volumes.
- Shadow map bias tuned for surfaces creates offset shafts; volumes can use zero bias.

## Verify
- [ ] Light shafts align with occluder silhouettes; no banding with temporal filtering on.
- [ ] Smoke casts soft shadows onto the ground and on itself.
