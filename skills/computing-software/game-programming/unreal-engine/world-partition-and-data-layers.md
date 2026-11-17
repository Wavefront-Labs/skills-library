---
id: computing-software.game-programming.unreal-engine.world-partition-and-data-layers
name: world-partition-and-data-layers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-asset-manager, world-partition, data-layers, streaming-sources, one-file-per-actor, hlod, runtime-grid, game-programming]
level: advanced
status: draft
description: "Build open worlds with Unreal World Partition: runtime grids, streaming sources, One File Per Actor, runtime Data Layers, HLODs and gameplay pitfalls."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition---data-layers-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition---hierarchical-level-of-detail-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# World Partition and Data Layers

**Goal:** one large map that streams automatically around players, edited by many people at once,
with switchable world states.

## Core ideas
- The map is divided into a **runtime grid** of cells; actors are assigned to cells by position. Cells
  within the **loading range** of a **streaming source** (by default the player controller) load at
  runtime.
- **One File Per Actor (OFPA)**: each actor is saved as its own file in `__ExternalActors__`, so
  people editing different actors do not conflict in source control.
- Editor loads regions on demand (World Partition window: select area > Load Region).

## Settings
World Settings > World Partition Setup: Runtime Grids (cell size e.g. 12800-25600 uu, loading range
e.g. 25600+), per grid priority. Actors can target a grid (`Runtime Grid` property) or be marked
**Is Spatially Loaded = false** to be always loaded (game-critical managers, but keep this set small).

## Streaming sources
- Player controllers are sources automatically.
- `UWorldPartitionStreamingSourceComponent` on actors (vehicles, cameras, teleport targets) to
  pre-load areas: activate it at the teleport destination, wait until
  `IsStreamingCompleted()` before moving the player.

## Data Layers
Group actors into Data Layer assets (e.g. `DL_Village_Destroyed`, `DL_Night_Events`). Runtime data
layers can be set at runtime to Unloaded / Loaded / Activated:
```cpp
UDataLayerManager* DLM = UDataLayerManager::GetDataLayerManager(GetWorld());
DLM->SetDataLayerInstanceRuntimeState(DLM->GetDataLayerInstanceFromAsset(VillageDestroyedAsset),
                                      EDataLayerRuntimeState::Activated);
```
(UE 5.1+ API; older versions use `UDataLayerSubsystem`.) Editor data layers organise editing only.

## HLOD
Hierarchical LOD layers build merged/simplified proxy meshes for unloaded distant cells so the horizon
is not empty. Build via the World Partition HLOD builder commandlet in CI
(`-run=WorldPartitionBuilderCommandlet -Builder=WorldPartitionHLODsBuilder`).

## Gameplay pitfalls
- Actors in unloaded cells do not exist: never hold hard references across cells; use soft references
  and IDs; persistent state (opened chests) must live in a save system, not in the actor.
- AI/physics near cell borders: objects can fall through floors whose cells are not yet loaded:
  wait for streaming around spawn points.
- Level Instances / Packed Level Actors for reusable building sets inside WP.

## Verify
- [ ] Walking/driving across the map at max speed never shows missing ground (loading range adequate).
- [ ] Teleports wait for streaming completion.
- [ ] Toggling a runtime data layer swaps world state without hitches beyond budget.
