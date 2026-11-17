---
id: computing-software.computer-graphics-engineering.opengl.vulkan-secondary-command-buffer-inheritance
name: vulkan-secondary-command-buffer-inheritance
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, command-buffers, command-buffer-inheritance, secondary-command-buffers-dynamic-rendering]
level: advanced
status: docs-checked
description: "Record Vulkan secondary command buffers inside dynamic rendering: VkCommandBufferInheritanceRenderingInfo, RENDER_PASS_CONTINUE, and state inheritance rules."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/cmdbuffers.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/renderpass.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secondary command buffer inheritance with dynamic rendering

Secondaries let worker threads record draws inside one rendering scope that the primary owns.

## Primary
```c
VkRenderingInfo ri = { VK_STRUCTURE_TYPE_RENDERING_INFO };
ri.flags = VK_RENDERING_CONTENTS_SECONDARY_COMMAND_BUFFERS_BIT;   // ONLY vkCmdExecuteCommands inside
ri.renderArea = {{0,0}, extent}; ri.layerCount = 1;
ri.colorAttachmentCount = 1; ri.pColorAttachments = &color; ri.pDepthAttachment = &depth;
vkCmdBeginRendering(primary, &ri);
vkCmdExecuteCommands(primary, workerCount, secondaries);
vkCmdEndRendering(primary);
```
With `CONTENTS_SECONDARY_COMMAND_BUFFERS_BIT` the primary may not record draws itself inside
that scope. To mix, end rendering and begin again with `VK_RENDERING_RESUMING_BIT` /
`SUSPENDING_BIT`.

## Secondary
```c
VkFormat colorFmt = swapFormat;
VkCommandBufferInheritanceRenderingInfo inh = { VK_STRUCTURE_TYPE_COMMAND_BUFFER_INHERITANCE_RENDERING_INFO };
inh.colorAttachmentCount = 1; inh.pColorAttachmentFormats = &colorFmt;
inh.depthAttachmentFormat = VK_FORMAT_D32_SFLOAT;
inh.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;
VkCommandBufferInheritanceInfo ii = { VK_STRUCTURE_TYPE_COMMAND_BUFFER_INHERITANCE_INFO, &inh };
VkCommandBufferBeginInfo bi = { VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO };
bi.flags = VK_COMMAND_BUFFER_USAGE_RENDER_PASS_CONTINUE_BIT | VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;
bi.pInheritanceInfo = &ii;
vkBeginCommandBuffer(secondary, &bi);
// set ALL state you need: pipeline, viewport, scissor, descriptor sets, push constants
vkCmdBindPipeline(...); vkCmdSetViewport(...); vkCmdSetScissor(...);
vkCmdDraw(...);
vkEndCommandBuffer(secondary);
```
Formats, sample count, `colorAttachmentCount` and `flags` (excluding `CONTENTS_SECONDARY_COMMAND_BUFFERS_BIT`) in the inheritance info must match the
primary's rendering info (for example `VUID-vkCmdExecuteCommands-colorAttachmentCount-06027`).

## What is (not) inherited
- **Not inherited:** bound pipelines, descriptor sets, push constants, dynamic state such as
  viewport/scissor. Each secondary starts with undefined state; set everything.
- `VK_NV_inherited_viewport_scissor` lets secondaries inherit viewport/scissor from the primary.
- Queries: active occlusion queries need `occlusionQueryEnable` in inheritance info and the
  `inheritedQueries` feature.

## When to use secondaries
- Parallel recording of one big pass (many thousands of draws). Each thread uses its own
  command pool.
- Not worth it for small passes: each secondary adds recording and execution overhead (measure it). Alternatively record multiple *primaries*
  in parallel and submit them in order, each with its own begin/end rendering using
  suspend/resume.

## Verify
- [ ] Validation clean; GPU capture shows one rendering scope containing all secondaries; CPU recording time scales with threads.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23). Confirmed: `VK_RENDERING_CONTENTS_SECONDARY_COMMAND_BUFFERS_BIT` makes `vkCmdExecuteCommands` the only valid command until the matching end; `VUID-vkCmdExecuteCommands-colorAttachmentCount-06027` exists and requires the inheritance `colorAttachmentCount` to equal the primary's, with a neighbouring rule that the inheritance `flags` equal the rendering flags minus the secondary-contents bit; `occlusionQueryEnable` requires the `inheritedQueries` feature (VUID-VkCommandBufferInheritanceInfo-occlusionQueryEnable-00056); all structure and flag names exist in vk.xml. Removed the tiler and mobile-driver performance claims and the NVIDIA vendor attribution.

Method: documentation only; no commands were run.
