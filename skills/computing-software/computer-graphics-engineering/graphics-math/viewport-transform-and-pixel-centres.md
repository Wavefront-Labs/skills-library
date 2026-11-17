---
id: computing-software.computer-graphics-engineering.graphics-math.viewport-transform-and-pixel-centres
name: viewport-transform-and-pixel-centres
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, projection, viewport-transform, pixel-centers, ndc, half-pixel-offset, screen-space]
level: practitioner
status: draft
description: "Map NDC to window coordinates correctly: viewport/depth range formulas per API, pixel-centre conventions (D3D9 half-pixel), y-flip in Vulkan, and screen-to-NDC for picking."
sources: ["https://www.khronos.org/opengl/wiki/Vertex_Post-Processing", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html", "https://learn.microsoft.com/en-us/windows/win32/direct3d10/d3d10-graphics-programming-guide-resources-coordinates"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Viewport transform and pixel centres

## Formulas
`x_w = x0 + (x_ndc + 1) * w / 2`, `y_w = y0 + (y_ndc + 1) * h / 2` (GL, origin bottom-left),
`z_w = n + (f - n) * (z_ndc + 1) / 2` for GL [-1,1] NDC depth (or `z_w = minDepth + z_ndc * (maxDepth - minDepth)`
for D3D/Vulkan [0,1]).

| API | NDC y | Window origin | NDC z |
|---|---|---|---|
| OpenGL | up | bottom-left | [-1,1] (or [0,1] with `glClipControl`) |
| Direct3D 10+ | up | top-left (y flipped in viewport) | [0,1] |
| Vulkan | **down** | top-left | [0,1] |
| Metal | up | top-left | [0,1] |
Vulkan: flip with a negative viewport height (`y = h, height = -h`, core in 1.1) or negate y in the
projection matrix.

## Pixel centres
- Modern APIs (GL, D3D10+, Vulkan, Metal): pixel (i, j) covers [i, i+1); its centre is at i + 0.5.
  `gl_FragCoord.xy` / `SV_Position.xy` are pixel centres (x.5).
- D3D9 had centres at integers: needed the infamous half-pixel offset in full-screen quads; ports of
  old code still carry it and introduce blur.
- Texture sampling: texel i centre at `(i + 0.5) / size` in UV.

## Screen to NDC (picking, unprojection)
```cpp
float x_ndc = 2.0f * (px + 0.5f) / width - 1.0f;
float y_ndc = 1.0f - 2.0f * (py + 0.5f) / height;    // top-left origin mouse coords, y-up NDC
```
Then multiply by `inverse(proj * view)` at z_ndc near/far and divide by w.

## Gotchas
- High-DPI: mouse coordinates in points vs framebuffer pixels; scale by the device pixel ratio.
- Sub-viewports: subtract the viewport origin before normalising.

## Verify
Render a 1-pixel-wide line at x = 0.5 in a full-screen orthographic projection: it must cover exactly
one pixel column with no blur.
