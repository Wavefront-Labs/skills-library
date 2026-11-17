---
id: computing-software.computer-graphics-engineering.rendering-techniques.sparse-voxel-octrees
name: sparse-voxel-octrees
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, spatial-structures, sparse-voxel-octree, svo, voxel-dag, voxel-ray-casting, esvo, voxels]
level: advanced
status: draft
description: "Build and ray cast sparse voxel octrees: child masks and pointer layouts, efficient SVO (ESVO) contours, DAG compression of identical subtrees, and GPU traversal."
sources: ["https://research.nvidia.com/publication/2010-02_efficient-sparse-voxel-octrees", "https://www.cse.chalmers.se/~uffe/HighResolutionSparseVoxelDAGs.pdf", "https://github.com/AdamYuan/SparseVoxelOctree"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sparse voxel octrees (SVO)

## 1. Structure
An octree where only non-empty children exist. Typical node: 8-bit **valid mask** (which children
exist), 8-bit **leaf mask**, and a pointer/offset to the first child; children stored contiguously
so `childIndex = popcount(validMask & ((1 << i) - 1))`.
Memory: a 2K^3 scene can fit in hundreds of MB vs 8 GB dense.

## 2. Building
- Voxelise geometry (GPU conservative rasterisation into a fragment list, or CPU triangle-box tests).
- Sort fragments by Morton code; build bottom-up level by level, merging 8 siblings into a parent.
- Store attributes (colour, normal) at leaves; average up the tree for LOD (mipmapping).

## 3. Ray casting
Laine & Karras "Efficient Sparse Voxel Octrees" (ESVO, 2010): stack-based traversal with
parametric ray-box intervals, using a small per-ray stack of parent nodes, PUSH/ADVANCE/POP steps;
mirror the ray so direction components are negative to simplify child ordering. Stop at the level
where the voxel projects to about a pixel (automatic LOD). ESVO also stores **contours** (pairs of
parallel planes per voxel) to approximate surfaces more tightly than cubes.

## 4. DAG compression
Kampe, Sintorn, Assarsson 2013: merge identical subtrees bottom-up (hash nodes by child pointers):
the octree becomes a directed acyclic graph, compressing geometry (not colours) by 10-100x;
colours stored separately with an index scheme (Dado et al. 2016). Enables 128K^3+ resolutions.

## 5. Uses
Voxel cone tracing GI (Crassin's SVO version), voxel game engines, large-scale point/voxel scene
rendering, collision for voxel worlds.

## Gotchas
- Pointer layouts determine cache behaviour; breadth-first child grouping is the norm.
- Editing SVOs/DAGs is expensive (DAG shared subtrees need copy-on-write).
- Precision: deep trees need care with float ray parameters; ESVO uses scaled integer-like tricks.

## Verify
- [ ] Ray-cast image matches rasterised voxels at full resolution.
- [ ] Memory per level reported; DAG compression ratio measured.
