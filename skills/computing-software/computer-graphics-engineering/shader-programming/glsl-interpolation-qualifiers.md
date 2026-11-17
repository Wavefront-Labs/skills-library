---
id: computing-software.computer-graphics-engineering.shader-programming.glsl-interpolation-qualifiers
name: glsl-interpolation-qualifiers
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-interfaces, interface-blocks, interpolation-qualifiers, flat-shading, noperspective, centroid, sample-qualifier, provoking-vertex, nointerpolation]
level: practitioner
status: docs-checked
description: "Control how vertex outputs are interpolated: flat for IDs and integers, noperspective for screen-space values, centroid/sample for MSAA edge artefacts, with HLSL equivalents."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://github.com/KhronosGroup/OpenGL-Refpages/blob/main/gl4/html/glProvokingVertex.xhtml", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-struct", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#vertexpostproc-flatshading"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GLSL interpolation qualifiers

**Goal:** each varying arrives in the fragment shader the way the effect needs —
perspective-correct, constant per primitive, or screen-linear — without MSAA edge garbage.

## 1. The qualifiers
| GLSL | HLSL | behaviour | use |
|---|---|---|---|
| (default) `smooth` | `linear` | perspective-correct | UVs, normals, world positions |
| `flat` | `nointerpolation` | value of the **provoking vertex** (HLSL: "do not interpolate") | material/object IDs, integers, per-face data |
| `noperspective` | `noperspective` | linear in screen space | screen-space distances, wireframe edge distance, 2D effects |
| `centroid` | `centroid` | sampled inside the covered area of the pixel | avoid extrapolated UVs at MSAA edges |
| `sample` | `sample` | interpolated at the sample location; per-sample pixel shader execution | MSAA-correct shading (expensive) |
```glsl
// vertex shader
flat out uint vMaterialId;
noperspective out vec3 vEdgeDist;
centroid out vec2 vLightmapUV;
// fragment shader: identical qualifiers on the inputs
flat in uint vMaterialId;
```

## 2. Integers must be flat
Integer and double-precision fragment inputs must be decorated `Flat` (Vulkan SPIR-V rule; GLSL `flat`); in HLSL the only valid modifier for int/uint is `nointerpolation`. Passing an
ID as a float and rounding is a classic precision bug at large values; use `flat uint`.

## 3. Provoking vertex
Flat values come from the primitive's provoking vertex. In OpenGL `glProvokingVertex` selects `GL_FIRST_VERTEX_CONVENTION`
or `GL_LAST_VERTEX_CONVENTION`; in Vulkan the provoking vertex follows the primitive topology (and
`VK_EXT_provoking_vertex` adds a selectable mode). Set it explicitly and test when you port between APIs. Per-face data
needs index buffers arranged so the provoking vertex carries it.

## 4. Centroid for MSAA
With MSAA, pixels partially covered by a triangle may be shaded at the pixel centre outside
the triangle → UVs extrapolate beyond the chart → lightmap/atlas bleeding along edges.
`centroid` fixes it; use it only on the varyings that need it.

## 5. Wireframe example (noperspective)
Geometry/mesh shader outputs barycentric-based edge distances in **pixels**; with
`noperspective`, line width stays constant across depth. With smooth interpolation lines
thicken with distance.

## Gotchas
- In Vulkan, `Flat`, `NoPerspective`, `Sample` and `Centroid` are not allowed on fragment outputs or vertex inputs, and two
  fragment inputs sharing a Location must carry the same such decorations.
- HLSL: `centroid` must be combined with `linear` or `noperspective`; `sample` needs shader model 4.1.
- A `sample`-qualified input (or `SV_SampleIndex` in HLSL) makes the pixel shader run per sample, a big cost.

## Verify
- [ ] Object-ID buffer shows exact IDs (no blended values at triangle interiors).
- [ ] MSAA lightmap edges free of bleeding with centroid on lightmap UVs.
- [ ] Same flat-shaded output across GL and Vulkan backends (provoking vertex matched).

## Checked

Checked 2026-10-26 against Vulkan-Docs interfaces and vertexpostproc chapters (main, 2026-10-23), Microsoft HLSL struct/interpolation modifier page, OpenGL-Refpages glProvokingVertex. Confirmed: HLSL names `linear`, `centroid`, `nointerpolation`, `noperspective`, `sample` and their rules (int/uint only `nointerpolation`; `centroid` combined with linear or noperspective; `sample` SM 4.1 and per-sample execution); Vulkan `Flat`/`NoPerspective`/`Sample`/`Centroid` placement rules and the integer/double-input-must-be-Flat rule (VUID-StandaloneSpirv-Flat-04744); `glProvokingVertex` accepts the first/last vertex conventions. Removed as unconfirmed: default provoking vertex of OpenGL vs D3D, the derivative-accuracy remark, the WebGL2 support claim.

Method: documentation only; no commands were run.
