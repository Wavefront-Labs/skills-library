---
id: computing-software.computer-graphics-engineering.opengl.vulkan-msaa-images-and-resolve
name: vulkan-msaa-images-and-resolve
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-images, vk-msaa, resolve-attachment, depth-resolve]
level: practitioner
status: docs-checked
description: "Set up Vulkan MSAA: sample count selection, multisampled attachments with in-pass resolve (dynamic rendering), depth/stencil resolve modes, and transient memory."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/renderpass.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/resources.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSAA images and resolve

## Pick a sample count
```c
VkSampleCountFlags counts = limits.framebufferColorSampleCounts & limits.framebufferDepthSampleCounts;
VkSampleCountFlagBits samples = (counts & VK_SAMPLE_COUNT_4_BIT) ? VK_SAMPLE_COUNT_4_BIT : VK_SAMPLE_COUNT_1_BIT;
```
The spec requires both `framebufferColorSampleCounts` and `framebufferDepthSampleCounts` to include 1 and 4 samples; 4x is the usual sweet spot.

## Images
```c
imageCI.samples = samples; imageCI.mipLevels = 1;          // MSAA images: 1 mip only
imageCI.usage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT | VK_IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT;
// memory: prefer VK_MEMORY_PROPERTY_LAZILY_ALLOCATED_BIT (tilers) else DEVICE_LOCAL
```
Depth must have the same sample count as colour.

## Resolve inside the pass (dynamic rendering)
```c
VkRenderingAttachmentInfo color = { VK_STRUCTURE_TYPE_RENDERING_ATTACHMENT_INFO };
color.imageView = msaaView;  color.imageLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
color.resolveMode = VK_RESOLVE_MODE_AVERAGE_BIT;
color.resolveImageView = swapchainView; color.resolveImageLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
color.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
color.storeOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;           // multisampled data discarded after resolve
```
On tile-based GPUs an in-pass resolve lets the implementation avoid writing the multisampled image to memory (an optimisation, not a spec guarantee);
`DONT_CARE` plus a transient image on lazily allocated memory lets it skip backing memory for the multisampled data.

## Depth/stencil resolve (core 1.2)
`pDepthAttachment->resolveMode = VK_RESOLVE_MODE_SAMPLE_ZERO_BIT` (always supported) or
`MIN_BIT`/`MAX_BIT` if listed in `VkPhysicalDeviceDepthStencilResolveProperties`. Needed when
later passes (SSAO, post) read a single-sample depth buffer.

## Resolve separately
`vkCmdResolveImage` resolves outside a render pass. For HDR + tone mapping, resolve after tone mapping per sample (custom resolve
shader reading `sampler2DMS`) to avoid bright-edge aliasing, at extra cost.

## Gotchas
- Pipeline `rasterizationSamples` must match attachment sample count
  (`VkPipelineMultisampleStateCreateInfo`).
- Integer color formats must use `SAMPLE_ZERO` (or `NONE`) as `resolveMode`; non-integer color formats use `AVERAGE`. For an sRGB resolve target the
  implementation should average in linear space and convert back before writing.
- `sampleShadingEnable` (per-sample shading) multiplies fragment cost by the sample count; use only for alpha-tested foliage or specular aliasing.
- MSAA doesn't combine naively with deferred shading; see MSAA-with-deferred techniques.

## Verify
- [ ] Edges antialiased; on mobile profiler, no external write bandwidth for the MSAA attachment.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23). Confirmed: `framebufferColorSampleCounts` and `framebufferDepthSampleCounts` must include 1 and 4 (required limits); multisampled images need `imageType` 2D, `mipLevels` 1, no cube-compatible flag and optimal tiling (VUID-VkImageCreateInfo-samples-02257); `VkRenderingAttachmentInfo` resolve rules (non-integer color: `AVERAGE`; integer color: `SAMPLE_ZERO`; VUID-...-06129 and 06130); depth/stencil resolve modes must come from `supportedDepthResolveModes` and `SAMPLE_ZERO_BIT` must be included; sRGB resolve averages in linear space. Removed the tile-bandwidth claims stated as fact and the 'full read+write' claim for `vkCmdResolveImage`.

Method: documentation only; no commands were run.
