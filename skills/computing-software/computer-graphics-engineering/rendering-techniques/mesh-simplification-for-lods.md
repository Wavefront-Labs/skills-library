---
id: computing-software.computer-graphics-engineering.rendering-techniques.mesh-simplification-for-lods
name: mesh-simplification-for-lods
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, polygonal-techniques, geometry-processing, mesh-simplification, quadric-error-metrics, meshoptimizer, meshopt-simplify, lod-generation, attribute-aware-simplification]
level: practitioner
status: docs-checked
description: "Generate LOD meshes automatically with quadric-error simplification (meshoptimizer): target counts and error, attribute weights, seams and borders, sloppy mode."
sources: ["https://github.com/zeux/meshoptimizer", "https://github.com/zeux/meshoptimizer/blob/master/src/meshoptimizer.h", "https://github.com/zeux/meshoptimizer/blob/master/gltf/README.md", "https://www.cs.cmu.edu/~./garland/Papers/quadrics.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mesh simplification for LODs

**Goal:** LOD chains generated in the asset pipeline that keep silhouettes, UV seams and
shading, with a known geometric error per level (Garland & Heckbert 1997).

## 1. Quadric error metrics
Edge collapses ordered by the sum of squared distances to the planes of the original
faces around each vertex (Garland and Heckbert, the quadrics paper linked in sources). meshoptimizer's simplifier
follows the topology of the original mesh to preserve attribute seams, borders and overall appearance.

## 2. meshoptimizer
```cpp
size_t target = size_t(indexCount * 0.5f) / 3 * 3;      // 50% triangles
float targetError = 1e-2f;                               // relative to mesh extents: 0.01 = 1% deformation
float lodError = 0.f;
std::vector<unsigned> lod(indexCount);
lod.resize(meshopt_simplify(lod.data(), indices, indexCount, &verts[0].x, vertexCount,
                            sizeof(Vertex), target, targetError, meshopt_SimplifyLockBorder, &lodError));
float worldError = lodError * meshopt_simplifyScale(&verts[0].x, vertexCount, sizeof(Vertex));
```
- The simplifier can stop short of the target because of topology constraints or the target error. `destination` must have room for
  `index_count` indices (not `target_index_count`). Store `worldError` per LOD for screen-space-error LOD selection;
  `meshopt_SimplifyErrorAbsolute` switches the limit to absolute units.
- `meshopt_simplifyWithAttributes` adds attribute values and weights (at most 32 attributes) to the error metric so
  normals, UVs and colours survive.
- `meshopt_SimplifyLockBorder` does not move vertices on the topological border (useful for simplifying portions of a
  larger mesh such as terrain chunks that must stitch).
- `meshopt_simplifySloppy`: does not follow the topology, so it does not preserve attribute seams or borders; worse geometric and
  attribute quality, for very distant LODs and proxies.
CLI route: `gltfpack -si R in.glb -o out.glb` (R between 0 and 1 is the target triangle ratio).

## 3. Seams
`meshopt_simplify` infers attribute discontinuities from the index buffer and tries to preserve them. Weld identical vertices first
(duplicates make the simplifier get stuck), and for faceted meshes or meshes with many seams use `meshopt_SimplifyPermissive`
with `meshopt_simplifyWithAttributes`; protect chosen seams (for example UV seams) with `meshopt_SimplifyVertex_Protect` in the
`vertex_lock` array, which you can fill using `meshopt_generatePositionRemap`.

## 4. After simplifying
Re-run `meshopt_optimizeVertexCache` + `meshopt_optimizeVertexFetch` on each LOD (index
order changes), and optionally share the vertex buffer across LODs with different index
buffers.

## Gotchas
- Thin features (fingers, antennae, fences) vanish early; protect with vertex locks
  (`vertex_lock` array with `meshopt_SimplifyVertex_Lock` / `_Priority`) or hand-author.
- Skinned meshes: preserve weights by including them as attributes, and check deformation.
- Error is geometric only: texture swimming can still occur — bake normal maps per LOD if
  needed.

## Verify
- [ ] Silhouette comparison at each LOD's switch distance (screenshots) passes review.
- [ ] Stored per-LOD error used by LOD selection; error < 1 px at switch distance.
- [ ] No cracks along UV seams or chunk borders.

## Checked

2026-10-26: meshoptimizer v1.3 (released 2026-09-25): src/meshoptimizer.h, README.md and gltf/README.md, read 2026-10-26. Confirmed: meshopt_simplify, meshopt_simplifyWithAttributes, meshopt_simplifySloppy and meshopt_simplifyScale signatures and semantics, target_error relative to mesh extents, destination sizing, the SimplifyLockBorder/Permissive/ErrorAbsolute options, the vertex_lock flags, gltfpack -si R. Wrong claim fixed: the old text said seams are handled by a position remap built with meshopt_generateShadowIndexBuffer; the README says discontinuities are inferred from the index buffer, vertices must be welded, and seams are protected with Permissive plus Protect locks and meshopt_generatePositionRemap. Removed the gltf-transform and tool-comparison claims, which were not read.

Method: documentation only; no commands were run.
