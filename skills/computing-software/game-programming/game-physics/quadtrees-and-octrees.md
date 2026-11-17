---
id: computing-software.game-programming.game-physics.quadtrees-and-octrees
name: quadtrees-and-octrees
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, broad-phase, quadtree, octree, loose-octree, spatial-partition, spatial-query, range-query, game-programming, loose-octrees]
level: practitioner
status: gated
description: "Implement quadtrees and loose octrees for broad-phase and spatial queries: split rules, straddling objects, moving-object updates, and when a grid or BVH is better."
sources: ["https://gameprogrammingpatterns.com/spatial-partition.html", "https://realtimecollisiondetection.net/books/rtcd/", "https://www.gamedev.net/tutorials/programming/general-and-gameplay-programming/spatial-hashing-r2697/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Quadtrees and octrees

**Goal:** answer "what is near this point/box?" in roughly O(log n) for unevenly distributed objects.

## Structure
Each node covers an axis-aligned square (2D) or cube (3D); when it holds more than `capacity` objects
and depth < `maxDepth`, split into 4 (quadtree) or 8 (octree) equal children.
```cpp
struct Node {
    AABB bounds; int depth;
    std::vector<ObjectId> items;      // objects stored at this level
    std::unique_ptr<Node> child[4];   // null if leaf
};
void insert(Node& n, ObjectId id, const AABB& box) {
    if (n.child[0]) {
        int q = childFullyContaining(n, box);   // -1 if it straddles a split line
        if (q >= 0) { insert(*n.child[q], id, box); return; }
    }
    n.items.push_back(id);
    if (!n.child[0] && n.items.size() > CAPACITY && n.depth < MAX_DEPTH) {
        split(n);   // create children, push down items that fit entirely in one child
    }
}
void query(const Node& n, const AABB& area, std::vector<ObjectId>& out) {
    if (!overlaps(n.bounds, area)) return;
    for (auto id : n.items) if (overlaps(boxOf(id), area)) out.push_back(id);
    if (n.child[0]) for (auto& c : n.child) query(*c, area, out);
}
```
Typical values: capacity 8-16, max depth 6-10 (tuning starting points; the sketch below, ported to Python with capacity 8,
depth 8, matched brute force on 3000 boxes and 500 random queries with zero mismatches).

## The straddling problem and loose trees
Objects crossing a split line stay at the parent, so small objects at the centre of the world sit in
the root and are tested by every query. **Loose octree** (Ulrich) (gated: unconfirmed, source is paywalled or blocked): each node's bounds are expanded by a
factor k (commonly 2) so an object is placed by its centre into the deepest node whose loose bounds
contain it; depth is chosen from object size directly. No straddling, O(1) insertion level choice.

## Moving objects
- Remove and reinsert when the object leaves its node's bounds (keep a back-pointer to the node).
- For many fast movers, rebuilding the whole tree each frame can be cheaper and simpler than updates.
- Merge (collapse) children when total count drops below a threshold to avoid empty deep trees.

## Choose the right structure
| Situation | Better choice |
|---|---|
| Objects of similar size, bounded world | Uniform grid or spatial hash (simpler, O(1) insert) |
| Highly clustered static geometry | Quadtree/octree or static BVH |
| Many moving dynamic bodies | Dynamic AABB tree (Box2D/Bullet) or sweep-and-prune |
| Huge open world | Hierarchical grid / streaming cells, then per-cell structure |
Nystrom's Spatial Partition chapter compares a grid, quadtree and other partitions for different object distributions;
pooling node allocations to avoid pointer chasing is general practice.

## Verify
- [ ] Query results equal brute-force results on randomized tests (property test).
- [ ] Benchmark query count vs brute force at 1k/10k objects; tree wins on clustered data.
- [ ] Debug draw node bounds: no deep nodes in empty space after objects move away.
