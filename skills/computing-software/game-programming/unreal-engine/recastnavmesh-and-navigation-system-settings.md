---
id: computing-software.game-programming.unreal-engine.recastnavmesh-and-navigation-system-settings
name: recastnavmesh-and-navigation-system-settings
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, unreal-ai, recastnavmesh, nav-mesh-bounds-volume, runtime-generation, game-programming, navigation-area-cost, multiple-agent-sizes]
level: practitioner
status: draft
description: "Configure Unreal navigation: NavMeshBoundsVolume, RecastNavMesh agent and tile settings, runtime generation modes, nav modifiers, multiple agent types and debug views."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/basic-navigation-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-how-to-modify-the-navigation-mesh-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RecastNavMesh and Navigation System settings

**Goal:** AI can path everywhere it should, nowhere it shouldn't, and navmesh updates at runtime
without hitches.

## Basics
- Place a **NavMeshBoundsVolume** covering walkable space; a `RecastNavMesh-Default` actor appears.
- Press **P** in the viewport to toggle navmesh display.
- Project Settings > Navigation Mesh (RecastNavMesh defaults) and Navigation System.

## Key RecastNavMesh settings
- **Agent Radius / Height / Max Step Height / Max Slope**: must match the character capsule.
- **Cell Size / Cell Height**: resolution (smaller = accurate, slower, more memory).
- **Tile Size UU**: tiles rebuild independently; smaller tiles = cheaper dynamic updates.
- **Runtime Generation** (Navigation System / per navmesh): Static (baked, cheapest), Dynamic
  Modifiers Only (static mesh but modifiers can change areas), Dynamic (rebuilds tiles when geometry
  moves).
- World Partition: use navigation data chunking with Static/Modifiers only; enable invoker-based
  generation for huge worlds (`Generate Navigation Only Around Navigation Invokers` + Navigation
  Invoker components on players/AI).

## Shaping the mesh
- **NavModifierVolume** with an Area Class: `NavArea_Null` (cut), `NavArea_Obstacle` (high cost), custom
  `UNavArea` subclasses with Default Cost / flags.
- Per-component: `Can Ever Affect Navigation`, `Area Class`, `bDynamicObstacle` (moves -> modifier only).
- **NavLinkProxy** / Smart Links for jumps, ladders and drops.

## Multiple agent types
Project Settings > Navigation System > Supported Agents: add entries (e.g. Humanoid r=34, Large r=120);
one RecastNavMesh per agent; the character's `NavAgentProps` picks the closest match.

## Debugging
- `show Navigation`, Gameplay Debugger (apostrophe key) navmesh and path categories.
- `RebuildNavigation` console command; Build > Build Paths in editor.
- Visual Logger records path queries per AI.

## Gotchas
- Navmesh not generating: volume missing, collision on meshes disabled for navigation, or the
  RecastNavMesh actor has a stale "Static" mode after streaming.
- Dynamic generation with large tiles causes hitches when doors move — shrink tiles or use dynamic
  obstacles.

## Verify
- [ ] Gameplay Debugger shows complete paths across all intended areas.
- [ ] Moving doors/obstacles update navmesh within a frame or two without spikes in `stat navigation`.
