---
id: computing-software.computer-graphics-engineering.opengl.vulkan-image-tiling-and-creation-flags
name: vulkan-image-tiling-and-creation-flags
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-images, image-tiling, linear-tiling, mutable-format]
level: advanced
status: docs-checked
description: "Choose Vulkan image tiling (OPTIMAL vs LINEAR vs DRM modifiers) and create flags (MUTABLE_FORMAT, CUBE_COMPATIBLE, ALIAS, EXTENDED_USAGE) with their costs."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/resources.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/formats.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image tiling and creation flags

## Tiling
| Tiling | Layout | Use |
|---|---|---|
| `OPTIMAL` | opaque, swizzled/compressed by the driver | everything the GPU renders or samples |
| `LINEAR` | row-major, `vkGetImageSubresourceLayout` gives rowPitch | CPU readback/upload of single 2D images, video interop |
| `DRM_FORMAT_MODIFIER_EXT` | explicit modifier | Linux dma-buf sharing with compositors/decoders |

`LINEAR` restrictions: format features come from `linearTilingFeatures`, which can be narrower than `optimalTilingFeatures`, and a
linear image cannot be multisampled (spec). Check `vkGetPhysicalDeviceImageFormatProperties2` for the extent, mip, layer and usage limits
before creating. Default: always optimal + staging buffer copies.

## Creation flags
| Flag | Purpose | Cost |
|---|---|---|
| `MUTABLE_FORMAT_BIT` | views with other compatible formats (sRGB + UNORM, UINT aliasing) | view formats must be compatible with the image format |
| + `VkImageFormatListCreateInfo` | list the formats you'll view as (each must be compatible with the image format) | |
| `CUBE_COMPATIBLE_BIT` | create cube / cube-array views (2D, square, arrayLayers at least 6) | |
| `2D_ARRAY_COMPATIBLE_BIT` | 2D/2D-array views of a 3D image | |
| `EXTENDED_USAGE_BIT` | usage valid for some view formats but not the image format (e.g. STORAGE on sRGB image via UNORM view) | |
| `ALIAS_BIT` | images with identical creation parameters that alias the same memory interpret its contents consistently (subject to the aliasing rules) | |
| `SPARSE_*` | sparse residency | special memory binding |
| `BLOCK_TEXEL_VIEW_COMPATIBLE_BIT` | uncompressed view of compressed blocks (GPU BC encoding) | |

## Common pattern: write in compute, sample as sRGB
```c
VkFormat fmts[2] = { VK_FORMAT_R8G8B8A8_UNORM, VK_FORMAT_R8G8B8A8_SRGB };
VkImageFormatListCreateInfo fl = { VK_STRUCTURE_TYPE_IMAGE_FORMAT_LIST_CREATE_INFO, NULL, 2, fmts };
VkImageCreateInfo ci = { VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO, &fl };
ci.flags = VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT | VK_IMAGE_CREATE_EXTENDED_USAGE_BIT;
ci.format = VK_FORMAT_R8G8B8A8_SRGB;
ci.usage = VK_IMAGE_USAGE_STORAGE_BIT | VK_IMAGE_USAGE_SAMPLED_BIT;
```
Storage view uses UNORM (encode sRGB manually in the shader), sampled view uses SRGB.

## Usage flags matter too
Every usage bit must be supported by the format features for the tiling in use, so extra bits narrow the formats you can pick. Don't add
`STORAGE`, `TRANSFER_SRC` or `COLOR_ATTACHMENT` "just in case".
`TRANSIENT_ATTACHMENT` + lazily allocated memory for attachments that never leave the tile.

## Verify
- [ ] Format support queried for each (format, tiling, usage, flags) combo at startup.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23), `resources.adoc`. Confirmed flag semantics for `MUTABLE_FORMAT_BIT`, `CUBE_COMPATIBLE_BIT` (2D, equal width and height, at least 6 layers), `2D_ARRAY_COMPATIBLE_BIT`, `BLOCK_TEXEL_VIEW_COMPATIBLE_BIT`, `EXTENDED_USAGE_BIT` and `ALIAS_BIT` (same creation parameters and aliased memory give consistent contents); `VkImageFormatListCreateInfo` entries must be compatible with the image format; linear images cannot be multisampled and use `linearTilingFeatures`. Removed the DCC/AFBC compression claims, the 'sampling linear images is slow' claim and the list of typical linear-image restrictions (the spec gives no such guarantee).

Method: documentation only; no commands were run.
