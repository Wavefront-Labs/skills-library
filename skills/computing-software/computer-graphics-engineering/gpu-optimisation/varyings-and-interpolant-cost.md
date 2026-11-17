---
id: computing-software.computer-graphics-engineering.gpu-optimisation.varyings-and-interpolant-cost
name: varyings-and-interpolant-cost
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, shader-optimisation, varying-count, interpolants, varying-packing, flat-interpolation, tile-based-gpus, mobile-gpu]
level: practitioner
status: draft
description: "Reduce varying cost: packing interpolants, fp16 varyings, flat and noperspective modes, and binning bandwidth on tile-based GPUs."
sources: ["https://developer.arm.com/documentation/101897/latest/Vertex-shading/Attribute-precision", "https://gpuopen.com/learn/rdna-performance-guide/", "https://developer.apple.com/documentation/metal/gpu_programming_techniques"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Varyings and interpolant cost

## 1. Where the cost is
- **Tile-based GPUs** (Mali, Adreno, Apple, PowerVR): the vertex shader output for every vertex is
  written to memory during binning and read back per tile. Each varying adds bandwidth
  proportional to vertex count. Mali Offline Compiler shows this as varying (V) cycles.
- **Immediate-mode desktop GPUs**: interpolation happens per pixel (AMD: in the shader with
  `v_interp` instructions; NVIDIA: attribute interpolation units). Many interpolants cost ALU and
  LDS/parameter cache space and can limit occupancy.

## 2. Reduce count
- Pack scalars into vec4s; two vec2 UVs into one vec4.
- Derive instead of pass: view vector = `camPos - worldPos` in the FS from one varying position;
  bitangent = `cross(N, T) * sign`; screen UV from `gl_FragCoord`.
- Remove debug/unused outputs (compilers remove unused ones only if the FS doesn't declare them).

## 3. Reduce precision
- `mediump`/`half` varyings halve storage and interpolation cost on Mali/Apple.
- Keep `highp` for UVs on large textures (> 1024 texels with sub-texel motion) and world positions.

## 4. Interpolation mode
- `flat` (GLSL) / `nointerpolation` (HLSL) for per-primitive IDs and material indices: no
  interpolation work, and integers require flat anyway.
- `noperspective` when screen-linear is what you want (cheaper on some GPUs, correct for
  screen-space effects).
- `centroid` only where needed (MSAA edge artefacts), it may add cost.

## 5. Vertex count multiplies everything on tilers
Geometry with many tiny triangles amplifies varying bandwidth. LODs reduce it more than shaving
one varying.

## Gotchas
- Moving work from FS to VS adds varyings; on tilers this can be a net loss.
- Packing too aggressively makes shaders unreadable; let the compiler pack locations where
  supported, but verify with the offline compiler.

## Verify
- [ ] Varying cycles (Mali OC) or interpolant count (RGA) reduced.
- [ ] Device bandwidth counters (read bandwidth during fragment phase) drop.
