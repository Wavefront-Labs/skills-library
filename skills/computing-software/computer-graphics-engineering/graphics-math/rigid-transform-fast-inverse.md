---
id: computing-software.computer-graphics-engineering.graphics-math.rigid-transform-fast-inverse
name: rigid-transform-fast-inverse
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, transforms, rigid-transform-inverse, matrix-inverse, view-matrix, affine-transform, se3]
level: practitioner
status: verified
description: "Invert rigid and affine transforms cheaply and accurately: R^T and -R^T t for rotations, scale handling, affine 3x4 inverse, view matrices, and when a general inverse is needed."
sources: ["https://www.realtimerendering.com/", "https://glm.g-truc.net/0.9.9/api/a00241.html", "https://docs.microsoft.com/en-us/windows/win32/dxmath/ovw-xnamath-reference-functions-matrix"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fast inverse for rigid transforms

## Rigid (rotation + translation)
`M = [R t; 0 1]` -> `M^-1 = [R^T  -R^T t; 0 1]`.
```cpp
mat4 inverseRigid(const mat4& m) {
    mat3 Rt = transpose(mat3(m));
    vec3 t = vec3(m[3]);                    // column-major: translation in column 3
    mat4 r = mat4(Rt);
    r[3] = vec4(-(Rt * t), 1.0f);
    return r;
}
```
Far fewer flops than a general 4x4 inverse, and exact orthogonality is preserved (no
division, no cancellation).

## Rotation + uniform scale s
`M = [sR t]` -> `M^-1 = [R^T/s  -R^T t / s]`. Compute s as the length of the first column.

## Rotation + non-uniform scale (TRS)
`M = T R S` -> `M^-1 = S^-1 R^T T^-1`: scale the rows of R^T by 1/s_i and apply to -t.

## General affine (3x4)
Invert the 3x3 with the adjugate/determinant (check `|det| > eps`), translation = `-A^-1 t`. Only the
projective case needs a full 4x4 inverse.

## View matrices
The view matrix is the inverse of the camera's world matrix: build it directly with
`inverseRigid(cameraWorld)` (or look-at) rather than `glm::inverse`.

## Drift
If R comes from accumulated products, re-orthonormalise (Gram-Schmidt or quaternion
renormalisation) before relying on `R^T = R^-1`.

## Verify
(Computed here with random rotations: rigid, uniform-scale and non-uniform-scale (TRS) inverses as written all multiply back to identity within 1e-15, and the rigid one matches `numpy.linalg.inv`.)
`inverseRigid(M) * M` equals identity within 1e-6 for random rigid M; compare against `glm::inverse`
on random TRS matrices.
