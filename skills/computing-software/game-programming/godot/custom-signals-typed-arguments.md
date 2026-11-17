---
id: computing-software.game-programming.godot.custom-signals-typed-arguments
name: custom-signals-typed-arguments
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, signals, custom-signals, typed-signals, emit, game-programming]
level: intro
status: verified
description: "Declare custom signals with typed arguments in GDScript, emit them, document them, and design signal APIs (past-tense names, minimal payloads) that keep scenes decoupled."
sources: ["https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html", "https://docs.godotengine.org/en/stable/classes/class_signal.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom signals with typed arguments

**Goal:** child nodes announce what happened; parents and listeners decide what to do.

## Declare and emit
```gdscript
class_name Health extends Node

## Emitted after health changes. `delta` is negative for damage.
signal health_changed(current: int, max_health: int, delta: int)
signal died

@export var max_health := 100
var current := max_health:
    set(v):
        var old := current
        current = clampi(v, 0, max_health)
        if current != old:
            health_changed.emit(current, max_health, current - old)
            if current == 0: died.emit()
```
- Godot 4: `signal_name.emit(args)` (first-class Signal objects). `emit_signal("name", ...)` still works
  but is untyped and typo-prone.
- Argument types are documentation and editor hints (the Godot docs say they show in the Signals dock); they
  are **not enforced** at emit time (run: `emit("wrong", 5)` on `signal s3(a: int, b: String)` reached the handler
  unchanged; only the argument count is checked), so keep emitters disciplined.
- `##` doc comments above a signal show in the editor's help.

## Design rules
- Name in past tense for events (`died`, `item_picked_up`), present for state changes (`health_changed`).
- Emit facts, not commands (`door_opened`, not `play_door_sound`).
- Pass the minimal data listeners need; pass `self` only if listeners need to identify the sender among many.
- Emit after state is updated, so listeners reading the emitter see consistent values.
- Don't emit in `_init`; nobody is connected yet. In `_ready`, children's listeners from the parent may
  not be connected yet either (parent `_ready` runs after children).

## Inspect
- Node dock > Signals lists built-in and custom signals; connected ones show an icon in the scene tree.
- `get_signal_connection_list("died")`, `has_signal()`, `is_connected()`.

## Verify
- [ ] Every custom signal has at least one listener or a reason to exist.
- [ ] Listener handlers match the signal's argument count: a mismatch logs `Method expected 1 argument(s), but called with 2.` at emit time and the handler does not run.
## Checked
Ran on Godot 4.7.2 headless: the `Health` class above with the setter (`current = 60` emits `60 100 -40`, then `0` emits `0 100 -60` and `died`); typed-signal emit with wrong types and with mismatched handler arity; `has_signal`, `is_connected`, `get_signal_connection_list`. `##` doc comments above a signal are listed in the GDScript documentation comments page. Child `_ready` before parent `_ready` shown in the lifecycle run (children C1, C2 ready before P).
