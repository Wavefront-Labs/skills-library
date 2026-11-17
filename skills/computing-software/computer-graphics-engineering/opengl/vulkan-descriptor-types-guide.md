---
id: computing-software.computer-graphics-engineering.opengl.vulkan-descriptor-types-guide
name: vulkan-descriptor-types-guide
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-descriptors, storage-image, texel-buffer, input-attachment, inline-uniform-block]
level: practitioner
status: docs-checked
description: "Pick the right Vulkan descriptor type: sampled vs combined image samplers, storage images, uniform/storage texel buffers, input attachments, inline uniform blocks."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/formats.adoc", "https://github.com/KhronosGroup/Vulkan-Guide/blob/main/chapters/mapping_data_to_shaders.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan descriptor types

| Type | GLSL | Usage flag | Use for |
|---|---|---|---|
| `SAMPLER` | `uniform sampler s;` | - | separate sampler state, shared across textures |
| `SAMPLED_IMAGE` | `uniform texture2D t;` -> `texture(sampler2D(t, s), uv)` | `SAMPLED` | bindless texture arrays + few samplers |
| `COMBINED_IMAGE_SAMPLER` | `uniform sampler2D tex;` | `SAMPLED` | simple: one descriptor per texture and sampler pair |
| `STORAGE_IMAGE` | `layout(rgba16f) uniform image2D img;` | `STORAGE` | compute writes, `imageLoad/Store`, atomics (usually layout `GENERAL`) |
| `UNIFORM_BUFFER` (+ `_DYNAMIC`) | `uniform Block {...};` | `UNIFORM_BUFFER` | small constant data, <= `maxUniformBufferRange` |
| `STORAGE_BUFFER` (+ `_DYNAMIC`) | `buffer Block {...};` | `STORAGE_BUFFER` | large arrays, read-write, runtime-sized |
| `UNIFORM_TEXEL_BUFFER` | `uniform samplerBuffer b;` / `textureBuffer` | `UNIFORM_TEXEL_BUFFER` + buffer view | formatted buffer reads |
| `STORAGE_TEXEL_BUFFER` | `layout(r32ui) uniform uimageBuffer b;` | `STORAGE_TEXEL_BUFFER` | formatted writes/atomics on buffers |
| `INPUT_ATTACHMENT` | `subpassInput` | `INPUT_ATTACHMENT` | same-pixel reads inside render pass subpasses |
| `INLINE_UNIFORM_BLOCK` (1.3) | `uniform Block {...};` | - | tiny constants stored in the set itself |
| `ACCELERATION_STRUCTURE_KHR` | `accelerationStructureEXT` | - | ray queries / ray tracing |

## Choosing
- **Combined vs separate:** separate sampled images plus a few shared samplers suit large texture
  arrays (`texture2D textures[]` + `sampler samplers[4]`) and need fewer descriptors; combined image
  samplers are simpler when each texture has its own sampler state.
- **UBO vs SSBO:** UBOs for small constant blocks (`maxUniformBufferRange`, guaranteed minimum
  16384 bytes); SSBOs for large, writable or runtime-sized arrays. std140 vs std430 layout rules differ.
- **Texel buffers** need a `VkBufferView` with a format; good for reading packed formats
  (`R16G16_SFLOAT`) with conversion, or image atomics semantics on buffers.
- **Inline uniform blocks:** a few dozen bytes per set without a buffer (limit
  `maxInlineUniformBlockSize`, guaranteed minimum 256 bytes); push constants are an alternative.

## Gotchas
- Storage images need `VK_FORMAT_FEATURE_STORAGE_IMAGE_BIT`; the mandatory-format tables do not
  require it for sRGB formats such as `R8G8B8A8_SRGB`, so query support or use a UNORM view of a
  mutable-format image (`VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT`).
- Descriptor type in the layout must match the write type and shader declaration exactly
  (sampled image vs combined is a mismatch).
- Dynamic variants count against separate limits (`maxDescriptorSetUniformBuffersDynamic`, minimum 8;
  `maxDescriptorSetStorageBuffersDynamic`, minimum 4).

## Verify
- [ ] Validation clean at draw; reflection (SPIRV-Reflect) types match layout bindings.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Limit minimums from the limits table: `maxUniformBufferRange` 16384, `maxInlineUniformBlockSize` 256, `maxDescriptorSetUniformBuffersDynamic` 8, `maxDescriptorSetStorageBuffersDynamic` 4.
- Confirmed: Inline uniform blocks are core in 1.3 (`VK_EXT_inline_uniform_block` promotedto 1.3). `R8G8B8A8_SRGB` has no `STORAGE_IMAGE` entry in the 4-byte mandatory format table while `R8G8B8A8_UNORM` does.
- Confirmed: GLSL type `accelerationStructureEXT` confirmed in GLSL_EXT_ray_tracing. Removed vendor and speed claims (mobile combined-sampler preference, UBO speed, texture cache).

Method: documentation only; no commands were run.
