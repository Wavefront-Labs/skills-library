---
id: computing-software.computer-graphics-engineering.graphics-math.barycentric-coordinates
name: barycentric-coordinates
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-math, barycentric-coordinates, point-in-triangle, attribute-interpolation, edge-functions, wireframe-shader, sv-barycentrics]
level: practitioner
status: verified
description: "Compute and use barycentric coordinates: edge-function and area formulations, point-in-triangle tests, attribute interpolation, hardware barycentrics in shaders."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 22.8", "https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/barycentric-coordinates.html", "https://microsoft.github.io/DirectX-Specs/d3d/Barycentrics.html", "https://registry.khronos.org/vulkan/specs/latest/man/html/BaryCoordKHR.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Barycentric coordinates

**Goal:** locate points relative to triangles and interpolate vertex data correctly — the
basis of rasterisation, ray-triangle hits, mesh sampling and wireframe effects (RTR4 ch. 22).

## 1. Definition
Point P inside triangle (A, B, C): `P = u·A + v·B + w·C`, `u + v + w = 1`. Inside iff all
three are in [0, 1]. Each weight is the ratio of the sub-triangle area opposite that vertex
to the total area.

## 2. Robust computation (2D or 3D)
```cpp
// Christer Ericson, Real-Time Collision Detection §3.4 (works in 3D for P on the triangle's plane)
void barycentric(Vec3 p, Vec3 a, Vec3 b, Vec3 c, float& u, float& v, float& w) {
    Vec3 v0 = b - a, v1 = c - a, v2 = p - a;
    float d00 = dot(v0, v0), d01 = dot(v0, v1), d11 = dot(v1, v1);
    float d20 = dot(v2, v0), d21 = dot(v2, v1);
    float denom = d00 * d11 - d01 * d01;           // ~0 for degenerate triangles: check
    v = (d11 * d20 - d01 * d21) / denom;
    w = (d00 * d21 - d01 * d20) / denom;
    u = 1.0f - v - w;
}
```
2D edge functions (rasterisers): `E_ab(P) = (P - A) × (B - A)`; weights = edge values divided
by twice the signed area. Use a consistent top-left fill rule for pixels exactly on edges.

## 3. Interpolating attributes
`attr(P) = u·attrA + v·attrB + w·attrC`. In screen space after projection this must be
**perspective-correct** (interpolate attr/w and 1/w, then divide) — see perspective-correct
interpolation. Ray-triangle (Möller–Trumbore) returns (v, w) directly in 3D: no correction needed.

## 4. Uniform sampling on a triangle
`r1, r2 ∈ [0,1)`: `su = sqrt(r1); u = 1 - su; v = r2 * su; w = 1 - u - v` — uniform area
distribution (for scattering points/particles on meshes, area lights). Choose triangles with
probability ∝ area.

## 5. Shader barycentrics
- HLSL `SV_Barycentrics` (confirm shader model in the DXC docs), Vulkan `gl_BaryCoordEXT` (`VK_KHR_fragment_shader_barycentric`):
  per-pixel barycentrics for wireframe overlays, custom interpolation, visibility-buffer
  shading.
- Fallback for wireframe: give each vertex of a triangle (1,0,0), (0,1,0), (0,0,1) as an
  attribute (non-indexed or with a geometry shader), edge distance = min component;
  antialias with `fwidth`.

## Gotchas
- Degenerate (zero-area) triangles: denominator ~0 → NaN; skip them.
- Thin triangles lose precision; compute relative to the vertex nearest P or in double.
- Winding/sign conventions differ between libraries (which weight belongs to which vertex) — test.

## Verify
(Computed: vertices give (1,0,0)/(0,1,0)/(0,0,1), centroid 1/3 each, an outside point gives -0.5 weights; the sqrt sampling formula gave means of 1/3 per weight with no negatives over 1e5 samples.)
- [ ] Unit tests: vertices map to (1,0,0)… ; centroid → (1/3,1/3,1/3); outside points get a negative weight.
- [ ] Uniform triangle sampling histogram is flat across the area.
- [ ] Wireframe shader lines constant width with fwidth-based AA.
