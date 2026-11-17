---
id: computing-software.computer-graphics-engineering.shader-programming.buffer-layout-rules-across-apis
name: buffer-layout-rules-across-apis
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-interfaces, buffer-layout, scalar-block-layout, std140, std430, cbuffer-packing]
level: advanced
status: docs-checked
description: "Match CPU structs to GPU buffer layouts across std140, std430, scalar block layout, HLSL cbuffer packing, Metal and WGSL, and test them automatically."
sources: ["https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#interfaces-resources-layout", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-packing-rules", "https://www.w3.org/TR/WGSL/#memory-layouts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Buffer layout rules across APIs

## 1. Rules table
| Layout | vec3 | float array stride | struct align | Notes |
|---|---|---|---|---|
| std140 (GL/Vulkan UBO) | 16 B align | 16 B | round up to 16 | Wasteful but universal |
| std430 (SSBO, Vulkan push constants) | 16 B align | 4 B | max member align | vec3 still 16-aligned |
| Vulkan scalar (`VK_EXT_scalar_block_layout`, core 1.2) | 4 B align | 4 B | max scalar align | Matches C packing |
| HLSL cbuffer | packs into 4-component registers; a variable never crosses a 16 B boundary | every array element starts a new 16 B vector | structs start on a new vector | `float3` + `float` share a register |
| WGSL uniform | vec3 aligns to 16 | array stride must be a multiple of 16 | | see the WGSL memory layout section for storage buffers |
| Metal | see the data-type alignment table in the Metal Shading Language Specification | | | |

## 2. Enable scalar layout (Vulkan)
```glsl
#extension GL_EXT_scalar_block_layout : require
layout(scalar, binding = 0) buffer Verts { vec3 pos[]; };
```
Enable `scalarBlockLayout` in `VkPhysicalDeviceVulkan12Features`. DXC: `-fvk-use-scalar-layout`.

## 3. Defensive habits
- Use `vec4` / explicit padding members instead of `vec3` in shared structs.
- Put matrices and vec4s first, scalars last.
- `static_assert(offsetof(Light, color) == 16)` and `sizeof` checks in C++ from reflection data
  (SPIRV-Cross / DXC reflection) in a unit test.
- Matrix majorness: transpose on upload or use `row_major` consistently (DXC `-Zpc` packs column-major).

## Gotchas
- Use `uint32_t` for flags in shared structs rather than C++ `bool`.
- std140 arrays of `float` waste 12 bytes per element; pack into `vec4[N/4]`.
- Mismatches often show as "half the lights wrong" rather than garbage; test with unique values.

## Verify
- [ ] Reflection-generated offsets match CPU offsets for every shared struct (CI test).

## Checked

Checked 2026-10-26 against Vulkan-Docs interfaces chapter and features chapter (main, 2026-10-23), WGSL spec (gpuweb main), Microsoft HLSL packing rules page, DXC docs. Confirmed: std140/std430 correspondence to the Vulkan base/extended alignment rules; scalar block layout (feature `scalarBlockLayout`, core 1.2) and DXC `-fvk-use-scalar-layout`; HLSL cbuffer packing (no straddling of 16-byte boundaries, array elements in their own vectors, structs start on a new vector); WGSL vec3 alignment 16 and uniform array stride multiple of 16. Removed as unconfirmed: HLSL StructuredBuffer packing row, Metal float3/packed_float3 sizes (Metal specification not readable here; the row now points to it), `bool` size claim.

Method: documentation only; no commands were run.
