---
id: computing-software.computer-graphics-engineering.gpu-optimisation.framebuffer-fetch-and-subpass-inputs
name: framebuffer-fetch-and-subpass-inputs
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, tile-based-gpus, framebuffer-fetch, subpass-input, dynamic-rendering-local-read, pixel-local-storage, on-chip-deferred]
level: sme
status: draft
description: "Keep G-buffer data on-chip on tilers: Vulkan subpass inputs and dynamic_rendering_local_read, GL framebuffer fetch, Metal programmable blending, and transient attachments."
sources: ["https://registry.khronos.org/vulkan/specs/1.3-extensions/man/html/VK_KHR_dynamic_rendering_local_read.html", "https://github.com/KhronosGroup/Vulkan-Samples/tree/main/samples/performance/subpasses", "https://registry.khronos.org/OpenGL/extensions/EXT/EXT_shader_framebuffer_fetch.txt", "https://developer.apple.com/documentation/metal/metal_sample_code_library/rendering_a_scene_with_deferred_lighting_in_objective-c"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Framebuffer fetch and subpass inputs

## 1. Goal
On tile-based GPUs (Mali, Adreno, PowerVR, Apple), a deferred renderer that writes the G-buffer to memory and
reads it back costs huge bandwidth. Reading the current pixel's attachment values directly from tile memory
keeps the whole G-buffer on-chip: write in pass A, read in pass B, never store.

## 2. Vulkan: subpasses
- One render pass, subpass 0 writes G-buffer colour attachments, subpass 1 declares them as input attachments.
- Dependency between subpasses with `VK_DEPENDENCY_BY_REGION_BIT` (pixel-local), src COLOR_ATTACHMENT_OUTPUT /
  dst FRAGMENT_SHADER, access COLOR_ATTACHMENT_WRITE -> INPUT_ATTACHMENT_READ.
- G-buffer attachments: `loadOp CLEAR/DONT_CARE`, `storeOp DONT_CARE`, image usage
  `TRANSIENT_ATTACHMENT | INPUT_ATTACHMENT`, memory `LAZILY_ALLOCATED` (often no physical backing).
```glsl
layout(input_attachment_index = 0, set = 0, binding = 0) uniform subpassInput gAlbedo;
vec4 albedo = subpassLoad(gAlbedo);
```
- With dynamic rendering, `VK_KHR_dynamic_rendering_local_read` (core in 1.4) gives the same: attachments in
  `VK_IMAGE_LAYOUT_RENDERING_LOCAL_READ_KHR`, a by-region pipeline barrier inside the render pass, and
  `vkCmdSetRenderingInputAttachmentIndicesKHR` to map input attachment indices.

## 3. OpenGL ES / GL
`EXT_shader_framebuffer_fetch`: declare `inout vec4 color;` and read the current value (programmable blending).
`ARM_shader_framebuffer_fetch_depth_stencil` reads depth; `EXT_shader_pixel_local_storage` gives typed
per-pixel scratch storage that never leaves the tile.

## 4. Metal
Programmable blending: fragment function parameters with `[[color(n)]]` read the attachment; G-buffer
textures with `MTLStorageModeMemoryless`.

## Gotchas
- Only the same pixel is readable; anything needing neighbours (SSAO, blur) forces a store.
- Desktop GPUs gain little and drivers may split subpasses anyway; keep a fallback path.
- MSAA input attachments read per sample (`subpassInputMS`), so shading may run per sample.
- Validation: missing BY_REGION or wrong layouts silently forces a flush on some drivers.

## Verify
- [ ] GPU vendor profiler (Mali Streamline, Snapdragon Profiler, Xcode) shows external memory write bandwidth
  for G-buffer near zero; frame bandwidth drops versus the two-pass version.
