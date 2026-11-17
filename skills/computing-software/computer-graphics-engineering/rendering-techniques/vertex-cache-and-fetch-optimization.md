---
id: computing-software.computer-graphics-engineering.rendering-techniques.vertex-cache-and-fetch-optimization
name: vertex-cache-and-fetch-optimization
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, polygonal-techniques, geometry-processing, vertex-cache-optimization, meshoptimizer, overdraw-optimization, vertex-fetch, acmr, index-reordering, gltfpack]
level: practitioner
status: docs-checked
description: "Reorder mesh indices and vertices for GPU efficiency with meshoptimizer: vertex cache optimisation, overdraw-aware ordering, vertex fetch locality, and measuring ACMR/ATVR."
sources: ["https://github.com/zeux/meshoptimizer", "https://github.com/zeux/meshoptimizer/blob/master/src/meshoptimizer.h", "https://tomforsyth1000.github.io/papers/fast_vert_cache_opt.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vertex cache and fetch optimisation

**Goal:** the same mesh drawn with fewer vertex shader invocations, less overdraw and
better memory locality, measured per asset with the statistics functions below.

## 1. The pipeline (order matters)
```cpp
// 1. dedupe vertices -> index buffer
std::vector<unsigned> remap(indexCount);
size_t vcount = meshopt_generateVertexRemap(remap.data(), nullptr, indexCount, verts, indexCount, sizeof(V));
meshopt_remapIndexBuffer(indices, nullptr, indexCount, remap.data());
meshopt_remapVertexBuffer(outVerts, verts, indexCount, sizeof(V), remap.data());
// 2. vertex cache: reorder triangles so recently transformed vertices are reused
meshopt_optimizeVertexCache(indices, indices, indexCount, vcount);
// 3. overdraw: reorder clusters of triangles roughly front-to-back from typical views
meshopt_optimizeOverdraw(indices, indices, indexCount, &outVerts[0].x, vcount, sizeof(V), 1.05f);
// 4. vertex fetch: reorder vertices in first-use order for memory locality
meshopt_optimizeVertexFetch(outVerts, indices, indexCount, outVerts, vcount, sizeof(V));
```
Threshold 1.05 means the resulting vertex cache hit ratio should be at most 5% worse than before the overdraw pass.

## 2. Metrics
```cpp
auto vc = meshopt_analyzeVertexCache(indices, indexCount, vcount, 16, 0, 0);
// vc.acmr: transformed vertices / triangle count (best 0.5, worst 3.0, optimum depends on topology)
// vc.atvr: transformed vertices / vertex count (best 1.0, worst 6.0)
auto od = meshopt_analyzeOverdraw(indices, indexCount, &v[0].x, vcount, sizeof(V));
auto vf = meshopt_analyzeVertexFetch(indices, indexCount, vcount, sizeof(V));
```
`acmr` is documented as best case 0.5 and worst case 3.0, `atvr` as best case 1.0 and worst case 6.0; the optimum depends on
topology, so compare before and after rather than against a fixed target. Log them in the asset pipeline.

## 3. Modern GPU notes
Vertex reuse details vary between GPU architectures, so `meshopt_optimizeVertexCache` uses an adaptive algorithm that works across GPUs.
`meshopt_optimizeVertexCacheFifo` (recommended cache size 16) targets fixed-size FIFO caches; the README says it is usually less
performant but about 2x faster to run, which can help rapid iteration.
For mesh shaders, build **meshlets** instead (`meshopt_buildMeshlets`).

## 4. Tooling shortcut
`gltfpack -i in.glb -o out.glb` optimises meshes for vertex fetch and transform cache and quantises geometry (see the gltfpack README).

## Gotchas
- Keep the order above: overdraw optimisation takes the cache-optimised indices and trades off at most the threshold of cache efficiency.
- Index buffers get reordered — any per-triangle data (face IDs) must be remapped too.
- Overdraw optimisation targets opaque, depth-tested rendering; skip it for transparent meshes.

## Verify
- [ ] Pipeline logs ACMR/ATVR/overdraw before vs after per asset.
- [ ] Visual output identical (only ordering changed).

## Checked

2026-10-26: meshoptimizer v1.3 (2026-09-25): src/meshoptimizer.h and README.md, read 2026-10-26. Confirmed: meshopt_generateVertexRemap, remapIndexBuffer, remapVertexBuffer, optimizeVertexCache, optimizeVertexCacheFifo (cache size 16, about 2x faster), optimizeOverdraw (threshold 1.05 means at most 5% worse cache ratio), optimizeVertexFetch, analyzeVertexCache/Overdraw/VertexFetch signatures and the documented acmr (0.5 to 3.0) and atvr (1.0 to 6.0) ranges. Removed the 10-40% gain, the typical ACMR 0.6-0.8, the no-FIFO-cache claim, the gltf-transform command and the claim that cache-after-overdraw undoes ordering, none of which the documentation states.

Method: documentation only; no commands were run.
