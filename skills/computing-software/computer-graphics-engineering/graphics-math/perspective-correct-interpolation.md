---
id: computing-software.computer-graphics-engineering.graphics-math.perspective-correct-interpolation
name: perspective-correct-interpolation
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, interpolation-math, perspective-correct-interpolation, homogeneous-coordinates, one-over-w, affine-texture-mapping, software-rasterizer]
level: practitioner
status: verified
description: "Interpolate vertex attributes correctly under perspective: why screen-space linear interpolation warps textures, the attribute/w and 1/w method."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 23.1.1", "https://www.comp.nus.edu.sg/~lowkl/publications/lowk_persp_interp_techrep.pdf", "https://www.scratchapixel.com/lessons/3d-basic-rendering/rasterization-practical-implementation/perspective-correct-interpolation-vertex-attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Perspective-correct interpolation

**Goal:** textures and attributes that don't swim or bend on triangles viewed at an angle
(see RTR4's rasterisation chapter).

## 1. The problem
After projection, screen-space x,y are `X/w, Y/w` — a non-linear map. Linear interpolation of
an attribute across the screen ("affine" mapping, PS1-era wobble) is wrong except when w is
constant across the triangle.

## 2. The fix
Quantities that ARE linear in screen space: `attr / w` and `1 / w`. So per pixel:
```cpp
// screen-space barycentrics (b0, b1, b2) from edge functions
float invW = b0 / w0 + b1 / w1 + b2 / w2;
float u = (b0 * u0 / w0 + b1 * u1 / w1 + b2 * u2 / w2) / invW;
```
Equivalently, convert screen barycentrics to perspective-correct ones:
`pb_i = (b_i / w_i) / Σ (b_j / w_j)` and use `pb` for all attributes.
Depth (z/w) is the one value that **is** interpolated linearly in screen space — which is why
the depth buffer stores z/w (and why its precision is non-linear).

## 3. Where you do this by hand
- **Visibility buffer / deferred texturing**: you store triangle IDs, then in a compute or
  full-screen pass reconstruct barycentrics from the pixel position and the three projected
  vertices — compute screen barycentrics, then apply the 1/w correction (and analytic
  derivatives for mip selection: interpolate UV at neighbouring pixels the same way).
- Software rasterisers, CPU occlusion culling, ray-traced primary visibility hybrid.
- Vulkan's `gl_BaryCoordEXT` (VK_KHR_fragment_shader_barycentric) is perspective-correct and `gl_BaryCoordNoPerspEXT` is screen-linear (Vulkan refpage); HLSL has `SV_Barycentrics` (confirm in the DXC docs).

## 4. Intentional non-perspective interpolation
Screen-space effects (wireframe edge distance in pixels, 2D UI on 3D quads in some styles) use
`noperspective` interpolation on purpose.

## Gotchas
- Using clip-space w of 0 or negative (vertices behind the camera) — clip before
  interpolating; the hardware does, your software path must too.
- Mixing perspective-correct barycentrics for some attributes and screen-linear for others
  causes seams in reconstructed G-buffers.

## Verify
(Computed here: for a point on a perspective-projected triangle with world barycentrics 0.3/0.2/0.5, the formula `pb_i = (b_i/w_i)/Σ(b_j/w_j)` recovered exactly 0.3/0.2/0.5 while the screen-space weights were 0.118/0.392/0.490.)
- [ ] Checkerboard on a ground plane at grazing angle: straight lines, no bending (vs reference).
- [ ] Visibility-buffer reconstruction matches forward-rendered UVs within float tolerance.
- [ ] Unit test: interpolated world position at pixel centre re-projects to that pixel.
