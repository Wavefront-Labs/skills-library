---
id: computing-software.computer-graphics-engineering.graphics-math.spatial-hashing-and-uniform-grids
name: spatial-hashing-and-uniform-grids
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, spatial-structures, spatial-hashing, uniform-grid, neighbour-search, broad-phase, counting-sort]
level: sme
status: draft
description: "Build uniform grids and spatial hashes for neighbour queries: cell sizing, hash functions, counting-sort grids on CPU/GPU, and when to use a BVH instead."
sources: ["https://matthias-research.github.io/pages/tenMinutePhysics/11-hashing.pdf", "https://www.realtimerendering.com/", "https://developer.download.nvidia.com/assets/cuda/files/particles.pdf", "https://www.cs.ucdavis.edu/~amenta/f15/GoodHashFunctions.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Uniform grids and spatial hashing

## 1. When
Many similar-sized objects (particles, boids, SPH, broad-phase for equal-size colliders) and fixed-radius
neighbour queries. Varied sizes or ray queries: use a BVH; sparse huge worlds: hash rather than dense grid.

## 2. Cell size
Cell size = query radius (or the largest object diameter). A query then checks the 3x3x3 cells around the
point. Smaller cells mean more cells per query; bigger means more false candidates.

## 3. Dense counting-sort grid (rebuild every frame, cache friendly)
```cpp
// 1) count
for (i) cellCount[cellIndex(p[i])]++;
// 2) exclusive prefix sum -> cellStart
// 3) scatter
for (i) sorted[cellStart[c] + cursor[c]++] = i;     // c = cellIndex(p[i])
// query: for each of 27 cells, iterate sorted[cellStart[c] .. cellStart[c+1])
```
On GPU: compute cell id per particle, radix sort (id, index) pairs, find cell start/end with a parallel pass
comparing neighbours (NVIDIA particles sample); then reorder particle data by cell for coherent reads.

## 4. Spatial hash (unbounded worlds)
```cpp
int64_t xi = floor(x / h), yi = floor(y / h), zi = floor(z / h);
uint32_t hash = (uint32_t)((xi * 92837111) ^ (yi * 689287499) ^ (zi * 283923481)) % tableSize;
```
Table size ~ 2x number of objects; collisions only cost extra candidates (always do the exact distance test).
Use `floor`, not truncation, so negative coordinates map correctly.

## 5. Dynamic objects spanning cells
Insert into every overlapped cell and dedupe pairs (e.g. only report a pair from the cell containing the min
corner of the overlap), or use a loose grid with cell size 2x the max object size and insert by centre.

## Gotchas
- Integer overflow in cell coordinates for large worlds: use 64-bit or camera-relative grids.
- Hash tables with linked lists per cell thrash caches; the counting-sort layout is faster.
- Clustering (all particles in a few cells) degrades to O(n^2); cap or switch structures.

## Verify
- [ ] Brute-force O(n^2) neighbour list equals the grid result on random tests including negative coords;
  timing scales linearly with n.
