---
id: computing-software.computer-graphics-engineering.shader-programming.shader-precision-qualifiers-mediump
name: shader-precision-qualifiers-mediump
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-interfaces, precision-qualifiers, mediump, highp, lowp, glsl-es, webgl, mobile-gpu, relaxedprecision, banding]
level: practitioner
status: docs-checked
description: "Use GLSL ES precision qualifiers safely on mobile and WebGL: what mediump really guarantees, which values must stay highp, texture coordinate and time precision bugs."
sources: ["https://registry.khronos.org/OpenGL/specs/es/3.0/GLSL_ES_Specification_3.00.pdf", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/webgl/specs/latest/1.0/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader precision qualifiers (mediump on mobile)

**Goal:** use 16-bit arithmetic where it's free speed on mobile GPUs, without the
blocky textures, jittering vertices and frozen animations that wrong precision causes.

## 1. What the qualifiers mean
| qualifier | guaranteed minimum (float) | typical hardware |
|---|---|---|
| `highp` | as IEEE-754 single (relative precision 2^-24) | fp32 |
| `mediump` | range (-2^14, 2^14), relative precision 2^-10 (~3 decimal digits) | fp16 on many mobile GPUs; fp32 elsewhere |
| `lowp` | range (-2, 2), absolute precision 2^-8 | fp16 or fixed point |
These are GLSL ES 3.00 minimums; an implementation may exceed them, so code that works on a device that uses fp32 for
mediump can break on one that uses fp16. Vulkan GLSL respects `mediump`/`lowp` in all versions (SPIR-V
`RelaxedPrecision`).

## 2. Defaults
GLSL ES fragment shaders have **no default float precision** (default int is mediump): declare one.
```glsl
#version 300 es
precision highp float;      // safe default; then opt into mediump per variable
precision mediump sampler2D;
```
Vertex shaders predeclare `precision highp float;` and `highp int`.

## 3. Must stay highp
- **Positions** (world/view/clip) and matrices — mediump world positions jitter visibly
  beyond a few hundred units.
- **Texture coordinates** for large textures or tiling: with 2^-10 relative precision a 2048-texel texture
  has no bits to spare; tiled UVs (uv * 100) lose sub-texel precision → blocky.
- **Time** accumulators: with 2^-10 relative precision, once `time` reaches a few thousand seconds the step between
  representable values is whole seconds, so animations step or freeze. Wrap time on the CPU and keep highp.
- Depth reconstruction, shadow map comparisons, large-range noise inputs.

## 4. Good mediump candidates
Colours, normalised normals/vectors for lighting, BRDF terms after normalisation,
blending factors, tone mapping — the majority of fragment math.

## 5. Precision in WebGL
Query: `gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_FLOAT)` returns a `WebGLShaderPrecisionFormat`
(rangeMin, rangeMax, precision) so you can check what each precision gives on the device.

## Gotchas
- Intermediate overflow: the guaranteed mediump range is below 2^14, so `dot(v, v)` of an unnormalised vector of
  length above 128 can overflow; on fp16 hardware (max 65504) the limit is about 255 → Inf/NaN → black pixels.
- Operations are performed at the precision of the operands or higher; assigning to a mediump
  variable stores the lower precision.
- Implementations honour mediump differently — test on more than one GPU vendor.

## Verify
- [ ] Shader tested on at least two mobile GPU vendors (or with a fp16-emulating debug path).
- [ ] 1-hour soak test: time-driven animations don't stutter or freeze.
- [ ] Large tiled textures stay sharp at oblique views on device.

## Checked

Checked 2026-10-26 against GLSL ES 3.00 specification (OpenGL Registry), GLSL 4.60 specification, WebGL 1.0 specification (KhronosGroup/WebGL). Confirmed: the required range/precision table for highp, mediump and lowp (section 4.5.1); predeclared default precision statements for the vertex and fragment languages (no default float precision in fragment shaders; default int mediump in fragment); Vulkan GLSL respects precision qualifiers for all versions; `getShaderPrecisionFormat` exists in WebGL. Removed as unconfirmed: the Arm savings claim, the three.js remark, the 'old mobile GPUs lacked highp' remark and the 30-minute figure (replaced by the 2^-10 arithmetic). Corrected: `dot(v,v)` overflow threshold.

Method: documentation only; no commands were run.
