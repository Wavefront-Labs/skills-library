---
id: computing-software.computer-graphics-engineering.rendering-techniques.smaa-integration
name: smaa-integration
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, antialiasing, smaa, morphological-antialiasing, edge-detection, smaa-t2x]
level: advanced
status: docs-checked
description: "Integrate SMAA 1x/T2x/S2x/4x: edge detection, blend weight and neighbourhood blending passes, area/search textures, presets, sRGB rules."
sources: ["https://github.com/iryoku/smaa"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMAA

SMAA (Subpixel Morphological Antialiasing) is a GPU MLAA implementation for DX9, DX10, DX11
and OpenGL. It handles each edge pattern through look-up tables to limit false positives, so it
does not antialias texture detail that is not a jaggy. The code is MIT licensed.

## 1. Three passes
1. **Edge detection** writes `edgesTex`. Choose luma, colour or depth detection. Depth is
   usually the fastest but may miss edges; luma is more expensive but catches visible edges
   depth misses; colour is usually the most expensive and catches chroma-only edges. The header
   advises luma for a first integration.
2. **Blending weight calculation** reads `edgesTex` and the precomputed `areaTex` and
   `searchTex`, and writes `blendTex`.
3. **Neighbourhood blending** blends each pixel with its neighbours using `blendTex`. Run it on
   every pixel.

Use oversized triangles instead of quads for the fullscreen passes to avoid overshading along
the diagonal.

## 2. Setup (from the header comments of SMAA.hlsl)
- Create two temporal RGBA render targets for `edgesTex` and `blendTex`. In DX10/DX11 the edges
  texture can be RG, although on NVIDIA GPUs an RG target seemed slower. Clear both every
  frame, including alpha.
- `areaTex` is 160x560 two-channel and `searchTex` is 64x16 one-channel (per the dimensions in
  AreaTex.h and SearchTex.h); both ship as C++ headers and DDS files. Load them in the format
  stated in the headers. They can be compressed as BC5 and BC4.
- All samplers: linear filtering and clamp. All reads and writes non-sRGB except the colour
  input and output of the neighbourhood blending pass. If sRGB reads are impossible there, SMAA
  still works but antialiases in gamma space. The colour input to colour/luma edge detection
  should not be sRGB.
- Define the target (`SMAA_HLSL_3`, `SMAA_HLSL_4`, `SMAA_HLSL_4_1`, `SMAA_GLSL_3`,
  `SMAA_GLSL_4`), `SMAA_RT_METRICS` and optionally a preset (`SMAA_PRESET_LOW`, `MEDIUM`,
  `HIGH`, `ULTRA`, described as about 60, 80, 95 and 99 percent of the quality) before including
  the header:
```hlsl
#define SMAA_RT_METRICS float4(1.0 / 1280.0, 1.0 / 720.0, 1280.0, 720.0)
#define SMAA_HLSL_4
#define SMAA_PRESET_HIGH
#include "SMAA.h"
```
- Validate `edgesTex` and `blendTex` against the reference demo's output first.
- Optimise afterwards: initialise a stencil buffer in the edge pass (the code already discards),
  and use the stencil to mask the weight pass.

## 3. Variants
- **SMAA T2x**: subpixel camera jitter ((0.25, -0.25) and (-0.25, 0.25)), SMAA on each jittered
  frame, a temporal resolve with optional CryEngine-style reprojection (`SMAA_REPROJECTION`),
  and per-sample `subsampleIndices` passed to the weight pass.
- **SMAA S2x**: render with MSAA 2x using the standard multisample pattern, separate the
  subsamples, run the full 1x pipeline on each and alpha blend the second run at 0.5.
- **SMAA 4x**: temporally jittered S2x with reprojection of the previous frame.
- Optional predicated thresholding (`SMAA_PREDICATION`) needs an extra texture in the edge pass.
  Do not try T2x with predicated edge detection from the start.
- With motion blur, the edge detection can be merged into it; use depth testing instead of
  stencil then.

## Verify
- [ ] The edges texture shows only geometric/shading edges and not text or texture detail.
- [ ] Results match the reference demo's edge and blend textures.

## Checked

Method: docs-checked 2026-11-09 against github.com/iryoku/smaa (README read in full, SMAA.hlsl header comment lines 1-295 read, AreaTex.h and SearchTex.h size defines). Dropped the performance figure, the "after tone mapping before UI" placement, the GL flip gotcha and the RG8 / RGBA8 format claims not stated in the sources.
