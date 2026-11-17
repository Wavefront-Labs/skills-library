---
id: computing-software.game-programming.godot.navigation-avoidance
name: navigation-avoidance
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-navigation, godot-avoidance, rvo, velocity-computed, navigationobstacle, avoidance-layers, crowd, game-programming]
level: practitioner
status: docs-checked
description: "Make Godot agents avoid each other with RVO avoidance: enabling it on NavigationAgent, velocity_computed flow, radius/neighbor settings, avoidance layers and NavigationObstacle."
sources: ["https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html", "https://docs.godotengine.org/en/stable/classes/class_navigationagent3d.html", "https://docs.godotengine.org/en/stable/classes/class_navigationobstacle3d.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Navigation avoidance

**Goal:** groups of agents following paths without bumping into each other or into moving obstacles.

## How it works
Godot's avoidance (RVO2-based) takes each agent's desired velocity and returns a **safe velocity**
that avoids collisions with nearby agents and obstacles, assuming all agents cooperate. It does not
replace pathfinding: agents still follow navmesh paths; avoidance only adjusts velocity locally.

## Enabling on an agent
```gdscript
@onready var agent: NavigationAgent3D = $NavigationAgent3D

func _ready() -> void:
    agent.avoidance_enabled = true
    agent.radius = 0.5                  # avoidance radius (independent of navmesh agent_radius)
    agent.neighbor_distance = 8.0
    agent.max_neighbors = 10
    agent.time_horizon_agents = 1.0
    agent.max_speed = speed
    agent.velocity_computed.connect(_on_velocity_computed)

func _physics_process(_d: float) -> void:
    if agent.is_navigation_finished(): 
        agent.velocity = Vector3.ZERO
        return
    var next := agent.get_next_path_position()
    agent.velocity = global_position.direction_to(next) * speed     # submit desired velocity

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    velocity = safe_velocity                                         # apply the safe one
    move_and_slide()
```
The movement happens in the callback; with avoidance enabled, moving in `_physics_process` directly
ignores the safe velocity. Only agents on the same navigation map that have avoidance enabled
themselves are considered. The agent must always be given a `target_position`, even if you only use it
for avoidance; otherwise the received `safe_velocity` is always zero.

## Tuning
- `time_horizon_agents` (default 1.0): the larger the value, the sooner the agent reacts to others but
  the less freedom it has in choosing velocities; too high a value slows agents considerably.
- `max_neighbors` (default 10) caps how many neighbours are considered; `neighbor_distance`
  (default 50.0) is the search radius, and a lower value reduces processing cost.
- `use_3d_avoidance` false (default) calculates avoidance along the x and z axes: correct for ground
  units. With `true` (air, water, space) agents only avoid other 3D-avoidance agents and radius-based
  obstacles, and ignore vertex-based obstacles.
- **Avoidance layers/mask**: let small critters avoid big units but not vice versa; separate teams.
- `avoidance_priority` (default 1.0): an agent does not adjust its velocity for agents with a lower
  priority, so those lower-priority agents steer around it (VIP escort walks straight).

## Obstacles
`NavigationObstacle3D` with `radius` (dynamic, moving obstacles agents should steer around) or
`vertices` (outline; clockwise winding pushes agents in, otherwise they are pushed out). With
`affect_navigation_mesh` an obstacle discards source geometry inside its shape when the navmesh is
baked. Moving obstacles should set `velocity` every frame so agents predict their motion, rather than
warping the obstacle.

## Verify
- [ ] 30 agents crossing paths in an open area do not overlap (debug draw radii).
- [ ] Agents steer around a moving obstacle with velocity set.
- [ ] Frame cost stays within budget with the expected crowd size.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the NavigationAgent3D and NavigationObstacle3D class pages and the using-NavigationAgents tutorial: avoidance_enabled and the velocity_computed flow, target_position requirement, defaults of time_horizon_agents, max_neighbors, neighbor_distance, avoidance_priority and use_3d_avoidance, obstacle radius/vertices/velocity/affect_navigation_mesh behaviour. Unconfirmed deadlock and crowd-size remarks were removed.

Method: documentation only; no commands were run.
