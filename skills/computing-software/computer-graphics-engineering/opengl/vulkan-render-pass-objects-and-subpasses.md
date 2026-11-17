---
id: computing-software.computer-graphics-engineering.opengl.vulkan-render-pass-objects-and-subpasses
name: vulkan-render-pass-objects-and-subpasses
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-pipelines, vulkan-render-pass, subpasses, input-attachments]
level: advanced
status: docs-checked
description: "Build VkRenderPass2 objects with attachments, load/store ops, subpasses and input attachments for tile-based GPUs, plus framebuffers and imageless variants."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/renderpass.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/xml/vk.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Render pass objects and subpasses

Dynamic rendering replaces render passes for most desktop code, but `VkRenderPass` subpasses
(or `VK_KHR_dynamic_rendering_local_read`, core in Vulkan 1.4) remain the way to keep G-buffer data on-chip on
tile-based mobile GPUs.

## Attachments
```c
VkAttachmentDescription2 att[3] = {};
// 0: swapchain colour
att[0] = (VkAttachmentDescription2){ VK_STRUCTURE_TYPE_ATTACHMENT_DESCRIPTION_2, .format = swapFmt,
  .samples = VK_SAMPLE_COUNT_1_BIT, .loadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE, .storeOp = VK_ATTACHMENT_STORE_OP_STORE,
  .initialLayout = VK_IMAGE_LAYOUT_UNDEFINED, .finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR };
// 1: albedo G-buffer, only lives inside the pass
att[1] = (VkAttachmentDescription2){ ..., .format = VK_FORMAT_R8G8B8A8_UNORM,
  .loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR, .storeOp = VK_ATTACHMENT_STORE_OP_DONT_CARE,
  .initialLayout = VK_IMAGE_LAYOUT_UNDEFINED, .finalLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL };
// 2: depth
att[2] = (VkAttachmentDescription2){ ..., .format = VK_FORMAT_D32_SFLOAT,
  .loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR, .storeOp = VK_ATTACHMENT_STORE_OP_DONT_CARE, ... };
```
`STORE_OP_DONT_CARE` on intermediate attachments + `LAZILY_ALLOCATED` memory with
`TRANSIENT_ATTACHMENT` usage lets an implementation avoid allocating and writing them (typically on tile-based GPUs).

## Subpasses
```c
VkAttachmentReference2 gbufOut = { ..., .attachment = 1, .layout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL };
VkAttachmentReference2 depthRef = { ..., .attachment = 2, .layout = VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL };
VkAttachmentReference2 gbufIn = { ..., .attachment = 1, .layout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL,
                                  .aspectMask = VK_IMAGE_ASPECT_COLOR_BIT };
VkAttachmentReference2 finalOut = { ..., .attachment = 0, .layout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL };
VkSubpassDescription2 sp[2] = {
  { ..., .colorAttachmentCount = 1, .pColorAttachments = &gbufOut, .pDepthStencilAttachment = &depthRef },
  { ..., .inputAttachmentCount = 1, .pInputAttachments = &gbufIn, .colorAttachmentCount = 1, .pColorAttachments = &finalOut } };
// + VkSubpassDependency2 0->1 with BY_REGION (see subpass dependencies skill)
```
Lighting shader reads the G-buffer at the same pixel:
```glsl
layout(input_attachment_index = 0, set = 0, binding = 0) uniform subpassInput gAlbedo;
vec4 albedo = subpassLoad(gAlbedo);
```
Descriptor type `VK_DESCRIPTOR_TYPE_INPUT_ATTACHMENT`; advance with `vkCmdNextSubpass2`.

## Framebuffers
`VkFramebuffer` binds concrete image views to the attachment slots, one per swapchain image.
`VK_KHR_imageless_framebuffer` (core 1.2) creates it with formats only and supplies views at
`vkCmdBeginRenderPass2` via `VkRenderPassAttachmentBeginInfo`, avoiding per-image framebuffers.

## Gotchas
- Pipelines are created against a render pass + subpass index; they're compatible with other
  render passes that match formats/samples (render pass compatibility rules), not load ops.
- Clear values array indexes by attachment number, including attachments not cleared.

## Verify
- [ ] On a Mali/Adreno device, profiler shows G-buffer attachments never written to memory (no external write bandwidth for them).

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and vk.xml. Confirmed: `VkAttachmentDescription2`, `VkSubpassDescription2`, `VkSubpassDependency2`, `vkCmdNextSubpass2`, `VkRenderPassAttachmentBeginInfo` and `VK_DESCRIPTOR_TYPE_INPUT_ATTACHMENT` exist; `VK_KHR_imageless_framebuffer` is promoted to Vulkan 1.2 and `VK_KHR_dynamic_rendering_local_read` to Vulkan 1.4 (vk.xml `promotedto`); imageless attachment views must have a single mip level and identity swizzle (renderpass.adoc); pipeline and render pass compatibility rules are in the spec. Removed the 'never touch DRAM' and 'desktop GPUs gain little' vendor claims and the Arm developer link, which could not be read.

Method: documentation only; no commands were run.
