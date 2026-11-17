---
id: computing-software.computer-graphics-engineering.graphics-math.trs-composition-and-matrix-decomposition
name: trs-composition-and-matrix-decomposition
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, transforms, trs-decomposition, matrix-decomposition, polar-decomposition, scene-graph, glm-decompose]
level: sme
status: draft
description: "Compose and decompose transform matrices: TRS order, extracting translation/rotation/scale, negative scale and shear, polar decomposition, and scene-graph pitfalls."
sources: ["https://www.realtimerendering.com/", "https://research.cs.wisc.edu/graphics/Courses/838-s2002/Papers/polar-decomp.pdf", "https://github.com/g-truc/glm/blob/master/glm/gtx/matrix_decompose.inl", "https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#transformations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TRS composition and decomposition

## 1. Compose
Column vectors (OpenGL/glm/glTF): `M = T * R * S`, applied right to left: scale, then rotate, then translate.
Row-vector conventions (DirectXMath) write `S * R * T`. Same transform, transposed storage - check the library.
glTF node local matrix is exactly `T * R * S`; world = parentWorld * local.

## 2. Decompose an affine matrix (no shear)
```cpp
vec3 t = vec3(M[3]);                                    // column 3
vec3 c0 = vec3(M[0]), c1 = vec3(M[1]), c2 = vec3(M[2]);
vec3 s = vec3(length(c0), length(c1), length(c2));
if (dot(cross(c0, c1), c2) < 0) s.x = -s.x;             // negative determinant: reflection
mat3 R = mat3(c0 / s.x, c1 / s.y, c2 / s.z);
quat q = quat_cast(R);                                  // then normalize(q)
```
- A reflection can be assigned to any one axis (or all three); choose one convention and stay consistent.
- Zero scale on an axis makes rotation undefined; guard with an epsilon and keep the previous rotation.

## 3. Shear and non-uniform scale under rotation
A child with rotation under a parent with non-uniform scale produces shear in world space: the world matrix
is no longer TRS. Options:
- **Polar decomposition** `M3 = R * S_sym` (iterate `Q = 0.5 * (Q + inverse(transpose(Q)))` until stable):
  nearest rotation plus symmetric stretch - best for animation blending.
- `glm::decompose` returns scale, rotation, translation, skew and perspective; for perspective-free affine
  matrices the last row is (0,0,0,1).
- Engines like Unity expose "lossyScale" for this reason; avoid non-uniform scale on parents of rotating children.

## 4. Normals
Transform normals by `transpose(inverse(mat3(M)))`; for pure rotation plus uniform scale `mat3(M)` then
normalise is enough. With a negative determinant, flip triangle winding (front face) too.

## Gotchas
- Decomposing then recomposing every frame accumulates error; keep TRS as the source of truth and build
  matrices from it.
- Interpolate decomposed components (lerp T and S, slerp R), never matrices element-wise.

## Verify
- [ ] Round-trip test: random T, R, S (including one negative scale) -> compose -> decompose -> compose
  equals the original within 1e-5.
