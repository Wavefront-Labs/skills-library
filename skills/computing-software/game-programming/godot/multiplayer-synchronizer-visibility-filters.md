---
id: computing-software.game-programming.godot.multiplayer-synchronizer-visibility-filters
name: multiplayer-synchronizer-visibility-filters
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, multiplayersynchronizer, visibility, interest-management, game-programming, replication-visibility]
level: practitioner
status: docs-checked
description: "Limit which peers receive Godot MultiplayerSynchronizer and spawner updates with public_visibility, set_visibility_for and visibility filters for interest management."
sources: ["https://docs.godotengine.org/en/stable/classes/class_multiplayersynchronizer.html", "https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html", "https://godotengine.org/article/multiplayer-in-godot-4-0-scene-replication/", "https://docs.godotengine.org/en/stable/classes/class_multiplayerspawner.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Synchronizer visibility filters

**Goal:** peers receive only the objects relevant to them (nearby enemies, own team data) to save
bandwidth and hide information.

## Controls on MultiplayerSynchronizer
- `public_visibility` (default true): synchronization is visible to all peers by default. Set false to
  start from nothing visible and use the options below.
- `set_visibility_for(peer, visible)`: per-peer setting; peer 0 updates `public_visibility` instead.
  `get_visibility_for(peer)` reads it.
- `add_visibility_filter(filter: Callable)` / `remove_visibility_filter(filter)`: filters are updated
  by `update_visibility(for_peer = 0)`.
- `visibility_update_mode`: `VISIBILITY_PROCESS_IDLE` (default), `VISIBILITY_PROCESS_PHYSICS`, or
  `VISIBILITY_PROCESS_NONE` (filters are not updated automatically; call `update_visibility()` yourself).
- `replication_interval` and `delta_interval` (both default 0.0) throttle synchronization.

## Interest management example
```gdscript
# on the server, enemy.gd
@onready var sync: MultiplayerSynchronizer = $MultiplayerSynchronizer
const RANGE := 60.0
func _ready() -> void:
    if not multiplayer.is_server(): return
    sync.public_visibility = false
    sync.visibility_update_mode = MultiplayerSynchronizer.VISIBILITY_PROCESS_NONE
    sync.add_visibility_filter(_visible_to)
    $VisTimer.timeout.connect(sync.update_visibility)   # on a timer, not every frame
func _visible_to(peer: int) -> bool:
    var p := Players.get_player(peer)
    return p != null and p.global_position.distance_to(global_position) < RANGE
```
If the synchronizer's `root_path` node was spawned by a **MultiplayerSpawner**, the node is also spawned
and despawned on a peer according to this synchronizer's visibility options, so design such nodes to
tolerate being despawned and respawned.

## Team-private data
Put secret properties (ammo, hand of cards) in a separate synchronizer and keep public state in another,
so visibility can differ per synchronizer.

## Verify
- [ ] The network profiler shows a peer receives no updates for far-away objects; hidden data never
  reaches other teams.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the MultiplayerSynchronizer and MultiplayerSpawner class pages: public_visibility default true, set_visibility_for (peer 0 behaviour), get_visibility_for, add/remove_visibility_filter, update_visibility, visibility_update_mode enum and default IDLE, delta_interval and replication_interval defaults, spawn/despawn follows synchronizer visibility. Fixed: update-mode names (Idle, Physics, None) are VISIBILITY_PROCESS_IDLE, VISIBILITY_PROCESS_PHYSICS, VISIBILITY_PROCESS_NONE; removed the claim that Physics mode re-evaluates every frame and the "4.2+" gate. Removed (not confirmed): all-filters-must-be-true, filters-run-on-authority-only, RPCs-not-filtered, O(n*m) cost note, respawn-state-from-spawn-properties, On Change vs Always wording, the 0.5 s timer value.
Method: documentation only; no commands were run.
