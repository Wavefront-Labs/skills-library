---
id: computing-software.computer-graphics-engineering.shader-programming.shaping-functions-and-smoothstep
name: shaping-functions-and-smoothstep
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, shaping-functions, smoothstep, step, easing, remap]
level: intro
status: draft
description: "Shape values in shaders with step, smoothstep, mix, pow, sin and remap functions to build gradients, falloffs, masks and antialiased edges."
sources: ["https://thebookofshaders.com/05/", "https://iquilezles.org/articles/functions/", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/smoothstep.xhtml"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shaping functions and smoothstep

## 1. Core functions
```glsl
float s = step(0.5, x);                 // 0 below edge, 1 at/above
float t = smoothstep(0.2, 0.8, x);      // Hermite 3t^2 - 2t^3, clamped
float m = mix(a, b, t);                 // lerp
float r = clamp((x - lo) / (hi - lo), 0.0, 1.0);   // remap to 0..1 (linearstep)
float p = pow(x, k);                    // bias toward 0 (k>1) or 1 (k<1); x must be >= 0
```
`smoothstep(e0, e1, x)` with e0 > e1 is undefined in GLSL (works on most GPUs, not guaranteed);
use `1.0 - smoothstep(e1, e0, x)`.

## 2. Useful shapes (Inigo Quilez)
```glsl
float almostIdentity(float x, float m, float n) {   // smooth floor near 0
  if (x > m) return x; float a = 2.0*n - m, b = 2.0*m - 3.0*n, t = x/m; return (a*t + b)*t*t + n; }
float expImpulse(float x, float k) { float h = k * x; return h * exp(1.0 - h); }  // peak at 1/k
float parabola(float x, float k) { return pow(4.0 * x * (1.0 - x), k); }
float gain(float x, float k) { float a = 0.5*pow(2.0*((x<0.5)?x:1.0-x), k); return (x<0.5)?a:1.0-a; }
float smootherstep(float x) { return x*x*x*(x*(x*6.0-15.0)+10.0); }   // C2 continuous
```

## 3. Antialiased edges
```glsl
float d = length(uv - 0.5) - 0.3;           // signed distance to circle edge
float w = fwidth(d);                        // ~1 pixel in d units
float alpha = 1.0 - smoothstep(-w, w, d);   // crisp at any zoom
```
Hard `step` aliases; smoothstep over a fixed width blurs when zoomed; fwidth adapts.

## 4. Debugging shapes
Plot the function: `float y = f(uv.x); col = mix(col, vec3(1,0,0), smoothstep(0.01, 0.0, abs(uv.y - y)));`.

## Gotchas
- `pow` of negative numbers is undefined (NaN on many GPUs).
- `smoothstep` with e0 == e1 divides by zero.
- Repeated `sin` of large values loses precision; wrap with `fract` first.

## Verify
- [ ] Plot each shaping curve on screen; edges look 1 px wide at every zoom level.
