---
id: computing-software.game-programming.game-engine-architecture.scene-graph-and-transform-propagation
name: scene-graph-and-transform-propagation
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, entity-systems, scene-graph, transform-hierarchy, world-matrix, dirty-flag, game-programming]
level: practitioner
status: draft
description: "Implement a transform hierarchy: local vs world matrices, lazy dirty-flag propagation, data-oriented sorted arrays for cache-friendly updates, reparenting and scale pitfalls."
sources: ["https://gameprogrammingpatterns.com/dirty-flag.html", "https://www.gameenginebook.com/", "https://docs.unity3d.com/ScriptReference/Transform.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scene graph and transform propagation

**Model:** each node stores a **local** transform (relative to parent); the **world** transform is
`parent.world * local`. Rendering, physics and audio consume world transforms.

## Lazy propagation with dirty flags
```cpp
struct Node { Transform local; Mat4 world; Node* parent; std::vector<Node*> children; bool dirty = true; };

void setLocal(Node* n, const Transform& t) { n->local = t; markDirty(n); }
void markDirty(Node* n) {
    if (n->dirty) return;                     // subtree already dirty: stop early
    n->dirty = true;
    for (Node* c : n->children) markDirty(c);
}
const Mat4& world(Node* n) {
    if (n->dirty) {
        n->world = n->parent ? world(n->parent) * n->local.toMatrix() : n->local.toMatrix();
        n->dirty = false;
    }
    return n->world;
}
```
Many local changes per frame cost one recomputation per node (Nystrom's Dirty Flag pattern).

## Data-oriented version (many nodes)
Store transforms in flat arrays **sorted so parents precede children** (depth-first or by depth).
Update in one linear pass:
```cpp
for (int i = 0; i < count; ++i)
    world[i] = parent[i] < 0 ? localM[i] : world[parent[i]] * localM[i];
```
Cache-friendly and parallelisable per depth level; changed-flag arrays skip clean subtrees. Reparenting
requires re-sorting (or appending and fixing on a slower path). This is how ECS engines (Unity
Entities `LocalToWorld`, Bevy transform propagation) do it.

## Gotchas
- **Non-uniform scale + rotation** in a parent produces shear in children; a TRS child can't
  represent it. Avoid non-uniform scale on parents of rotating children, or store full matrices.
- **Reparenting:** keep world position by setting `local = inverse(newParent.world) * world`.
- Floating point drift from accumulating many incremental rotations: re-orthonormalise or store TRS
  and rebuild matrices.
- Deep hierarchies (bones, UI) are fine; very wide flat ones cost little; what hurts is frequent
  reparenting and per-node virtual calls in the update.
- Readers mid-frame see stale world transforms if propagation runs once per frame; define when it
  runs (e.g. after gameplay, before physics sync and rendering) or use lazy getters.
- Unity: `Transform.SetPositionAndRotation`, `hasChanged`, and avoiding deep hierarchies of moving
  objects (each move dirties all children; `TransformAccessArray` for jobs).

## Verify
- [ ] Unit test: moving a parent moves children; reparenting preserves world pose within epsilon.
- [ ] Profile: transform update scales linearly with changed nodes, not total nodes.
