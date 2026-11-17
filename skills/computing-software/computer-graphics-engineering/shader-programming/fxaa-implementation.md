---
id: computing-software.computer-graphics-engineering.shader-programming.fxaa-implementation
name: fxaa-implementation
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, post-processing-shaders, fxaa, antialiasing, luma-edge-detection]
level: practitioner
status: draft
description: "Integrate FXAA 3.11 as a post-process: luma input, quality presets, where it goes relative to tone mapping and UI, and its blur/temporal limits."
sources: ["https://developer.download.nvidia.com/assets/gamedev/files/sdk/11/FXAA_WhitePaper.pdf", "https://github.com/NVIDIAGameWorks/GraphicsSamples/blob/master/samples/es3aep-kepler/FXAA/assets/shaders/FXAA.h"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FXAA

## 1. Pipeline placement
Scene (HDR) -> tone mapping -> **FXAA on LDR, gamma-encoded colour** -> UI. FXAA keys on
perceptual luma; running it on linear HDR misses edges and over-blurs highlights.

## 2. Luma
Either store luma in alpha in the tone-map pass:
```glsl
outColor = vec4(ldr, dot(ldr, vec3(0.299, 0.587, 0.114)));   // FXAA_GREEN_AS_LUMA 0
```
or compile with `FXAA_GREEN_AS_LUMA 1` and use green directly (slightly lower quality, no extra
work).

## 3. Call
```glsl
#define FXAA_PC 1
#define FXAA_GLSL_130 1
#define FXAA_QUALITY__PRESET 12          // 10-15 fast/low, 20-29 more search steps, 39 max
#include "Fxaa3_11.h"
vec4 c = FxaaPixelShader(uv, vec4(0), tex, tex, tex, 1.0 / resolution, vec4(0), vec4(0), vec4(0),
                         0.75,   // subpix: 0 sharp .. 1 soft
                         0.166,  // edgeThreshold: 0.125 high quality, 0.25 fast
                         0.0833, // edgeThresholdMin: skip dark areas
                         0, 0, 0, vec4(0));
```
Sample with bilinear filtering and clamp-to-edge; FXAA relies on filtered half-pixel taps.

## 4. Limits
- Spatial only: shimmering on moving thin geometry stays; TAA or MSAA handles temporal aliasing.
- Blurs text and fine texture detail: apply before UI and keep `subpix` around 0.5-0.75.
- Cost roughly 1 ms at 4K on low-end GPUs; cheaper than SMAA, softer than it.

## Gotchas
- Wrong `rcpFrame` (1/resolution) scale ruins edge search; recompute on resize.
- Running FXAA twice (engine plus post stack) double-blurs.

## Verify
- [ ] Toggle FXAA on a stair-stepped edge capture; UI text stays sharp.
