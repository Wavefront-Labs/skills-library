---
id: computing-software.computer-graphics-engineering.gpu-optimisation.tbdr-architecture-and-hidden-surface-removal
name: tbdr-architecture-and-hidden-surface-removal
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, tile-based-gpus, tbdr, hidden-surface-removal, tile-based-rendering, mobile-gpu, forward-pixel-kill, apple-gpu]
level: practitioner
status: draft
description: "Understand tile-based deferred rendering GPUs: binning and tiling phases, on-chip tile memory, hidden surface removal (PowerVR HSR, Apple, Mali FPK) and what breaks it."
sources: ["https://developer.apple.com/documentation/metal/tailor_your_apps_for_apple_gpus_and_tile-based_deferred_rendering", "https://developer.arm.com/documentation/102662/latest/", "https://docs.imgtec.com/starter-guides/powervr-architecture/html/index.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TBDR architecture and hidden surface removal

## 1. Two phases
1. **Binning (geometry) phase**: all vertex shading for the render pass; transformed primitives are
   sorted into screen tiles (16x16 or 32x32 px) and written to a parameter buffer in memory.
2. **Rendering (fragment) phase**: per tile, rasterise and shade only that tile's primitives,
   with colour/depth kept in fast on-chip **tile memory**; at the end write (store) the results
   once to DRAM.
Bandwidth for depth testing, blending and MSAA stays on chip: the reason tilers are power-efficient.

## 2. Hidden surface removal
- **PowerVR HSR / Apple GPUs (TBDR)**: per tile, the hardware resolves visibility for all opaque
  primitives before shading, so each pixel is shaded once regardless of draw order (perfect
  overdraw removal for opaque geometry).
- **Arm Mali Forward Pixel Kill (FPK)**: fragments in flight are killed if a later opaque fragment
  covers them; order still matters somewhat - sort front to back.
- **Adreno**: low-resolution Z (LRZ) pass for early rejection; binning or direct mode per pass.

## 3. What disables HSR/FPK
- `discard`/alpha test, shader depth writes, alpha blending, and (on some GPUs) per-fragment side
  effects (storage writes) - these primitives must be shaded in order.
- Draw opaque first, then alpha-tested, then blended. Prefer alpha blending over alpha test for
  small overlay effects on PowerVR/Apple where discard is particularly costly.

## 4. Implications for app design
- Render passes are the unit of work; a pass's loads/stores dominate bandwidth (see load/store ops
  skill).
- Don't sample a render target in the same frame it's produced unless necessary (forces a store
  and a new pass); use subpasses/framebuffer fetch.
- Geometry cost is paid twice in bandwidth (write and read of the parameter buffer): see binning
  cost.

## Gotchas
- A depth prepass is usually unnecessary on HSR GPUs and can be a net loss (extra geometry pass).
- `glClear` at pass start is free (it's a load op); clearing mid-pass with a quad is not.

## Verify
- [ ] Overdraw counters (Arm Streamline, Xcode) show near 1x for opaque geometry.
- [ ] Alpha-tested materials limited and drawn after opaques.
