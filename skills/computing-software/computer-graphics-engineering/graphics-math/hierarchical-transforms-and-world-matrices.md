---
id: computing-software.computer-graphics-engineering.graphics-math.hierarchical-transforms-and-world-matrices
name: hierarchical-transforms-and-world-matrices
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, transforms, hierarchical-transforms, scene-graph, world-matrix, dirty-flags, reparenting]
level: practitioner
status: draft
description: "Compute world matrices in scene hierarchies: local vs world, parent-first update order, dirty flags, reparenting while keeping world pose, and non-uniform scale shear."
sources: ["https://www.realtimerendering.com/", "https://gameprogrammingpatterns.com/dirty-flag.html", "https://docs.unity3d.com/ScriptReference/Transform.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hierarchical transforms and world matrices

## Definitions
`World(node) = World(parent) * Local(node)` with column vectors (`v_world = W * v_local`). Row-vector
conventions (DirectXMath) reverse the multiplication order: `W = L * W_parent`.

## Update order
Process parents before children. Store nodes in a flat array sorted so every parent precedes its
children (breadth-first or depth-first order), then one linear pass:
```cpp
for (size_t i = 0; i < n; ++i)
    world[i] = parent[i] < 0 ? local[i] : world[parent[i]] * local[i];
```
Cache-friendly, parallelisable by depth level, and avoids recursion.

## Dirty flags
Mark a node dirty when its local changes; dirtiness propagates to descendants. Recompute only dirty
subtrees; also update bounding volumes. Engines like Unity expose `hasChanged`; Unreal uses
component transform update notifications.

## Reparenting while keeping world pose
```cpp
local_new = inverse(world(newParent)) * world(node);
```
With non-uniform scale in the new parent, the result may need shear, which a TRS local cannot
represent: the world pose changes slightly. Avoid non-uniform scale on parents.

## Non-uniform scale and shear
Rotated child under a non-uniformly scaled parent becomes sheared. Decomposing the world matrix back
into TRS then loses information. Keep scale on leaf meshes, not on grouping nodes.

## Normals
Transform normals with the inverse transpose of the world upper 3x3 (or cofactor matrix), not the
world matrix itself, when non-uniform scale is present.

## Precision
Deep hierarchies and huge world coordinates accumulate float error; use camera-relative rendering or
double-precision world positions for large worlds.

## Verify
Unit test: world positions of children after rotating/scaling/reparenting match a reference computed
with full 4x4 multiplication in double precision.
