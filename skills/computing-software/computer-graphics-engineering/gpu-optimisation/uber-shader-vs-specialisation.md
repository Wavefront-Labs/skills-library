---
id: computing-software.computer-graphics-engineering.gpu-optimisation.uber-shader-vs-specialisation
name: uber-shader-vs-specialisation
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, shader-optimisation, uber-shader, shader-variants, specialization-constants, shader-permutations, pso-compilation]
level: advanced
status: draft
description: "Choose uber-shaders vs specialised variants: uniform branch cost, worst-case register pressure, permutation explosion, specialisation constants and async fallback."
sources: ["https://dolphin-emu.org/blog/2017/07/30/ubershaders/", "https://docs.vulkan.org/spec/latest/chapters/pipelines.html#pipelines-specialization-constants", "https://therealmjp.github.io/posts/shader-permutations-part1/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Uber-shader vs specialisation trade-offs

## 1. The spectrum
| Approach | Runtime cost | Build/load cost |
|---|---|---|
| One uber-shader with uniform branches | branches + worst-case registers | 1 PSO, instant |
| Specialisation constants | near-specialised code | PSO per combination, compile at runtime |
| Preprocessor permutations | optimal code | N binaries offline, N PSOs |

## 2. Uber-shader costs
- **Uniform branches** (same value for the whole draw) are cheap on modern GPUs (scalar branch, no
  divergence), but:
- **Register allocation is for the worst path**: one expensive feature anywhere lowers occupancy
  for every material using the shader.
- Code size and instruction cache misses; fewer compile-time folds.
MJP's permutation series covers the analysis in depth.

## 3. Permutation costs
Every boolean feature doubles variants. 10 features = 1024 variants x passes x platforms. Leads to
long builds, large packages and PSO compile hitches at runtime.

## 4. Hybrid strategies
- **Async specialisation with uber fallback** (Dolphin's ubershaders): draw with the uber-shader
  while the specialised PSO compiles in the background; swap when ready. Eliminates hitches at a
  temporary GPU cost.
- **Group features by cost**: make cheap features dynamic branches, expensive/register-heavy
  features (e.g. parallax occlusion, SSS) static permutations.
- **Specialisation constants** keep one SPIR-V module but get folded code: good middle ground on
  Vulkan/Metal (function constants).
- Track which variants actually ship (material usage scan) and only build those.

## 5. Measuring
- Compare occupancy/VGPR counts of uber vs specialised in RGA/Nsight.
- Count runtime PSO creations and their time in a playthrough.

## Gotchas
- Driver PSO compilation still happens per specialisation; specialisation constants don't remove
  hitches, only offline build size.
- Dynamic branches on per-pixel data (not uniform) diverge; that's a different, costlier case.

## Verify
- [ ] Occupancy of the common path not capped by rarely used features.
- [ ] No first-use hitches (PSO pre-warm or async fallback works).
