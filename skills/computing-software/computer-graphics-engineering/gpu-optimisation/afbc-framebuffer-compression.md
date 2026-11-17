---
id: computing-software.computer-graphics-engineering.gpu-optimisation.afbc-framebuffer-compression
name: afbc-framebuffer-compression
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, tile-based-gpus, afbc, framebuffer-compression, arm-mali, bandwidth, ubwc, mobile-gpu]
level: practitioner
status: draft
description: "Benefit from Arm Frame Buffer Compression (AFBC): qualifying formats and usages, Vulkan/GLES conditions that disable it, and verifying with counters."
sources: ["https://developer.arm.com/documentation/101897/latest/Buffers-and-textures/AFBC-textures", "https://developer.arm.com/Architectures/Arm%20Frame%20Buffer%20Compression", "https://developer.qualcomm.com/sites/default/files/docs/adreno-gpu/developer-guide/gpu/best_practices_texture.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AFBC framebuffer compression

## 1. What it is
Arm Frame Buffer Compression is lossless block compression (16x16 superblocks) used transparently
by Mali GPUs (and display controllers) for render targets and textures. It reduces DRAM bandwidth
for writes and later reads (often 30-50% for typical content), and supports "transaction
elimination"-like savings for constant blocks. Qualcomm's equivalent is UBWC; Apple and desktop GPUs
have their own (lossless DCC).

## 2. Conditions (Mali, per Arm best practices)
AFBC is applied automatically when:
- The format is supported (8-bit UNORM colour formats, depth/stencil on newer Malis, some 10-bit and
  fp16 formats on recent generations).
- The image uses OPTIMAL tiling, is not too small (driver heuristics, e.g. > 16x16).
- Usage flags don't include **STORAGE** (on older Malis) or other incompatible flags; avoid
  `VK_IMAGE_USAGE_STORAGE_BIT` unless needed. Images with `MUTABLE_FORMAT` and incompatible views,
  or certain sample counts, may disable it.
- Images are not written by the CPU (linear mapped).

## 3. Practical rules
- Request only the usage flags you need.
- Keep render targets in 8-bit UNORM where quality allows (RGBA8, RGB10A2 support depends on GPU).
- Compute shader writes to storage images typically disable AFBC on older Mali; use fragment
  shaders for full-screen writes on those GPUs.
- Swapchain images: the compositor and display can consume AFBC directly on supported Android
  devices; use the default swapchain formats.

## 4. Verify
- Arm Streamline / Performance Studio counters: external read/write bandwidth per frame; compare a
  build with STORAGE usage on vs off.
- Some drivers expose AFBC status via `VK_EXT_image_compression_control` (query
  `VkImageCompressionPropertiesEXT`), which also allows requesting fixed-rate (lossy) compression on
  supporting devices.

## Gotchas
- Lossy fixed-rate compression (AFRC) is a separate opt-in feature; don't confuse with lossless AFBC.
- Copying AFBC images to linear buffers forces decompression.

## Verify
- [ ] Bandwidth counters confirm compression (lower write bandwidth) for main render targets.
- [ ] No unnecessary STORAGE usage on colour targets.
