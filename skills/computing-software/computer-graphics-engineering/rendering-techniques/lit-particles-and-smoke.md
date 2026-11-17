---
id: computing-software.computer-graphics-engineering.rendering-techniques.lit-particles-and-smoke
name: lit-particles-and-smoke
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, volumetrics, lit-particles, smoke-rendering, six-way-lighting, soft-particles, vfx, particle-lighting]
level: practitioner
status: draft
description: "Light particles and smoke convincingly: per-vertex vs per-pixel lighting, normal-mapped and 6-way lightmaps, soft particles, shadow receiving, and volumetric fog injection."
sources: ["https://realtimevfx.com/t/smoke-lighting-and-texture-re-usability-in-skull-bones/5339", "https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.0/manual/six-way-lighting.html", "https://developer.download.nvidia.com/whitepapers/2007/SDK10/SoftParticles_hi.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lit particles and smoke

## 1. Lighting models for particle sprites
| Model | Cost | Look |
|---|---|---|
| Unlit (baked into texture) | lowest | wrong when lighting changes |
| Per-vertex lighting (ambient SH + main light + few points) | low | soft, OK for smoke |
| Normal-mapped sprites | medium | crisp detail, can look flat-shaded |
| **6-way lightmaps** (light from +X,-X,+Y,-Y,+Z,-Z baked from a sim) | medium | best for volumetric smoke |

## 2. Six-way lighting
Bake smoke simulations (Houdini/EmberGen) lit from 6 directions into two RGBA textures. At runtime,
transform the light direction into the particle's tangent space and blend:
```glsl
vec3 l = lightDirTS;                                     // tangent space light dir
float x = l.x > 0.0 ? tex0.r : tex0.g;                    // +X / -X
float y = l.y > 0.0 ? tex0.b : tex0.a;                    // +Y / -Y
float z = l.z > 0.0 ? tex1.r : tex1.g;                    // +Z (front) / -Z (back, transmission)
float lit = x * l.x * l.x + y * l.y * l.y + z * l.z * l.z;
```
Unity VFX Graph and UE Niagara both support this workflow. Ambient: sample SH with the 6-way
weights too.

## 3. Soft particles
Fade alpha where the particle approaches opaque geometry:
`alpha *= saturate((sceneLinearDepth - particleLinearDepth) / fadeDistance)`. Removes hard
intersection lines.

## 4. Shadows
- Receiving: sample the shadow map at the particle position (per vertex for cost, per pixel for
  big particles).
- Casting: particle shadow maps (optical depth accumulated in light space) or let volumetric fog
  handle it.

## 5. Volumetric integration
Inject particle density into the froxel fog volume for correct lighting and sorting with fog; large
dense smoke can be rendered as true volumes (UE Heterogeneous Volumes, NanoVDB).

## 6. Overdraw
Smoke is overdraw-heavy: tight sprite meshes (cut alpha-zero corners, "particle cutout"),
lower-res offscreen particle buffer (half or quarter res, upsampled with depth-aware filter).

## Gotchas
- Per-pixel lighting with many lights on full-screen smoke is expensive: clamp light count.
- Billboards rotating to face the camera shift lighting if normals aren't recomputed; use
  camera-facing tangent frames.

## Verify
- [ ] Smoke responds to moving light direction (backlit glow, front shading).
- [ ] No hard lines at geometry intersections; overdraw view acceptable.
