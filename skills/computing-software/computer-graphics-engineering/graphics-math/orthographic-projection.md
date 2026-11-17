---
id: computing-software.computer-graphics-engineering.graphics-math.orthographic-projection
name: orthographic-projection
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, projection, orthographic-projection, shadow-map-projection, clip-space, depth-range, 2d-ui-projection]
level: practitioner
status: verified
description: "Build and use orthographic projection matrices: OpenGL vs Vulkan/D3D depth ranges, pixel-exact 2D UI, directional-light shadow fitting, and zoom."
sources: ["https://www.songho.ca/opengl/gl_projectionmatrix.html", "https://www.realtimerendering.com/", "https://registry.khronos.org/vulkan/specs/1.3/html/vkspec.html#vertexpostproc-coord-transform", "https://learn.microsoft.com/en-us/windows/win32/direct3d9/directly-mapping-texels-to-pixels"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Orthographic projection

## 1. Matrix
Maps the box [l,r] x [b,t] x [-n,-f] (right-handed view space, camera looks down -Z) to clip space, w = 1.
```text
OpenGL (z in [-1,1]):                   Vulkan/D3D (z in [0,1]):
| 2/(r-l)  0        0         -(r+l)/(r-l) |   | 2/(r-l) 0       0         -(r+l)/(r-l) |
| 0        2/(t-b)  0         -(t+b)/(t-b) |   | 0       2/(t-b) 0         -(t+b)/(t-b) |
| 0        0       -2/(f-n)   -(f+n)/(f-n) |   | 0       0       -1/(f-n)  -n/(f-n)     |
| 0        0        0          1           |   | 0       0       0          1           |
```
glm: `glm::ortho` uses [-1,1] unless `GLM_FORCE_DEPTH_ZERO_TO_ONE` (checked in glm's matrix_clip_space.hpp); `orthoRH_ZO` and `orthoRH_NO` select the range explicitly.
Vulkan's clip-space Y points down: flip with a negative viewport height or negate `[1][1]`.

## 2. Depth is linear
Unlike perspective, ortho depth is linear in view z, so precision is uniform; reversed-Z gives little benefit.
Near can be negative (objects behind the camera position still render) - handy for shadow boxes.

## 3. Pixel-exact 2D/UI
`ortho(0, width, height, 0, -1, 1)` (top-left origin). Sprites align to pixels if vertex positions are integers
and textures are sampled at texel centres. D3D9 needed a half-pixel offset; D3D10+, GL and Vulkan do not.

## 4. Directional-light shadows
- Fit the ortho box to the view frustum slice (cascade) in light space; use a bounding sphere for a
  rotation-stable size.
- Snap the box origin to shadow-texel increments `(r-l)/shadowRes` to stop shimmering when the camera moves.
- Extend near toward the light to include off-screen casters (or use depth clamp / pancaking).

## 5. Orthographic camera zoom
Scale l,r,b,t by the zoom factor, keeping aspect: `halfH = size; halfW = size * aspect`. Moving the camera
along its view axis does not change apparent size.

## Gotchas
- Using the GL matrix on Vulkan/D3D maps half the depth range outside [0,1] and clips geometry.
- Lighting/specular code that assumes a camera position breaks: view direction is constant `-Z` in ortho.

## Verify
(Computed: for l,r,b,t,n,f = -2,2,-1,1,1,10 the GL matrix maps z=-n,-f to -1,+1 and the ZO matrix maps them to 0,1.)
- [ ] Unit test: box corners map to clip-space cube corners for the target API; a 1-px line at integer
  coordinates covers exactly one pixel row.
