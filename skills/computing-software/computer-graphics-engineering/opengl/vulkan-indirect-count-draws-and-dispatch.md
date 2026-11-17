---
id: computing-software.computer-graphics-engineering.opengl.vulkan-indirect-count-draws-and-dispatch
name: vulkan-indirect-count-draws-and-dispatch
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, command-buffers, vkcmddrawindexedindirectcount, draw-indirect-count, vkcmddispatchindirect]
level: advanced
status: docs-checked
description: "Drive Vulkan draws from GPU-written buffers: vkCmdDrawIndexedIndirectCount, dispatch indirect, struct layouts, barriers and drawIndirectFirstInstance."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/drawing.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indirect count draws and indirect dispatch

## Command structs
```c
typedef struct VkDrawIndexedIndirectCommand {   // 20 bytes
    uint32_t indexCount, instanceCount, firstIndex; int32_t vertexOffset; uint32_t firstInstance;
} VkDrawIndexedIndirectCommand;
typedef struct VkDispatchIndirectCommand { uint32_t x, y, z; } VkDispatchIndirectCommand;
```
Mirror them in GLSL (`std430`, 20-byte stride) and let a culling compute shader write them.

## Recording
```c
// culling pass wrote cmds[] and drawCount
VkBufferMemoryBarrier2 b = { VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER_2 };
b.srcStageMask  = VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT;
b.srcAccessMask = VK_ACCESS_2_SHADER_STORAGE_WRITE_BIT;
b.dstStageMask  = VK_PIPELINE_STAGE_2_DRAW_INDIRECT_BIT;      // indirect args are read here
b.dstAccessMask = VK_ACCESS_2_INDIRECT_COMMAND_READ_BIT;
b.buffer = indirectBuf; b.size = VK_WHOLE_SIZE;
// (also cover countBuf) -> vkCmdPipelineBarrier2
vkCmdDrawIndexedIndirectCount(cmd, indirectBuf, 0, countBuf, 0, maxDraws,
                              sizeof(VkDrawIndexedIndirectCommand));
```
The GPU reads `count = min(*countBuf, maxDraws)`. Using `VERTEX_SHADER` stage or
`SHADER_READ` access instead of `DRAW_INDIRECT` + `INDIRECT_COMMAND_READ` is the classic missing
barrier: the indirect read is not covered by the dependency.

Dispatch indirect: `vkCmdDispatchIndirect(cmd, argsBuf, offset)`; same barrier, stage
`DRAW_INDIRECT` covers dispatch args too.

## Requirements
- Count variants: core in 1.2 (feature `drawIndirectCount`), else `VK_KHR_draw_indirect_count`.
- `multiDrawIndirect` feature for `drawCount > 1` in plain `vkCmdDrawIndexedIndirect`.
- `drawIndirectFirstInstance` feature to use non-zero `firstInstance` (commonly used to pass a
  per-draw object index); otherwise use `gl_DrawID` (`shaderDrawParameters`, 1.1 feature).
- Buffers need `VK_BUFFER_USAGE_INDIRECT_BUFFER_BIT`; offsets multiple of 4.

## Per-draw data lookup
```glsl
#extension GL_ARB_shader_draw_parameters : require   // or use gl_DrawID in Vulkan GLSL directly
uint obj = gl_InstanceIndex;                          // when firstInstance = object id and instanceCount = 1
// or: uint obj = drawToObject[gl_DrawID];
```

## Gotchas
- `stride` must be >= 20 and a multiple of 4; you can embed extra per-draw data after the command
  by using a larger stride.
- `maxDrawIndirectCount` is at least 2^16-1 when `multiDrawIndirect` is supported and 1 otherwise
  (limits table).
- Reset the count buffer each frame (`vkCmdFillBuffer` + transfer->compute barrier).

## Verify
- [ ] A capture tool shows the expected number of draws executed; no flicker.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: `VkDrawIndexedIndirectCommand` has five 32-bit members (20 bytes); the executed draw count is the minimum of the count buffer value and `maxDrawCount`; stride must be a multiple of 4 and at least the command size (VUID-vkCmdDrawIndexedIndirectCount-stride-03142); `firstInstance` must be 0 without `drawIndirectFirstInstance`.
- Confirmed: `VK_PIPELINE_STAGE_2_DRAW_INDIRECT_BIT` is the stage where indirect command parameters are consumed; `drawIndirectCount` is in `VkPhysicalDeviceVulkan12Features` (`VK_KHR_draw_indirect_count` promotedto 1.2); limit table: `maxDrawIndirectCount` 1 without and 2^16-1 with `multiDrawIndirect`.
- Removed the vendor-specific flicker anecdote and tool names (no source).

Method: documentation only; no commands were run.
