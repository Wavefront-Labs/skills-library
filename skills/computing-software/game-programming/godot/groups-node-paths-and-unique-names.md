---
id: computing-software.game-programming.godot.groups-node-paths-and-unique-names
name: groups-node-paths-and-unique-names
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, godot-groups, unique-name, node-paths, get-node, call-group, game-programming]
level: intro
status: verified
description: "Find nodes robustly in Godot 4: groups and call_group, scene unique names (%Name), exported NodePaths/node references instead of brittle $Parent/Child paths."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/groups.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/scene_unique_nodes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Groups, node paths and unique names

**Goal:** scripts that survive reorganising the scene tree.

## Ranking of ways to reference nodes
1. **Exported node reference** (Godot 4): `@export var target: Node3D` then drag in the inspector.
   Survives renames and moves within the scene.
2. **Scene unique name**: right-click node > *Access as Unique Name*, then `%HealthBar` from any script
   in the same scene. Survives reparenting inside that scene.
3. `$Relative/Path` for direct, stable children only.
4. `get_node("../../Something")` up the tree: brittle, avoid ("call down, signal up").

```gdscript
@export var spawn_points: Array[Marker3D]
@onready var health_bar: ProgressBar = %HealthBar
```
- `%Name` only works within the scene that owns the node; instanced sub-scenes have their own unique-name scope.
  From outside, go through the instance: `get_node("Hand/Sword/%Hilt")` or `get_node("Hand/Sword").get_node("%Hilt")`
  (Godot docs, Scene Unique Nodes). In code, `unique_name_in_owner = true` only resolves once the node's `owner` is set
  (run: `n.get_node("%HealthBar")` found the child after `h.owner = n`).
- `get_node_or_null()` when a node may be absent.

## Groups
Tag nodes with groups (the Groups dock, or code) to address sets without paths.
```gdscript
func _ready() -> void:
    add_to_group("enemies")

# anywhere
for e in get_tree().get_nodes_in_group("enemies"):
    e.alert(player.global_position)
get_tree().call_group("enemies", "alert", player.global_position)     # calls method on all
get_tree().call_group_flags(SceneTree.GROUP_CALL_DEFERRED, "enemies", "die")
get_tree().get_first_node_in_group("player")
if body.is_in_group("damageable"): body.take_damage(10)
```
- Groups are great for "all of type X" queries and save/load (`get_nodes_in_group("persist")`).
- Group names are strings: define constants (`const ENEMIES := &"enemies"`) to avoid typos.
- Global groups (the Groups tab of the Globals dock in Project Settings, 4.3+) appear in the editor with descriptions.

## Gotchas
- `get_nodes_in_group` allocates an array each call; cache in hot paths or maintain your own registry.
- Unique names and groups are per-node properties saved in the scene; instanced scenes keep their own.

## Verify
- [ ] Moving a node in the scene tree breaks no script (exports or unique names used).
- [ ] No `get_node("../..")` upward paths in gameplay scripts.
## Checked
Ran on Godot 4.7.2 headless: `add_to_group`, `get_nodes_in_group` (2 nodes), `get_first_node_in_group`, `call_group` (names changed immediately), `call_group_flags(SceneTree.GROUP_CALL_DEFERRED, ...)` (name changed only after the next frame), `get_children()` typed array, `%Name` lookup with `unique_name_in_owner`. Same-scene limitation, `%` in the middle of a path, and Global Groups (present in the 4.3 and 4.4 docs, absent from 4.2) from the Godot docs "Scene Unique Nodes" and "Groups" pages. The Groups dock and Access as Unique Name steps are as described in the same docs pages (editor not opened).
