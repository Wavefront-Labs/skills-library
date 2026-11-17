---
id: computing-software.computer-graphics-engineering.gpu-optimisation.shader-loop-unrolling-and-constant-folding
name: shader-loop-unrolling-and-constant-folding
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, shader-optimisation, loop-unrolling, constant-folding, specialization-constants, hlsl-attributes, shader-compiler]
level: practitioner
status: draft
description: "Control loop unrolling and constant folding in shaders: [unroll]/[loop] attributes, compile-time constant loop bounds, specialisation constants and checking the generated ISA."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-for", "https://docs.vulkan.org/spec/latest/chapters/pipelines.html#pipelines-specialization-constants", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/ext/GL_EXT_control_flow_attributes.txt"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loop unrolling and constant folding

## 1. Why
Unrolled loops remove counter/branch overhead, let the compiler schedule fetches early, and turn
array indexing into registers (dynamic indexing into local arrays may spill to scratch memory).
Costs: code size, instruction cache pressure, and registers (lower occupancy).

## 2. Attributes
HLSL:
```hlsl
[unroll] for (int i = 0; i < 8; i++) { ... }      // force (needs constant trip count)
[unroll(4)] for (...)                            // partial
[loop] for (int i = 0; i < n; i++) { ... }       // keep as a loop
```
GLSL with `GL_EXT_control_flow_attributes`:
```glsl
#extension GL_EXT_control_flow_attributes : require
[[unroll]] for (int i = 0; i < 8; i++) { }
[[dont_unroll]] for (...) { }
```
MSL: `#pragma unroll` inside the function body (clang).

## 3. Make bounds constant
- Loop count from a `#define` or a `const int` folds; from a uniform it doesn't.
- **Specialisation constants** (Vulkan `layout(constant_id = 0) const int KERNEL = 9;`, Metal
  function constants, D3D: compile-time defines) give constant folding without separate source
  variants; the driver folds at pipeline creation.
- Dead branches on constant `bool`s disappear entirely.

## 4. Dynamic array indexing
`float w[9]; ... w[i]` with non-constant `i` may go to scratch (slow) on some compilers. Unroll so
`i` becomes constant, or use constant arrays in a uniform/constant buffer.

## 5. Check the result
- DXC: `-Fc out.asm` (DXIL), then RGA/vendor tools for ISA.
- Vulkan: `VK_KHR_pipeline_executable_properties` gives instruction counts and register usage at
  runtime; RGA and Mali OC offline.
- Compare register count and scratch usage before/after.

## Gotchas
- Forcing `[unroll]` on long loops with texture fetches can explode register pressure and lower
  occupancy, making the shader slower overall.
- Loops containing derivative operations must stay uniform; unrolling doesn't fix non-uniform
  derivative use.
- Some drivers ignore hints; the ISA is the truth.

## Verify
- [ ] ISA shows the intended unroll and no scratch spills.
- [ ] GPU time measured, not just instruction count.
