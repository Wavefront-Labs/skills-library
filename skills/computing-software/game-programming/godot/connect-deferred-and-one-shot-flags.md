---
id: computing-software.game-programming.godot.connect-deferred-and-one-shot-flags
name: connect-deferred-and-one-shot-flags
category: computing-software
field: game-programming
product: godot
tags: [godot, signals, connect-deferred, connect-one-shot, call_deferred, game-programming]
level: practitioner
status: verified
description: "Use Godot ConnectFlags well: CONNECT_DEFERRED for safe physics/tree changes, CONNECT_ONE_SHOT for single-fire waits, CONNECT_PERSIST for editor connections, and call_deferred."
sources: ["https://docs.godotengine.org/en/stable/classes/class_object.html#enum-object-connectflags", "https://docs.godotengine.org/en/stable/classes/class_object.html#class-object-method-call-deferred"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CONNECT_DEFERRED and CONNECT_ONE_SHOT

**Goal:** signal handlers that run at a safe time and connections that clean themselves up.

## Flags (Object.ConnectFlags, combinable with |)
- `CONNECT_DEFERRED`: handler is queued and runs at idle time (end of frame), not inside `emit`.
- `CONNECT_PERSIST`: saved into the scene when connected in the editor/tool scripts.
- `CONNECT_ONE_SHOT`: disconnects after the first emission.
- `CONNECT_REFERENCE_COUNTED`: same callable can be connected multiple times; disconnect count must
  match.
```gdscript
area.body_entered.connect(_on_body_entered, CONNECT_DEFERRED)
anim.animation_finished.connect(_on_intro_done, CONNECT_ONE_SHOT)
```

## Why deferred
Physics signals (`body_entered`, `area_entered`) fire while the physics server is flushing queries.
Changing collision state there errors. Run on 4.7.2: `shape.disabled = true` in a `body_entered` handler logs
"Can't change this state while flushing queries. Use call_deferred() or set_deferred() to change monitoring state instead.",
and `area.monitoring = false` logs "Function blocked during in/out signal. Use set_deferred("monitoring", true/false).".
Adding a plain `Area2D` child and `queue_free()` in the handler logged no error in the same test.
Options:
- connect with `CONNECT_DEFERRED`,
- inside the handler: `collision_shape.set_deferred("disabled", true)`,
  `add_child.call_deferred(pickup)`, `queue_free()`.
Also useful to avoid re-entrancy: an emit that triggers another emit of the same signal.

## call_deferred
`method.call_deferred(args)` (Callable form) or `call_deferred("method", args)` queues a call for idle
time. Deferred calls ran in FIFO order (1, 2, 3 for three calls queued in that order, with the Callable and string forms mixed). `set_deferred(property, value)`
for properties.

## One-shot vs await
`await anim.animation_finished` is often cleaner than a ONE_SHOT connection in sequential code;
use ONE_SHOT when you need a handler method (multiple outcomes, or can't suspend the caller).

## Gotchas
- Deferred handlers see state *after* the frame's processing — the emitting object may already be
  freed; check `is_instance_valid` on arguments.
- Deferred argument values are captured at emit time (run: the handler received the value passed to `emit`, not a later change to the source variable).
- ONE_SHOT connections that never fire stay connected (leak if the emitter lives forever).

## Verify
- [ ] Pickup collection that disables its shape produces no flushing-queries errors.
- [ ] `get_connections()` empty after a ONE_SHOT fires.
## Checked
Ran on Godot 4.7.2 headless: `CONNECT_ONE_SHOT` and `CONNECT_DEFERRED` behaviour; physics callback errors for `disabled`, `monitoring`, and the no-error cases above using a real `Area2D` plus `StaticBody2D` overlap; `set_deferred("disabled", true)`, `add_child.call_deferred(...)` and `queue_free()` in the callback (no errors); FIFO order of `call_deferred`. Flags from the 4.7.2 `Object` class reference. "Deferred calls run after `_process` of the frame" was not checked and is not claimed.
