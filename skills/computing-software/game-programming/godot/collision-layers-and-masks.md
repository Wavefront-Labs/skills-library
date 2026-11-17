---
id: computing-software.game-programming.godot.collision-layers-and-masks
name: collision-layers-and-masks
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-physics, collision-layers, collision-mask, layer-names, physics-layers, game-programming]
level: intro
status: docs-checked
description: "Plan Godot collision layers and masks: layer vs mask semantics, naming layers in Project Settings, setting bits from code and common layouts for players, enemies, projectiles."
sources: ["https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html#collision-layers-and-masks", "https://docs.godotengine.org/en/stable/classes/class_collisionobject2d.html", "https://docs.godotengine.org/en/stable/classes/class_tileset.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collision layers and masks

**Goal:** objects collide, detect and ray-hit exactly the things they should.

## Semantics
- **collision_layer**: what this object **is** (the layers it exists on).
- **collision_mask**: what this object **looks for / collides with**.
- A scans for B if A's mask includes a layer B is in; an object not in one of the mask layers is
  ignored by that body. Set the masks on both sides for symmetric, predictable behaviour. By default
  all bodies are on layer 1 and scan layer 1.
- Areas: detection requires the area's mask to include the other object's layer.
- Raycasts and ShapeCasts only have a mask.

## Name the layers
Project Settings > Layer Names > 2D Physics / 3D Physics:
```
1 world   2 player   3 enemies   4 player_projectiles   5 enemy_projectiles   6 pickups   7 hurtboxes   8 triggers
```
The Inspector then shows the names for each layer.

## Typical setup
| Object | Layer | Mask |
|---|---|---|
| Player body | player | world, enemies |
| Enemy body | enemies | world, player |
| Player bullet (Area) | player_projectiles | world, enemies |
| Pickup (Area) | pickups | player |
| Enemy hurtbox (Area) | hurtboxes | (none: monitorable only) |

## From code
```gdscript
set_collision_layer_value(4, true)            # 1-based layer number
set_collision_mask_value(3, false)
collision_mask = (1 << 0) | (1 << 2)          # bitmask: layers 1 and 3
const MASK_WORLD := 1 << 0
@export_flags_2d_physics var hit_mask := 1    # inspector layer picker for your own exports
```
I-frames: temporarily remove the hurtbox layer, or toggle `monitorable`.

## Gotchas
- There are 32 layers; don't burn one per enemy type.
- Function calls that enable all layers by default take the mask `0xffffffff`.
- TileSet physics layers have their own collision layer and mask (`TileSet.set_physics_layer_collision_layer()` and `_mask()`).

## Verify
- [ ] A table like the above exists in project docs and matches the inspector.
- [ ] Player bullets never hit the player; pickups ignore enemies.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Physics introduction tutorial (32 layers, collision_layer and collision_mask meaning and defaults, Project Settings > Layer Names > 2D Physics, bitmask code and set_collision_layer_value / set_collision_mask_value, @export_flags_2d_physics), the Area2D, RayCast3D and TileSet class pages (area mask must include the other layer; rays only have a mask; per-physics-layer collision layer and mask). Removed the unsupported either-mask-matches rule and the set_deferred remarks.

Method: documentation only; no commands were run.
