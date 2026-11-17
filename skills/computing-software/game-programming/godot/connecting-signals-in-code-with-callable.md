---
id: computing-software.game-programming.godot.connecting-signals-in-code-with-callable
name: connecting-signals-in-code-with-callable
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, signals, signal-connect, callable, bind, connect-flags, game-programming, callable-bind]
level: practitioner
status: verified
description: "Connect Godot 4 signals in code: Signal.connect with Callables and lambdas, bind/unbind for extra args, CONNECT_ONE_SHOT/DEFERRED/REFERENCE_COUNTED flags, and disconnect hygiene."
sources: ["https://docs.godotengine.org/en/stable/classes/class_signal.html", "https://docs.godotengine.org/en/stable/classes/class_callable.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Connecting signals in code with Callable

**Goal:** dynamic connections (spawned enemies, generated buttons) that pass extra context and clean up.

## Connect
```gdscript
func _ready() -> void:
    $Button.pressed.connect(_on_button_pressed)                     # method reference = Callable
    player.health.died.connect(_on_player_died, CONNECT_ONE_SHOT)
    timer.timeout.connect(func(): spawn_wave(wave + 1))             # lambda

func add_slot(i: int) -> void:
    var b := Button.new()
    b.pressed.connect(_on_slot_pressed.bind(i))                     # extra arg appended after signal args
    add_child(b)

func _on_slot_pressed(index: int) -> void: equip(index)
```
- `bind(args)` appends arguments **after** the signal's own (run: `sig2.connect(hb.bind(99))` called `hb(1, 2, 99)`);
  `unbind(n)` drops the last n signal args (run: `sig2.connect(h0.unbind(2))` called a 0-arg method from a 2-arg signal).
- Lambdas capture variables by value at creation time (locals); member access goes through `self`.

## Flags
| Flag | Effect |
|---|---|
| `CONNECT_ONE_SHOT` | disconnects after first emission |
| `CONNECT_DEFERRED` | callback runs at idle time (end of frame); safe for physics callbacks that add/remove nodes |
| `CONNECT_REFERENCE_COUNTED` | can connect the same callable multiple times; needs as many disconnects |
| `CONNECT_PERSIST` | saved with the scene (editor/tool use) |

## Disconnect and lifetime
- Connections to a **freed Object's method** are removed automatically when that object is freed (run: the connection
  count went from 1 to 0 after `free()`).
- Lambdas are not tied to an object you control: store the Callable to disconnect it later.
```gdscript
var _on_tick := func(): count += 1
func _enter_tree() -> void: Clock.ticked.connect(_on_tick)
func _exit_tree() -> void: if Clock.ticked.is_connected(_on_tick): Clock.ticked.disconnect(_on_tick)
```
- Connecting the same callable twice errors (`Signal 'ticked' is already connected to given callable ...`) unless
  REFERENCE_COUNTED; guard with `is_connected` when connect may run more than once (re-entering the tree). With
  REFERENCE_COUNTED, two connects need two disconnects (run: still connected after the first).

## Editor vs code
Use the editor's signal connections for static wiring inside one scene and code connections for anything dynamic
(`CONNECT_PERSIST` is the flag that saves a connection made from a tool script into the scene).

## Verify
- [ ] Re-adding a node to the tree doesn't double-connect.
- [ ] No errors about calling methods on freed instances after enemies die.
## Checked
Ran on Godot 4.7.2 headless: `bind`, `unbind`, double connect error text, REFERENCE_COUNTED disconnect counting, `CONNECT_ONE_SHOT` (handler ran once, `get_connections()` empty afterwards), `CONNECT_DEFERRED` (handler ran at the next idle step, after `emit` returned), lambda connect plus `is_connected`/`disconnect` with a stored Callable, auto-removal for a freed target's method, and `get_connections()` entries having the keys `signal`, `callable`, `flags`. Flag meanings (`CONNECT_PERSIST`, `CONNECT_REFERENCE_COUNTED`) from the 4.7.2 `Object` class reference.
