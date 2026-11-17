---
id: computing-software.computer-graphics-engineering.opengl.vulkan-samplers-and-immutable-samplers
name: vulkan-samplers-and-immutable-samplers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-images, vulkan-samplers, immutable-samplers, vksamplercreateinfo, anisotropic-filtering]
level: practitioner
status: docs-checked
description: "Create Vulkan samplers: filtering, mip LOD, anisotropy feature, border colours, depth compare, and immutable samplers baked into set layouts."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/samplers.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/formats.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sampler creation and immutable samplers

**Goal:** a small set of well-chosen samplers, created once, optionally baked into descriptor
layouts.

## 1. Create
```cpp
VkSamplerCreateInfo s{VK_STRUCTURE_TYPE_SAMPLER_CREATE_INFO};
s.magFilter = s.minFilter = VK_FILTER_LINEAR;
s.mipmapMode = VK_SAMPLER_MIPMAP_MODE_LINEAR;               // trilinear
s.addressModeU = s.addressModeV = s.addressModeW = VK_SAMPLER_ADDRESS_MODE_REPEAT;
s.minLod = 0.f; s.maxLod = VK_LOD_CLAMP_NONE;               // maxLod 0.25 with NEAREST mipmapMode keeps the base level
s.anisotropyEnable = features.samplerAnisotropy;            // must be ENABLED at device creation
s.maxAnisotropy = std::min(16.f, limits.maxSamplerAnisotropy);
```
Variants worth having: point-clamp (G-buffer/LUT fetch), linear-clamp (post), linear-repeat-aniso
(materials), shadow compare sampler (`compareEnable = VK_TRUE`, `compareOp = LESS_OR_EQUAL`,
the depth format must support `SAMPLED_IMAGE_DEPTH_COMPARISON` (and `SAMPLED_IMAGE_FILTER_LINEAR` for linear filtering)).
`borderColor` applies only with `CLAMP_TO_BORDER`; custom colours need
`VK_EXT_custom_border_color`.

## 2. Immutable samplers
```cpp
VkDescriptorSetLayoutBinding b{0, VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, 1,
                               VK_SHADER_STAGE_FRAGMENT_BIT, &linearSampler};
```
The sampler becomes part of the layout: no sampler writes in descriptor updates, and it is required for YCbCr conversion
samplers (a combined image sampler with an immutable sampler). Changing it means a new layout and pipeline.

## Gotchas
- `maxSamplerAllocationCount` has a guaranteed minimum of 4000: dedupe samplers by create-info hash.
- `unnormalizedCoordinates` forbids mips, anisotropy and repeat; meant for texel-exact fetch.
- The absolute value of `mipLodBias` must not exceed `maxSamplerLodBias` (guaranteed minimum 2; 14 in Roadmap 2022 and the Vulkan 1.4 limits);
  use it for upscaler/TAA negative bias as the upscaler documents, not per-texture hacks.
- Using anisotropy without enabling the device feature is a validation error and undefined.

## Verify
- [ ] Ground plane at grazing angle is sharp with aniso and blurry without (feature works).
- [ ] Sampler count logged at startup stays small and stable.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23). Confirmed in `samplers.adoc`: the spec's own note that `minLod = 0`, `maxLod = 0.25` with `VK_SAMPLER_MIPMAP_MODE_NEAREST` rounds to the base level (the old comment said 0.25 means no mips regardless of mipmap mode); the sampler anisotropy feature must be enabled (VUID-VkSamplerCreateInfo-anisotropyEnable-01070); `unnormalizedCoordinates` forbids anisotropy and compare; |`mipLodBias`| must be at most `maxSamplerLodBias` (a VUID, not a clamp; limit minimum 2); `maxSamplerAllocationCount` minimum 4000; `VK_FORMAT_FEATURE_2_SAMPLED_IMAGE_DEPTH_COMPARISON_BIT` exists and depth formats with sampled support must provide it (formats.adoc). Removed the hardware-PCF and embedded-sampler performance claims and the `log2` bias formula.

Method: documentation only; no commands were run.
