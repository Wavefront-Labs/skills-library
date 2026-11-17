---
id: computing-software.computer-graphics-engineering.rendering-techniques.clustered-and-tiled-lighting
name: clustered-and-tiled-lighting
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [rendering-techniques, clustered-lighting, tiled-lighting, light-culling, compute-shader, many-lights, light-list, aabb-test, depth-slicing, bandwidth]
level: advanced
status: docs-checked
description: "Implement clustered shading light culling on the GPU: cluster AABB grid, logarithmic depth slices, active clusters, sphere-AABB tests and the light grid and index list structures."
sources: ["http://www.aortiz.me/2018/12/21/CG.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clustered and tiled lighting

**Goal:** cull many dynamic lights per view-space volume on the GPU, then shade each sample using only
the lights stored for its cluster (Ola Olsson et al., "Clustered Deferred and Forward Shading";
walkthrough by Angel Ortiz, with GLSL compute shaders).

## 1. Why clusters
- Tiled shading batches samples by screen-space proximity. Grouping by screen position handles depth
  discontinuities poorly and can cause edge cases where a single pixel movement causes performance
  issues. Clustered shading groups by view-space position instead.
- The article describes clustered shading as compute bound rather than bandwidth limited, and as
  offering the highest light-culling efficiency among the current many-light algorithms it compares.
- Steps from the original paper: build the cluster structure; render to a G-buffer or Z pre-pass; find
  visible clusters; reduce repeated values in the visible list; cull lights and assign them to
  clusters; shade using the light list.

## 2. Build the cluster grid
Tile the view frustum as in tiled shading, then subdivide along depth. The paper discusses three depth
schemes:
- Uniform in NDC: clusters near the far plane are huge, near the near plane tiny (NDC is non-linear).
- Uniform in view space: near clusters are huge, far clusters wide and thin.
- Exponentially spaced for self-similar subdivision (chosen by the paper's authors).

The article uses the DOOM 2016 (Tiago Sousa) slice formula, whose only variable is Z, so scale and bias
can be precomputed:
```glsl
slice = floor( log(Z) * numSlices / log(Far/Near)  -  numSlices * log(Near) / log(Far/Near) );
```
That is one log, one multiply and one add per depth lookup. Example grid: 16x9x24 clusters, one
compute thread per cluster.

Per cluster, compute an AABB in view space: take the tile's screen-space min and max points, transform
to view space with the inverse projection, intersect the rays through them (all rays meet at the origin
in view space) with the cluster's near and far depth planes, and take min and max of the four
intersection points. Store the min and max points in a cluster array.

The AABB list stays valid while the frustum shape is unchanged: compute it at load and again when FOV
or similar camera properties change. The author's RenderDoc profiling suggested recomputing every frame
would also be cheap.

## 3. Active clusters (optional)
Skipping this step is valid: you can run light culling on every cluster each frame, but it is less
efficient. Finding active clusters needs a Z pre-pass (or a deferred G-buffer):
1. In parallel, each pixel computes its cluster ID and marks that cluster active in a list.
2. The sparse list is compacted into another list using atomic operations.
3. Light culling then tests lights only against the compacted list.

## 4. Light culling
- Point lights: test the light sphere against the cluster AABB (`testSphereAABB`): intersecting when
  the distance from the sphere centre to the AABB is less than the radius.
- Spotlights: the article does not implement them and points to Emil Persson's Just Cause 3
  presentation for spotlight culling.

Data structures (shader storage buffers on the GPU, so incoherent access needs barriers):
- **Global light list**: every light in the scene.
- **Global light index list**: indices of the lights affecting clusters, grouped by cluster, but without
  explicit grouping information; the order is not necessarily sequential per cluster.
- **Light grid**: one element per cluster with two unsigned ints, an offset into the index list and the
  count of lights intersecting the cluster.
Storing indices rather than lights saves memory because clusters tend to share lights, and compute and
pixel shaders can read the same structure.

Culling compute shader pattern from the article (dispatched six times, each thread group covering 4 of
24 Z slices, the largest the author could fit in one group):
1. Each thread represents a cluster and keeps a local list of visible light indices and a count.
2. Threads loop over the lights in batches of thread-group size: each thread loads one light into
   shared memory, a `barrier()` follows, then each thread tests its cluster's AABB against every light
   in shared memory.
3. `offset = atomicAdd(globalIndexCount, visibleLightCount)` gives each cluster a unique offset; copy
   the local indices to `globalLightIndexList` at that offset and write offset and count to the light
   grid.
4. A fragment shader finds its cluster index, reads the light grid entry and loops over those lights.
The author reports this simple method handles lights in the order of tens of thousands.

## Gotchas
- The article's own code uses OpenGL's default depth layout and says it should use reverse Z.
- Further optimisation topics named by the article (not detailed there): BVH over lights, light sorting,
  scalar-register optimisation on GCN, and applying the cluster structure to probes and decals as DOOM
  2016 did.

## Checked
2026-11-08. Confirmed against the aortiz.me clustered shading article: tiled shading depth-discontinuity remark, three depth schemes, DOOM slice formula and scale/bias remark, 16x9x24 grid, AABB construction and update frequency, optional active-cluster pass and Z pre-pass requirement, sphere-AABB test, light grid and index list structures, batch-with-shared-memory culling shader and `atomicAdd` offsets, six dispatches. Removed: the earlier draft's two-pass count/prefix-sum scheme, cone bounds for spotlights, over/under-conservative bound advice, and the 3dgep Forward+ source (not read this batch).
Method: documentation only; no commands were run.

## Verify
- [ ] Depth slices use the logarithmic formula with the camera's actual near and far planes.
- [ ] Light grid offsets and counts match a CPU brute-force reference on a test scene.
- [ ] Silhouette and depth-discontinuity regions tested against a brute-force light loop.
