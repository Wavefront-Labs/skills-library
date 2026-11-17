---
id: computing-software.computer-graphics-engineering.shader-programming.baked-sdf-volume-textures
name: baked-sdf-volume-textures
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, sdf-raymarching, sdf-volume-texture, jump-flooding, mesh-to-sdf, distance-fields, 3d-textures, compute-shader]
level: advanced
status: draft
description: "Bake meshes into SDF volume textures and generate 2D SDFs with jump flooding: voxel distance computation, sign determination, storage formats and sampling for ray marching."
sources: ["https://www.comp.nus.edu.sg/~tants/jfa.html", "https://docs.unrealengine.com/5.3/en-US/mesh-distance-fields-in-unreal-engine/", "https://github.com/christopherbatty/SDFGen"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Baked SDF volume textures

## 1. When to bake
Analytic SDFs don't exist for arbitrary meshes. Baking a distance field into a 3D texture lets you
ray march, soft-shadow, AO, collide particles and do GI tracing against real assets (UE's Mesh
Distance Fields, Lumen software tracing).

## 2. Mesh -> 3D SDF
1. Choose a bounding box with padding (~2-4 voxels) and a resolution (32^3-128^3 per mesh).
2. For each voxel centre: unsigned distance to the nearest triangle (BVH accelerated; or a GPU
   brute force for small meshes).
3. Sign: count ray-triangle crossings along several rays (odd = inside), or use the angle-weighted
   pseudo-normal of the closest feature. Ray parity is robust to small holes when you vote over
   multiple directions.
4. Store as `R16_FLOAT` or `R8_SNORM` normalised by a max distance (narrow band). 8-bit is enough
   for marching if you keep the band to ~4 voxels and fall back to the bounding box outside.

Tools: SDFGen (Batty, fast sweeping), `mesh-to-sdf` crates, Unity's SDF Bake Tool, UE built-in.

## 3. Jump flooding (JFA) for 2D/3D SDFs on GPU
Seed pixels (e.g. glyph edges or voxelised surface) store their own coordinates; then passes with
step `k = N/2, N/4, ..., 1` each look at 9 (2D) or 27 (3D) neighbours at offset `k` and keep the
nearest seed:
```glsl
for (int y = -1; y <= 1; y++) for (int x = -1; x <= 1; x++) {
    vec2 s = texelFetch(seeds, ivec2(p) + ivec2(x, y) * k, 0).xy;
    if (s.x >= 0.0) { float d = distance(p, s); if (d < best) { best = d; bestSeed = s; } }
}
```
log2(N) passes; one extra pass at k=1 (JFA+1) fixes most errors. Run inside and outside seeds to
get a signed field. Used for outlines, glow, text SDFs and voronoi.

## 4. Sampling
- Trilinear sampling of the texture is continuous; scale distances back to world units.
- Outside the volume, use distance to the box plus the box SDF value as a bound.
- Many meshes: combine into a global low-res SDF clipmap for long-range tracing, per-mesh fields for
  near detail.

## Gotchas
- Thin geometry thinner than a voxel disappears or leaks; increase resolution or thicken.
- Non-watertight meshes make sign determination wrong; parity voting reduces but doesn't remove
  errors.
- Trilinear filtering of a distance field is not an exact SDF; march with step factor < 1 near
  surfaces.

## Verify
- [ ] Slice view of the baked volume shows correct sign (inside negative) everywhere.
- [ ] Ray-marched silhouette matches the raster mesh within one voxel.
