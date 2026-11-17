---
id: computing-software.computer-graphics-engineering.shader-programming.noise-derivatives-and-curl-noise
name: noise-derivatives-and-curl-noise
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, noise-derivatives, curl-noise, analytic-derivatives, gradient-noise, particles, flow-field]
level: advanced
status: draft
description: "Compute analytic gradient-noise derivatives for cheap normals and erosion-style fBm, and build divergence-free curl noise for particle and smoke advection."
sources: ["https://iquilezles.org/articles/gradientnoise/", "https://iquilezles.org/articles/morenoise/", "https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph2007-curlnoise.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Noise derivatives and curl noise

## 1. Why analytic derivatives
Finite differences need 3 extra noise evaluations (4x cost) for a gradient. Gradient/value noise
is a polynomial blend of corner values, so its derivative is available almost for free.

## 2. 2D value noise with derivatives (Quilez)
```glsl
vec3 noised(vec2 x) {                 // returns (value, d/dx, d/dy)
    vec2 i = floor(x), f = fract(x);
    vec2 u  = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);       // quintic
    vec2 du = 30.0 * f * f * (f * (f - 2.0) + 1.0);
    float a = hash(i), b = hash(i + vec2(1,0)), c = hash(i + vec2(0,1)), d = hash(i + vec2(1,1));
    float k1 = b - a, k2 = c - a, k4 = a - b - c + d;
    return vec3(a + k1*u.x + k2*u.y + k4*u.x*u.y,
                du * vec2(k1 + k4*u.y, k2 + k4*u.x));
}
```
For gradient noise the derivative also includes the gradient vectors themselves; Quilez's article
gives the full 3D version returning `vec4(value, gradient)`.

## 3. Uses of derivatives
- Terrain normals: `n = normalize(vec3(-d.x, 1.0, -d.y))` (after scaling by amplitude/frequency).
- Erosion-like fBm: attenuate each octave by accumulated slope:
```glsl
float a = 0.0, b = 1.0; vec2 dsum = vec2(0);
for (int i = 0; i < 8; i++) {
    vec3 n = noised(p);
    dsum += n.yz;
    a += b * n.x / (1.0 + dot(dsum, dsum));
    b *= 0.5; p = m2 * p * 2.0;          // m2 = rotation to break axis alignment
}
```
- Remember the chain rule per octave: derivative of `noise(p * freq)` is `freq * dnoise`.

## 4. Curl noise (Bridson 2007)
Velocity `v = curl(psi)` of a vector potential is divergence-free: particles swirl without sinks
or sources, which reads as fluid.
```glsl
// 3D: psi = three decorrelated noise fields; need their gradients
vec3 curlNoise(vec3 p) {
    vec4 nx = noised3(p);                       // (value, grad)
    vec4 ny = noised3(p + vec3(31.4, 15.9, 26.5));
    vec4 nz = noised3(p + vec3(-17.2, 8.3, 41.7));
    return vec3(nz.z - ny.w,  nx.w - nz.y,  ny.y - nx.z);   // (dPz/dy - dPy/dz, dPx/dz - dPz/dx, dPy/dx - dPx/dy)
}
```
2D: `v = vec2(dpsi/dy, -dpsi/dx)` from a single scalar noise.
Near obstacles, ramp psi to zero by distance so flow slides along surfaces.

## Gotchas
- Value noise derivatives are discontinuous with the cubic smoothstep fade; use the quintic fade for
  C2 continuity.
- Finite-difference curl with a too-small epsilon in fp16 gives garbage; analytic is safer.

## Verify
- [ ] Analytic gradient matches central differences within tolerance at random points.
- [ ] Particles advected by curl noise neither clump nor spread out over time (divergence ~ 0).
