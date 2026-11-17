---
id: computing-software.computer-graphics-engineering.gpu-optimisation.shader-fast-math-approximations
name: shader-fast-math-approximations
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, shader-optimisation, fast-math, polynomial-approximation, rsqrt, transcendental-functions, alu-optimisation]
level: advanced
status: draft
description: "Use fast math approximations in shaders: rsqrt, fast acos/atan polynomials, exp2/log2 bases, pow avoidance, sin-free rotations and when precision loss shows up."
sources: ["https://seblagarde.wordpress.com/2014/12/01/inverse-trigonometric-functions-gpu-optimization-for-amd-gcn-architecture/", "https://www.humus.name/Articles/Persson_LowLevelThinking.pdf", "https://github.com/michaldrobot/ShaderFastLibs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fast approximations in shaders

## 1. Know the hardware
- `rsqrt`, `rcp`, `exp2`, `log2`, `sin`, `cos` are single transcendental-unit ops (quarter rate on
  many GPUs). `sqrt` is often `rcp(rsqrt(x))`; `pow(x, y)` = `exp2(y * log2(x))` (3 ops).
- `acos`, `asin`, `atan`, `atan2` compile to long polynomial sequences (20-40 instructions).
- Division is `x * rcp(y)`.
Emil Persson's "Low-level thinking in shader code" is the reference for what compiles to what.

## 2. Substitutions
| Instead of | Use |
|---|---|
| `normalize(v)` when only direction needed | `v * inversesqrt(dot(v, v))` (same thing; but share the `dot` if you also need length) |
| `length(a - b) < r` | `dot(d, d) < r * r` |
| `pow(x, 2.0)`, `pow(x, 5.0)` | `x * x`, `x2 = x*x; x2 * x2 * x` |
| `exp(x)` | `exp2(x * 1.442695)` (fold the constant into an existing multiply) |
| `acos(x)` | Lagarde polynomial: `(-0.156583 * abs(x) + 1.570796) * sqrt(1 - abs(x))`, mirror for x<0 |
| `atan(y, x)` | polynomial on `min/max` ratio (ShaderFastLibs `atanFast`) |
| rotation by angle per pixel | precompute `vec2(cos, sin)` on CPU or VS |
| `smoothstep` for a linear ramp | `saturate(x * a + b)` (MAD + free saturate) |

## 3. Free modifiers
`saturate`, negate and `abs` are usually free input/output modifiers; `clamp(x, 0, 1)` compiles to
saturate. Write `x * a + b` forms the compiler can fuse into MAD/FMA.

## 4. Fitting your own polynomial
For an expensive function on a known range: fit a minimax polynomial (Sollya, numpy
`polyfit` as a start, Remez for minimax), evaluate with Horner's rule, and check max error over the
range and at endpoints.

## Gotchas
- Fast approximations near domain edges (acos at +-1) can produce NaN from `sqrt` of tiny
  negatives; clamp inputs.
- Approximate `rcp` is not IEEE exact; don't use for values that must round-trip (indices).
- `-ffast-math`-like flags in compilers (DXC `-Gis` off, relaxed precision) already enable some of
  this; verify in ISA rather than assuming.

## Verify
- [ ] ISA / instruction count drops (RGA, Mali OC, Nsight SASS).
- [ ] Max absolute error plotted across the input range is within the visual tolerance.
