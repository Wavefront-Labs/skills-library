---
id: computing-software.game-programming.unreal-engine.world-partition-hlod
name: world-partition-hlod
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, world-partition-hlod, hlod, world-partition, streaming, rendering-performance, game-programming]
level: practitioner
status: draft
description: "Set up HLOD for Unreal World Partition: HLOD layers (instancing, merged, simplified), assigning actors, building with the commandlet and checking distant cells."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition---hierarchical-level-of-detail-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-builder-commandlet-reference"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# World Partition HLOD

**Goal:** unloaded distant cells still render as cheap proxies, so the horizon is not empty.

## HLOD layers
Create **HLOD Layer** assets and assign them (Actor details > HLOD Layer, or a default layer in
World Settings > World Partition Setup). Layer types:
| Type | Result | Use |
|---|---|---|
| Instancing | ISM of the original meshes with their lowest LOD | lots of repeated meshes (trees, rocks) |
| Merged Mesh | meshes merged into one, materials preserved | buildings |
| Simplified Mesh | merged + simplified + baked material | dense varied geometry, far distance |
| Approximated Mesh | approximated geometry with baked textures | distant buildings/cities |
| Custom | your own builder | |
Each layer sets cell size and loading range; a parent layer can build HLOD of HLODs (HLOD1, HLOD2).

## Build
Editor: Build > Build HLODs. CI/command line:
```bat
UnrealEditor-Cmd.exe MyGame.uproject /Game/Maps/OpenWorld -run=WorldPartitionBuilderCommandlet ^
  -AllowCommandletRendering -builder=WorldPartitionHLODsBuilder -Log
```
`-SetupHLODs` then `-BuildHLODs` can be split across machines for large worlds (`-DistributedBuild`).
HLOD actors are saved as external actors (OFPA); submit them to source control.

## Debug
`wp.Runtime.HLOD 0/1` toggles HLOD display; `wp.Runtime.ToggleDrawRuntimeHash2D` shows cells and HLOD
state; World Partition editor window shows HLOD actor bounds.

## Gotchas
- Actors with Is Spatially Loaded off are always loaded and are excluded from HLOD.
- Nanite meshes: Instancing layers with Nanite keep quality cheaply; simplified layers bake textures,
  watch memory.
- Forgetting to rebuild after big edits leaves stale proxies that pop when cells load.
- Large Merged layers create huge meshes; tune cell size.

## Verify
- [ ] Flying across the map shows distant proxies, no gaps; switch to loaded cells has minimal popping.
