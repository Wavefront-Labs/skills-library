---
id: computing-software.computer-graphics-engineering.shader-programming.triplanar-mapping
name: triplanar-mapping
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, surface-shaders, material-effects, triplanar-mapping, world-space-uv, terrain-texturing, whiteout-blend, procedural-meshes, normal-map-blending]
level: practitioner
status: draft
description: "Texture meshes without UVs (terrain, voxels, procedural rock) with triplanar mapping: sharpened blend weights, correct triplanar normal-map blending, and cost reduction."
sources: ["https://bgolus.medium.com/normal-mapping-for-a-triplanar-shader-10bf39dca05a", "https://developer.nvidia.com/gpugems/gpugems3/part-i-geometry/chapter-1-generating-complex-procedural-terrains-using-gpu", "https://catlikecoding.com/unity/tutorials/advanced-rendering/triplanar-mapping/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Triplanar mapping

**Goal:** stretch-free texturing on cliffs, caves, voxel and procedurally generated meshes
where UVs don't exist or would distort.

## 1. Albedo
```glsl
vec3 triWeights(vec3 n, float sharpness) {
    vec3 w = pow(abs(n), vec3(sharpness));      // sharpness 4-8 narrows blend zones
    return w / (w.x + w.y + w.z);
}
vec3 triplanarAlbedo(vec3 pos, vec3 n, float scale) {
    vec3 w = triWeights(n, 4.0);
    vec3 cx = texture(albedo, pos.zy * scale).rgb;   // projection along X
    vec3 cy = texture(albedo, pos.xz * scale).rgb;   // along Y (top)
    vec3 cz = texture(albedo, pos.xy * scale).rgb;   // along Z
    return cx * w.x + cy * w.y + cz * w.z;
}
```
`pos` in world space (moving objects swim — use object space for those). Different
textures for top vs sides (grass top, rock sides) via `n.y > 0` selection on the Y sample.

## 2. Normal maps (where most implementations are wrong)
Each planar projection has its own implicit tangent frame. Swizzle, blend in tangent
space per plane, then back to world (Ben Golus' "whiteout" method):
```glsl
vec3 tnX = texture(normalMap, pos.zy * scale).xyz * 2.0 - 1.0;
vec3 tnY = texture(normalMap, pos.xz * scale).xyz * 2.0 - 1.0;
vec3 tnZ = texture(normalMap, pos.xy * scale).xyz * 2.0 - 1.0;
tnX = vec3(tnX.xy + n.zy, abs(tnX.z) * n.x);   // whiteout blend with the surface normal
tnY = vec3(tnY.xy + n.xz, abs(tnY.z) * n.y);
tnZ = vec3(tnZ.xy + n.xy, abs(tnZ.z) * n.z);
vec3 w = triWeights(n, 4.0);
vec3 N = normalize(tnX.zyx * w.x + tnY.xzy * w.y + tnZ.xyz * w.z);
```
Also flip X for negative-facing sides (`sign(n.x)` etc.) to avoid mirrored lighting.
Simply blending the three normal map samples as if they were world normals gives wrong,
flat-looking lighting.

## 3. Cost
3 samples per texture × (albedo, normal, ORM) = 9 fetches. Reduce:
- Skip planes with weight < 0.01 (branch — profitable on desktop, test on mobile).
- **Biplanar** mapping (IQ): pick the two dominant axes only → 2 samples.
- Stochastic/dithered single-plane selection + TAA.

## Gotchas
- Mipmapping is fine (UVs are continuous per plane), but anisotropic filtering matters at
  grazing angles on the planes.
- Large world coordinates lose precision → texture jitter far from origin; use
  camera-relative or tile-local positions.
- Repetition is very visible on large terrain: mix scales or add noise-based variation.

## Verify
- [ ] No stretching on vertical cliffs; blend seams not visible at 45° slopes.
- [ ] Lighting with triplanar normals matches a UV-mapped reference on a sphere.
- [ ] Texture fetch count/GPU time measured; optimisation applied if over budget.
