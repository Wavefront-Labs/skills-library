---
id: computing-software.computer-graphics-engineering.opengl.vulkan-specialization-constants-and-dynamic-state
name: vulkan-specialization-constants-and-dynamic-state
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-pipelines, specialization-constants, dynamic-state, extended-dynamic-state, vkspecializationinfo, constant-id, pipeline-permutations]
level: advanced
status: docs-checked
description: "Cut Vulkan pipeline permutations: bake compile-time variants with specialization constants and move per-draw state into dynamic and extended dynamic state."
sources: ["https://docs.vulkan.org/spec/latest/chapters/pipelines.html", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/pipelines.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/versions.adoc", "https://github.com/KhronosGroup/Vulkan-Guide/blob/main/chapters/dynamic_state.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan specialization constants and dynamic state

**Goal:** the smallest number of pipelines that still gives the compiler constants to
optimise with, and state that varies per draw set by commands, not new pipelines.

## 1. Specialization constants
```glsl
layout(constant_id = 0) const int  LIGHT_COUNT   = 4;
layout(constant_id = 1) const bool USE_NORMAL_MAP = true;
layout(local_size_x_id = 2) in;                     // compute workgroup size from a constant
```
```cpp
struct Spec { int32_t lights; VkBool32 normalMap; uint32_t wg; } s{8, VK_TRUE, 64};
VkSpecializationMapEntry e[] = {{0, offsetof(Spec,lights), 4}, {1, offsetof(Spec,normalMap), 4},
                                {2, offsetof(Spec,wg), 4}};
VkSpecializationInfo si{3, e, sizeof s, &s};
stage.pSpecializationInfo = &si;                    // per shader stage
```
- The value becomes a constant when the pipeline is created, so the compiler can optimise with it.
- Same SPIR-V, many variants: avoids an offline permutation explosion. Each value combo is
  still a separate pipeline compile — use for things that are fixed per material/quality level.
- Bools are 32-bit (`VkBool32`) in the data block.

## 2. Dynamic state
Core 1.0 basics every renderer should use: `VIEWPORT`, `SCISSOR` (no pipeline rebuild on resize).
Extended dynamic state (core 1.3):
```cpp
VkDynamicState ds[] = { VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR,
  VK_DYNAMIC_STATE_CULL_MODE, VK_DYNAMIC_STATE_FRONT_FACE, VK_DYNAMIC_STATE_PRIMITIVE_TOPOLOGY,
  VK_DYNAMIC_STATE_DEPTH_TEST_ENABLE, VK_DYNAMIC_STATE_DEPTH_WRITE_ENABLE,
  VK_DYNAMIC_STATE_DEPTH_COMPARE_OP, VK_DYNAMIC_STATE_STENCIL_OP, VK_DYNAMIC_STATE_DEPTH_BIAS };
// record:
vkCmdSetCullMode(cmd, VK_CULL_MODE_NONE);          // double-sided material
vkCmdSetDepthCompareOp(cmd, VK_COMPARE_OP_GREATER_OR_EQUAL); // reversed-Z
```
`VK_EXT_extended_dynamic_state3` adds blend, polygon mode, sample count etc. (support varies).

## 3. Choosing
| varies | mechanism |
|---|---|
| per frame/draw, cheap state (viewport, cull, depth test, bias) | dynamic state |
| per material, affects shader code paths | specialization constant |
| per draw data (matrices, ids) | push constants / buffers |
| truly different shaders | separate pipeline |

## Gotchas
- Dynamic state declared in the pipeline **must** be set before draw, every command buffer;
  missing it is a validation error and undefined on hardware.
- A map entry whose `constantID` the shader does not use has no effect, and a constant without an
  entry keeps its default value.

## Verify
- [ ] Pipeline count logged at load matches the expected permutation set.
- [ ] Resizing and toggling culling/depth modes never creates a pipeline at runtime.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Boolean specialization constants use `VkBool32` size; unused `constantID` entries do not affect the pipeline; constants without an entry keep their SPIR-V default (pipelines chapter).
- Confirmed: Extended dynamic state 1 is required in 1.3 and extended dynamic state 2 is promoted except patch control points and logic op (versions appendix); `VK_EXT_extended_dynamic_state3` exists as an extension (vk.xml).
- Removed mobile-driver and ISA-inspection remarks (no source found).

Method: documentation only; no commands were run.
