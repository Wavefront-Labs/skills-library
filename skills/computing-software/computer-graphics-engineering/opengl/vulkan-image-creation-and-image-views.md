---
id: computing-software.computer-graphics-engineering.opengl.vulkan-image-creation-and-image-views
name: vulkan-image-creation-and-image-views
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-images, image-views, vkimagecreateinfo, vkimageviewcreateinfo, image-usage, mutable-format]
level: practitioner
status: docs-checked
description: "Create Vulkan images and views correctly: usage flags, tiling, format feature checks, subresource ranges, mutable formats for sRGB/UNORM views."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/resources.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/formats.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image creation and image views

**Goal:** create a VkImage with exactly the capabilities you need, and views that expose the
right slice/format to each consumer.

## 1. Image
```cpp
VkImageCreateInfo ci{VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO};
ci.imageType = VK_IMAGE_TYPE_2D; ci.format = VK_FORMAT_R8G8B8A8_SRGB;
ci.extent = {w, h, 1}; ci.mipLevels = mips; ci.arrayLayers = 1;
ci.samples = VK_SAMPLE_COUNT_1_BIT; ci.tiling = VK_IMAGE_TILING_OPTIMAL;
ci.usage = VK_IMAGE_USAGE_SAMPLED_BIT | VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_TRANSFER_SRC_BIT;
ci.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
```
- Check support first: `vkGetPhysicalDeviceFormatProperties2` -> `optimalTilingFeatures`
  (`SAMPLED_IMAGE_FILTER_LINEAR`, `COLOR_ATTACHMENT`, `STORAGE_IMAGE`, `BLIT_SRC/DST`), and
  `vkGetPhysicalDeviceImageFormatProperties2` for max extent/samples.
- Ask only for the usages you need: each usage bit must be supported by the format features for the tiling in use.
- `LINEAR` tiling is meant for host access; its format features come from `linearTilingFeatures` and can be narrower than
  optimal tiling (query `vkGetPhysicalDeviceImageFormatProperties2`), and a linear image cannot be multisampled.
- Cube maps: `arrayLayers = 6*n` + `VK_IMAGE_CREATE_CUBE_COMPATIBLE_BIT`.

## 2. View
```cpp
VkImageViewCreateInfo vi{VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO};
vi.image = img; vi.viewType = VK_IMAGE_VIEW_TYPE_2D; vi.format = ci.format;
vi.subresourceRange = {VK_IMAGE_ASPECT_COLOR_BIT, 0, VK_REMAINING_MIP_LEVELS, 0, VK_REMAINING_ARRAY_LAYERS};
```
- One view per use: full chain for sampling, single-mip views for rendering into or for compute
  writes (attachment views must specify a single mip level; storage image, input attachment and attachment views must use the identity swizzle).
- Depth-stencil: a view used through a descriptor must have either the `DEPTH` or the `STENCIL` aspect, not both; attachments can use both.
- Cube as array for compute writes: `VIEW_TYPE_2D_ARRAY` over 6 layers.

## 3. Different format views
To write an sRGB image as UNORM in compute (sRGB formats have no mandatory storage-image support), create
the image with `VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT` plus `VkImageFormatListCreateInfo` listing
both formats, then make a UNORM storage view and an SRGB sampled view.
`VkImageViewUsageCreateInfo` restricts a view's usage so the SRGB view need not support STORAGE. If the image's own format lacks a
usage (for example `STORAGE` on an sRGB format), also set `VK_IMAGE_CREATE_EXTENDED_USAGE_BIT`: the spec then allows any usage supported by at least one view format.

## Gotchas
- The spec's mandatory-format table lists no required features for the 3-channel `VK_FORMAT_R8G8B8_*` formats; use RGBA unless you query support.
- Destroy views before the image they were created from.
- Component swizzles are only for sampled views: storage image, input attachment and framebuffer attachment views must use the identity swizzle (spec).

## Verify
- [ ] Validation clean at creation and first use; format features checked at startup.
- [ ] RenderDoc shows each view's mip/layer range as intended.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23). Confirmed: identity swizzle is required for storage image, input attachment and framebuffer attachment views (`resources.adoc`, `descriptorsets.adoc`); attachment image views must specify a single mip level (VUID-VkRenderingAttachmentInfo-imageView-12486 and the framebuffer rule); a depth/stencil view in a descriptor must include the depth or the stencil aspect but not both (VUID-VkDescriptorImageInfo-imageView-01976); linear images cannot be multisampled (VUID-VkImageCreateInfo-samples-02257) and take their features from `linearTilingFeatures`; `VK_IMAGE_CREATE_EXTENDED_USAGE_BIT` semantics; `VkImageFormatListCreateInfo` entries must be compatible with the image format; the mandatory-format table has no entries for `R8G8B8_*` and no storage-image entry for `R8G8B8A8_SRGB`. Removed the DCC/AFBC compression claims and the storage-view `levelCount` rule, which the spec does not state.

Method: documentation only; no commands were run.
