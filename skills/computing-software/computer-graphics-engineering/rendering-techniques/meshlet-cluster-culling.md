---
id: computing-software.computer-graphics-engineering.rendering-techniques.meshlet-cluster-culling
name: meshlet-cluster-culling
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, meshlet-culling, cluster-culling, mesh-shaders, meshoptimizer, normal-cone, hi-z-occlusion]
level: sme
status: docs-checked
description: "Cull meshlets on the GPU: build clusters with meshoptimizer, frustum/normal-cone/Hi-Z occlusion tests in task shaders or compute, and two-pass occlusion."
sources: ["https://github.com/zeux/meshoptimizer", "https://github.com/zeux/meshoptimizer/blob/master/src/meshoptimizer.h", "https://microsoft.github.io/DirectX-Specs/d3d/MeshShader.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Meshlet / cluster culling

## 1. Build meshlets
```cpp
const size_t maxV = 64, maxT = 126; const float coneWeight = 0.25f;
size_t maxM = meshopt_buildMeshletsBound(indexCount, maxV, maxT);
std::vector<meshopt_Meshlet> m(maxM); std::vector<unsigned> mv(maxM*maxV); std::vector<unsigned char> mt(maxM*maxT*3);
size_t n = meshopt_buildMeshlets(m.data(), mv.data(), mt.data(), idx, indexCount,
                                 &pos[0].x, vertexCount, sizeof(vec3), maxV, maxT, coneWeight);
for (size_t i = 0; i < n; ++i) {
  meshopt_Bounds b = meshopt_computeMeshletBounds(&mv[m[i].vertex_offset], &mt[m[i].triangle_offset],
                         m[i].triangle_count, &pos[0].x, vertexCount, sizeof(vec3));
  // store b.center, b.radius, b.cone_axis, b.cone_cutoff
}
```
Run `meshopt_optimizeVertexCache` first. The README recommends 64 vertices / 126 triangles for NVIDIA (in v0.25 or earlier max_triangles must
be divisible by 4, so 124); for earlier AMD GPUs equal limits such as 64/64 or 128/128 tend to be best, and 64/96 is a more achievable
compromise. `cone_weight` 0 if cone culling is unused, otherwise between 0 and 1 (0.25 is a reasonable default). Measure on your hardware.

## 2. Tests (per meshlet, in task/amplification shader or compute)
1. **Frustum**: bounding sphere vs 6 planes (or 4 sides + near).
2. **Backface cone**: `dot(normalize(center - camPos), coneAxis) >= coneCutoff` means all triangles face away;
   cull.
3. **Occlusion**: project the sphere to a screen rect, pick the Hi-Z mip where the rect covers about 2x2 texels,
   compare the sphere's nearest depth with the max depth stored there.

## 3. Two-pass occlusion culling
1. Draw meshlets that were visible last frame (tested against frustum only).
2. Build Hi-Z (max-depth pyramid; with reversed-Z use min) from that depth.
3. Test all remaining meshlets against the new Hi-Z; draw the newly visible ones and update the visibility bits.
No CPU readback and no one-frame-late popping.

## 4. Without mesh shaders
Compute culling writes surviving meshlets' triangles into an index buffer (or indirect draw args per
meshlet), then one `DrawIndexedIndirect`/`ExecuteIndirect`.

## Gotchas
- The cone test must use the meshlet's world transform; non-uniform scale breaks cones (skip the test there).
- Hi-Z from the previous frame plus camera cuts misses disocclusions; the two-pass scheme fixes it.
- In D3D12 the amplification shader payload must not exceed 16 KB per instance; emit meshlet indices, not data.

## Verify
- [ ] Debug overlay coloured per meshlet; counters show frustum/cone/occlusion rejection rates; no
  popping when rotating quickly or behind moving occluders.

## Checked

2026-10-26: meshoptimizer v1.3 (2026-09-25) README.md and meshoptimizer.h, and DirectX-Specs MeshShader.md, read 2026-10-26. Confirmed: meshopt_buildMeshletsBound, meshopt_buildMeshlets and meshopt_computeMeshletBounds signatures, cone_weight guidance (0.25 reasonable default), the cone rejection test dot(normalize(cone_apex - camera_position), cone_axis) >= cone_cutoff, and the D3D12 amplification-shader payload limit of 16k bytes. Wrong claim fixed: the NVIDIA-recommended limits are 64 vertices and 126 triangles (124 only for v0.25 or earlier). The AMD advice was restated from the README. The Hi-Z occlusion and two-pass sections are technique description, not API claims, and were left as written.

Method: documentation only; no commands were run.
