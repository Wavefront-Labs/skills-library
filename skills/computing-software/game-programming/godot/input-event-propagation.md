---
id: computing-software.game-programming.godot.input-event-propagation
name: input-event-propagation
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-input, inputevent, _unhandled_input, _input, _gui_input, set-input-as-handled, mouse-filter, event-propagation, game-programming]
level: practitioner
status: docs-checked
description: "Route Godot input correctly: _input, _gui_input, _shortcut_input and _unhandled_input order, marking events handled, Control mouse_filter, UI blocking clicks."
sources: ["https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html", "https://docs.godotengine.org/en/stable/classes/class_control.html#class-control-property-mouse-filter", "https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html", "https://docs.godotengine.org/en/stable/classes/class_inputevent.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input event propagation

**Goal:** clicks on UI do not also fire the gun, pause menus swallow gameplay input, and every event
is handled by exactly one place.

## Order of delivery (per event)
1. `_input(event)` on nodes (reverse tree order: children/later nodes first).
2. **GUI**: the Control under the mouse / with focus gets `_gui_input(event)`; Controls consume mouse
   events depending on `mouse_filter`.
3. `_shortcut_input(event)` (only for key, shortcut and joypad button events).
4. `_unhandled_key_input(event)` for key events.
5. `_unhandled_input(event)`: what nothing above handled. **Put gameplay input here.**
6. Physics picking (`CollisionObject` `_input_event`) for 2D/3D objects under the mouse, when object
   picking is enabled on the viewport.
Any stage calling `get_viewport().set_input_as_handled()` (or `accept_event()` inside `_gui_input`)
stops further propagation. GUI mouse events travel up only through the direct ancestors of the targeted
Control (subject to `mouse_filter`); GUI keyboard and joypad events are handled only by the Control that
received them and otherwise continue as non-GUI events to `_unhandled_input`.

## Gameplay input in _unhandled_input
```gdscript
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("fire"):
        fire()
        get_viewport().set_input_as_handled()
    elif event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
        look(event.relative)
```
Because UI handles mouse clicks first, clicking a button no longer also shoots.
For continuous actions (holding fire, movement), polling `Input.is_action_pressed` in
`_physics_process` ignores propagation: gate it with a state check (menu open) or use events.

## Control mouse_filter
| Value | Effect |
|---|---|
| `MOUSE_FILTER_STOP` | Receives mouse events through `_gui_input()` and does not pass them on. Default for every Control. |
| `MOUSE_FILTER_PASS` | Receives, then passes to the parent Control if not handled. |
| `MOUSE_FILTER_IGNORE` | Invisible to the mouse (decorative full-screen containers, HUD labels). |
A full-screen HUD root left on STOP swallows all clicks: gameplay never gets mouse input. Set HUD
containers to IGNORE.

## Pause menus
Set the menu's `process_mode = PROCESS_MODE_WHEN_PAUSED` (or ALWAYS) and `get_tree().paused = true`;
paused nodes do not get `_process`, `_physics_process`, `_input` or `_input_event` calls (signals still
work). The menu handles `ui_cancel` in `_unhandled_input`
or its own `_input` to close.

## Echo and pressed
`event.is_action_pressed("x", allow_echo, exact_match)` ignores key repeat unless `allow_echo` is true;
`event.is_echo()` filters manually (key events only). Gamepad buttons never produce echo events.

## Verify
- [ ] Clicking any button never triggers gameplay actions.
- [ ] HUD does not block world clicks (mouse_filter IGNORE on non-interactive Controls).
- [ ] Pause menu receives input while gameplay ignores it.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Using InputEvent tutorial (delivery order _input, GUI, _shortcut_input, _unhandled_key_input, _unhandled_input, physics picking; reverse depth-first order; set_input_as_handled and accept_event; GUI keyboard and joypad events do not travel up the tree), the Control class page (mouse_filter default MOUSE_FILTER_STOP and the three modes), the Node class page (PROCESS_MODE_WHEN_PAUSED and PROCESS_MODE_ALWAYS), the pausing tutorial (callbacks that stop when paused), and InputEvent.is_action_pressed and is_echo.

Method: documentation only; no commands were run.
