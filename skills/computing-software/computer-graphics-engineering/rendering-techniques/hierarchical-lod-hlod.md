---
id: computing-software.computer-graphics-engineering.rendering-techniques.hierarchical-lod-hlod
name: hierarchical-lod-hlod
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-lod, hlod, hierarchical-lod, proxy-meshes, open-world, draw-call-reduction, world-partition]
level: practitioner
status: draft
description: "Use hierarchical LOD (HLOD) for large worlds: clustering many objects into merged proxy meshes and atlases, switching cluster vs children, and build pipelines in UE/Unity."
sources: ["https://docs.unrealengine.com/5.3/en-US/hierarchical-level-of-detail-in-unreal-engine/", "https://docs.unrealengine.com/5.3/en-US/world-partition---hierarchical-level-of-detail-in-unreal-engine/", "https://github.com/Unity-Technologies/HLODSystem"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hierarchical LOD (HLOD)

## 1. Problem
Per-object LODs reduce triangles but not object count: a distant city of 10 000 buildings still
costs 10 000 draws, culling tests and transforms. HLOD replaces groups of distant objects with a
single merged proxy.

## 2. Building
1. **Cluster** objects spatially (grid cells or bounding-volume clustering), e.g. 64-256 m cells.
2. For each cluster, generate a **proxy mesh**: merge meshes, simplify aggressively (or remesh via
   voxelisation for a watertight shell - UE "Approximate"/"Merge"/"Simplify" settings), bake their
   materials into one atlas (albedo, normal, ORM).
3. Recurse: clusters of clusters for multiple HLOD levels.
Store proxies alongside the originals; streaming systems load proxies for far cells and originals
for near cells (UE World Partition HLOD layers).

## 3. Runtime switching
- Show the proxy when the cluster's screen size is below a threshold; otherwise show its children.
- Children and proxy must not render together: switch whole clusters with a dithered crossfade or
  hide the swap distance behind fog/distance.
- Streaming: proxies are resident far away so originals can stay unloaded.

## 4. Tools
- Unreal: HLOD layers in World Partition (build via commandlet `-run=WorldPartitionBuilderCommandlet
  -Builder=WorldPartitionHLODsBuilder`), legacy HLOD Outliner in UE4.
- Unity: Unity-Technologies/HLODSystem package, or custom with mesh simplification (e.g.
  meshoptimizer simplify) and atlas baking.
- Simplygon for production proxy generation.

## Gotchas
- Material baking loses per-object shader effects (animated, emissive, translucent); exclude such
  objects from clusters.
- Proxy lighting must match: bake normals correctly and keep lightmaps/probe sampling consistent.
- Too-large clusters swap visibly; too small don't save enough draws.

## Verify
- [ ] Draw calls and culling time for distant views drop by an order of magnitude.
- [ ] Transition distance hides swaps (record a flythrough).
