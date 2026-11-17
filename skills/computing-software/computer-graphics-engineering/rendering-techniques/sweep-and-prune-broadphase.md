---
id: computing-software.computer-graphics-engineering.rendering-techniques.sweep-and-prune-broadphase
name: sweep-and-prune-broadphase
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, spatial-structures, sweep-and-prune, broadphase, collision-detection, sort-and-sweep, physics]
level: practitioner
status: docs-checked
description: "Sweep-and-prune broadphase as implemented in Bullet btAxisSweep3: quantised endpoints on 3 axes, incremental edge sorting that adds and removes pairs, and its limits."
sources: ["https://github.com/bulletphysics/bullet3/blob/master/src/BulletCollision/BroadphaseCollision/btAxisSweep3.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sweep and prune broadphase (Bullet btAxisSweep3)

This skill describes the structure of Bullet's `btAxisSweep3` as read from its headers and
internal implementation (`btAxisSweep3.h` and `btAxisSweep3Internal.h`).

## 1. Structure
- `btAxisSweep3Internal` implements 3D axis sweep and prune. It uses quantised integers to
  represent the begin and end points of each object's AABB on each of the 3 axes. You do not use
  the internal class directly.
- `btAxisSweep3` quantises into `unsigned short` and defaults to `maxHandles = 16384`.
  `bt32BitAxisSweep3` quantises into `unsigned int` and defaults to `maxHandles = 1500000`: higher
  precision and more objects, at the cost of more memory and a bit of performance. The header
  recommends `bt32BitAxisSweep3` or `btDbvtBroadphase` for large worlds with many objects.
- The constructor takes the world AABB (`worldAabbMin`, `worldAabbMax`); the quantisation factor
  is the integer range divided by the world size, so objects must stay inside the world bounds.
- Pairs live in a `btOverlappingPairCache` (a hashed pair cache is created if you pass none),
  and an optional user callback is told of pair additions and removals.
- Each object has a handle holding the indices of its min and max edge on each axis; the edges are
  kept in a sorted array per axis.

## 2. Incremental update
`updateHandle` quantises the new AABB, then for each axis computes how far the min and max
edges moved and re-sorts only those edges:
- Expanding (min edge moving down, max edge moving up) can only add overlaps: `sortMinDown` /
  `sortMaxUp`.
- Shrinking (min edge moving up, max edge moving down) can only remove overlaps: `sortMinUp` /
  `sortMaxDown`.
- Each swap with a neighbouring edge is an adjacent exchange. When a min edge passes a max edge of
  another object, a 2D overlap test on the other two axes (`testOverlap2D`) decides whether to add
  (or, when shrinking, remove) the pair in the pair cache. Only if the objects already overlap on
  both other axes does the pair change.
- Inserting a handle sorts its edges into place on each axis, updating overlaps on the last axis.
  Removing a handle purges the pairs containing it from the pair cache.
- `calculateOverlappingPairs` processes deferred pair removals when the pair cache uses them.

## 3. When it degrades
- The header's own advice: for large worlds and many objects use the 32-bit variant or
  `btDbvtBroadphase` (a dynamic AABB tree).
- Handle count is capped by `maxHandles` and positions are quantised, so the 16-bit variant has
  limited precision on large worlds.

## Gotchas
- Objects outside the declared world AABB are clamped during quantisation; quantisation errors
  are made conservative so the reconstructed AABB is larger than the true one.
- Remove handles through the broadphase so their pairs are purged from the pair cache.

## Verify
- [ ] The reported pair set matches a brute-force N^2 AABB test on random scenes.
- [ ] Moving one object a long distance still produces the correct pairs (many swaps, same result).

## Checked
2026-11-09. Read: Bullet btAxisSweep3.h and btAxisSweep3Internal.h (class comments,
constructor defaults, quantisation, updateHandle, sortMinDown and its comments on adding and
removing overlaps, pair cache creation). Removed: the generic single-axis sort code, the
Baraff attribution, axis-variance advice, the claim of near O(n) behaviour, multi-SAP
suggestions, the comparison table of broadphases, the fat-AABB advice, and the realtimecollisiondetection.net and jitter-physics
sources (landing pages, not read).
Method: docs-checked 2026-11-09 against Bullet btAxisSweep3.h and btAxisSweep3Internal.h.
