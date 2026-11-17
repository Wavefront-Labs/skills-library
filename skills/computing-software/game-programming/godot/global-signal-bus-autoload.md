---
id: computing-software.game-programming.godot.global-signal-bus-autoload
name: global-signal-bus-autoload
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, signal-bus, event-bus, autoload, decoupling, game-programming]
level: intro
status: docs-checked
description: "Create a global signal bus autoload in Godot for cross-scene events (achievements, UI, audio), with typed signals, and know when it hurts more than it helps."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html", "https://docs.godotengine.org/en/stable/classes/class_object.html", "https://docs.godotengine.org/en/stable/classes/class_signal.html", "https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global event bus autoload

**Goal:** systems in unrelated scenes (HUD, achievements, audio, analytics) react to gameplay events
without references to each other.

## Setup
```gdscript
# events.gd, registered as autoload "Events" (Project Settings > Globals > Autoload)
extends Node

signal enemy_killed(enemy_type: StringName, position: Vector2)
signal coin_collected(amount: int)
signal level_completed(level_id: String, time_sec: float)
signal player_health_changed(current: int, maximum: int)
```
```gdscript
# enemy.gd
func die() -> void:
    Events.enemy_killed.emit(type, global_position)
    queue_free()

# achievements.gd (another autoload or node)
func _ready() -> void:
    Events.enemy_killed.connect(_on_enemy_killed)
```
- The bus only declares signals; no logic, no state.
- Script-only autoload (a .gd file) is enough.

## Rules that keep it sane
- Use the bus for **global, many-to-many, cross-scene** events. Parent/child or sibling communication
  inside one scene should use direct signals ("call down, signal up").
- Group signals by domain and keep the list small; a bus with 100 signals is a hidden global API.
- Listeners with a shorter lifetime than the bus: the class reference says the connection is lost when
  the callable's object is freed; disconnect explicitly in other cases.
- Emitting is synchronous: listeners run immediately, inside the emitter's call. Heavy listeners slow the
  emitter; `CONNECT_DEFERRED` runs the listener at the end of the frame instead of instantly.
- Hard to trace: name signals clearly and grep for `Events.` to see all emitters and listeners.

## Testing
A bus makes systems testable in isolation: emit `Events.coin_collected.emit(5)` in a test scene and assert
the HUD updated.

## Verify
- [ ] HUD/achievements work when the emitting scene is loaded alone (no direct references).
- [ ] No in-scene parent/child communication goes through the bus.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the autoloads tutorial (script autoload registered under Project Settings > Globals > Autoload) and the Object and Signal class pages (CONNECT_DEFERRED triggers at the end of the frame; a connection is lost when the callable's object is freed). The unsupported claim that lambdas do not auto-disconnect was removed.

Method: documentation only; no commands were run.
