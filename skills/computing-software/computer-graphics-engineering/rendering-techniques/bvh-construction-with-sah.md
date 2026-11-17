---
id: computing-software.computer-graphics-engineering.rendering-techniques.bvh-construction-with-sah
name: bvh-construction-with-sah
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, path-tracing, bvh-construction, sah, surface-area-heuristic, binned-sah, lbvh, bvh-traversal, refitting]
level: advanced
status: docs-checked
description: "Build ray tracing BVHs with the surface area heuristic: SAH cost model, bucketed splits as in pbrt-v4, leaf rules, flat depth-first node layout, Morton-code LBVH/HLBVH."
sources: ["https://pbr-book.org/4ed/Primitives_and_Intersection_Acceleration/Bounding_Volume_Hierarchies", "https://jacco.ompf2.com/2022/04/13/how-to-build-a-bvh-part-1-basics/", "https://research.nvidia.com/publication/2012-06_maximizing-parallelism-construction-bvhs-octrees-and-k-d-trees"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BVH construction with SAH

**Goal:** a bounding volume hierarchy that minimises expected ray traversal cost, built fast enough
for your use. The reference throughout is PBR 4th ed., section 7.3 (pbrt-v4's `BVHAggregate`).

## 1. The SAH cost
Making a node a leaf costs, for any ray reaching it, the sum of the intersection times of its
primitives. Splitting costs the traversal time of the interior node plus, for each child, the
probability that the ray also passes through the child times the cost of that child's primitives.
For a convex volume B inside A, the probability that a uniformly distributed ray through A also
passes through B is the ratio of their surface areas, so child probabilities are `SA(child) / SA(node)`.
Builders usually minimise this greedily, one node at a time. pbrt assumes the same intersection cost
for every primitive; in its code a leaf costs the primitive count and a split costs
`1/2 + (count_L * SA(L) + count_R * SA(R)) / SA(node)`.

## 2. Bucketed SAH build (top-down)
How pbrt-v4 does it (default `SplitMethod::SAH`; the other methods are `HLBVH`, `Middle`, `EqualCounts`):
1. Bound the primitive centroids and split along the dimension where that centroid bound is widest.
   If all centroids coincide (zero centroid extent) or the node's surface area is 0, make a leaf.
2. With 2 or fewer primitives, just split them in half (SAH is not worth it at that point).
3. Otherwise drop each primitive into one of 12 buckets by centroid position along the axis; per bucket
   keep a count and the union of primitive bounds.
4. Evaluate the 11 split positions (after each bucket but the last) with a forward and a backward
   scan accumulating `count * surface area`; pick the cheapest.
5. Create a leaf if the node has at most `maxPrimsInNode` primitives and the leaf cost is not above the
   split cost; otherwise partition at the chosen bucket and recurse. `maxPrimsInNode` defaults to 1
   and is capped at 255. Children are built in parallel for large nodes.
Leaf primitives are made contiguous by reordering the primitive array, so a leaf stores only an offset
and a count.

## 3. Flatten for traversal
- Convert the built tree to a linear array in depth-first order: the first child follows its parent in
  memory, so only the offset of the second child is stored.
- pbrt's `LinearBVHNode` holds bounds, either a primitives offset (leaf) or second-child offset
  (interior), a primitive count (0 means interior) and the split axis, with 32-byte alignment so a node
  never straddles two cache lines. Jacco Bikker's tutorial also reaches a 32-byte node.
- Traversal uses an explicit stack (pbrt: 64 entries) and the stored split axis with the ray direction
  sign to visit the nearer child first. After a hit inside a leaf, remaining nodes are still visited
  because they may hold a closer hit.

## 4. Fast builds: LBVH and HLBVH
- LBVH turns construction into sorting: compute Morton codes of primitive centroids, sort, and the
  sorted order already groups nearby primitives.
- pbrt's HLBVH uses 10 bits per axis (30-bit codes), radix sorts them, builds an LBVH per cluster
  ("treelet"), then builds the upper levels over at most 4096 treelet roots with SAH.
- The tree uses only centroids, not primitive extent, so for scenes with primitives of very different
  sizes it is worse than an SAH tree.
- Karras (HPG 2012) builds the whole tree in parallel, using an in-place algorithm for binary radix
  trees, to avoid sequential level-by-level construction on GPUs.

## 5. Animation
Refitting and rebuilding are the two standard approaches for animated models (topics in Jacco Bikker's
BVH tutorial series; the fetched part 1 only introduces them). Choose by measuring traversal cost over
the animation, not by assumption.

## Gotchas
- pbrt buckets primitives by centroid position within the centroid bounds, not within the node's AABB.
- Let construction end in a leaf larger than your target size when no split is cheaper (one reader of
  Bikker's tutorial reports a large slowdown from forcing small leaves).
- Evaluating SAH only on the widest centroid axis (as pbrt does) is a simplification, not the only choice.

## Checked
2026-11-08. Confirmed against PBR 4th ed. section 7.3 (SAH model, surface-area probability, bucket count, centroid-based binning, forward/backward scans, leaf and split cost expressions, 2-primitive fallback, `maxPrimsInNode`, flattening, node alignment, stack traversal, HLBVH Morton/treelet details), Bikker BVH part 1 (32-byte node, refit/rebuild listed as topics) and the Karras 2012 abstract. Removed: typical constants (C_trav, C_isect), "2-3x slower" for midpoint splits, all-three-axes binning, 16 bins, BVH4/BVH8 collapsing, spatial splits, TLAS/BLAS and hardware-RT claims, benchmark scenes and Embree.
Method: documentation only; no commands were run.

## Verify
- [ ] Report SAH cost and average nodes/triangles visited per ray vs a median-split build.
- [ ] Refit path tested on animated mesh: traversal cost tracked over frames.
