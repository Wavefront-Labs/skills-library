---
id: computing-software.game-programming.godot.navigation-links
name: navigation-links
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-navigation, navigationlink, navigationlink3d, off-mesh-link, link-reached, jump-links, ladders, teleporters, game-programming]
level: practitioner
status: docs-checked
description: "Connect disconnected navmesh areas in Godot with NavigationLink2D/3D: jump-downs, ladders and teleporters, bidirectional links, travel costs and custom traversal on link_reached."
sources: ["https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationlinks.html", "https://docs.godotengine.org/en/stable/classes/class_navigationlink3d.html", "https://docs.godotengine.org/en/stable/classes/class_navigationagent3d.html#signals", "https://docs.godotengine.org/en/stable/classes/class_projectsettings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Navigation links

**Goal:** agents path across gaps the navmesh cannot connect (ledges to drop from, ladders,
teleporters, doors) and play the right traversal when they get there.

## Placing a link
Add `NavigationLink3D` to the scene; set `start_position` and `end_position` (local) with the gizmo so
each end sits on (or within the map's link connection radius of) a navmesh polygon. Properties:
- `bidirectional`: false for one-way drops (ledge down only).
- `navigation_layers`: which agents may use it (e.g. only climbers).
- `enter_cost` (added once) and `travel_cost` (multiplier on length): make teleporters cheap or
  ladders expensive to influence path choice.
- `enabled`: toggle at runtime (locked door).

## Traversal
The pathfinder includes the link as a straight segment. The agent reaches the link start and then
the next path position is the link end; by default your movement code would try to walk straight
through the air/wall. Detect the link and play custom movement:
```gdscript
func _ready() -> void:
    agent.link_reached.connect(_on_link_reached)

func _on_link_reached(details: Dictionary) -> void:
    var owner = details.get("owner")              # the NavigationLink3D node
    var to: Vector3 = details.get("link_exit_position")
    if owner.is_in_group("jump_link"):
        traversing = true
        await jump_to(to)                         # play jump animation / arc tween
        traversing = false
    elif owner.is_in_group("teleporter"):
        global_position = to
```
While `traversing`, skip normal path-following in `_physics_process`. Dictionary keys include
`position`, `type`, `rid`, `owner`, `link_entry_position`, `link_exit_position`, depending on
`path_metadata_flags`; the entry and exit positions are only present when `owner` is a
`NavigationLink3D` (see agent docs).

## Generating links
For procedural levels, create links in code (`NavigationLink3D.new()` with positions) or directly
through `NavigationServer3D.link_create()`, `link_set_start_position`, `link_set_map`.

## Gotchas
- Each link end searches for the closest navmesh polygon within the link connection radius (project
  setting `navigation/3d/default_link_connection_radius`, or per map with
  `NavigationServer3D.map_set_link_connection_radius()`); if none is found in range the link is disabled.
- Links are not obstacles or collision: the physics world must allow the traversal (open the door
  collider when the door link is enabled).

## Verify
- [ ] Debug navigation shows the link; agents choose it when it is the shorter/cheaper route.
- [ ] Agents perform the custom traversal and resume path following at the exit.
- [ ] Disabling a link makes agents re-path around it.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the using-NavigationLinks tutorial and class pages: start_position/end_position, bidirectional (default true), navigation_layers, enter_cost (default 0.0) and travel_cost (default 1.0), enabled (a disabled link is ignored by map_get_path), the link_reached signal and its details keys, the link connection radius setting and per-map setter, and NavigationServer3D link_create/link_set_start_position/link_set_map. The claim about edge-scanning tools was removed as unsupported.

Method: documentation only; no commands were run.
