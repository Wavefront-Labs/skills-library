---
id: computing-software.computer-graphics-engineering.gpu-optimisation.render-pass-load-store-ops-on-tilers
name: render-pass-load-store-ops-on-tilers
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, tile-based-rendering, mobile-gpu, load-store-ops, transient-attachments, memoryless, lazily-allocated, msaa-resolve-on-tile, bandwidth]
level: advanced
status: draft
description: "Save mobile GPU bandwidth with correct render pass load/store ops, transient/memoryless attachments, on-tile MSAA resolve and avoiding pass splits, across Vulkan, Metal and GLES."
sources: ["https://developer.arm.com/documentation/101897/latest/Render-passes", "https://docs.vulkan.org/samples/latest/samples/performance/render_passes/README.html", "https://developer.apple.com/documentation/metal/resource_fundamentals/choosing_a_resource_storage_mode_for_apple_gpus", "https://developer.qualcomm.com/sites/default/files/docs/adreno-gpu/developer-guide/gpu/best_practices_system.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Render pass load/store ops on tile-based GPUs

**Goal:** minimise DRAM traffic on mobile/Apple GPUs, where reading and writing framebuffer
memory costs far more power and time than shading.

## 1. Tile-based rendering in one paragraph
Mali, Adreno, PowerVR and Apple GPUs bin geometry into screen tiles, then render each tile
entirely in on-chip memory. Framebuffer data touches DRAM only at the **start** of a pass
(load) and **end** (store). Your load/store choices decide that traffic.

## 2. Pick ops deliberately
| attachment | load | store |
|---|---|---|
| colour you overwrite fully | `CLEAR` or `DONT_CARE` | `STORE` if used later |
| depth/stencil used only in this pass | `CLEAR` | **`DONT_CARE`** |
| MSAA colour | `CLEAR` | `DONT_CARE` + resolve attachment `STORE` |
| G-buffer consumed in same pass (subpass/framebuffer fetch) | `CLEAR` | `DONT_CARE` |
`LOAD` reads the whole attachment from DRAM — never use it by default. Vulkan:
`VK_ATTACHMENT_LOAD_OP_*` / `STORE_OP_*` (`STORE_OP_NONE` for read-only); Metal:
`MTLLoadAction`/`MTLStoreAction`; GLES: `glInvalidateFramebuffer` before unbind for
don't-care, `glClear` at start for clear.

## 3. Transient / memoryless attachments
Attachments that never leave the tile (depth, MSAA samples, G-buffer in a single pass) need no
DRAM backing:
- Vulkan: image usage `TRANSIENT_ATTACHMENT` + memory `LAZILY_ALLOCATED`.
- Metal: `MTLStorageModeMemoryless`.
Saves memory as well as bandwidth (4x MSAA depth at 1440p ≈ 60 MB otherwise).

## 4. MSAA resolve on tile
Resolve as part of the render pass (resolve attachment / `MTLStoreActionMultisampleResolve`),
never via a separate blit/resolve pass — that writes and reads all samples to DRAM. With this,
4x MSAA is nearly free on tilers.

## 5. Don't split passes unnecessarily
Each pass break = flush tiles to DRAM and reload. Causes: switching render targets mid-frame,
reading back the current attachment, `glFlush`/queries in between, changing framebuffer for a
tiny overlay. Merge passes; use subpasses/`VK_KHR_dynamic_rendering_local_read`/framebuffer
fetch for deferred lighting on-tile.

## Measure
Arm Mobile Studio (Streamline counters: external read/write bytes), Snapdragon Profiler,
Xcode GPU capture (bandwidth per pass). Compare DRAM bytes per frame before/after.

## Gotchas
- Desktop GPUs mostly ignore these hints — the bugs (DONT_CARE on something you needed) show up
  only on mobile: garbage/flicker.
- `glInvalidateFramebuffer` must be called while the FBO is bound, before switching away.

## Verify
- [ ] Per-pass load/store table reviewed; no unintended LOADs.
- [ ] External bandwidth counters reduced on device; frame time/power improved.
- [ ] Transient attachments confirmed lazily allocated (memory reports).
