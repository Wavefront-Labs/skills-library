---
id: computing-software.computer-graphics-engineering.opengl.vulkan-compute-to-graphics-barriers
name: vulkan-compute-to-graphics-barriers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-synchronization, compute-to-graphics-barrier, storage-image-barrier, compute-vertex-sync]
level: advanced
status: docs-checked
description: "Barrier recipes for Vulkan compute feeding graphics: SSBO to vertex input, indirect args, storage image to sampling, and graphics output into compute."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/renderpass.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute <-> graphics barrier recipes (sync2)

Format: `srcStage / srcAccess -> dstStage / dstAccess` (+ layout).

| Producer -> consumer | Barrier |
|---|---|
| CS writes SSBO -> VS reads it as **vertex buffer** | `COMPUTE_SHADER / SHADER_STORAGE_WRITE -> VERTEX_ATTRIBUTE_INPUT / VERTEX_ATTRIBUTE_READ` |
| CS writes SSBO -> **index buffer** | `... -> INDEX_INPUT / INDEX_READ` |
| CS writes SSBO -> VS reads as SSBO (vertex pulling) | `... -> VERTEX_SHADER / SHADER_STORAGE_READ` |
| CS writes **indirect args/count** | `... -> DRAW_INDIRECT / INDIRECT_COMMAND_READ` |
| CS writes UBO data | `... -> VERTEX_SHADER|FRAGMENT_SHADER / UNIFORM_READ` |
| CS writes storage image -> FS samples it | `COMPUTE_SHADER / SHADER_STORAGE_WRITE -> FRAGMENT_SHADER / SHADER_SAMPLED_READ`, layout `GENERAL -> SHADER_READ_ONLY_OPTIMAL` |
| Render target -> CS reads it (post-process) | `COLOR_ATTACHMENT_OUTPUT / COLOR_ATTACHMENT_WRITE -> COMPUTE_SHADER / SHADER_SAMPLED_READ`, `COLOR_ATTACHMENT_OPTIMAL -> SHADER_READ_ONLY_OPTIMAL` |
| Depth buffer -> CS builds Hi-Z | `EARLY_FRAGMENT_TESTS | LATE_FRAGMENT_TESTS / DEPTH_STENCIL_ATTACHMENT_WRITE -> COMPUTE_SHADER / SHADER_SAMPLED_READ`, `DEPTH_ATTACHMENT_OPTIMAL -> DEPTH_READ_ONLY_OPTIMAL` |
| CS writes storage image -> CS next dispatch reads it | `COMPUTE_SHADER / SHADER_STORAGE_WRITE -> COMPUTE_SHADER / SHADER_STORAGE_READ` (layout stays `GENERAL`) |
| FS samples texture -> CS overwrites it next frame (WAR) | `FRAGMENT_SHADER / NONE -> COMPUTE_SHADER / SHADER_STORAGE_WRITE` |

## Recording example
```c
VkBufferMemoryBarrier2 bufs[2] = {
  { VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER_2, NULL,
    VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT, VK_ACCESS_2_SHADER_STORAGE_WRITE_BIT,
    VK_PIPELINE_STAGE_2_VERTEX_ATTRIBUTE_INPUT_BIT, VK_ACCESS_2_VERTEX_ATTRIBUTE_READ_BIT,
    VK_QUEUE_FAMILY_IGNORED, VK_QUEUE_FAMILY_IGNORED, particleBuf, 0, VK_WHOLE_SIZE },
  { VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER_2, NULL,
    VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT, VK_ACCESS_2_SHADER_STORAGE_WRITE_BIT,
    VK_PIPELINE_STAGE_2_DRAW_INDIRECT_BIT, VK_ACCESS_2_INDIRECT_COMMAND_READ_BIT,
    VK_QUEUE_FAMILY_IGNORED, VK_QUEUE_FAMILY_IGNORED, argsBuf, 0, VK_WHOLE_SIZE } };
VkDependencyInfo d = { VK_STRUCTURE_TYPE_DEPENDENCY_INFO };
d.bufferMemoryBarrierCount = 2; d.pBufferMemoryBarriers = bufs;
vkCmdPipelineBarrier2(cmd, &d);
```
Batch all barriers between two passes into one `vkCmdPipelineBarrier2` call. A single global
`VkMemoryBarrier2` covers all buffers and images in the dependency without naming them; image barriers
are needed for layout changes and queue family ownership transfers.

## Async compute queue
If compute runs on a different queue: semaphore between queues (wait stage = consumer stage),
plus queue family ownership transfer for `EXCLUSIVE` resources, or `CONCURRENT` sharing.

## Gotchas
- `VK_ACCESS_2_SHADER_READ_BIT` is defined as the logical OR of the more specific shader read bits
  (`SHADER_SAMPLED_READ`, `SHADER_STORAGE_READ`, ...); prefer the specific bit that matches the descriptor type.
- Vertex input reads are not "shader reads": the spec defines `VERTEX_ATTRIBUTE_READ` (stage
  `VERTEX_ATTRIBUTE_INPUT`) as read access to a vertex buffer in a drawing command, so a barrier
  to `VERTEX_SHADER/SHADER_READ` does not cover a vertex buffer fetch.

## Verify
- [ ] Sync validation clean; no particle flicker on AMD/NVIDIA/Intel/Mali test devices.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23), `chapters/synchronization.adoc`. All stage and access bit names in the table and example exist in vk.xml. Confirmed: `INDEX_READ` occurs in `INDEX_INPUT`, `VERTEX_ATTRIBUTE_READ` in `VERTEX_ATTRIBUTE_INPUT`, `INDIRECT_COMMAND_READ` for indirect command data; `DEPTH_STENCIL_ATTACHMENT_WRITE` occurs in either `EARLY_FRAGMENT_TESTS` or `LATE_FRAGMENT_TESTS` (the table previously listed only the late stage); `SHADER_READ` is defined as the OR of the specific shader read bits. Removed the claim that the vertex-buffer hazard shows only on some GPUs.

Method: documentation only; no commands were run.
