---
id: computing-software.computer-graphics-engineering.shader-programming.tileable-periodic-noise
name: tileable-periodic-noise
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, tileable-noise, periodic-noise, pnoise, seamless-textures, noise-baking]
level: practitioner
status: draft
description: "Make seamlessly tiling noise textures: periodic lattice hashing (pnoise), 4D torus mapping, tileable fBm and Worley, and baking to textures without seams."
sources: ["https://github.com/stegu/webgl-noise", "https://thebookofshaders.com/11/", "https://www.ronja-tutorials.com/post/029-tiling-noise/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tileable / periodic noise

## 1. Periodic lattice (best)
Wrap the integer lattice coordinates before hashing so the noise repeats every `period` units:
```glsl
float pnoise(vec2 p, vec2 period) {
    vec2 i = floor(p), f = fract(p);
    vec2 i0 = mod(i, period), i1 = mod(i + 1.0, period);   // wrap lattice
    float a = hash(i0), b = hash(vec2(i1.x, i0.y)), c = hash(vec2(i0.x, i1.y)), d = hash(i1);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
```
Ashima/Gustavson `webgl-noise` ships `pnoise(vec3 P, vec3 rep)` for classic Perlin with period.
Period must be an integer number of lattice cells.

## 2. Tileable fBm
Each octave doubles frequency; double the period too so every octave tiles at the same texture
size:
```glsl
float f = 0.0, amp = 0.5; vec2 per = vec2(4.0);
for (int o = 0; o < 6; o++) { f += amp * pnoise(uv * per, per); per *= 2.0; amp *= 0.5; }
```
Do not add rotation matrices between octaves; rotation breaks periodicity.

## 3. Torus mapping (when you only have non-periodic noise)
Map the 2D tile onto a 4D torus and sample 4D noise:
```glsl
vec2 a = uv * 6.2831853;
vec4 p = vec4(cos(a.x), sin(a.x), cos(a.y), sin(a.y)) * radius;
float n = snoise4(p);
```
Works with any 4D noise; cost is higher and features stretch slightly.

## 4. Tileable Worley
Wrap cell ids with `mod(id + offset, period)` before hashing the feature point; keep the distance
computed with the unwrapped offset.

## 5. Cross-fade (last resort)
Blend `noise(p)` with shifted copies weighted by distance to the edges. Cheap but reduces contrast
in the middle; avoid for anything but quick fixes.

## Gotchas
- Baking: sample at texel centres (`(x + 0.5) / size`) and use a period that divides the texture
  size, or the last column won't match the first.
- Mipmaps of a tileable texture should be generated with wrap addressing, not clamp, to keep the
  seams invisible at lower mips.

## Verify
- [ ] Render the texture tiled 3x3 at high contrast; no visible seams at any mip.
