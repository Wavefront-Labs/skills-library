---
id: computing-software.computer-graphics-engineering.opengl.vulkan-depth-stencil-formats-and-aspects
name: vulkan-depth-stencil-formats-and-aspects
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-images, depth-stencil-format, image-aspect, separate-depth-stencil-layouts]
level: practitioner
status: docs-checked
description: "Choose a supported Vulkan depth/stencil format, use the correct aspect masks in views, barriers and copies, and separate depth/stencil layouts."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/formats.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/copies.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/commonvalidity/image_layout_transition_common.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depth/stencil formats and aspect masks

## Format choice
Only some formats are guaranteed: `D16_UNORM` (depth attachment and sampled), and **at least
one of** `X8_D24_UNORM_PACK32` / `D32_SFLOAT`, and at least one of `D24_UNORM_S8_UINT` /
`D32_SFLOAT_S8_UINT` (depth/stencil attachment support). Always query:
```c
VkFormat pickDepth(VkPhysicalDevice gpu, bool needStencil) {
    std::vector<VkFormat> cands = needStencil
        ? std::vector<VkFormat>{ VK_FORMAT_D32_SFLOAT_S8_UINT, VK_FORMAT_D24_UNORM_S8_UINT }
        : std::vector<VkFormat>{ VK_FORMAT_D32_SFLOAT, VK_FORMAT_X8_D24_UNORM_PACK32, VK_FORMAT_D16_UNORM };
    for (VkFormat f : cands) {
        VkFormatProperties p; vkGetPhysicalDeviceFormatProperties(gpu, f, &p);
        if (p.optimalTilingFeatures & VK_FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT) return f;
    }
    return VK_FORMAT_UNDEFINED;
}
```
Use `D32_SFLOAT` for reversed-Z; `D16_UNORM` for shadow maps (half the bandwidth) if precision allows.

## Aspect masks
| Where | Aspect |
|---|---|
| Image view for depth attachment | `DEPTH` (or `DEPTH` plus `STENCIL` for combined formats used as attachment) |
| Image view for **sampling** | exactly one aspect: `DEPTH` or `STENCIL` (two views to sample both) |
| Barrier `subresourceRange` on combined format | `DEPTH` plus `STENCIL` (both) unless `separateDepthStencilLayouts` is enabled |
| `vkCmdCopyImageToBuffer` | one aspect per region; for `D24_UNORM_S8_UINT` the depth aspect copies as `X8_D24_UNORM_PACK32` |
| Clear | `vkCmdClearDepthStencilImage` / attachment clear with appropriate aspect |

## Separate depth/stencil layouts (core 1.2)
Layouts like `DEPTH_ATTACHMENT_OPTIMAL` / `STENCIL_READ_ONLY_OPTIMAL` (and
`DEPTH_READ_ONLY_STENCIL_ATTACHMENT_OPTIMAL`) allow e.g. reading depth in a shader while still
writing stencil. With `separateDepthStencilLayouts` enabled, barriers may target one aspect.
Sync2 also adds `ATTACHMENT_OPTIMAL` / `READ_ONLY_OPTIMAL` generic layouts (1.3), simplifying code.

## Gotchas
- Sampling a depth image needs `VK_FORMAT_FEATURE_SAMPLED_IMAGE_BIT`; only `D16_UNORM` and
  `D32_SFLOAT` are guaranteed to have it, and `SAMPLED_IMAGE_FILTER_LINEAR_BIT` is not in the
  mandatory set for any depth format, so query before sampling or filtering.
- Comparison samplers (`compareEnable = VK_TRUE`) are for `sampler2DShadow`; sampling raw depth needs
  a non-compare sampler.

## Verify
- [ ] Format selection logged per device; validation clean for barriers on combined depth-stencil images.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Mandatory format tables: `D16_UNORM` supports depth/stencil attachment, sampled image and blit source; at least one of `X8_D24_UNORM_PACK32` / `D32_SFLOAT` and at least one of `D24_UNORM_S8_UINT` / `D32_SFLOAT_S8_UINT` support the depth/stencil attachment feature; `D32_SFLOAT` has sampled-image and blit-source; no depth format has `SAMPLED_IMAGE_FILTER_LINEAR_BIT` guaranteed.
- Confirmed: Descriptor image views of depth/stencil images must include either the depth or the stencil aspect but not both (VUID-VkDescriptorImageInfo-imageView-01976); barriers on combined depth/stencil images need both aspects unless `separateDepthStencilLayouts` is enabled (feature in `VkPhysicalDeviceVulkan12Features`); the copy-aspect table maps the depth aspect of `D24_UNORM_S8_UINT` to `X8_D24_UNORM_PACK32`.
- Removed AMD, mobile and stencil-sampler-type remarks (no source found).

Method: documentation only; no commands were run.
