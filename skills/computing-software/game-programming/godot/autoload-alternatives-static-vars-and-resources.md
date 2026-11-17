---
id: computing-software.game-programming.godot.autoload-alternatives-static-vars-and-resources
name: autoload-alternatives-static-vars-and-resources
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, static-variables, autoload-alternatives, shared-resources, dependency-injection, game-programming, godot-dependency-injection]
level: practitioner
status: docs-checked
description: "Avoid autoload sprawl in Godot 4 with static variables and functions on class_name scripts, shared Resource instances, and passing dependencies down the scene tree."
sources: ["https://docs.godotengine.org/en/stable/tutorials/best_practices/autoloads_versus_regular_nodes.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#static-variables", "https://docs.godotengine.org/en/stable/classes/class_resource.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Alternatives to autoload

**Goal:** share data and helpers without turning every system into a global node.

## Static functions and variables (Godot 4.1+)
```gdscript
class_name Rng
static var _r := RandomNumberGenerator.new()
static func seed_with(s: int) -> void: _r.seed = s
static func chance(p: float) -> bool: return _r.randf() < p

class_name EnemyRegistry
static var all: Array[Enemy] = []
# in Enemy: _enter_tree() -> EnemyRegistry.all.append(self); _exit_tree() -> EnemyRegistry.all.erase(self)
```
- No node, no process callbacks, no tree position.
- Static variables belong to the class and keep the script from being unloaded; reset them explicitly on
  new game. `@static_unload` marks a script whose statics can be reset and unloaded, but the
  GDScript reference warns that, due to a bug, scripts are currently never freed even with it.
- `@export` and `@onready` cannot be applied to a static variable.

## Shared Resources
A `.tres` resource loaded by multiple nodes is **the same instance**: the engine keeps a global cache of
loaded resources, referenced by path.
```gdscript
# player_stats.tres (class_name PlayerStats extends Resource; Resource already has a `changed` signal)
@export var stats: PlayerStats          # assign the same .tres to HUD and Player
stats.health -= 10; stats.emit_changed()
```
- Great for designer-visible shared data (ScriptableObject-style). Beware: runtime modifications affect
  the cached instance.
- Use `duplicate()` (or `resource_local_to_scene`, shown as "Local to Scene") when each user needs its
  own copy.

## Pass dependencies down
The scene that owns two systems wires them: `hud.health = player.health` in the level's `_ready`, or
exported node references. Explicit, testable, no globals.

## When autoload is still right
Needs `_process`/input, must survive scene changes as a node (music player, transition overlay), or owns
child nodes (CanvasLayer UI). The best-practices guide also accepts autoloads for broad-scoped systems
that manage their own information, such as a quest or dialogue system.

## Verify
- [ ] Each remaining autoload needs node features; pure data/helpers moved to statics or resources.
- [ ] New game resets static and shared-resource state.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Autoloads versus regular nodes best-practices page (static functions, static var since Godot 4.1, autoload is not a true singleton), the GDScript reference (static variables, @static_unload and its bug warning, @export/@onready limits) and the Resource class page (global path cache, resource_local_to_scene, duplicate, emit_changed, built-in changed signal). Unconfirmed remarks were removed.

Method: documentation only; no commands were run.
