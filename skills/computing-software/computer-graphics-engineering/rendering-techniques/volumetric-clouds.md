---
id: computing-software.computer-graphics-engineering.rendering-techniques.volumetric-clouds
name: volumetric-clouds
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, volumetrics, volumetric-clouds, raymarching, cloud-noise, beer-powder, temporal-reprojection]
level: sme
status: draft
description: "Render real-time volumetric clouds: weather map and noise shapes, raymarching with Beer-Lambert and phase functions, light marching, and temporal reprojection."
sources: ["https://www.guerrilla-games.com/read/the-real-time-volumetric-cloudscapes-of-horizon-zero-dawn", "https://advances.realtimerendering.com/s2017/", "https://sebh.github.io/publications/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Volumetric clouds

## 1. Density field
- **Weather map** (2D, covering km): coverage, cloud type, precipitation.
- **Base shape**: 128^3 tiling 3D texture of Perlin-Worley + Worley fBm.
- **Detail**: 32^3 Worley fBm, used to erode edges.
- **Height gradient** per cloud type (stratus/cumulus) remaps density by altitude in the
  cloud layer (e.g. 1.5-4 km).
```glsl
float density(vec3 p) {
  vec4 w = weather(p.xz);
  float h = heightFraction(p);
  float base = remap(shapeNoise(p * 0.0003), 1.0 - w.r, 1.0, 0.0, 1.0) * heightGradient(h, w.b);
  float detail = detailNoise(p * 0.002);
  return clamp(remap(base, detail * 0.35, 1.0, 0.0, 1.0), 0.0, 1.0);
}
```

## 2. Raymarch
- March from the cloud layer entry to exit (ray-sphere against the planet shells), 64-128
  steps with larger steps in empty space, blue-noise jitter on the start offset.
- At each sample: transmittance `T *= exp(-sigma_t * density * dt)`; light marching toward the sun
  (6 samples with growing step) for self-shadowing.
- Scattering: Henyey-Greenstein dual-lobe phase (forward silver lining) and multiple-scattering
  approximation (several octaves with reduced extinction, Wrenninge).
- Stop when T < 0.01.

## 3. Performance
Render at quarter resolution and update 1/16 of pixels per frame with temporal reprojection
(Horizon Zero Dawn), then upscale with depth-aware blending against the scene.

## Gotchas
- Banding without jitter; flicker with jitter but without temporal accumulation.
- Clouds behind mountains: use scene depth to end the march.
- Atmosphere integration: apply aerial perspective to cloud colour by distance.

## Verify
- [ ] Stable clouds with a moving camera at 1-2 ms; sunsets show forward-scattering silver lining.
