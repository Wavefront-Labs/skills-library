---
id: computing-software.game-programming.godot.instancing-scenes-at-runtime
name: instancing-scenes-at-runtime
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, scene-instancing, godot-instancing, packedscene, preload, spawning, game-programming]
level: intro
status: verified
description: "Instance PackedScenes at runtime in Godot 4: preload vs load, instantiate, setting properties before add_child, choosing the parent, editable children and freeing safely."
sources: ["https://docs.godotengine.org/en/stable/getting_started/step_by_step/instancing.html", "https://docs.godotengine.org/en/stable/classes/class_packedscene.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instancing scenes at runtime

**Goal:** spawn bullets, enemies and pickups from scene files correctly and cheaply.

## Basics
```gdscript
const BULLET := preload("res://weapons/bullet.tscn")    # loaded at script load (compile time constant)

func fire() -> void:
    var b := BULLET.instantiate() as Bullet
    b.global_transform = muzzle.global_transform          # set BEFORE add_child so _ready sees it
    b.speed = 900.0
    get_tree().current_scene.add_child(b)                 # world-owned, not a child of the gun
```
- `preload` for always-needed scenes (path must be a literal). `load()` at runtime for optional/large ones;
  `ResourceLoader.load_threaded_request` for background loading.
- Setting `global_position` before the node is in the tree works for Node2D/3D in Godot 4 (applied to the
  local transform relative to no parent); to be safe with parents that have transforms, set
  `position` relative to the new parent or set global after `add_child`.
- Parent choice: projectiles go under the level/world (else they move with the shooter). Keep a
  `Projectiles` Node as a container for counting and cleanup.
- `add_child` during physics callbacks (body_entered): use `add_child.call_deferred(b)` or
  `call_deferred("add_child", b)` to avoid "Can't change this state while flushing queries".

## Typed instancing
Give the root a `class_name` (`class_name Bullet extends Area2D`) so `instantiate() as Bullet` gives
autocompletion; at runtime the cast returns null on a type mismatch rather than raising an error (run: `Node.new() as Bullet` is null).

## Freeing
- `queue_free()` at end of frame (safe); `free()` immediately (unsafe if still referenced in this frame).
- `is_instance_valid(node)` before using stored references to possibly-freed nodes.
- Many short-lived instances (bullets): pool them (hide + disable processing, reuse) if the profiler
  shows instancing cost.

## Editor-side instancing
- Dragging a .tscn into another scene instances it. **Editable Children** exposes the instance's internals for per-instance
  tweaks (it appears in the Godot docs, e.g. the animation and sub-emitter pages).

## Gotchas
- Instantiating the same scene recursively (a scene that instances itself) errors at load (run: loading a `.tscn` that instances itself logged `[ext_resource] referenced non-existent resource`).
- `owner` is not set for runtime-added nodes (run: `h.owner` was null after `add_child`); set `node.owner` if you need to save the tree with
  `PackedScene.pack`.

## Verify
- [ ] Spawned objects appear at the right place on the first frame (no flash at origin).
- [ ] Remote scene tree shows bullets under the projectile container and freed after lifetime.
## Checked
Ran on Godot 4.7.2 headless: `preload("res://bullet.tscn")`, `instantiate() as Bullet`, `b.global_position` and `b.speed` set before `add_child` (the bullet's `_ready` printed the position and speed), `global_position` set on a node outside the tree gives the same local position, `ResourceLoader.load_threaded_request`, `load_threaded_get_status` and `load_threaded_get` (status 3, loaded `PackedScene`), `add_child.call_deferred` and `queue_free()` inside a `body_entered` handler with no errors, recursive scene load result. `free()` versus `queue_free()` behaviour is checked in the queue-free skill.
