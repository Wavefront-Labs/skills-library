---
id: computing-software.computer-graphics-engineering.graphics-math.meshlet-building-with-meshoptimizer
name: meshlet-building-with-meshoptimizer
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, geometry-processing, meshlet-building, meshoptimizer, mesh-shaders, cluster-culling, gpu-driven-rendering]
level: advanced
status: draft
description: "Build meshlets for mesh shaders and cluster culling with meshoptimizer: vertex/triangle limits, cone culling data, bounds, vertex cache order, and GPU-friendly packing."
sources: ["https://github.com/zeux/meshoptimizer", "https://developer.nvidia.com/blog/introduction-turing-mesh-shaders/", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/mesh-shader"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Meshlet building

A meshlet is a small cluster of triangles (e.g. up to 64 vertices / 124 triangles) processed by one
mesh-shader workgroup and culled as a unit.

## meshoptimizer
```cpp
const size_t max_vertices = 64, max_triangles = 124;   // NVIDIA guidance; 64/64 or 128/128 on AMD
const float cone_weight = 0.25f;                       // trade cluster compactness for cone culling quality
size_t max_meshlets = meshopt_buildMeshletsBound(index_count, max_vertices, max_triangles);
std::vector<meshopt_Meshlet> meshlets(max_meshlets);
std::vector<unsigned int> meshlet_vertices(max_meshlets * max_vertices);
std::vector<unsigned char> meshlet_triangles(max_meshlets * max_triangles * 3);
size_t count = meshopt_buildMeshlets(meshlets.data(), meshlet_vertices.data(), meshlet_triangles.data(),
    indices, index_count, &positions[0].x, vertex_count, sizeof(Vec3), max_vertices, max_triangles, cone_weight);
meshlets.resize(count);
for (auto& m : meshlets) {
    meshopt_optimizeMeshlet(&meshlet_vertices[m.vertex_offset], &meshlet_triangles[m.triangle_offset],
                            m.triangle_count, m.vertex_count);
    meshopt_Bounds b = meshopt_computeMeshletBounds(&meshlet_vertices[m.vertex_offset],
        &meshlet_triangles[m.triangle_offset], m.triangle_count, &positions[0].x, vertex_count, sizeof(Vec3));
    // store b.center, b.radius (sphere culling), b.cone_axis, b.cone_cutoff (backface cone culling)
}
```
- Run `meshopt_optimizeVertexCache` (and optionally `optimizeOverdraw`) on the index buffer before
  building so spatially coherent triangles end up together.
- Local triangle indices are 8-bit (into the meshlet's vertex list): limit `max_vertices` to 255 or
  fewer.
- Pad/round triangle data to 4 bytes per meshlet for aligned GPU loads.

## Culling data
- Bounding sphere: frustum and occlusion (HiZ) culling in the task/amplification shader.
- Normal cone: cull the whole meshlet if `dot(normalize(center - camera), cone_axis) >= cone_cutoff`.
  Effective for dense, smooth geometry; useless for foliage (wide cones).

## LOD hierarchies
For Nanite-style continuous LOD, group meshlets, simplify groups (`meshopt_simplify` with locked
borders), re-cluster, and build a DAG with error bounds; meshoptimizer has `meshopt_buildMeshletsFlex`
/ clusterlod demos for this.

## Verify
Visualise meshlets with random colours; check average triangles per meshlet near the limit (low fill
wastes workgroups) and count culled meshlets per frame.
