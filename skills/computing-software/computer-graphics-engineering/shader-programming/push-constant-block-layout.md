---
id: computing-software.computer-graphics-engineering.shader-programming.push-constant-block-layout
name: push-constant-block-layout
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-interfaces, push-constant-layout, push-constants, root-constants, vulkan, std430, pipeline-layout]
level: practitioner
status: docs-checked
description: "Lay out push constant blocks correctly: 128-byte minimum limit, offset/stage ranges, std430-style packing, HLSL vk::push_constant and D3D12 root constants equivalents."
sources: ["https://docs.vulkan.org/spec/latest/chapters/descriptorsets.html#descriptorsets-push-constants", "https://docs.vulkan.org/spec/latest/chapters/interfaces.html", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/SPIR-V.rst", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/root-signature-limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Push constant block layout

## 1. Limits
- `maxPushConstantsSize` has a required minimum of **128 bytes** (256 bytes for Vulkan 1.4 devices). Design for 128 unless
  you check the limit.
- D3D12 root constants share the 64-DWORD (256-byte) root signature budget with everything else (descriptor tables
  cost 1 DWORD, root constants 1 DWORD each, root descriptors 2).

## 2. Declaring
```glsl
layout(push_constant) uniform PC {
    mat4  model;        // offset 0,  64 bytes
    uint  materialIdx;  // offset 64
    float time;         // offset 68
    vec2  pad;          // offset 72 (explicit, keeps CPU struct obvious)
} pc;
```
Push constant blocks must obey the base-alignment rules that GLSL std430 satisfies (vec3 aligns to 16, scalars to 4,
arrays of scalars stride 4), and there may be only one push constant block statically used per entry point. With
`scalarBlockLayout` enabled (`-fvk-use-scalar-layout` in DXC) you can drop vec3 padding.

HLSL via DXC:
```hlsl
struct PC { float4x4 model; uint materialIdx; float time; };
[[vk::push_constant]] PC pc;          // Vulkan
// D3D12: ConstantBuffer<PC> pc : register(b0); with root constants of 18 DWORDs in the root signature
```
Mark `row_major` or transpose on the CPU consistently (DXC `-Zpc` packs matrices column-major).

## 3. Pipeline layout ranges
```c
VkPushConstantRange r = { VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT, 0, sizeof(PC) };
vkCmdPushConstants(cmd, layout, r.stageFlags, 0, sizeof(PC), &pc);
```
- `stageFlags` in `vkCmdPushConstants` must include every stage flag of the push constant ranges that overlap the
  updated bytes.
- Per-stage ranges let VS use bytes 0-63 and FS 64-79; each stage block then declares members at
  the matching `layout(offset = 64)`.
- The bound pipeline's layout must be compatible with the layouts used to set the push constants it reads; binding an
  incompatible layout does not disturb the values, but re-push before drawing with it.

## 4. Matching the CPU struct
```cpp
struct alignas(16) PC { glm::mat4 model; uint32_t materialIdx; float time; float pad[2]; };
static_assert(sizeof(PC) <= 128);
static_assert(offsetof(PC, time) == 68);
```
Generate the struct from shader reflection (SPIRV-Reflect `spvReflectEnumeratePushConstantBlocks`)
to avoid drift.

## Gotchas
- Using push constants for large per-draw data can exceed the limit; put an index in push
  constants and fetch the rest from a storage buffer.
- Each statically used block member must lie inside the `VkPushConstantRange` of every entry point that uses it,
  with matching stage flags, and within `[0, maxPushConstantsSize)`.

## Verify
- [ ] `static_assert` offsets against reflection output.
- [ ] Block size is within the minimum 128 bytes, or the device limit is queried.

## Checked

Checked 2026-10-26 against Vulkan-Docs main (2026-10-23: interfaces, descriptorsets, limits chapters), DXC docs/SPIR-V.rst, SPIRV-Reflect header, Microsoft root signature limits page. Confirmed: `maxPushConstantsSize` minimums (128, 256 for 1.4); one push constant block per entry point; member offsets inside the `VkPushConstantRange` and below the limit; pipeline-layout compatibility rule for push constants; `vkCmdPushConstants` stage-flag rule; `[[vk::push_constant]]` and `-fvk-use-scalar-layout`; `spvReflectEnumeratePushConstantBlocks`; D3D12 64-DWORD root signature limit and DWORD costs. Corrected: 1.4 minimum, removed unconfirmed 'most desktop GPUs give 256' and the claim that push constants are lost on incompatible bind.

Method: documentation only; no commands were run.
