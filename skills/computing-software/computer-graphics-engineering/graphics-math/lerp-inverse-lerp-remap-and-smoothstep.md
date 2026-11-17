---
id: computing-software.computer-graphics-engineering.graphics-math.lerp-inverse-lerp-remap-and-smoothstep
name: lerp-inverse-lerp-remap-and-smoothstep
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-encoding, inverse-lerp, remap-range, lerp, smoothstep, exponential-smoothing]
level: practitioner
status: verified
description: "Use interpolation helpers correctly: precise lerp forms, inverse lerp and remap, clamped vs unclamped, smoothstep/smootherstep, frame-rate independent damping and step pitfalls."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/smoothstep.xhtml", "https://en.cppreference.com/w/cpp/numeric/lerp", "https://www.rorydriscoll.com/2016/03/07/frame-rate-independent-damping-using-lerp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lerp, remap and smoothstep variants

## Lerp
```cpp
float lerp(float a, float b, float t) { return a + t * (b - a); }      // fast, not exact at t=1
float lerpExact(float a, float b, float t) { return (1 - t) * a + t * b; } // exact endpoints, monotonic issues
```
`a + t*(b-a)` may not return exactly b at t = 1 for large differences (computed in float32: a=1e8, b=1e-3 gives 0.0); `(1-t)a + tb` returns both
endpoints exactly but can be non-monotonic. C++20 `std::lerp` guarantees exact endpoints (t = 0 and 1) and monotonicity for finite a, b (cppreference).
GLSL `mix(a, b, t)`.

## Inverse lerp and remap
```cpp
float invLerp(float a, float b, float v) { return (v - a) / (b - a); }   // guard a == b
float remap(float iMin, float iMax, float oMin, float oMax, float v) {
    return lerp(oMin, oMax, invLerp(iMin, iMax, v));
}
float remapClamped(...) { return lerp(oMin, oMax, std::clamp(invLerp(iMin, iMax, v), 0.f, 1.f)); }
```
Decide clamped vs unclamped deliberately; unclamped remap extrapolates.

## Smoothstep family
- `smoothstep(e0, e1, x)`: `t = clamp((x-e0)/(e1-e0), 0, 1); t*t*(3 - 2t)` (C1).
- Smootherstep (Perlin): `t^3 (t (6t - 15) + 10)` (C2, second derivative is 0 at both ends: checked symbolically).
- GLSL: results are undefined if `e0 >= e1`; to reverse, use `1 - smoothstep(e0, e1, x)`
  rather than swapping the edges (works on most drivers but is not guaranteed).
- Anti-aliased edges: `smoothstep(-w, w, d)` with `w = fwidth(d)` (or `length(fwidth)`).

## Frame-rate independent smoothing
`x = lerp(x, target, 1 - exp(-lambda * dt))` (or `1 - pow(r, dt)`). The common
`x = lerp(x, target, 0.1)` per frame converges at different speeds at 30 vs 144 fps.

## Step
`step(edge, x)` returns 0 for `x < edge`, 1 otherwise; note the argument order (edge first), the
reverse of most people's intuition.

## Verify
Unit tests: endpoints, midpoint, monotonicity on random a, b, t; damping reaches the same value after 1 s
at different dt.
