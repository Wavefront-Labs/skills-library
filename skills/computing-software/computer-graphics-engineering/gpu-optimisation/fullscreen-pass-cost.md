---
id: computing-software.computer-graphics-engineering.gpu-optimisation.fullscreen-pass-cost
name: fullscreen-pass-cost
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, fragment-cost, fullscreen-pass-cost, post-processing, bandwidth, half-resolution, compute-shader, pass-merging]
level: practitioner
status: draft
description: "Estimate and cut the cost of fullscreen passes: bandwidth per pass at resolution, merging passes, half-resolution effects, compute vs pixel shader, and tiler-specific costs."
sources: ["https://developer.arm.com/documentation/101897/latest/", "https://gpuopen.com/learn/rdna-performance-guide/", "https://www.iryoku.com/next-generation-post-processing-in-call-of-duty-advanced-warfare/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fullscreen pass cost

## 1. Back-of-envelope
Bytes per pass = pixels x (bytes read + bytes written).
At 4K (8.3 M px), reading one RGBA16F (8 B) and writing one RGBA16F = 133 MB per pass. At 60 fps
that's 8 GB/s for one simple pass. A chain of 15 post passes approaches 100+ GB/s - a big slice of
a console's or mobile SoC's bandwidth (mobile: 10-50 GB/s total).

## 2. Reduce
- **Merge** passes: tonemap + grading LUT + vignette + grain + chromatic aberration in one uber
  pass; fold exposure into it.
- **Lower resolution** for low-frequency effects: SSAO, bloom, DoF, volumetrics, SSR at half or
  quarter res with depth-aware upsampling.
- **Smaller formats**: R11G11B10F instead of RGBA16F; R8 for masks/AO.
- **Skip** when inactive: no DoF pass when nothing is out of focus; tile classification
  (compute) to run expensive paths only where needed (e.g. motion blur tiles with motion).
- **Fullscreen triangle**, not a quad: avoids the diagonal seam's helper-pixel waste.

## 3. Compute vs pixel shader
- Compute with shared memory wins for neighbourhood filters (blurs, SSAO), reductions, and when
  writing multiple outputs.
- Pixel shaders get framebuffer compression (DCC) on output and ROP-based writes; on tilers they
  can stay on-chip within a render pass (compute always goes to memory).
- On mobile, prefer fragment shaders for simple fullscreen passes; compute often breaks render
  passes and loses tile benefits.

## 4. Tiler specifics
Each fullscreen pass that reads the previous result as a texture forces a full write-out and read-in
of the framebuffer to/from DRAM. Use subpasses / framebuffer fetch for per-pixel operations
(tonemapping right after lighting) to keep data in tile memory.

## Gotchas
- Dependent multi-tap filters at full res (e.g. 13-tap bloom at full res) are expensive; use mip
  chains.
- Overlapping fullscreen passes with async compute can hide them on desktop GPUs; measure overlap.

## Verify
- [ ] Per-pass GPU time and bandwidth listed; total post cost within budget (e.g. < 2 ms at 4K).
- [ ] Half-res versions visually acceptable in A/B.
