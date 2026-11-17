---
id: computing-software.game-programming.unreal-engine.level-streaming
name: level-streaming
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, unreal-asset-manager, level-streaming, sublevels, streaming-volumes, loadstreamlevel, level-instance, persistent-level, game-programming]
level: practitioner
status: draft
description: "Stream sublevels in Unreal without World Partition: persistent level and sublevels, streaming volumes, LoadStreamLevel, dynamic level instances and hitches."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/level-streaming-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/loading-and-unloading-levels-using-blueprints-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/level-streaming-volumes-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Level streaming

**Goal:** load parts of a linear or hub-based game (rooms, building interiors, arenas) on demand,
with a persistent level that never unloads.

## Structure
Persistent level (game mode setup, lighting scenario, always-needed actors) + **sublevels** added in the
Levels window (Window > Levels). Each sublevel's streaming method: **Blueprint** (load from code) or
**Always Loaded**. World Partition maps use cells instead; this skill is for non-WP maps or Level
Instances.

## Loading from code
```cpp
FLatentActionInfo Latent;
Latent.CallbackTarget = this;
Latent.ExecutionFunction = FName("OnInteriorLoaded");   // UFUNCTION() void OnInteriorLoaded();
Latent.UUID = 1; Latent.Linkage = 0;
UGameplayStatics::LoadStreamLevel(this, FName("Interior_Tavern"), /*bMakeVisibleAfterLoad*/ true,
                                  /*bShouldBlockOnLoad*/ false, Latent);
// later
UGameplayStatics::UnloadStreamLevel(this, FName("Interior_Tavern"), Latent, false);
```
Or `ULevelStreaming* L = UGameplayStatics::GetStreamingLevel(this, Name); L->SetShouldBeLoaded(true);
L->SetShouldBeVisible(true);` and bind `L->OnLevelShown`.

## Dynamic instances
`ULevelStreamingDynamic::LoadLevelInstance(World, "/Game/Rooms/Room_A", Location, Rotation, bSuccess)`
loads the same level asset multiple times at different transforms (procedural dungeons from room
levels). Each instance gets a unique package name.

## Streaming volumes
Level Streaming Volumes assigned to sublevels (Level Details > Streaming Volumes) load/unload based on
the player's viewpoint being inside. Simple for interiors; usage modes: Loading and Visibility,
Visibility only, Blocking on load (avoid: hitches).

## Timing and hitches
- Loading is async, but making a level **visible** adds its actors to the world on the game thread
  (time-sliced by `s.LevelStreamingComponentsRegistrationGranularity`,
  `s.LevelStreamingActorsUpdateTimeLimit`). Big sublevels still hitch: keep them small.
- Load a few seconds ahead (corridors, airlocks, elevators hide streaming).
- Lighting: use lighting scenarios or build lighting with all sublevels; dynamic lighting avoids issues.
- Multiplayer: servers and clients must have the same levels visible; streaming level visibility is
  replicated via the PlayerController (`ServerUpdateLevelVisibility`).

## Verify
- [ ] Walking through a streaming boundary shows no hitch beyond budget (Insights trace).
- [ ] Unloading frees memory (`memreport` before/after or `stat levels`).
- [ ] `stat levels` shows expected loaded/visible state at checkpoints.
