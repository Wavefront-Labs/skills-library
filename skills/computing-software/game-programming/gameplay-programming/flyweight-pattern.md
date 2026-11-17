---
id: computing-software.game-programming.gameplay-programming.flyweight-pattern
name: flyweight-pattern
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, flyweight-pattern, intrinsic-state, extrinsic-state, tile-types, instanced-rendering, memory-optimization, game-programming]
level: practitioner
status: draft
description: "Use the Flyweight pattern to share immutable data across many game objects: intrinsic vs extrinsic state, tile/terrain type objects, GPU instancing analogy and engine equivalents."
sources: ["https://gameprogrammingpatterns.com/flyweight.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flyweight pattern

**Goal:** thousands of trees, tiles, bullets or units that share their heavy common data instead of
each carrying a copy (Nystrom, GPP "Flyweight").

## Split the state
- **Intrinsic** (context-free, shared, immutable): mesh, textures, base stats, movement cost, sounds.
- **Extrinsic** (per instance): position, rotation, health, current animation frame.
```cpp
struct TerrainType {                 // flyweight: one object per kind of terrain
    int movementCost; bool isWater; const Texture* texture;
};
class World {
    TerrainType grass{1, false, &grassTex}, hill{3, false, &hillTex}, river{2, true, &riverTex};
    const TerrainType* tiles[W][H];  // each tile is just a pointer (or a 1-byte index)
public:
    int movementCost(int x, int y) const { return tiles[x][y]->movementCost; }
};
```
A grid of pointers/indices into a small table replaces a grid of fat structs or an enum plus scattered
`switch` statements; data and behaviour for a terrain live together.

## Rendering analogy
GPU instancing is the same idea at the hardware level: one mesh and material (intrinsic) drawn many
times with a per-instance buffer of transforms/colours (extrinsic). Engines: Unity GPU instancing /
`Graphics.RenderMeshInstanced`, Unreal Instanced Static Mesh / HISM components, Godot `MultiMesh`.

## In engine data
- Unity ScriptableObject stat assets referenced by prefabs (see unity scriptableobject-data-containers).
- Unreal Data Assets / Data Table rows referenced by actors; Godot shared Resources (do not
  `duplicate()` unless per-instance mutation is needed; `resource_local_to_scene` makes per-instance copies).

## Pitfalls
- Mutating shared intrinsic data at runtime changes every instance (the classic "all enemies got the
  buff" bug). Keep flyweights immutable at runtime, or copy-on-write.
- Index tables must stay stable when saved (store ids, not pointers).
- Do not over-apply: if each instance really differs, a flyweight adds indirection for nothing.

## Verify
- [ ] Memory profile shows one copy of shared data regardless of instance count.
- [ ] No runtime code writes to flyweight objects (const-correctness or read-only assets).
- [ ] Save files store type ids that resolve after reordering the type table.
