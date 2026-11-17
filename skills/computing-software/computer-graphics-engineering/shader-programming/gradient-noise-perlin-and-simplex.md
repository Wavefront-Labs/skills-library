---
id: computing-software.computer-graphics-engineering.shader-programming.gradient-noise-perlin-and-simplex
name: gradient-noise-perlin-and-simplex
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, procedural-texturing, perlin-noise, simplex-noise, value-noise, gpu-hash, shader-random, quintic-fade, noise-tiling]
level: practitioner
status: draft
description: "Implement value, gradient (Perlin) and simplex noise in shaders: integer hash choice, quintic interpolation, output ranges."
sources: ["https://thebookofshaders.com/11/", "https://thebookofshaders.com/10/", "https://www.jcgt.org/published/0009/03/02/", "https://github.com/stegu/webgl-noise", "https://iquilezles.org/articles/gradientnoise/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gradient noise in shaders: Perlin and simplex

**Goal:** smooth, artefact-free procedural noise that looks the same on every GPU and stays
stable at large coordinates.

## 1. Hash first (the part people get wrong)
The famous `fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453)` breaks down: `sin`
precision differs per GPU and degrades for large `p` → visible patterns/banding. Prefer
integer hashes (JCGT 2020 "Hash Functions for GPU Rendering"):
```glsl
uint pcg(uint v) { uint s = v * 747796405u + 2891336453u;
                   uint w = ((s >> ((s >> 28u) + 4u)) ^ s) * 277803737u; return (w >> 22u) ^ w; }
uvec2 pcg2d(uvec2 v) { v = v * 1664525u + 1013904223u; v.x += v.y * 1664525u; v.y += v.x * 1664525u;
                       v ^= v >> 16u; v.x += v.y * 1664525u; v.y += v.x * 1664525u; v ^= v >> 16u; return v; }
float rand01(uvec2 p) { return float(pcg2d(p).x) * (1.0 / 4294967296.0); }
```
WebGL1/GLES2 lack uint — there, use a sin-free float hash (Dave Hoskins' `hash12`) and keep
coordinates small.

## 2. Value vs gradient noise
- **Value noise**: random value per lattice point, interpolated — blocky, visible grid.
- **Gradient (Perlin) noise**: random gradient per lattice point, dot with offset — far
  fewer grid artefacts, zero at lattice points.
```glsl
vec2 grad(ivec2 c) { float a = 6.2831853 * rand01(uvec2(c)); return vec2(cos(a), sin(a)); }
float perlin(vec2 p) {
    ivec2 i = ivec2(floor(p)); vec2 f = fract(p);
    vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);              // quintic fade (C2)
    float a = dot(grad(i),               f);
    float b = dot(grad(i + ivec2(1, 0)), f - vec2(1, 0));
    float c = dot(grad(i + ivec2(0, 1)), f - vec2(0, 1));
    float d = dot(grad(i + ivec2(1, 1)), f - vec2(1, 1));
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);                   // ≈ [-0.7, 0.7]
}
```
Cubic fade (`3f²-2f³`) has discontinuous second derivatives → visible creases in normals
from noise; use quintic.

## 3. Simplex noise
Simplex lattice (triangles in 2D, tetrahedra in 3D): fewer evaluations in higher dimensions
(N+1 corners vs 2^N), no axis-aligned artefacts. Use the well-tested Ashima/Gustavson
`webgl-noise` implementations (`snoise(vec3)`) rather than writing your own; output ≈ [-1, 1].
3D/4D simplex is the default choice for animated volumetric noise (4D = 3D + time).

## 4. Ranges and tiling
Normalise empirically: Perlin 2D output is not [-1, 1]. Remap with `n * 0.5 + 0.5` after
scaling, and clamp. Tileable noise: wrap lattice coordinates `i % period` before hashing.

## Gotchas
- Large world coordinates (≥ 10^4) lose float precision in `fract(p)` → stair-stepping;
  offset coordinates relative to camera or use double-precision origin shifting.
- Derivatives: analytic derivative versions (IQ's) are cheaper than finite differences
  for normals.
- Texture-based noise (precomputed tileable 3D texture) is often faster on mobile.

## Verify
- [ ] Noise image shows no grid-aligned artefacts or diagonal patterns.
- [ ] Same output on two GPU vendors (pixel diff) with integer hashing.
- [ ] Value histogram checked; remap gives the intended range.
