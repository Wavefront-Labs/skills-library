---
id: creative-arts.animation.blender.gpu-out-of-memory
name: gpu-out-of-memory
category: creative-arts
field: animation
product: blender
tags: [blender, gpu, gpu-out-of-memory, out-of-memory, vram, render-optimization, cycles]
level: practitioner
status: docs-checked
description: "Fix Cycles out-of-GPU-memory errors: texture size limits, Simplify, tile size, texture cache, persistent data, culling, memory fallback, NVLink and CPU fallback."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/simplify.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# gpu-out-of-memory

Goal: get a scene that fails with an out-of-memory error on the GPU to render there.

## See where the memory goes

- Watch the GPU's memory in the vendor's monitor (`nvidia-smi`, `rocm-smi`, Task Manager > GPU) during scene sync, and close other GPU users (a second Blender, a rendered viewport, a browser).
- The manual's own hint: image textures are the usual cost. Uncompressed, 8k, 4k, 2k and 1k textures take about 256 MB, 64 MB, 16 MB and 4 MB each.
- Other likely consumers: subdivision, hair and particles, volumes, and large render buffers with many passes.

## Fixes in order

1. **Simplify** (Render Properties > Simplify, tick it): the Render settings include **Max Subdivision**, **Child Particles** and **Texture Size Limit** (scales textures down so none is larger than the chosen value). Texture Resolution scales image textures down too.
2. **Texture Cache** (Performance > Texture Cache): uses tiled, mipmapped `.tx` files so only the needed tiles and resolutions load. Costs a small render-speed hit and disk space. Use Generate, or Auto Generate.
3. **Tile Size** (Performance > Memory, default 2048): tiles are cached to disk while rendering; lowering to 1024 or 512 reduces memory, typically at a small performance cost.
4. Turn **Persistent Data** off (Performance > Final Render). It keeps render data in memory after a render.
5. Cull what the camera cannot see: Simplify > Culling > Camera Cull and Distance Cull.
6. Reduce volume detail (Simplify > Viewport > Volume Resolution only affects the viewport), and use smaller textures.
7. On NVIDIA cards linked by NVLink, enable Preferences > System > Distribute Memory Across Devices.

## Host memory fallback

With CUDA, OptiX, HIP and Metal devices, if GPU memory is full Blender automatically tries to use system memory. That has a performance impact but usually still beats CPU rendering. Reduce memory rather than relying on it.

## Last resort

Render that shot on CPU, where system RAM is usually much larger than VRAM. Keep settings the same.

## Verify

The shot renders on the GPU with the Device still set to GPU Compute and no memory error, after any Simplify limits are removed again for finals if quality matters.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: Simplify names (Max Subdivision, Child Particles, Texture Resolution, Texture Size Limit, Camera Cull, Distance Cull), Tile Size under Performance > Memory with default 2048 and 1024/512 advice, Texture Cache and Persistent Data, memory fallback list (CUDA, OptiX, HIP, Metal), Distribute Memory Across Devices for NVLink, the texture size memory figures.
Removed as unconfirmed: the exact error strings, the old Use Tiling checkbox (not in the 5.2 panel), instance-cost claims, a 90 percent peak-memory rule, and the claim that CPU and GPU results match within noise.
Method: documentation only; no commands were run.
