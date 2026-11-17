---
id: computing-software.computer-graphics-engineering.graphics-math.unproject-screen-to-world-rays
name: unproject-screen-to-world-rays
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, projection-matrix, unproject, screen-to-world, inverse-view-projection, ndc, depth-reconstruction, reversed-z, mouse-ray]
level: practitioner
status: draft
description: "Convert screen pixels to world-space rays and positions: pixel to NDC conventions per API, inverse view-projection unprojection."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 4.7", "https://www.khronos.org/opengl/wiki/Compute_eye_space_from_window_space", "https://mynameismjp.wordpress.com/2009/03/10/reconstructing-position-from-depth/", "https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-resources-coordinates"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unproject screen points to world rays

**Goal:** mouse picking rays, world positions from the depth buffer for deferred lighting /
SSAO / decals, and screen-space effects — correct for every API convention (RTR4 §4.7).

## 1. Pixel → NDC
```cpp
// pixel (px, py) with origin top-left, size (W, H); sample at pixel centre
float x_ndc = 2.0f * (px + 0.5f) / W - 1.0f;
float y_ndc = 1.0f - 2.0f * (py + 0.5f) / H;     // flip: NDC y up (GL, D3D). Vulkan NDC y points DOWN: no flip
```
Depth range in NDC: OpenGL [-1, 1]; D3D/Vulkan/Metal/WebGPU [0, 1]; reversed-Z swaps near (1)
and far (0).

## 2. Ray from the camera
```cpp
Mat4 invVP = inverse(proj * view);
Vec4 pNear = invVP * Vec4(x_ndc, y_ndc, zNearNdc, 1);   // zNearNdc = 0 (D3D/VK), -1 (GL), 1 (reversed-Z)
Vec4 pFar  = invVP * Vec4(x_ndc, y_ndc, zFarNdc, 1);    // far = 1 (or 0 reversed-Z)
Vec3 a = pNear.xyz / pNear.w, b = pFar.xyz / pFar.w;
Ray r{ a, normalize(b - a) };
```
With an infinite far plane, unprojecting z_far gives w ≈ 0 — use the near point and the camera
position (perspective) to form the direction instead. Orthographic cameras: origins differ per
pixel, direction is constant (camera forward).

## 3. World position from depth (shader)
```glsl
float d = texelFetch(depthTex, pix, 0).r;              // raw device depth
vec4 ndc = vec4(uv * 2.0 - 1.0, d, 1.0);               // D3D/VK depth [0,1]; GL: d*2-1
ndc.y = -ndc.y;                                         // only if uv origin is top-left and API NDC y is up
vec4 wp = invViewProj * ndc; vec3 world = wp.xyz / wp.w;
```
Cheaper and more precise for view-space work: reconstruct linear view depth from the projection
terms (`viewZ = P[3][2] / (d - P[2][2])` form for standard projections) and multiply by a
per-pixel view ray interpolated from frustum corners.

## 4. Precision
- Large world coordinates: unproject into camera-relative space (view matrix without
  translation), add the camera position in double on the CPU if needed.
- Use the same jittered/unjittered projection the depth was rendered with (TAA jitter!).

## Gotchas
- Mixing row/column-major or multiplying in the wrong order yields rays that are almost right
  near the centre and wrong at the edges — test corners.
- Forgetting the perspective divide by w.
- Viewport offsets (split-screen, canvas not at origin) must be subtracted before NDC.

## Verify
- [ ] Clicking each screen corner hits the expected world points in a test grid scene.
- [ ] Reconstructed positions re-project to the same pixel (round-trip error < 0.01 px).
- [ ] Tests run with reversed-Z and with GL vs D3D conventions if both are supported.
