---
id: computing-software.computer-graphics-engineering.shader-programming.finding-nan-inf-black-pixels
name: finding-nan-inf-black-pixels
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, nan-propagation, black-pixels, inf, isnan, normalize-zero, pow-negative, taa-nan-spread]
level: practitioner
status: draft
description: "Track down NaN/Inf black or white pixels in shaders: the usual culprits, debug visualisation with isnan/isinf, how TAA and bloom spread them."
sources: ["https://renderdoc.org/docs/how/how_debug_shader.html", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-isnan", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://developer.nvidia.com/nsight-graphics"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finding NaN/Inf and black pixels

**Goal:** locate and eliminate the stray black (or white) pixels that appear on one GPU, grow
into blotches through TAA/bloom, and vanish when you try to capture them.

## 1. Usual culprits
| expression | failure |
|---|---|
| `normalize(v)` with v ≈ 0 | 0/0 = NaN (degenerate normals, zero-length tangents, H when L = −V) |
| `pow(x, y)` with x < 0 | NaN (e.g. `pow(dot(N,H), spec)` with negative dot) |
| `sqrt(x)` x < 0, `log(x)` x ≤ 0 | NaN / −Inf (Fresnel, GGX terms with tiny roughness) |
| `acos/asin` outside [−1, 1] | NaN (rounding pushes dot products to 1.0000001) |
| `x / y` y = 0 | Inf, then Inf·0 = NaN (BRDF denominators `4·NdotL·NdotV`) |
| fp16 overflow > 65504 | Inf (bright lights in half-precision buffers) |
| uninitialised variables / out-of-range texture reads | garbage incl. NaN |

## 2. Make them visible
```glsl
vec3 c = shade();
if (any(isnan(c)) || any(isinf(c))) c = vec3(1.0, 0.0, 1.0);   // magenta debug override
```
Put this in a debug permutation at the end of each pass (lighting, post, TAA) to find the first
pass producing them. RenderDoc: pixel history on an affected pixel, then debug the shader at that
pixel; Nsight/PIX have similar pixel history.

## 3. Why they spread
NaN compares false with everything, survives blending, and propagates through filters:
- TAA history: one NaN pixel contaminates neighbours via the resolve kernel and stays forever.
- Bloom/blur downsample: a NaN becomes a growing black square.
Sanitise inputs to temporal and blur passes in release builds:
`c = (any(isnan(c)) || any(isinf(c))) ? vec3(0) : c;` — or `max(c, 0.0)` doesn't work (NaN-aware
behaviour of max varies) — use explicit checks.

## 4. Defensive math
```glsl
vec3 safeNormalize(vec3 v) { float l2 = dot(v, v); return l2 > 1e-12 ? v * inversesqrt(l2) : vec3(0, 0, 1); }
float NdotL = max(dot(N, L), 0.0);   float NdotV = max(dot(N, V), 1e-4);   // avoid 0 denominators
float a = max(roughness * roughness, 1e-3);                             // GGX alpha floor
float x = clamp(dotValue, -1.0, 1.0);  float ang = acos(x);
```
Clamp emissive/HDR values stored in fp16 targets (`min(c, 65000.0)`).

## Gotchas
- Fast-math compiler flags (some drivers) can optimise away `isnan` checks — verify in ISA or
  use bit tricks (`(floatBitsToUint(x) & 0x7fffffff) > 0x7f800000u`).
- Different GPUs produce NaN in different places (denormal flushing, fast `rsqrt`) — a pass that's
  clean on one vendor can fail on another.

## Verify
- [ ] Debug NaN overlay enabled in CI screenshot tests across vendors shows no magenta.
- [ ] Temporal and blur passes sanitise inputs; a deliberately injected NaN doesn't persist.
- [ ] Known-risky functions use safe variants (grep normalize/pow/acos in hot shaders).
