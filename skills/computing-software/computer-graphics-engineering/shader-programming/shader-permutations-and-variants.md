---
id: computing-software.computer-graphics-engineering.shader-programming.shader-permutations-and-variants
name: shader-permutations-and-variants
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-toolchain, shader-permutations, shader-variants, uber-shaders, variant-stripping]
level: advanced
status: docs-checked
description: "Manage shader permutations: keyword/define design, combinatorial explosion, stripping unused variants, uber-shaders vs specialisation, and caching compiled variants."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#pipelines-specialization-constants", "https://therealmjp.github.io/posts/shader-permutations-part1/", "https://therealmjp.github.io/posts/shader-permutations-part2/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader permutations and variants

## 1. Where they come from
Each boolean `#define` doubles variants: 10 independent features = 1024 shaders per pass per
platform. Compile time, disk size, PSO creation hitches and memory all scale with it.

## 2. Options, cheapest to most variants
| Technique | Cost |
|---|---|
| Dynamic branch on a uniform (`if (cb.useNormalMap)`) | One shader; all invocations take the same path, usually cheap but still measure |
| Specialisation constants (Vulkan GLSL `layout(constant_id = N) const ...`, `VkSpecializationInfo`) | One source; values are set at pipeline creation |
| Static `#define` permutations | Fastest code, most variants |
Rule: only make a feature a static permutation when the dynamic version costs registers or
measurably slows the shader (texture fetches you cannot skip, big loops).

## 3. Keep the set small
- Group mutually exclusive options into one enum keyword (`LIGHTING_MODEL=0..3`) instead of
  booleans.
- Generate variants from **materials actually used**: scan content at build time and compile only
  referenced combinations (stripping).
- Log misses at runtime (`variant X requested but not built`) and fall back to a superset variant.

## 4. Build and cache
- Hash (source + defines + compiler version + flags) as the cache key; distributed or
  incremental compile (DXC/glslang in a job system).
- Ship a pipeline cache / PSO library and pre-warm on load screens.
- Record PSOs seen during QA playthroughs to build the precompile list.

## Gotchas
- Defines that only change constants (e.g. kernel radius) can be uniforms or specialisation constants.
- Register pressure: an uber-shader can need registers for its worst path, lowering occupancy. Measure with ISA output.
- Variant count multiplies across passes (depth, shadow, forward, gbuffer).

## Verify
- [ ] Total variant count tracked in CI; runtime miss log empty after QA pass.

## Checked

Checked 2026-10-26 against GLSL 4.60 specification (specialization constants, section 12.2.1) and Vulkan-Docs pipelines chapter (main, 2026-10-23). Confirmed: specialisation constants are declared with `layout(constant_id = N) const` and can be set later by the client API (default value retained if never changed); Vulkan sets them through `VkSpecializationInfo` at pipeline creation. The variant-count arithmetic (2^N) is computed. Removed as unconfirmed: Metal function constants, the 'uniform branches are cheap on modern GPUs' assertion and the Unity stripping page (not readable).

Method: documentation only; no commands were run.
