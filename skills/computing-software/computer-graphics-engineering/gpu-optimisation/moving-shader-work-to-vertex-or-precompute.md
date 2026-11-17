---
id: computing-software.computer-graphics-engineering.gpu-optimisation.moving-shader-work-to-vertex-or-precompute
name: moving-shader-work-to-vertex-or-precompute
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, shader-optimisation, per-vertex-lighting, precompute, lut-baking, fragment-cost, mobile-optimisation, gouraud]
level: practitioner
status: draft
description: "Cut fragment cost by moving work upstream: per-vertex lighting and interpolation, uniform/CPU precomputation, LUT baking, and when the quality trade-off is acceptable."
sources: ["https://developer.arm.com/documentation/101897/latest/Shader-code/Uniform-subexpressions", "https://developer.apple.com/documentation/metal/gpu_programming_techniques", "https://learnopengl.com/Lighting/Basic-Lighting"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Moving work to the vertex shader or precompute

Pixels outnumber vertices by 10-100x in typical scenes. Work that varies slowly or not at all
across a primitive shouldn't run per pixel.

## 1. Uniform subexpressions
Anything depending only on uniforms (light direction in object space, `inverse(matrix)`, colour
conversions of constants, `sin(time)`) should be computed once on the CPU or in a tiny compute pass.
Mali's offline compiler reports "uniform computation" separately; drivers try to hoist these but
cannot always (e.g. across function calls or with dynamic indexing).

## 2. Per-vertex instead of per-pixel
Good candidates:
- Diffuse ambient/SH lighting (low frequency) on dense meshes.
- Fog factor, distance fades, vertex-colour tints.
- Texture coordinate transforms (scroll, scale, rotate) - also enables the hardware to prefetch
  non-dependent texture reads on some GPUs.
- Point light attenuation for small lights on detailed meshes.
Bad candidates: specular highlights (Gouraud artefacts), anything with normal maps, large
triangles (low-poly floors), shadows.

## 3. Bake into LUTs and textures
- BRDF integration (split-sum DFG LUT), SSS profiles, toon ramps, complex curves (filmic tonemap
  as 1D/3D LUT), noise.
- Trade ALU for a texture fetch only if the shader is ALU-bound; if it is texture/bandwidth-bound,
  computing analytically is cheaper.

## 4. Bake per mesh / per scene
Lightmaps, AO, curvature, thickness maps, vertex AO; precomputed visibility. Static work done once
offline is free at runtime.

## Gotchas
- Interpolated values are linear in screen space (perspective-correct): non-linear functions
  (normalise, pow) computed per vertex then interpolated differ from per-pixel results.
- More varyings cost bandwidth on tilers; moving work to the VS can make you varying-bound.
- Measure before and after: compilers already hoist some of this.

## Verify
- [ ] Offline compiler (Mali OC / RGA / DXC stats) shows lower fragment cycles.
- [ ] Visual diff on representative meshes acceptable at target view distances.
