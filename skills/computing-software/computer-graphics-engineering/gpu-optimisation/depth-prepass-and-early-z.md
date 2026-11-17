---
id: computing-software.computer-graphics-engineering.gpu-optimisation.depth-prepass-and-early-z
name: depth-prepass-and-early-z
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, fill-rate, fragment-bound, depth-prepass, early-z, hi-z, front-to-back-sorting, discard, conservative-depth, overdraw, front-to-back, discard-cost]
level: advanced
status: draft
description: "Cut pixel shading cost with early depth testing: what disables early-Z (discard, depth writes, UAVs), front-to-back sorting, when a depth prepass pays off."
sources: ["https://developer.arm.com/documentation/101897/latest/Fragment-shading/Early-ZS-testing", "https://gpuopen.com/learn/understanding-gpu-context-rolls/", "https://www.khronos.org/opengl/wiki/Early_Fragment_Test", "Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 18.4.5, 23.7"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depth prepass and early-Z

**Goal:** expensive pixel shaders run once per visible pixel, not once per covering
triangle (RTR4 §18.4.5, §23.7).

## 1. How early-Z works
GPUs test depth **before** the pixel shader (per-pixel early-Z, plus coarse Hi-Z per tile)
when the result can't be changed by the shader. If the fragment is hidden, the shader is skipped.

## 2. Things that disable or weaken early-Z
- Shader writes depth (`gl_FragDepth`, `SV_Depth`) — use conservative depth instead:
  `layout(depth_greater) out float gl_FragDepth;` / `SV_DepthGreaterEqual` keeps Hi-Z partially working.
- `discard`/`clip`/alpha test with depth writes on: depth can't be written early (test may still
  happen early on some GPUs, but writes are late → later fragments don't benefit).
- Pixel shader writes to UAVs/storage images (side effects): early tests disabled unless forced
  with `[earlydepthstencil]` / `layout(early_fragment_tests) in;` (only if semantically safe).
- Alpha-to-coverage, changing depth compare direction mid-frame (Hi-Z invalidation on some
  hardware), sampling the bound depth buffer.

## 3. Front-to-back sorting (cheap first step)
Sort opaque draws roughly front to back (by distance bucket, inside material/state sort) so
early-Z rejects more. Coarse sorting is enough; big occluders first.

## 4. Depth prepass
Render opaque geometry depth-only first (position-only vertex stream, no pixel shader or a
trivial one), then the main pass with `depthCompare = EQUAL` (or LESS_EQUAL) and depth writes off.
Worth it when:
- pixel shading is expensive and overdraw is high (forward+ with many lights, complex materials);
- you need depth early anyway (SSAO, Hi-Z occlusion culling, contact shadows, light clustering).
Not worth it when geometry cost dominates (dense meshes, mobile vertex-bound) — it doubles
vertex work. **Tile-based mobile GPUs** do hidden surface removal per tile (Mali FPK, PowerVR
HSR, Adreno LRZ) — a prepass is often unnecessary there; profile first.

## 5. Alpha-tested geometry
Do alpha-tested foliage in the prepass with `discard`, then main pass with EQUAL depth test and
**no discard** — the main pass regains full early-Z.

## Gotchas
- EQUAL test requires bit-identical positions in both passes: same vertex shader math
  (`invariant gl_Position;` / `precise`) or z-fighting gaps appear.
- Reversed-Z: use GREATER/GREATER_EQUAL consistently.

## Verify
- [ ] GPU profiler shows pixel shader invocations ≈ screen pixels × small overdraw factor.
- [ ] A/B GPU time with/without prepass on target hardware recorded.
- [ ] No shaders write depth or use discard unintentionally in the main opaque pass.
