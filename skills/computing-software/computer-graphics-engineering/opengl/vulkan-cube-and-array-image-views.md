---
id: computing-software.computer-graphics-engineering.opengl.vulkan-cube-and-array-image-views
name: vulkan-cube-and-array-image-views
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-images, cube-image-view, array-layers, per-face-views]
level: practitioner
status: docs-checked
description: "Create Vulkan cube maps, cube arrays and 2D arrays: CUBE_COMPATIBLE images, face order, per-face/per-mip views for rendering, and copying faces."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/resources.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/textures.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/samplers.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cube and array image views

## Creating a cube map
```c
VkImageCreateInfo ci = { VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO };
ci.flags = VK_IMAGE_CREATE_CUBE_COMPATIBLE_BIT;
ci.imageType = VK_IMAGE_TYPE_2D; ci.extent = { size, size, 1 };      // must be square
ci.arrayLayers = 6 * cubeCount; ci.mipLevels = mips;
ci.format = VK_FORMAT_R16G16B16A16_SFLOAT;
ci.usage = VK_IMAGE_USAGE_SAMPLED_BIT | VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT | VK_IMAGE_USAGE_TRANSFER_DST_BIT;
```
Layer order per cube: +X, -X, +Y, -Y, +Z, -Z (layers 0-5); with `CUBE_COMPATIBLE_BIT` the image must
be 2D, square, with at least 6 array layers. Cube array views need feature `imageCubeArray`.

## Views
| Purpose | viewType | layers |
|---|---|---|
| Sample as cube | `VK_IMAGE_VIEW_TYPE_CUBE` | base 0, count 6 |
| Sample as cube array | `CUBE_ARRAY` | multiple of 6 |
| Render one face/mip (prefilter passes) | `2D` | base = face, count 1, baseMip = m, levelCount 1 |
| Render all faces in one pass (multiview/layered) | `2D_ARRAY` | 6 |
| Compute writes to all faces | `2D_ARRAY` storage view, index face with `gl_GlobalInvocationID.z` | 6 |
For compute writes a `2D_ARRAY` view over the faces is the straightforward pattern
(`imageStore(img, ivec3(xy, face), v)`); sample through the cube view.

## Face orientation
The layer-to-face mapping and the per-face coordinate selection (`sc`, `tc`, `rc`) are defined by the
spec's cube map face selection table (layer 0 = +X ... layer 5 = -Z). When rendering faces with a
camera, derive the look and up vectors from that table and from your projection's y flip, and verify
by rendering a labelled test scene and sampling `texture(cube, dir)` with known directions.

## Uploading faces from KTX/DDS
One `VkBufferImageCopy` per (face, mip) with `imageSubresource.baseArrayLayer = face`.
KTX stores faces in cube order already; equirectangular HDRIs need a compute conversion pass.

## Gotchas
- Cube filtering is seamless by default; `VK_EXT_non_seamless_cube_map` adds an opt-out
  (`VK_SAMPLER_CREATE_NON_SEAMLESS_CUBE_MAP_BIT_EXT`, needs the `nonSeamlessCubeMap` feature).
- Transition every layer the view covers (layers 0-5 for a cube view).

## Verify
- [ ] Debug sampling with axis directions shows the expected labelled faces; validation clean on layered rendering.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23). Confirmed in `resources.adoc`: cube and cube-array view layers are ordered +X, -X, +Y, -Y, +Z, -Z, and `CUBE_COMPATIBLE_BIT` requires a 2D image with equal width and height and `arrayLayers` of at least 6; in `textures.adoc`: the layer-number table and that, without `VK_SAMPLER_CREATE_NON_SEAMLESS_CUBE_MAP_BIT_EXT`, cube filtering is seamless (the earlier text said there is no toggle). Removed the 'RenderMan convention' claim, the hard-coded up vectors, the driver-specific storage-view claim and the blit-region claim, none of which the spec states.

Method: documentation only; no commands were run.
