---
id: computing-software.computer-graphics-engineering.graphics-math.oblique-near-plane-clipping
name: oblique-near-plane-clipping
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, projection, oblique-near-plane, planar-reflections, portals, clip-planes, lengyel]
level: sme
status: draft
description: "Clip planar reflections and portals with an oblique near plane: Lengyel's projection modification, plane in view space, depth precision cost, and API variants."
sources: ["https://terathon.com/lengyel/Lengyel-Oblique.pdf", "https://www.terathon.com/code/oblique.html", "https://docs.unity3d.com/ScriptReference/Camera.CalculateObliqueMatrix.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oblique near-plane clipping

## 1. Problem
Rendering a mirror/water reflection or portal view, geometry behind the mirror plane must be clipped.
User clip planes (`gl_ClipDistance`) cost a varying per vertex and work everywhere; the oblique near plane
replaces the camera's near plane with the mirror plane for free inside the projection matrix.

## 2. Lengyel's method (OpenGL-style [-1,1] depth)
```cpp
// clipPlane: mirror plane in VIEW space (n.x, n.y, n.z, d), normal pointing toward the visible side (away from camera)
void makeOblique(mat4& P, vec4 C) {
  vec4 q;
  q.x = (sign(C.x) + P[2][0]) / P[0][0];     // glm column-major: P[col][row]
  q.y = (sign(C.y) + P[2][1]) / P[1][1];
  q.z = -1.0f;
  q.w = (1.0f + P[2][2]) / P[3][2];
  vec4 c = C * (2.0f / dot(C, q));
  P[0][2] = c.x; P[1][2] = c.y; P[2][2] = c.z + 1.0f; P[3][2] = c.w;   // replace row 3
}
```
General form for [0,1] depth (D3D/Vulkan): `q = inverse(P) * vec4(sign(C.x), sign(C.y), 1, 1)`,
`c = C * (dot(row4(P), q) / dot(C, q))`, and replace row 3 with `c` (no +1 term).
- Transform the world plane to view space with the inverse transpose of the view matrix.
- Ensure the camera is on the negative side of the plane (flip the plane otherwise) or everything is clipped.

## 3. Use in planar reflection
1. Reflect the camera across the mirror plane (reflection matrix), flip the winding (the reflection
   inverts handedness).
2. Build the projection with the oblique near plane at the mirror (offset by a small bias to avoid seams).
3. Render to a texture; sample it in the mirror shader with projective screen coordinates.

## Gotchas
- The far plane gets skewed: depth precision drops, worst when the clip plane is nearly parallel to the
  view direction. Keep scene depth needs modest in reflection passes, or fall back to clip distances.
- Engines' own helpers: Unity `Camera.CalculateObliqueMatrix(planeInViewSpace)`.
- Frustum culling still uses the original frustum plus the mirror plane.

## Verify
- [ ] Objects intersecting the water surface are cut exactly at the plane in the reflection; no clipping of
  objects in front of it when the camera tilts.
