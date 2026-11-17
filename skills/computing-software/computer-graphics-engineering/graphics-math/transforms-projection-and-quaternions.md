---
id: computing-software.computer-graphics-engineering.graphics-math.transforms-projection-and-quaternions
name: transforms-projection-and-quaternions
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [graphics-math, linear-algebra, matrices, homogeneous-coordinates, model-view-projection, mvp, row-major, column-major, handedness, perspective-projection, reversed-z, depth-precision, normal-matrix, quaternions, slerp, nlerp, euler-angles, gimbal-lock, glm, directxmath, srgb, linear-colour, colour-spaces, transforms]
level: practitioner
status: draft
description: "The graphics maths that bites in practice: TRS order, row/column-major and handedness conventions, perspective and reversed-Z depth, normal matrices, quaternions and slerp, sRGB."
sources: ["https://www.songho.ca/opengl/gl_projectionmatrix.html", "https://developer.nvidia.com/content/depth-precision-visualized", "Lengyel, Foundations of Game Engine Development, Vol. 1"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transforms, projection and quaternions

**Goal:** get transforms, cameras and rotations right the first time by knowing which
conventions your libraries use and the few formulas that matter.

## 1. Conventions — decide and write them down
Three independent choices; mixing them is the #1 source of "everything is mirrored /
upside down / rotating the wrong way":
- **Vector convention:** column vectors (`v' = M · v`, matrices compose right-to-left;
  GLM, OpenGL docs, most maths texts) vs row vectors (`v' = v · M`, left-to-right;
  DirectXMath, classic D3D docs).
- **Storage order:** column-major vs row-major in memory — a separate question from the
  above. GLSL expects column-major by default; HLSL defaults to column-major packing
  for `cbuffer` matrices too (despite DirectXMath being row-vector) — which is why D3D
  samples often transpose before upload or use `row_major`. Check, don't assume.
- **Handedness and axes:** right-handed (OpenGL, Vulkan conventionally, Blender Z-up,
  glTF Y-up) vs left-handed (D3D conventionally, Unity Y-up, Unreal Z-up). Plus clip-space
  depth range: GL `[-1, 1]`, D3D/Vulkan/Metal `[0, 1]`; Vulkan's clip Y points down.

## 2. Model transforms: scale, then rotate, then translate
With column vectors: `M = T · R · S` (S applied first). Rotating after translating
orbits the object around the origin instead of spinning it in place. Hierarchies:
`world_child = world_parent · local_child`.
- Inverse of a rigid transform (rotation + translation) is cheap:
  `R⁻¹ = Rᵀ`, `t⁻¹ = −Rᵀ·t`. Don't call a general 4×4 inverse per object per frame.
- **Normals** transform by `(M₃ₓ₃⁻¹)ᵀ`, not `M`, when M has non-uniform scale; directions
  use `w = 0`, points `w = 1`.
- View matrix = inverse of the camera's world transform (`lookAt` builds it directly).

## 3. Perspective projection and depth precision
Right-handed, GL-style `[-1,1]` depth, vertical field of view `fovy`, aspect `a`:
```
f = 1 / tan(fovy / 2)
| f/a  0       0              0            |
| 0    f       0              0            |
| 0    0  (far+near)/(near-far)  2·far·near/(near-far) |
| 0    0      -1              0            |
```
After the divide by `w`, depth is proportional to `1/z`: precision is packed near the
near plane. With a standard 24-bit/float depth buffer, pushing **near** out matters far
more than pulling far in (near 0.01 → 0.1 m is a 10× improvement).
**Reversed-Z** (map near → 1, far → 0, with a 32-bit float depth buffer, depth test
`GREATER`, clear to 0) pairs float precision with the 1/z distribution and nearly
eliminates z-fighting even with an infinite far plane. Requires `[0,1]` clip depth (in
GL: `glClipControl(GL_LOWER_LEFT, GL_ZERO_TO_ONE)`).
Use your library's matching variant (`glm::perspectiveRH_ZO`, `XMMatrixPerspectiveFovLH`)
instead of hand-rolling, and say which in a comment.

## 4. Rotations: quaternions
- **Euler angles** are fine for UI/authoring but suffer **gimbal lock** (losing a degree
  of freedom when the middle axis hits ±90°) and interpolate badly. Order matters
  (XYZ ≠ ZYX) and engines differ.
- **Unit quaternion** for rotation by angle θ about unit axis `n`:
  `q = (n·sin(θ/2), cos(θ/2))`. Compose `q = q₂ · q₁` (q₁ first). Rotate vector:
  `v' = q · (v, 0) · q*`, or convert to a matrix once for many vectors.
- `q` and `−q` are the same rotation. Before interpolating, if `dot(q₁, q₂) < 0`, negate one —
  otherwise you take the long way round (the classic 359° spin).
- **slerp** gives constant angular speed; **nlerp** (lerp + normalise) is cheaper,
  commutative, and fine for small steps (animation blending). Re-normalise
  quaternions periodically to fight drift.
- Look-rotation from forward/up and axis-angle helpers exist in every maths library — use them.

## 5. Colour spaces (the maths part)
- sRGB-encoded 8-bit values are **not** linear light. Decode before lighting/blending:
  piecewise curve (`c ≤ 0.04045 ? c/12.92 : ((c+0.055)/1.055)^2.4`); ≈ `c^2.2`.
- Averaging, blending, filtering and lighting must happen in linear space; encode once at
  output. Resizing sRGB images without decoding darkens fine detail.
- Wide-gamut output (Display P3, Rec.2020/HDR) needs a gamut conversion matrix and the
  appropriate transfer function (PQ/HLG for HDR) — beyond plain sRGB.

## Gotchas
- Floating-point precision degrades far from the origin (32-bit float has ~7 significant
  digits: at 100 km, ~1 cm steps). Large worlds use camera-relative rendering or origin rebasing.
- Comparing floats with `==` after transforms; use epsilons.
- Non-uniform scale + rotation in a parent makes a child's transform shear — avoid
  non-uniform scale on parents.

## Verify
- [ ] A one-line convention note (vector, storage, handedness, depth range) exists in the codebase.
- [ ] A test object rotated 90° about +Y ends up where the convention says.
- [ ] Non-uniformly scaled sphere lights correctly (normal matrix).
- [ ] Two quaternions 350° apart interpolate the short way.
- [ ] No z-fighting on distant coplanar-ish surfaces with the chosen near/far/reversed-Z setup.
