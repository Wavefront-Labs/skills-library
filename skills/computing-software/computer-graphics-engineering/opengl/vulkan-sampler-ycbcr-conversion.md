---
id: computing-software.computer-graphics-engineering.opengl.vulkan-sampler-ycbcr-conversion
name: vulkan-sampler-ycbcr-conversion
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-images, ycbcr-conversion, nv12-textures, video-textures]
level: advanced
status: docs-checked
description: "Sample NV12/YUV video frames in Vulkan with sampler YCbCr conversion: multi-planar formats, model/range, chroma siting, and immutable sampler rules."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/samplers.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/formats.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/xml/vk.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sampler YCbCr conversion (core 1.1)

Video decoders and cameras produce multi-planar YCbCr (NV12 = `VK_FORMAT_G8_B8R8_2PLANE_420_UNORM`,
P010 = `G10X6_B10X6R10X6_2PLANE_420_UNORM_3PACK16`). A YCbCr conversion object makes the
sampler return RGB directly, with hardware chroma upsampling.

## Create
```c
VkSamplerYcbcrConversionCreateInfo yc = { VK_STRUCTURE_TYPE_SAMPLER_YCBCR_CONVERSION_CREATE_INFO };
yc.format = VK_FORMAT_G8_B8R8_2PLANE_420_UNORM;
yc.ycbcrModel = VK_SAMPLER_YCBCR_MODEL_CONVERSION_YCBCR_709;     // 601 or 2020 to match the content
yc.ycbcrRange = VK_SAMPLER_YCBCR_RANGE_ITU_NARROW;               // narrow or full to match the content
yc.xChromaOffset = VK_CHROMA_LOCATION_MIDPOINT;                  // match the stream's chroma siting
yc.yChromaOffset = VK_CHROMA_LOCATION_MIDPOINT;
yc.chromaFilter = VK_FILTER_LINEAR;                              // needs ..._LINEAR_FILTER format feature
vkCreateSamplerYcbcrConversion(dev, &yc, NULL, &conv);

VkSamplerYcbcrConversionInfo ci = { VK_STRUCTURE_TYPE_SAMPLER_YCBCR_CONVERSION_INFO, NULL, conv };
samplerCI.pNext = &ci;          // sampler: clamp-to-edge, no anisotropy, unnormalized coords off
viewCI.pNext = &ci;             // the image view MUST carry the same conversion
```

## Descriptor rules
The sampler must be an **immutable sampler** in the set layout
(`pImmutableSamplers`), used through `COMBINED_IMAGE_SAMPLER`. Drivers may consume multiple
descriptors per such binding; query `VkSamplerYcbcrConversionImageFormatProperties::combinedImageSamplerDescriptorCount`
and size pools accordingly. Shader side is an ordinary `sampler2D`; output is RGB in the model's
primaries, non-linear (apply EOTF yourself for HDR/linear workflows).

## Checks
- Feature `samplerYcbcrConversion`.
- `vkGetPhysicalDeviceFormatProperties` for the multi-planar format: `MIDPOINT/COSITED_CHROMA_SAMPLES_BIT`,
  `SAMPLED_IMAGE_YCBCR_CONVERSION_LINEAR_FILTER_BIT`, etc.
- Images are created with `VK_IMAGE_CREATE_DISJOINT_BIT` if planes live in separate memory;
  bind per plane with `VkBindImagePlaneMemoryInfo`.

## Uploading planes
Copy Y to aspect `PLANE_0` and interleaved CbCr to `PLANE_1` (half resolution) with
`vkCmdCopyBufferToImage` regions per plane.

## Gotchas
- Wrong range (full vs narrow) gives washed-out or crushed blacks; a wrong model gives slightly
  wrong colours.
- Android hardware buffers: use `VK_ANDROID_external_memory_android_hardware_buffer` and the
  suggested conversion parameters from `VkAndroidHardwareBufferFormatPropertiesANDROID`.
- If the hardware path is unavailable, sample planes as R8/RG8 views and convert in the shader.

## Verify
- [ ] Colour bars test video matches reference RGB values within a couple of code values.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and vk.xml. Confirmed in `samplers.adoc`: a sampler with YCbCr conversion must use CLAMP_TO_EDGE address modes with anisotropy and unnormalized coordinates disabled (VUID-VkSamplerCreateInfo-addressModeU-01646); the sampler must come from a combined image sampler with an immutable sampler; an image view with the conversion needs identity swizzle and the same format (VUID-VkImageViewCreateInfo-pNext-01970 and 06658); chroma offsets need the matching `MIDPOINT`/`COSITED` chroma sample format feature; `VkAndroidHardwareBufferFormatPropertiesANDROID` has the `suggestedYcbcrModel`, `suggestedYcbcrRange` and suggested chroma offset members; format names, `VkSamplerYcbcrConversionImageFormatProperties::combinedImageSamplerDescriptorCount`, `VkBindImagePlaneMemoryInfo`; conversion is core in Vulkan 1.1. Removed the codec-to-chroma-siting mapping and the colour-cast claim, which the spec does not state.

Method: documentation only; no commands were run.
