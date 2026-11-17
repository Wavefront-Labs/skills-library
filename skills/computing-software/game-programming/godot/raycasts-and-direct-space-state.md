---
id: computing-software.game-programming.godot.raycasts-and-direct-space-state
name: raycasts-and-direct-space-state
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-physics, raycast3d, raycast2d, physicsdirectspacestate, intersect-ray, shapecast, game-programming, shapecast3d]
level: practitioner
status: docs-checked
description: "Ray and shape queries in Godot 4: RayCast2D/3D and ShapeCast nodes, PhysicsDirectSpaceState intersect_ray/intersect_shape with query parameters, exclusions and mouse picking."
sources: ["https://docs.godotengine.org/en/stable/tutorials/physics/ray-casting.html", "https://docs.godotengine.org/en/stable/classes/class_physicsdirectspacestate3d.html", "https://docs.godotengine.org/en/stable/classes/class_raycast3d.html", "https://docs.godotengine.org/en/stable/classes/class_physicsrayqueryparameters3d.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# RayCast nodes and direct space state queries

**Goal:** line-of-sight, ground checks, hitscan and mouse picking with correct masks and no stale results.

## RayCast nodes (persistent rays)
```gdscript
@onready var ground_ray: RayCast3D = $GroundRay      # target_position = Vector3(0, -1.1, 0)
func _physics_process(_d: float) -> void:
    if ground_ray.is_colliding():
        var n := ground_ray.get_collision_normal()
        var p := ground_ray.get_collision_point()
        var who := ground_ray.get_collider()
```
- Updates every `_physics_process`. After changing the ray or its parent mid-frame call `force_raycast_update()` for an immediate update.
- `collision_mask`, `collide_with_areas`, `collide_with_bodies`, `exclude_parent` (default true), `hit_from_inside`.
- `add_exception(node)` (a CollisionObject) to ignore specific bodies.
- **ShapeCast2D/3D**: sweeps a shape; multiple results (`get_collision_count()`), good for thick bullets
  and ledge checks.

## Direct queries (one-off, from code)
```gdscript
func line_of_sight(from: Vector3, to: Vector3) -> Dictionary:
    var space := get_world_3d().direct_space_state
    var q := PhysicsRayQueryParameters3D.create(from, to, collision_mask, [get_rid()])  # exclude self
    q.collide_with_areas = false
    return space.intersect_ray(q)     # {} if nothing; else collider, collider_id, normal, position, face_index, rid, shape
```
- Physics may run on a separate thread, so the only time accessing the space is safe is during
  `_physics_process`; elsewhere it may error because the space is locked.
- `intersect_shape(PhysicsShapeQueryParameters3D, max_results = 32)` for overlap tests (explosion
  radius), `cast_motion` for the safe and unsafe fractions of a motion, `get_rest_info` for the nearest
  contact, `intersect_point` to test which solid shapes contain a point.
- 2D equivalents: `get_world_2d().direct_space_state`, `PhysicsRayQueryParameters2D`.

## Mouse picking (3D)
```gdscript
func _unhandled_input(e: InputEvent) -> void:
    if e is InputEventMouseButton and e.pressed:
        var cam := get_viewport().get_camera_3d()
        var from := cam.project_ray_origin(e.position)
        var to := from + cam.project_ray_normal(e.position) * 1000.0
        pending_pick = [from, to]       # do the query in _physics_process
```
Or set `input_ray_pickable` on CollisionObjects and use their `input_event` signal.

## Gotchas
- Query `exclude` arrays take RIDs (`body.get_rid()`), not nodes.
- A ray starting inside a collider doesn't hit it unless `hit_from_inside` is true (default false); the
  returned `normal` is then `Vector3(0, 0, 0)`.
- Results are Dictionaries (empty when no hit): check `result.is_empty()` before indexing. `face_index` is only valid for a `ConcavePolygonShape3D`, otherwise -1.

## Verify
- [ ] Debug > Visible Collision Shapes shows rays; masks exclude self and triggers.
- [ ] Ground check works on slopes and moving platforms.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Ray-casting tutorial and the RayCast3D, ShapeCast3D, PhysicsDirectSpaceState3D, PhysicsRayQueryParameters3D and CollisionObject3D class pages: force_raycast_update, collide_with_areas (false), collide_with_bodies (true), exclude_parent (true), hit_from_inside (false), add_exception, ShapeCast get_collision_count, PhysicsRayQueryParameters3D.create(from, to, collision_mask, exclude as RIDs), intersect_ray result fields, intersect_shape max_results default 32, cast_motion, get_rest_info, intersect_point, space only safe during _physics_process, input_ray_pickable and input_event.

Method: documentation only; no commands were run.
