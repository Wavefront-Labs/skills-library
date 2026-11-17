---
id: computing-software.game-programming.godot.renderingserver-and-physicsserver-direct
name: renderingserver-and-physicsserver-direct
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-performance, renderingserver, physicsserver, servers, rid, optimisation, game-programming]
level: advanced
status: docs-checked
description: "Bypass the scene tree with RenderingServer and PhysicsServer2D/3D for thousands of objects: RIDs, canvas items and instances, bodies and shapes, and manual lifetime management."
sources: ["https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html", "https://docs.godotengine.org/en/stable/classes/class_renderingserver.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using servers directly

**Goal:** draw and simulate thousands of simple things (bullets, particles with collision, grass)
without one Node each.

## Why
Nodes are convenient but heavy: tree notifications, transforms, signals, scripts. Servers are the
low-level APIs nodes use internally; you hold **RIDs** (opaque handles) and call the server directly.

## RenderingServer 2D
```gdscript
var items: Array[RID] = []
var tex := preload("res://bullet.png")

func spawn(pos: Vector2) -> void:
    var ci := RenderingServer.canvas_item_create()
    RenderingServer.canvas_item_set_parent(ci, get_canvas_item())      # draw under this node
    RenderingServer.canvas_item_add_texture_rect(ci, Rect2(-tex.get_size() / 2, tex.get_size()), tex)
    RenderingServer.canvas_item_set_transform(ci, Transform2D(0, pos))
    items.append(ci)

func _exit_tree() -> void:
    for ci in items: RenderingServer.free_rid(ci)                      # you own the lifetime
```
Keep a reference to `tex`: resources are reference-counted, and references to a resource's RID are not counted.

## RenderingServer 3D
`instance_create()`, `instance_set_base(inst, mesh.get_rid())`, `instance_set_scenario(inst, get_world_3d().scenario)`,
`instance_set_transform(inst, xform)`. For many identical meshes, consider a MultiMesh instead.

## PhysicsServer2D
```gdscript
var body := PhysicsServer2D.body_create()
PhysicsServer2D.body_set_mode(body, PhysicsServer2D.BODY_MODE_KINEMATIC)
var shape := PhysicsServer2D.circle_shape_create()
PhysicsServer2D.shape_set_data(shape, 4.0)
PhysicsServer2D.body_add_shape(body, shape)
PhysicsServer2D.body_set_space(body, get_world_2d().space)
PhysicsServer2D.body_set_state(body, PhysicsServer2D.BODY_STATE_TRANSFORM, Transform2D(0, pos))
PhysicsServer2D.body_set_collision_layer(body, 1 << 3)
# cleanup: PhysicsServer2D.free_rid(body); PhysicsServer2D.free_rid(shape)
```
For bullets, often skip physics bodies entirely: move data in arrays and use
`direct_space_state.intersect_ray` / `intersect_point` per bullet, or simple distance checks.

## Pattern
Keep simulation in packed arrays (positions, velocities), update in one `_physics_process`, push
transforms to the server in a loop. One node, thousands of entities.

## Gotchas
- You own the lifetime of server-created RIDs: free them with `free_rid` in `_exit_tree` / on despawn.
- The servers tutorial notes that multiple threads cannot be used with some server setups; read it before calling servers off the main thread.
- Debugging is harder (nothing in the remote tree); keep counts visible in a debug overlay.

## Verify
- [ ] The server-drawn version performs better than the node version in a profile of both.
- [ ] Resource and RID counts return to baseline after clearing (no leaked RIDs).

## Checked

2026-10-28. Confirmed against: RenderingServer reference (canvas_item_create, canvas_item_set_parent, canvas_item_add_texture_rect, canvas_item_set_transform, instance_create, instance_set_base, instance_set_scenario, instance_set_transform, free_rid), PhysicsServer2D reference (body_create, body_set_mode, BODY_MODE_KINEMATIC, circle_shape_create, shape_set_data, body_add_shape, body_set_space, body_set_state, BODY_STATE_TRANSFORM, body_set_collision_layer, free_rid) and the using-servers tutorial.

Removed or rewritten: the queued-to-render-thread statement, the MultiMesh speed claim, the 5,000-bullet target and the leaked-RID-until-exit claim.

Method: documentation only; no commands were run.
