---
id: computing-software.game-programming.game-physics.fat-aabbs-and-bvh-refit
name: fat-aabbs-and-bvh-refit
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, fat-aabb, dynamic-aabb-tree, bvh, game-programming]
level: practitioner
status: verified
description: "Keep a dynamic AABB tree cheap: fattened AABBs with velocity margins, refit vs rebuild decisions, tree rotations and static/dynamic tree split."
sources: ["https://box2d.org/files/ErinCatto_DynamicBVH_GDC2019.pdf", "https://github.com/erincatto/box2d"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BVH refit vs rebuild and fat AABBs

**Goal:** update a dynamic bounding-volume tree for thousands of moving bodies without rebuilding
every frame (Erin Catto, *Dynamic Bounding Volume Hierarchies*, GDC 2019).

## Fat AABBs
Store each proxy with an AABB enlarged by a margin (Box2D v2.4: `b2_aabbExtension` 0.1 m plus a velocity prediction
`b2_aabbMultiplier` 4; Box2D v3: at most `B2_MAX_AABB_MARGIN` 0.05 m, limited to 1/8 of a small shape's extent, no velocity
prediction). When the tight AABB still fits inside the fat one, do
nothing; only when it escapes, remove and reinsert (or move) the leaf.
- Bigger margin: fewer tree updates, more false-positive pairs. Tune on profile data.

## Insertion quality
Choose the sibling using the surface area heuristic with branch-and-bound (cost = area of new
parent + increased area of ancestors). Then apply **tree rotations** on the path back up to reduce
area; this keeps the tree good under constant churn.

## Refit vs rebuild
- **Refit:** recompute parent boxes bottom-up from leaves; O(n), fast, but quality degrades as
  objects move far from their original grouping.
- **Rebuild:** top-down SAH or binned build; best quality, costs more. Do it for static geometry at
  load, or for dynamic trees incrementally/asynchronously when a quality metric (Catto's SAH cost, the
  total surface area of the internal nodes) degrades.
- Box2D v3 keeps separate trees per body type (static, kinematic, dynamic) and, per its source comment, uses a two-phase
  refit and rebuild (similar to Jolt) rather than constant reinsertion; the dynamic and kinematic trees are rebuilt
  in the step's broad-phase task.

## Static vs dynamic split
Static geometry in its own tree means moving bodies never perturb it, and static-vs-static pairs
are never queried.

## Verify
- Track tree cost metric and updates per frame; margins should cut reinserts by an order of magnitude.
- Ray-cast benchmark before/after rotations.
