---
id: computing-software.computer-graphics-engineering.shader-programming.shader-branch-divergence
name: shader-branch-divergence
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-optimisation, shader-optimization, divergence, uniform-control-flow, simd, wave-divergence, branching, dynamically-uniform, early-exit]
level: advanced
status: draft
description: "Reason about shader branches on SIMD GPUs: when branches are free (uniform), when divergence costs both paths, structuring code for coherence, and measuring it in profilers."
sources: ["https://developer.nvidia.com/blog/using-cuda-warp-level-primitives/", "https://gpuopen.com/learn/rdna-performance-guide/", "https://developer.arm.com/documentation/101897/latest/Shader-code/Uniform-control-flow", "https://www.khronos.org/opengl/wiki/Core_Language_(GLSL)#Dynamically_uniform_expression"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shader branch divergence

**Goal:** use branches where they save work and avoid them where they double it, based on
how GPUs actually execute (32/64-lane SIMD waves).

## 1. The model
A wave (warp) of 32–64 threads shares one instruction pointer. For `if (c)`:
- All lanes agree (**uniform** or coherent) → only the taken path runs. Branch is cheap.
- Lanes disagree (**divergent**) → both paths execute with lanes masked. Cost = sum of both.
Pixel shaders run 2x2 quads packed into waves, so coherence is spatial: adjacent pixels
taking the same path is what matters.

## 2. Branches that pay off
- Uniform conditions: material flags, quality settings, light counts from a constant buffer
  → `if` beats computing both and lerping.
- Spatially coherent early-outs: `if (NdotL <= 0) return ambient;` — large contiguous regions
  agree; skipping shadow/specular math is a net win.
- Skipping expensive texture fetches when the weight is ~0 (triplanar planes, decals, layers)
  if regions are coherent.
- Tiled/clustered light loops where neighbouring pixels share light lists.

## 3. Branches that hurt
- Per-pixel noise-driven or hash-driven choices (dithered) → near-random divergence.
- Short both-sides branches: just compute both and `mix`/`select` (compiler often does this).
- Loops with per-lane trip counts (ray marching, POM): the wave runs until the slowest lane
  finishes. Cap iterations; sort or bin work in compute.

## 4. Help the compiler and hardware
- Make conditions provably uniform: values from uniforms/push constants, or
  `WaveReadLaneFirst`/subgroupBroadcastFirst to scalarise.
- Hoist texture sampling with implicit derivatives **out** of divergent branches (derivatives
  are undefined in non-uniform control flow) — or use `textureLod/textureGrad`.
- `[branch]` / `[flatten]` attributes (HLSL) to force behaviour when the compiler guesses wrong.
- In compute, group similar work: sort by material/ray direction, use wave-level ballot to
  process uniform subsets.

## 5. Measure
- Nsight Graphics: "Warp divergence"/"thread utilisation" metrics; RGP: instruction timing
  and active lanes; Mali offline compiler: shortest vs longest path cycles.
- A/B: replace the condition with a constant and compare GPU time to bound the cost.

## Gotchas
- Old "branches are slow on GPUs" advice dates from GPUs without real branching; modern GPUs
  branch cheaply when coherent.
- Divergence inside a loop that contains barriers (compute) is invalid, not just slow.

## Verify
- [ ] Profiler shows high lane utilisation in hot shaders after changes.
- [ ] Each early-out branch justified by an A/B GPU timing.
- [ ] No implicit-derivative texture samples inside divergent branches (lint/grep).
