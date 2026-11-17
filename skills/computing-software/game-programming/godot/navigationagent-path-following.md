---
id: computing-software.game-programming.godot.navigationagent-path-following
name: navigationagent-path-following
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-navigation, navigationagent, navigationagent3d, navigationagent2d, target-position, get-next-path-position, navigation-map-sync, game-programming]
level: practitioner
status: docs-checked
description: "Move characters along Godot navigation paths with NavigationAgent2D/3D: target_position, get_next_path_position, waiting for map sync, path desired distances and repathing."
sources: ["https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html", "https://docs.godotengine.org/en/stable/classes/class_navigationagent3d.html", "https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_introduction_3d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NavigationAgent path following

**Goal:** an NPC that walks to a target over a baked navmesh, updates when the target moves, and
stops cleanly.

## Scene
```
Enemy (CharacterBody3D)
  CollisionShape3D
  NavigationAgent3D
```
A `NavigationRegion3D` with a baked `NavigationMesh` must exist in the level (see godot navigation
region baking).

## Script
```gdscript
extends CharacterBody3D
@export var speed := 4.0
@onready var agent: NavigationAgent3D = $NavigationAgent3D

func _ready() -> void:
    agent.path_desired_distance = 0.5      # how close before advancing to the next path point
    agent.target_desired_distance = 1.0    # how close counts as arrived
    # The map has not synchronized yet in _ready(); an early query returns an empty path.
    set_physics_process(false)
    await get_tree().physics_frame
    set_physics_process(true)

func set_target(pos: Vector3) -> void:
    agent.target_position = pos

func _physics_process(_delta: float) -> void:
    if agent.is_navigation_finished():
        velocity = Vector3.ZERO
        return
    var next := agent.get_next_path_position()
    var dir := global_position.direction_to(next)
    dir.y = 0
    velocity = dir.normalized() * speed
    move_and_slide()
```
Call `get_next_path_position()` **once per physics frame**; the class reference says this call is
required every physics frame to update the agent's internal path logic.

## Re-pathing to moving targets
Setting `target_position` every frame forces a new path query every frame, which can make the agent
"dance" between two positions or look backwards for a frame. Throttle: update when the target moved
more than a threshold or on a timer. A very fast agent can overshoot `path_desired_distance` and
backtrack; raise the desired distances to suit its speed.

## Signals
`navigation_finished`, `target_reached`, `waypoint_reached`, `link_reached`, `path_changed`,
`velocity_computed` (avoidance). `target_reached` fires once per loaded path when the agent is within
`target_desired_distance` of the target, just before `navigation_finished`; use it for gameplay
("arrived at cover").

## Agent parameters vs navmesh
The baked navmesh's `agent_radius`/`agent_height`/`agent_max_climb`/`agent_max_slope` define where
agents can walk. NavigationAgent's `radius` is only for avoidance. Agents of different sizes need
different navigation maps/regions baked with different radii, selected via `navigation_layers`.

## Debugging
Debug > Visible Navigation shows navmeshes; `agent.debug_enabled = true` draws the current path.
`NavigationServer3D.map_get_iteration_id(agent.get_navigation_map())` is 0 until the map has first
synchronized; the tutorial's own example skips the query while it is 0.

## Verify
- [ ] Agent reaches targets around obstacles and stops within target_desired_distance.
- [ ] No "map not synced" empty paths on the first frame.
- [ ] 50 agents chasing the player stay within the frame budget with throttled re-pathing.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the using-NavigationAgents tutorial and the NavigationAgent3D class page: target_position, path_desired_distance, target_desired_distance, is_navigation_finished, get_next_path_position once per physics frame, the empty-path-before-map-sync pitfall and the map_get_iteration_id check, the list of signals, per-frame repath symptoms, agent debug_enabled, and that the Debug menu's Visible Navigation shows navigation (ProjectSettings debug shapes). Removed the unsupported 0.25 s throttle figure and the query_path batching remark.

Method: documentation only; no commands were run.
