---
id: computing-software.computer-graphics-engineering.opengl.vulkan-host-image-copy
name: vulkan-host-image-copy
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-memory, host-image-copy, vkcopymemorytoimage, texture-upload-cpu]
level: advanced
status: docs-checked
description: "Upload textures from the CPU without staging buffers or command buffers using VK_EXT_host_image_copy (optional in 1.4): usage flag, host layout transitions, limits."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_host_image_copy.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/copies.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/versions.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host image copy (VK_EXT_host_image_copy, Vulkan 1.4 optional feature)

Copies between host memory and an image are executed by the CPU: no staging buffer, no command
buffer, no queue submission. Useful for loader threads and for images updated rarely.

## Requirements
- Feature `hostImageCopy`; image created with `VK_IMAGE_USAGE_HOST_TRANSFER_BIT` (EXT name
  `..._HOST_TRANSFER_BIT_EXT`).
- The layout used must be listed in `VkPhysicalDeviceHostImageCopyProperties::pCopyDstLayouts`.
- `identicalMemoryTypeRequirements` reports whether adding the host-transfer usage leaves the image's
  memory type requirements unchanged; `optimalTilingLayoutUUID` identifies the implementation's
  optimal-tiling swizzle layout (relevant to `VK_HOST_IMAGE_COPY_MEMCPY_BIT`).
- A Vulkan 1.4 implementation with a graphics queue must support `hostImageCopy` or provide an
  additional transfer-capable queue, so the feature is optional.

## Upload
```c
// 1. Transition on the host (no command buffer)
VkHostImageLayoutTransitionInfo t = { VK_STRUCTURE_TYPE_HOST_IMAGE_LAYOUT_TRANSITION_INFO };
t.image = img; t.oldLayout = VK_IMAGE_LAYOUT_UNDEFINED; t.newLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
t.subresourceRange = { VK_IMAGE_ASPECT_COLOR_BIT, 0, mipCount, 0, 1 };
vkTransitionImageLayout(device, 1, &t);
// 2. Copy each mip from host memory
VkMemoryToImageCopy r = { VK_STRUCTURE_TYPE_MEMORY_TO_IMAGE_COPY };
r.pHostPointer = pixels; r.imageSubresource = { VK_IMAGE_ASPECT_COLOR_BIT, 0, 0, 1 };
r.imageExtent = { w, h, 1 };
VkCopyMemoryToImageInfo ci = { VK_STRUCTURE_TYPE_COPY_MEMORY_TO_IMAGE_INFO };
ci.dstImage = img; ci.dstImageLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
ci.regionCount = 1; ci.pRegions = &r;
vkCopyMemoryToImage(device, &ci);
```
Function names are suffixed `EXT` when using the extension instead of 1.4 core.

## Synchronisation
`vkCopyMemoryToImage` does not check whether the image memory is in use: the application must
guarantee that earlier submitted commands that read or write the copy regions have completed (for
example by waiting on a fence or timeline value). `dstImageLayout` must be the current layout of
the subresources and one of `pCopyDstLayouts`.

## When to use / not
- Fits streaming code that loads textures on worker threads without a staging buffer, command buffer
  or queue submission (extension issue 1). Measure against staged `vkCmdCopyBufferToImage` for your
  workload.
- `VK_HOST_IMAGE_COPY_MEMCPY_BIT` flag + `vkCopyImageToMemory` let you copy the raw tiled bytes for caching.

## Verify
- [ ] Texture renders correctly with no staging buffers allocated; validation clean (layout listed in pCopyDstLayouts).

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: `VK_EXT_host_image_copy` is promoted to 1.4 but optional (`hostImageCopy` in `VkPhysicalDeviceVulkan14Features`); a 1.4 implementation with a graphics queue must support the feature or an extra transfer queue (appendix).
- Confirmed: `VK_IMAGE_USAGE_HOST_TRANSFER_BIT` is required for `vkTransitionImageLayout`; `newLayout` and `dstImageLayout` must be in `pCopyDstLayouts`; `dstImageLayout` must be the current layout; the copy does not check whether the memory is in use (copies chapter).
- Confirmed: `VkMemoryToImageCopy`, `VkCopyMemoryToImageInfo`, `VkHostImageLayoutTransitionInfo` members and `VK_HOST_IMAGE_COPY_MEMCPY_BIT` match vk.xml.
- Removed UMA/ReBAR suitability and discrete-GPU claims (no source found).

Method: documentation only; no commands were run.
