---
id: computing-software.computer-graphics-engineering.rendering-techniques.pixel-art-3d-rendering
name: pixel-art-3d-rendering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, npr, pixel-art-3d, low-resolution-rendering, pixel-perfect, camera-snapping, retro-rendering, outlines]
level: practitioner
status: draft
description: "Render 3D scenes as stable pixel art: low-res render targets with integer upscaling, camera texel snapping, pixel-perfect outlines, limited palettes and avoiding shimmer."
sources: ["https://www.youtube.com/watch?v=jguyR4yJb1M", "https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html", "https://t3ssel8r.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pixel art and low-res 3D rendering

## 1. Render small, upscale by integers
- Render the 3D scene into a low-res target (e.g. 320x180 or 640x360) with point sampling and no
  MSAA/TAA; upscale to the window by an integer factor with nearest filtering; letterbox the rest.
- Orthographic camera is typical (isometric/dimetric look); perspective works with care.

## 2. Stop the shimmer: texel snapping
With a moving camera, geometry edges crawl because the pixel grid moves relative to the world.
1. Snap the camera's position to the world-space size of one low-res pixel, in the camera's own
   plane:
```cpp
vec3 camRight = ..., camUp = ...;
float pxWorld = orthoHeight / lowResHeight;
float r = dot(camPos, camRight), u = dot(camPos, camUp);
vec2 snapped = round(vec2(r, u) / pxWorld) * pxWorld;
vec2 remainder = vec2(r, u) - snapped;                 // sub-pixel error
camPosSnapped = camPos + camRight * (snapped.x - r) + camUp * (snapped.y - u);
```
2. Render with the snapped camera, then offset the upscaled image on screen by
   `remainder / pxWorld * upscaleFactor` screen pixels for smooth scrolling.
Rotation still causes shimmer; restrict rotation or accept it (popular 3D pixel-art games keep the
camera angle fixed while panning).

## 3. Pixel-perfect outlines
Edge detection on low-res depth and normals (1-pixel outlines exactly), with separate thresholds for
outer silhouettes (depth) and inner creases (normals); lighten inner edges and darken outer ones for
the hand-made look (t3ssel8r style).

## 4. Shading and palette
- Quantised lighting (cel bands) and limited palettes (posterise or palette LUT) with optional
  ordered dithering on the low-res grid.
- Textures authored at matching texel density (1 texel = 1 screen pixel at default zoom) with point
  sampling and no mipmaps.

## Gotchas
- Non-integer upscale makes some pixels wider: always integer.
- Sub-pixel object movement shimmers as well; snap object positions to the pixel grid for sprites
  and small props, or accept it for smooth motion.
- UI rendered at low res must align to the same grid.

## Verify
- [ ] Panning the camera produces no crawling edges.
- [ ] Every screen pixel block is uniform size at the chosen scale.
