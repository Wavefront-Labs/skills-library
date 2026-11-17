---
id: computing-software.computer-graphics-engineering.graphics-math.reflection-and-mirror-matrices
name: reflection-and-mirror-matrices
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, transforms, reflection-matrix, householder, planar-reflections, mirror-transform, winding-order]
level: practitioner
status: draft
description: "Build reflection transforms: Householder mirror about a plane, reflecting cameras for planar mirrors and water, winding flips from negative determinants, oblique clipping."
sources: ["https://www.realtimerendering.com/", "https://en.wikipedia.org/wiki/Householder_transformation", "https://www.terathon.com/lengyel/Lengyel-Oblique.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reflection and mirror transforms

## Reflection about a plane
Plane `n . x + d = 0` with unit n:
```
R = I - 2 n n^T          (3x3 linear part)
t = -2 d n               (translation)
M = [R t; 0 1]
```
Reflects point p to `p - 2 (n . p + d) n`. `det(R) = -1`.

## Planar mirror/water reflection rendering
1. Reflect the camera: `view_reflected = view * M_reflect` (column-vector convention).
2. Negative determinant flips triangle winding: swap front-face mode (`glFrontFace(GL_CW)`,
   `FrontCounterClockwise` toggle in D3D) or culling will remove the visible faces.
3. Clip geometry below/behind the mirror plane: user clip plane or an **oblique near plane**
   (Lengyel) in the projection matrix.
4. Render to a texture and sample it in screen space on the mirror surface (with distortion for
   water).

## Mirroring meshes
Scaling by -1 on one axis mirrors a model: reverse winding (swap two indices per triangle) and flip
tangent handedness (bitangent sign) for normal mapping.

## Detecting reflections in a transform
`det(upper3x3) < 0` means the transform contains a reflection: needed when decomposing matrices
(choose one axis scale negative) and for winding decisions in a renderer.

## Reflecting vectors
Direction reflection: `r = v - 2 (v . n) n` (GLSL `reflect(v, n)` expects v pointing toward the
surface). Normals reflect with the same R (orthogonal, so inverse transpose = itself).

## Verify
Reflect a point twice: identity. Render a mirror test scene: mirrored text reads backwards, nothing
behind the mirror appears, culling correct.
