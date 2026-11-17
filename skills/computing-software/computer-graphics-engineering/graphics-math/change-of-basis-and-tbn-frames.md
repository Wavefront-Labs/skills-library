---
id: computing-software.computer-graphics-engineering.graphics-math.change-of-basis-and-tbn-frames
name: change-of-basis-and-tbn-frames
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, transforms, change-of-basis, tbn-matrix, tangent-space, mikktspace, orthonormal-basis]
level: sme
status: draft
description: "Change coordinate bases correctly: basis matrices and their inverses, tangent-space TBN frames with MikkTSpace and handedness, and branchless orthonormal bases."
sources: ["https://www.realtimerendering.com/", "http://www.mikktspace.com/", "https://jcgt.org/published/0006/01/01/", "https://learnopengl.com/Advanced-Lighting/Normal-Mapping"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change of basis and TBN frames

## 1. Basis matrices
If a frame has axes X, Y, Z (unit, expressed in world) and origin O, the matrix with those as columns
`B = [X Y Z]` maps local -> world: `v_world = B * v_local`. World -> local is `inverse(B)`, which for an
orthonormal basis is `transpose(B)`: `v_local = (dot(v,X), dot(v,Y), dot(v,Z))`.
Changing the basis of a transform A (expressed in frame 1) into frame 2: `A' = inverse(B) * A * B`.

## 2. Tangent space (TBN)
```glsl
// vertex shader: tangent.w carries handedness (+1 / -1), as in glTF and MikkTSpace
vec3 N = normalize(normalMatrix * aNormal);
vec3 T = normalize(mat3(model) * aTangent.xyz);
T = normalize(T - dot(T, N) * N);                 // Gram-Schmidt re-orthogonalise
vec3 Bt = cross(N, T) * aTangent.w;
mat3 TBN = mat3(T, Bt, N);                        // tangent -> world
// fragment: n = normalize(TBN * (texture(normalMap, uv).xyz * 2.0 - 1.0));
```
- Bake and render with the same tangent basis: MikkTSpace is the standard (Blender, Substance, Unreal, glTF);
  generate tangents with mikktspace.c if the asset lacks them. Mismatched tangents show seams on mirrored UVs.
- MikkTSpace expects per-pixel bitangent reconstruction `cross(N, T) * w` from *unnormalised interpolated*
  vertex vectors; normalising per vertex or per pixel slightly differently from the baker gives subtle shading
  errors.
- Normal map green channel: OpenGL convention +Y up, DirectX -Y; flip G when importing the other kind.

## 3. Orthonormal basis from one vector
Branchless Duff et al. (2017), robust near all directions:
```glsl
void onb(vec3 n, out vec3 b1, out vec3 b2) {
  float s = n.z >= 0.0 ? 1.0 : -1.0;
  float a = -1.0 / (s + n.z), b = n.x * n.y * a;
  b1 = vec3(1.0 + s * n.x * n.x * a, s * b, -s * n.x);
  b2 = vec3(b, s + n.y * n.y * a, -n.y);
}
```
Use for sampling hemispheres around a normal; avoids the `cross(n, up)` degeneracy.

## Gotchas
- Non-uniform scale: tangents transform with the model matrix, normals with the inverse transpose.
- Mirrored UVs need w = -1; forcing w = +1 inverts lighting on one half.

## Verify
- [ ] glTF NormalTangentMirrorTest sample renders identically to the reference; ONB test over random unit vectors keeps orthonormality within 1e-6.
