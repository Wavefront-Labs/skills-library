---
id: computing-software.computer-graphics-engineering.gpu-optimisation.dynamic-resolution-scaling
name: dynamic-resolution-scaling
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, fill-rate, fragment-bound, dynamic-resolution, drs, gpu-time-budget, upscaling, viewport-scaling, frame-budget]
level: advanced
status: draft
description: "Hold frame rate with dynamic resolution scaling: GPU-time feedback controller, rendering into a sub-rectangle of full-size targets, upscaling with TAA/FSR."
sources: ["https://www.intel.com/content/www/us/en/developer/articles/technical/dynamic-resolution-rendering-article.html", "https://gpuopen.com/fidelityfx-superresolution-2/", "https://docs.unrealengine.com/5.3/en-US/dynamic-resolution-in-unreal-engine/", "Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 18"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic resolution scaling

**Goal:** keep GPU frame time under budget in heavy scenes by lowering internal resolution
automatically, invisibly to the player.

## 1. Controller
Measure GPU frame time with timestamps (results from 1–3 frames ago) and adjust the scale:
```cpp
float headroom = targetMs * 0.95f - gpuMs;            // keep ~5% margin
scale += (headroom / targetMs) * gain;                 // gain ~0.1-0.3; proportional control
scale = clamp(scale, minScale /*0.6*/, 1.0f);
// increase slowly, decrease fast: limit upward step per frame to avoid oscillation
```
Smooth GPU time (moving median) to ignore single spikes; decrease immediately on large
overruns. Scale per axis (area ∝ scale²) or quantise to steps (e.g. 2–5% increments) to help
caching and avoid shimmer.

## 2. Render at variable size without reallocating
Allocate render targets at full (max) resolution once; render into a sub-rectangle via
viewport/scissor of `scale × size`. All screen-space passes must use the active rectangle:
- UV computations: `uv * renderSize / targetSize`, clamp sampling to the valid region (avoid
  bilinear reads outside the rect).
- History buffers (TAA) and motion vectors in the same scaled space.
Reallocation per change causes hitches and memory churn — avoid.

## 3. Upscale to display
- Temporal upscalers (TAA-U, FSR 2/3, DLSS, XeSS) take jittered low-res input and output full
  res; they are designed for varying input sizes (pass the current render size each frame).
- Spatial (FSR 1, bilinear + sharpen) as a cheap fallback.
- Render **UI at native resolution** after upscaling; some post effects (film grain, final
  sharpening) too.

## 4. What to scale
Only resolution-dependent passes (G-buffer, lighting, post) benefit; shadow maps and compute
simulations don't. If the bottleneck is geometry or CPU, DRS won't help — check scaling
actually reduces GPU time in profiles.

## Gotchas
- Mip bias: lower render resolution needs negative texture LOD bias
  (`log2(renderWidth/displayWidth)`) or textures get blurry beyond the upscale.
- Screen-space effects with pixel-sized kernels (SSAO radius, bloom) must scale parameters with
  resolution to look consistent.
- Oscillation between scales is visible as breathing sharpness — tune hysteresis.

## Verify
- [ ] Stress scene: frame time stays within budget; scale responds within a few frames.
- [ ] No visible pumping in a static scene (scale stable).
- [ ] UI crisp; screen-space effects consistent across scales.
