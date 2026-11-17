---
id: computing-software.computer-graphics-engineering.rendering-techniques.virtualized-geometry-cluster-dag
name: virtualized-geometry-cluster-dag
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-lod, virtualized-geometry, nanite, cluster-lod, meshlets, dag, continuous-lod]
level: sme
status: draft
description: "Understand Nanite-style virtualized geometry: cluster DAG of simplified groups, monotonic-error cut selection, page streaming and software raster of tiny triangles."
sources: ["https://advances.realtimerendering.com/s2021/Karis_Nanite_SIGGRAPH_Advances_2021_final.pdf", "https://docs.unrealengine.com/5.3/en-US/nanite-virtualized-geometry-in-unreal-engine/", "https://github.com/zeux/meshoptimizer"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Virtualized geometry (Nanite-style cluster DAG)

Karis et al., SIGGRAPH 2021 Advances. Render film-quality meshes with pixel-sized triangles at a
cost proportional to screen resolution, not source triangle count.

## 1. Build (offline)
1. Split the mesh into **clusters** of ~128 triangles (meshlets) with good locality.
2. Group neighbouring clusters (e.g. 8-32), lock the group's outer boundary edges, **simplify** the
   group to half the triangles, and re-split the result into new clusters.
3. Repeat on the new clusters, forming levels. Because groups change between levels, the hierarchy
   is a **DAG**, not a tree, which avoids locked boundaries accumulating as cracks/seams across levels.
4. Each cluster stores its own simplification error and its parent group's error; enforce
   monotonic errors (parent >= child) for consistent selection.
meshoptimizer provides building blocks (`meshopt_buildMeshlets`, `meshopt_simplify` with locked
borders, and a `clusterlod` demo).

## 2. Runtime cut selection
For each cluster: render it if its projected error is below the threshold (~1 pixel) **and** its
parent group's projected error is above the threshold. Because errors are monotonic, this selection
can be evaluated per cluster independently (parallel on GPU) and always yields a watertight cut.
A BVH over clusters accelerates the search (persistent-thread traversal in compute).

## 3. Rasterisation
- Clusters with large triangles: hardware raster (mesh shaders / primitive shaders or indirect draws).
- Clusters with tiny triangles: **software rasteriser** in compute writing 64-bit atomics
  (depth << 32 | visible cluster+triangle ID) into a visibility buffer - faster than hardware for
  pixel-sized triangles (hardware's 2x2 quad shading and setup overhead).
- Material shading later from the visibility buffer (deferred material pass per material bin).

## 4. Culling and streaming
- Two-pass occlusion culling with Hi-Z on instances and clusters.
- Geometry stored in fixed-size **pages**; stream pages on demand based on the selected cut (like
  virtual texturing for geometry).

## 5. Limits
- Opaque rigid meshes were the original scope (UE added masked, skinned and tessellated later).
- Aggregate geometry (foliage of many small disjoint parts) simplifies poorly.
- Complex to build; for custom engines, start with meshlet culling + discrete LODs.

## Gotchas
- Simplification must preserve UV/normal seams via attribute-aware error metrics.
- Error projection must use a conservative bounding sphere per group for monotonicity.

## Verify
- [ ] Debug view of clusters/triangles shows ~pixel-sized triangles at all distances.
- [ ] No cracks between clusters of different levels.
