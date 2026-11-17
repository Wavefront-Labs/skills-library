---
id: computing-software.computer-graphics-engineering.gpu-optimisation.render-scale-and-checkerboard-rendering
name: render-scale-and-checkerboard-rendering
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, fragment-cost, checkerboard-rendering, render-scale, dynamic-resolution, temporal-reconstruction, upscaling, console-rendering]
level: advanced
status: draft
description: "Lower shading cost via render scale: fixed and dynamic resolution, checkerboard rendering with MSAA sample tricks or ID buffers, and temporal reconstruction."
sources: ["https://www.gdcvault.com/play/1022990/Rendering-Rainbow-Six-Siege", "https://www.gdcvault.com/play/1024709/4K-Checkerboard-in-Battlefield-1", "https://advances.realtimerendering.com/s2016/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Render scale and checkerboard rendering

## 1. Render scale
Render the 3D scene at a fraction of output resolution (e.g. 0.67-0.85 per axis) and upscale.
Shading cost scales with pixel count (0.75^2 = 56%). Dynamic resolution adjusts the scale per frame
from GPU timing to hold frame rate (see dynamic resolution scaling skill).

## 2. Checkerboard rendering (CBR)
Shade half the pixels each frame in a checkerboard pattern, alternating every frame; reconstruct the
missing half from the previous frame (reprojected) and spatial neighbours.
- **MSAA trick** (Rainbow Six Siege, PS4 Pro titles): render at half resolution (e.g. 1920x2160 for
  4K... or quarter res with 2x MSAA) with programmable sample positions so the samples land on a
  checkerboard of full-res pixel centres; shading runs per pixel-pair but depth/IDs at full
  checkerboard res.
- **ID buffer** (PS4 Pro hardware feature): per-sample object/primitive IDs at full res guide the
  reconstruction to avoid mixing edges between objects.
- Reconstruction: for missing pixels, use reprojected history if valid (velocity, depth/ID match);
  otherwise interpolate from the 4 neighbours, with edge-directed weighting.
- Combine with TAA for stability.

## 3. Costs and artefacts
- Saves ~40-50% of shading; G-buffer and some passes still at checkerboard resolution.
- Artefacts: sawtooth/dithering on fast motion, transparency and particles (no reliable history),
  thin features.
- Post-process passes must handle the checkerboard layout or run after reconstruction.

## 4. Today
Temporal upscalers (FSR 2+, DLSS, XeSS, TSR) generally outperform CBR at similar cost and are
simpler to integrate; CBR remains relevant on consoles with existing pipelines or where ML upscalers
aren't available.

## Gotchas
- Sample position programming APIs differ (D3D12 `SetSamplePositions`, Vulkan
  `VK_EXT_sample_locations`); not universally supported on PC.
- UI must render at full output resolution after reconstruction.

## Verify
- [ ] A/B against native: artefacts acceptable in motion tests; GPU savings measured.
- [ ] Compare with a temporal upscaler at the same cost before committing to CBR.
