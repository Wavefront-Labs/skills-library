---
id: computing-software.game-programming.godot.area-detection-and-overlap
name: area-detection-and-overlap
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-physics, area2d, area3d, overlap-detection, triggers, gravity-override, game-programming]
level: intro
status: docs-checked
description: "Use Area2D/Area3D for triggers, hit/hurt boxes and zones: monitoring vs monitorable, body vs area signals, overlap queries, space overrides and timing pitfalls."
sources: ["https://docs.godotengine.org/en/stable/tutorials/physics/using_area_2d.html", "https://docs.godotengine.org/en/stable/classes/class_area2d.html", "https://docs.godotengine.org/en/stable/classes/class_area3d.html", "https://docs.godotengine.org/en/stable/tutorials/physics/troubleshooting_physics_issues.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Area detection and overlap

**Goal:** pickups, damage zones, hitboxes and water volumes that detect exactly what they should.

## Signals
| Signal | Fires for |
|---|---|
| `body_entered(body)` / `body_exited` | PhysicsBody (Character/Rigid/Static/Animatable) and TileMaps whose TileSet has collision shapes |
| `area_entered(area)` / `area_exited` | other Areas |
| `body_shape_entered(...)` | per-shape detail (which collision shape was hit) |

```gdscript
extends Area2D
func _ready() -> void:
    body_entered.connect(_on_body_entered)
func _on_body_entered(body: Node2D) -> void:
    if body is Player:
        body.collect(self)
        queue_free()
```

## Monitoring vs monitorable
- `monitoring = true` (default): this area **detects** others (the entered/exited signals require it).
- `monitorable = true` (default): other monitoring areas **can detect** this area.
- Hurtbox (receives hits): monitorable; hitbox (deals hits): monitoring. Turn off what you don't need: cheaper.
- Detection also requires layer/mask: the area's **mask** must include the other object's **layer**.

## Polling
`get_overlapping_bodies()` / `get_overlapping_areas()` / `has_overlapping_bodies()`: for performance
reasons the lists are modified once during the physics step, not immediately after objects move or
are spawned, so wait for the next physics step.
```gdscript
hitbox.monitoring = true
await get_tree().physics_frame          # let the overlap list update
for a in hitbox.get_overlapping_areas(): (a as Hurtbox).hit(damage)
```

## Space overrides
Area properties `gravity_space_override`, `gravity`, `gravity_point` (planet gravity), `linear_damp`,
`angular_damp` affect RigidBodies inside (water, low gravity zones); the `*_space_override` modes decide
how they combine, and `priority` (higher is processed first) orders overlapping areas. Area3D also has
`wind_*` properties and audio bus override / reverb bus settings for audio zones.

## Gotchas
- Fast-moving objects can tunnel through thin shapes (see the Troubleshooting physics issues page); use
  a raycast or ShapeCast for hitscan.
- `body_entered` fires again if a body leaves and re-enters; guard one-shot pickups with a flag.

## Verify
- [ ] Debug > Visible Collision Shapes shows areas where expected; layers/masks set per role.
- [ ] Spawning inside an area triggers the expected entry on the next physics frame.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Using Area2D tutorial and the Area2D and Area3D class pages: body_entered, area_entered and body_shape_entered signals and what they report (including TileMaps with collision shapes), monitoring and monitorable (both default true), overlap lists updated once per physics step, the area mask must include the other object's layer, gravity/damp space overrides, priority, wind and audio/reverb properties on Area3D; tunneling advice in Troubleshooting physics issues. The unconfirmed 'flushing queries' error text was removed.

Method: documentation only; no commands were run.
