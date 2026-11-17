---
id: computing-software.game-programming.godot.nodes-scenes-and-signals
name: nodes-scenes-and-signals
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, nodes, scenes, packedscene, signals, autoload, singleton, characterbody2d, characterbody3d, move_and_slide, _ready, _process, _physics_process, onready, export, groups, call-down-signal-up, instancing, game-programming]
level: practitioner
status: docs-checked
description: "Structure a Godot 4 game: scenes as reusable units, GDScript lifecycle callbacks, signals for child-to-parent messages, groups, autoloads, instancing, and CharacterBody movement."
sources:
  - https://docs.godotengine.org/en/stable/getting_started/step_by_step/
  - https://docs.godotengine.org/en/stable/tutorials/best_practices/
  - https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html
  - https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html
  - https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html
  - https://docs.godotengine.org/en/stable/tutorials/scripting/groups.html
  - https://docs.godotengine.org/en/stable/tutorials/scripting/instancing_with_signals.html
  - https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html
  - https://docs.godotengine.org/en/stable/tutorials/scripting/nodes_and_scene_instances.html
  - https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nodes, scenes and signals in Godot 4

**Goal:** organise a Godot project so scenes are self-contained and reusable, nodes
communicate without brittle path dependencies, and movement/physics code runs in the
right callback. Examples are GDScript for Godot 4.x.

## Mental model
- A **node** does one thing (sprite, collision shape, timer, audio). A **scene** is a
  saved tree of nodes that can be instanced inside another scene. Player, Enemy, Bullet,
  HUD, Level can each be a scene.
- Design scenes to have no dependencies where possible (the best-practices page). If a
  scene needs something from outside, have the parent provide it (dependency injection)
  instead of the scene reaching up the tree.

## Lifecycle
```gdscript
extends CharacterBody2D

@export var speed := 220.0
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D   # initialised right before _ready

signal died
signal health_changed(new_value: int)

func _physics_process(delta: float) -> void:   # fixed rate
    velocity.x = Input.get_axis("move_left", "move_right") * speed
    move_and_slide()              # uses and updates `velocity`

func _process(delta: float) -> void:   # every rendered frame
    anim.flip_h = velocity.x < 0
```
- `@onready` makes a member variable initialise right before `_ready()`.
- Physics processing runs at a fixed rate, 60 times per second by default (Physics Fps
  setting); `_process` runs per rendered frame.
- Move physics bodies in `_physics_process()`. For `CharacterBody2D` use `move_and_slide()`
  or `move_and_collide()` rather than setting position directly; `move_and_slide()` reads
  and modifies the body's `velocity` property.

## Communication
- **Child to parent:** connect to a signal. The best-practices page calls this extremely
  safe, to be used to "respond" to behaviour, not start it; by convention signal names are
  past-tense verbs.
```gdscript
# in the child
health_changed.emit(health)
died.emit()

# in the parent
$Player.health_changed.connect($HUD.set_health)
```
- Node paths and signal connections break when a scene is restructured, so keep
  cross-scene paths to a minimum.
- **Groups:** `get_tree().call_group("guards", "enter_alert_mode")` calls a method on
  every node in a group.

## Autoloads (singletons)
The best-practices page says to create an autoload "singleton" node when a script or
scene has to be globally accessible, and to prefer regular nodes with their own scripts
where possible (see "Autoloads versus regular nodes").

## Instancing at runtime
```gdscript
const BULLET := preload("res://bullet/bullet.tscn")
func fire() -> void:
    var b := BULLET.instantiate()
    get_tree().current_scene.add_child(b)
```
Bullets added as children of a moving player move with it; the instancing-with-signals page
has the player emit a `shoot` signal so the main scene spawns the bullet instead.
Free nodes with `queue_free()`, which the manual recommends unless you know what you are
doing; freeing a node also frees its children.

## Static typing
Enable the `UNTYPED_DECLARATION` warning to require typed declarations.

## Verify
- [ ] Physics movement only in `_physics_process`.
- [ ] Children talk upward via signals, not long node paths.
- [ ] Spawned nodes are added to the level, and freed with `queue_free()`.

## Checked
2026-11-01. Confirmed in the Godot manual (scene organization, signals, idle and physics
processing, groups, instancing with signals, using CharacterBody2D, nodes and scene instances,
static typing): the items listed above. Removed: F6 standalone-run rule, children-first
_ready order, 3.x versus 4.x API differences, Input Map and Project Settings paths, the
`%NodeName` and `@export` target advice, event-bus advice, null `$Child` in initialisers,
speed claim for static typing, export templates and C# web export notes, which the fetched
pages do not state.
Method: documentation only; no commands were run.
