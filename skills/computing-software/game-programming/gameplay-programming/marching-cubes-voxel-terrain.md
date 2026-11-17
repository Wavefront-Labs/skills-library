---
id: computing-software.game-programming.gameplay-programming.marching-cubes-voxel-terrain
name: marching-cubes-voxel-terrain
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, procedural-generation, marching-cubes, voxel-terrain, isosurface-extraction, game-programming]
level: practitioner
status: verified
description: "Generate destructible voxel terrain meshes with marching cubes: density fields, edge/triangle tables, vertex interpolation, normals, chunking, seams, LOD and threading."
sources: ["https://paulbourke.net/geometry/polygonise/", "https://developer.nvidia.com/gpugems/gpugems3/part-i-geometry/chapter-1-generating-complex-procedural-terrains-using-gpu"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Marching cubes voxel terrain

**Goal:** smooth editable terrain (caves, digging) generated from a density field, meshed per chunk fast
enough to update while playing.

## Density field
Scalar `d(x,y,z)`: negative = solid, positive = air (or reverse; pick one). Typical:
`d = y - baseHeight + noise3D(p * freq) * amp` plus caves `+ worm/3D noise`. Store per chunk a
(N+1)^3 grid of samples (N = 16 or 32 cells), including one extra layer to share boundary samples.

## Meshing a cell
1. Read 8 corner densities; build an 8-bit index (bit set where corner is solid).
2. `edgeTable[index]` (12-bit mask) says which edges are crossed; `triTable[index]` lists up to 5
   triangles as edge indices (Paul Bourke's tables: an 8-bit index per cell, a 12-bit edge mask and at most 5 triangles per cell, as his page states). Checks run here: the interpolation with da = -0.3, db = 0.9 gives t = 0.25 and a vertex exactly at density 0; central-difference normals on a sphere field matched the analytic radial direction to about 0.0003 per component.
3. For each crossed edge between corners a and b, place the vertex by linear interpolation:
   `t = da / (da - db); v = pa + t * (pb - pa)`.
4. Share vertices per edge across neighbouring cells (edge-indexed cache) to get an indexed mesh and smooth
   normals.

## Normals
Gradient of density by central differences: `n = normalize((d(x+1)-d(x-1), d(y+1)-d(y-1), d(z+1)-d(z-1)))`
— smoother than averaging face normals and consistent across chunk borders (needs one extra sample of
padding around the chunk).

## Chunking and edits
- Chunks of 32^3 cells; edits modify density samples within a brush radius, then remesh affected chunks
  (including neighbours if the brush touches their shared border samples).
- Generate meshes on worker threads (pure function: samples -> vertices/indices); upload on main thread.
- Collision: generate a mesh collider from the same data (cooking can be the bottleneck; do it async if
  the engine allows).

## LOD and seams
Lower LOD chunks sample every 2nd/4th point; seams appear where LODs meet. Solutions: Transvoxel
algorithm (transition cells, Eric Lengyel), skirts, or same-LOD rings near the player.

## Ambiguities
Classic marching cubes has ambiguous cases that can give inconsistent topology (scikit-image's docs say the Lewiner variant, unlike Lorensen et al., resolves ambiguities and guarantees topologically correct results; in a test on a noisy 33^3 field both `method='lorensen'` and `'lewiner'` produced closed meshes, so do not assume holes appear on every field); use the tables from a corrected
variant (MC33 or consistent table choice) or dual methods (Surface Nets, Dual Contouring for sharp
features).

## Gotchas
- Floating-point noise sampled differently per chunk at borders -> cracks; sample by world coordinates
  exactly.
- Memory: store densities as bytes/halfs; many games store only material + density per voxel.

## Verify
- [ ] Dig across chunk borders: no cracks, normals continuous.
- [ ] Remeshing a chunk stays under the frame budget on worker threads.
