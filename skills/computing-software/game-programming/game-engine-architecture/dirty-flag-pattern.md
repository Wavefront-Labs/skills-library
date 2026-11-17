---
id: computing-software.game-programming.game-engine-architecture.dirty-flag-pattern
name: dirty-flag-pattern
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, data-oriented-design, dirty-flag, lazy-evaluation, transform-hierarchy, world-matrix, cache-invalidation, game-programming]
level: practitioner
status: draft
description: "Apply the dirty flag pattern for derived data like scene-graph world transforms: when to recompute, propagation to children, batching updates, and invalidation bugs."
sources: ["https://gameprogrammingpatterns.com/dirty-flag.html", "https://www.gameenginebook.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dirty flag pattern

**Goal:** avoid recomputing expensive derived data (world transforms, bounding boxes, UI layout,
path costs) every time a primary value changes; recompute once, when needed (Nystrom, GPP
"Dirty Flag").

## Canonical example: world transforms in a hierarchy
World = parent.world * local. Moving a parent changes every descendant's world transform.
Recomputing eagerly on every local change wastes work when an object moves several times per frame
or when a parent and child both move.
```cpp
struct Node {
    Transform local;
    Transform world;
    bool dirty = true;
    std::vector<Node*> children;

    void setLocal(const Transform& t) { local = t; dirty = true; }
};
// Once per frame, before rendering/physics read world transforms:
void render(Node& n, const Transform& parentWorld, bool parentDirty) {
    bool dirty = n.dirty || parentDirty;
    if (dirty) { n.world = parentWorld * n.local; n.dirty = false; }
    draw(n, n.world);
    for (Node* c : n.children) render(*c, n.world, dirty);
}
```
Dirtiness is propagated during the single traversal instead of marking every descendant on each set.

## Pull vs push
- **Lazy pull:** `getWorld()` checks the flag and recomputes on demand. Simple, but each getter
  must walk up to check parents, or children must be marked when parents change.
- **Batch at a sync point:** recompute all dirty items once per frame in a known phase (shown above,
  or Unity-style "transform changed" sweeps). Better cache behaviour and predictable cost.

## When it pays
- Derived value is expensive relative to the flag check.
- The primary value changes more often than the derived value is read.
- Otherwise (e.g. read every frame, changed every frame), drop the flag and compute directly.

## Bugs to watch
- **Forgetting to set the flag** on one code path that mutates the primary data: make the field
  private and the setter the only writer.
- **Stale reads** from systems that read the derived data before the sync point; document the phase
  where it is valid.
- **Memory of the old value:** keep it if consumers need deltas (e.g. physics velocity from transform
  change).
- Multithreading: dirty flags written by many threads need atomics or per-thread lists of dirty ids.

## Variants
Dirty lists (vector of dirty ids) instead of flags when few of many objects change; versioned
counters (`generation` number compared with cached generation) for multiple consumers.

## Verify
- [ ] Move a parent and child in the same frame: world transform computed once each.
- [ ] Unit test: every public mutator sets the flag (or bumps the version).
- [ ] Profiling shows transform update cost scales with changed objects, not total objects.
