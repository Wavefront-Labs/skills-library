---
id: computing-software.computer-graphics-engineering.shader-programming.sdf-material-ids-and-colouring
name: sdf-material-ids-and-colouring
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, sdf-raymarching, sdf-materials, material-id, raymarching, smooth-union, shadertoy]
level: practitioner
status: draft
description: "Assign materials in ray-marched SDF scenes: returning (distance, id) from map, blending materials across smooth unions, and shading once after the march."
sources: ["https://iquilezles.org/articles/smin/", "https://iquilezles.org/articles/distfunctions/", "https://iquilezles.org/articles/normalsSDF/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Material IDs and colouring in ray-marched scenes

## 1. Return id with distance
```glsl
vec2 opU(vec2 a, vec2 b) { return a.x < b.x ? a : b; }   // (dist, materialId)

vec2 map(vec3 p) {
    vec2 res = vec2(sdPlane(p, vec3(0,1,0), 0.0), 1.0);
    res = opU(res, vec2(sdSphere(p - vec3(0,1,0), 1.0), 2.0));
    res = opU(res, vec2(sdBox(p - vec3(2.5,0.5,0), vec3(0.5)), 3.0));
    return res;
}
```
March using `map(p).x`; after the hit, read `map(p).y` once to pick the material. Keep the
march loop and normal estimation on a distance-only `mapD` if the id bookkeeping costs registers.

## 2. Shade after the march
```glsl
vec2 h = march(ro, rd);
vec3 pos = ro + rd * h.x;
vec3 nor = calcNormal(pos);
vec3 alb = h.y < 1.5 ? floorPattern(pos.xz) : h.y < 2.5 ? vec3(0.8,0.2,0.1) : vec3(0.2,0.4,0.9);
```
Avoid per-step material evaluation inside `map`; texture or noise lookups in the march loop
multiply cost by the step count.

## 3. Blending materials on smooth unions
Quilez's `smin` can return the blend factor:
```glsl
vec2 sminMix(float a, float b, float k) {     // returns (dist, mix 0..1)
    float h = max(k - abs(a - b), 0.0) / k;
    float m = h * h * 0.5;
    float s = m * k * 0.5;
    return a < b ? vec2(a - s, m) : vec2(b - s, 1.0 - m);
}
```
Carry colours (`vec4(dist, rgb)`) and `mix` them with the returned factor for seamless blends.

## 4. Procedural detail
Use world-space position (`pos`) or object-local position for patterns so they stick to moving
objects: return local coordinates from `map` via an out parameter when needed. For textures on
SDFs, triplanar mapping with the normal is the default.

## Gotchas
- Comparing float ids with `==` fails after interpolation; use thresholds (`< 1.5`).
- Bump/displacement added only during shading (not in `map`) leaves silhouettes smooth; add to
  `map` if silhouettes must change, and lower the step factor.

## Verify
- [ ] Debug view colours by id; no speckle at material boundaries.
- [ ] Frame time unchanged when adding materials (no material work inside the march).
