---
id: computing-software.computer-graphics-engineering.graphics-math.culling-and-spatial-partitioning-math
name: culling-and-spatial-partitioning-math
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [graphics-math, frustum-culling, occlusion-culling, bvh, octree, bounding-volume, aabb, sphere-bound, spatial-partitioning, kd-tree, hierarchical-z, separating-axis-theorem, broad-phase, frustum-planes]
level: advanced
status: draft
description: "The math and data structures behind visibility culling: frustum planes, bounding-volume tests, BVH/octree construction, and hierarchical occlusion culling."
sources: ["https://www.realtimerendering.com/", "https://developer.nvidia.com/gpugems/gpugems/part-v-performance-and-practicalities/chapter-29-efficient-occlusion-culling"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Culling and spatial partitioning math

**Goal:** decide what *not* to draw/trace/test, cheaply and correctly — the core
lever behind every "how does it render a huge scene at 60fps" question, and a
common source of pop-in/flicker bugs when the math is slightly wrong.

## Frustum culling
- The view frustum is 6 half-spaces (planes); a point is inside if it's on the
  inside (positive, by convention) side of all 6. Extract planes from the
  combined view-projection matrix (standard Gribb/Hartmann extraction) rather than
  re-deriving from FOV/aspect by hand — fewer places to get a sign wrong.
- Test a **bounding volume**, not the full mesh: sphere-vs-plane
  (`dot(center,normal) + d` vs `-radius`) is cheapest; AABB-vs-plane needs the
  box's half-extent projected onto the plane normal. Sphere bounds are looser but
  O(1) rotation-invariant; AABB bounds are tighter for axis-aligned content but
  must be recomputed (not just rotated) when the object rotates.
- **Conservative is correct, aggressive is a bug**: a culling test must never
  reject something actually visible. When in doubt (e.g. a bound that's an
  approximation), err toward "test more precisely" or "don't cull," not toward
  tighter bounds that risk false negatives — a brief one-frame object pop-out is a
  worse bug than a few extra draws.

## Occlusion culling
- Frustum culling only removes what's outside the view; **occlusion culling**
  removes what's inside the view but hidden behind other geometry (a wall, a
  building). Harder because visibility depends on the whole scene's current state,
  not just one object's bound.
- **Hierarchical Z-buffer / hardware occlusion queries**: render occluders first,
  build a depth hierarchy (mip-mapped min/max depth), test each candidate's bound
  against it before issuing its real draw. Has a frame of latency if queries are
  read back async (test against *last* frame's depth) — usually fine, occasionally
  causes a one-frame pop on fast camera motion.
- **Software/CPU occlusion** (precomputed potentially-visible-set / PVS, portal
  culling for indoor scenes, or a software rasteriser of coarse occluders) avoids
  the GPU round-trip latency — the right choice when occlusion decisions must gate
  what's even submitted to the GPU (GPU-driven culling pipelines typically combine
  frustum + a software/compute-rasterised occlusion pass per frame).

## Spatial partitioning structures
- **BVH** (bounding volume hierarchy): binary tree of bounding volumes, built
  top-down (SAH — surface area heuristic — split for quality) or bottom-up
  (LBVH via Morton codes for fast GPU builds of dynamic scenes). The standard
  structure for ray tracing (this is literally what DXR's BLAS is) and for
  broad-phase collision/culling.
- **Octree/quadtree**: spatial subdivision by fixed regions rather than content-
  fitted bounds — simpler to update incrementally, good for roughly uniform-
  density scenes (terrain, voxels); degrades (empty/overfull cells) on very
  non-uniform density without adaptive depth.
- **Grid / spatial hashing**: O(1) cell lookup, best for roughly uniform object
  size and density (particle systems, broad-phase physics) — cell size should
  roughly match the typical object/query size, too fine wastes memory, too coarse
  defeats the purpose.
- Rebuild cost matters: static scenes build once; dynamic scenes need incremental
  update (refit bounds up the tree) or periodic rebuild — refit is cheap but
  degrades tree quality over time (loose/overlapping bounds), needing an
  occasional full rebuild.

## Verify
- [ ] Frustum plane extraction tested against known points (camera-space origin,
      far corners) rather than trusted on first compile.
- [ ] Culling bounds confirmed conservative — test an object straddling the
      frustum edge/occluder boundary and confirm it isn't falsely culled.
- [ ] Occlusion culling latency (if GPU-query-based) checked for visible pop on
      fast camera motion; mitigated with a small bound expansion if needed.
- [ ] Spatial structure rebuild/refit strategy matched to how often the scene's
      objects actually move, not applied uniformly to static and dynamic content.
