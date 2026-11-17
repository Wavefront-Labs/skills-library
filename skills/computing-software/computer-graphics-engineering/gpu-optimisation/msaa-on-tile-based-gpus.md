---
id: computing-software.computer-graphics-engineering.gpu-optimisation.msaa-on-tile-based-gpus
name: msaa-on-tile-based-gpus
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, tile-based-gpus, mobile-msaa, msaa, on-tile-resolve, memoryless, transient-attachments, render-pass]
level: practitioner
status: draft
description: "Use MSAA cheaply on tile-based GPUs: on-tile resolve, transient/memoryless sample attachments, render pass resolve attachments, no blit resolves."
sources: ["https://developer.arm.com/documentation/101897/latest/Fragment-shading/Multisampling", "https://github.com/KhronosGroup/Vulkan-Samples/tree/main/samples/performance/msaa", "https://registry.khronos.org/OpenGL/extensions/EXT/EXT_multisampled_render_to_texture.txt"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MSAA on tile-based GPUs

On tilers, 4x MSAA is nearly free in bandwidth if samples never leave tile memory: the GPU resolves
on chip and writes only the single-sample result. Done wrong, it costs 4x bandwidth.

## 1. Vulkan
- Multisampled colour/depth attachments: `VK_IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT` with
  `LAZILY_ALLOCATED` memory (no backing memory on most tilers).
- Load op CLEAR or DONT_CARE; store op **DONT_CARE** for the MSAA images.
- Add a **resolve attachment** (single-sample) in the same subpass (`pResolveAttachments`, or
  dynamic rendering `resolveImageView` + `resolveMode`) so the resolve happens on tile at the end
  of the pass.
- Depth resolve only if needed (`VK_KHR_depth_stencil_resolve`), otherwise DONT_CARE.
The Khronos Vulkan-Samples "MSAA" sample measures the difference (resolve in render pass vs
`vkCmdResolveImage` afterwards: the latter writes all samples to DRAM first).

## 2. OpenGL ES
- `EXT_multisampled_render_to_texture`: attach a single-sample texture with
  `glFramebufferTexture2DMultisampleEXT(..., samples)`; the driver keeps samples on tile and
  resolves implicitly. Best option on GLES.
- Avoid `glBlitFramebuffer` resolves from a multisampled renderbuffer (writes full sample data).
- Call `glInvalidateFramebuffer` on depth after the pass.

## 3. Metal
MSAA textures with `.memoryless` storage, store action `.multisampleResolve` with a resolve
texture.

## 4. Costs that remain
- Fragment shading is per pixel (unless sample-rate shading), but tile memory per pixel grows with
  samples: tiles may shrink (more tiles, more binning overhead) on some GPUs; 4x is usually the
  sweet spot, 8x rarely worth it.
- Alpha-to-coverage works well with MSAA for foliage.

## Gotchas
- Any pass that later reads the MSAA image (e.g. custom resolve in a later pass) forces sample
  storage to DRAM; do custom resolves in a subpass or via framebuffer fetch.
- Post-processing should operate on the resolved image.

## Verify
- [ ] Bandwidth counters with 4x MSAA close to no-MSAA in the main pass.
- [ ] No vkCmdResolveImage/glBlitFramebuffer in captures for MSAA resolves.
