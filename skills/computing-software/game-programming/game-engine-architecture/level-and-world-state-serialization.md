---
id: computing-software.game-programming.game-engine-architecture.level-and-world-state-serialization
name: level-and-world-state-serialization
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, serialization, level-serialization, world-state, delta-save, stable-ids, entity-references, save-game, game-programming]
level: advanced
status: draft
description: "Save and restore a level's dynamic state: stable entity ids, delta against authored level data, cross-entity references, spawned vs placed objects and load ordering."
sources: ["https://www.gameenginebook.com/", "https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Level and world state serialization

**Goal:** a save that restores the world exactly (opened doors, killed enemies, dropped items,
NPC states) while staying small and surviving content patches.

## Save deltas, not worlds
The level file already contains the authored state. Save only what changed:
- **Placed objects** (authored in the level): store a record only if their state differs from authored
  defaults, or a "destroyed" marker.
- **Spawned objects** (runtime-created: dropped loot, corpses, projectiles you choose to persist):
  store the full record including the prefab/type id.
- **Global state** (quest flags, inventory, time of day): separate section, independent of level.

## Stable ids
Every placed object needs an id that is identical every time the level loads and survives
level edits: a GUID assigned in the editor on placement (never index in the scene list, never
memory address or runtime name like `Enemy (12)`). Spawned objects get ids from a save-persistent
counter or GUID at spawn.

## Record format
```
LevelSave {
  level_id, level_content_version
  destroyed: [guid...]
  modified: [{guid, components: {Door: {open:true}, Health: {current: 12}}}]
  spawned:  [{guid, type: "loot/potion_small", transform, components:{...}}]
}
```
Only components marked saveable participate (reflection flags or an `ISaveable` interface with
`Save()`/`Load()`).

## References between objects
Serialize references as target guids. Load in two passes:
1. Create/restore all objects (apply destroyed, spawn spawned, apply component data).
2. Resolve references (guid -> live object) and call `OnPostLoad` hooks.
Never let `Load()` of one object assume another is already restored.

## Ordering and side effects
- Suppress gameplay events during restore (no "door opened" sound, no quest triggers firing).
- Physics: restore transforms and velocities, then wake/sleep bodies explicitly.
- AI: restore high-level state (patrol, alert) and let it re-plan, rather than saving the whole
  behaviour tree memory.

## Content patches
- If a guid in the save no longer exists in the level, drop the record and log it.
- New objects added to the level by a patch appear with authored defaults automatically.
- Version the save; migrate component data when schemas change.

## Engine pointers
Unity: assign `[SerializeField] string guid` in `OnValidate`/editor script if empty and unique;
Godot: `persist` group + `save()` dict per node (docs "Saving games"), use unique ids instead of node
paths for spawned nodes; Unreal: `USaveGame` + `FActorGuid`/`SaveGame` UPROPERTY flag with
`FObjectAndNameAsStringProxyArchive` (ArIsSaveGame).

## Verify
- [ ] Save, quit, load: world matches (automated comparison of saveable component data).
- [ ] Load a save made before moving/adding objects in the level: no crashes, stale records dropped.
- [ ] No gameplay events fire during load (event log is empty for the restore phase).
