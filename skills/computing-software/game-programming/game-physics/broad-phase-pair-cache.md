---
id: computing-software.game-programming.game-physics.broad-phase-pair-cache
name: broad-phase-pair-cache
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, pair-cache, broad-phase, contact-pairs, game-programming]
level: practitioner
status: verified
description: "Manage broad-phase overlapping pairs: persistent pair caches, begin/end overlap events, hash sets keyed by body ids and keeping contact data across frames."
sources: ["https://github.com/erincatto/box2d", "https://box2d.org/files/ErinCatto_SequentialImpulses_GDC2006.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pair caches and pair management

**Goal:** turn per-frame broad-phase overlaps into a stable set of pairs with begin/persist/end
events and warm-starting data.

## Pair key
```cpp
uint64_t pairKey(uint32_t a, uint32_t b) { if (a > b) std::swap(a, b); return (uint64_t(a) << 32) | b; }
```
Ordered ids make (a,b) and (b,a) the same pair. Store pairs in an open-addressing hash map
(key -> Contact index) plus a dense array of contacts for iteration.

## Per-step update
1. Broad-phase reports **new** overlaps only for proxies that moved. Box2D's broad phase does not persist
   pairs (its header says it reports potentially new pairs and the client tracks later overlap); it gathers moved
   proxies from the dynamic tree and keeps a hash set of shape pairs that already have a contact
   (`pairSet`, key `min(id) << 32 | max(id)`, the same layout as `pairKey` above).
2. For each candidate: filter (same body, collision masks, joints that disable collision), look up
   the key; create a contact if missing.
3. Narrow phase runs on all contacts; contacts whose fat AABBs stop overlapping are destroyed.
4. Emit events by comparing touching state this step vs last: begin, persist, end. Box2D's begin/end events
   are about touching (manifold has points), not about fat-AABB overlap, so a pair can exist in the cache for
   many steps before its first begin event.

## Why persistent
- Warm starting: last frame's accumulated impulses per manifold point make stacks converge.
- Events: gameplay wants enter/exit, not a per-frame list.
- Avoids allocating contacts each frame.

## Pitfalls
- Destroying a body must remove its pairs immediately (iterate the body's contact edge list) or
  stale contacts reference freed memory.
- Do not mutate the pair set while iterating callbacks; queue user actions (destroy, spawn) until
  after the step.
- Determinism: iterate contacts in a deterministic order (sorted by key or creation order), not hash
  order, if lockstep or replays matter.

## Verify
- Stress test 10k bodies: pair count matches brute force at random frames.
- Begin/end events strictly alternate per pair.

## Checked (2026-10-22)
- Box2D main (3.2.0 dev, fetched 2026-10-22): `B2_SHAPE_PAIR_KEY` in `src/table.h` is `min << 32 | max`; `b2BroadPhase` comment says it does not persist pairs, has `pairSet` and `movedSiblings` (no move buffer in this version, text corrected); `b2ContactBeginTouchEvent` / `b2ContactEndTouchEvent` in `include/box2d/types.h`.
- Erin Catto GDC 2006 PDF (read with pypdf): arbiters stored in a set keyed by ordered body ids, contact ids matched across frames, accumulated impulses persisted.
- Re-implemented the pair key and begin/end bookkeeping in Python (the C++ is not compiled here): 2000 bodies, 300 frames with a spatial hash, 15000 begins and 13954 ends, begin/end strictly alternate per pair (assertions held) and the pair set equalled brute force at 6 sampled frames.
