---
id: computing-software.game-programming.godot.simulating-input-with-parse-input-event
name: simulating-input-with-parse-input-event
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-input, parse_input_event, inputeventaction, action-press, input-simulation, automated-testing, game-programming]
level: practitioner
status: docs-checked
description: "Simulate input in Godot 4 with Input.parse_input_event and action_press: InputEventAction vs key events, on-screen buttons, replays and automated tests."
sources: ["https://docs.godotengine.org/en/stable/classes/class_input.html#class-input-method-parse-input-event", "https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html", "https://docs.godotengine.org/en/stable/classes/class_inputeventaction.html", "https://docs.godotengine.org/en/stable/classes/class_touchscreenbutton.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simulating input with parse_input_event

**Uses:** virtual on-screen buttons, input replays, bots and automated tests that drive the real
input path.

## Two approaches
| API | Effect |
|---|---|
| `Input.parse_input_event(ev)` | Feeds an event to the game; also generates `Node._input()` calls. |
| `Input.action_press("jump", strength)` / `action_release` | Does not cause `_input()` calls; intended for `is_action_pressed()` and `is_action_just_pressed()` polling. |

Use `parse_input_event` when gameplay reacts in `_input`/`_unhandled_input`; `action_press` is enough
for code that only polls. Neither affects the operating system (an `InputEventMouseMotion` does not move
the OS cursor; use `warp_mouse()`).

```gdscript
func press_action(action: StringName, pressed := true, strength := 1.0) -> void:
    var ev := InputEventAction.new()
    ev.action = action
    ev.pressed = pressed
    ev.strength = strength
    Input.parse_input_event(ev)

func click_at(pos: Vector2) -> void:
    for down in [true, false]:
        var ev := InputEventMouseButton.new()
        ev.button_index = MOUSE_BUTTON_LEFT
        ev.pressed = down
        ev.position = pos
        ev.global_position = pos
        Input.parse_input_event(ev)
```

## Facts
- With `Input.use_accumulated_input` enabled, similar OS events are merged and emitted when the frame is
  done; `Input.flush_buffered_events()` sends buffered events to the game loop now (the engine already
  does this at least once per frame). In tests, await a frame (`await get_tree().process_frame`) before
  asserting.
- Always send the release; a simulated press stays pressed until released (`Input.action_release`).
  `Input.is_anything_pressed()` also returns true for actions simulated with `action_press()`.
- Touch-screen buttons: `TouchScreenButton` with an `action` set already triggers that action; custom
  Control buttons can call `press_action` in `button_down`/`button_up`.

## Tests
Reset input state between tests (`Input.action_release` for every action used).

## Verify
- [ ] Simulated jump triggers the same code path and animation as a keyboard press.
- [ ] No actions remain pressed after a test (`Input.is_anything_pressed()` is false).

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Input, InputEventAction and TouchScreenButton class pages: parse_input_event also generates _input calls and does not affect the OS, action_press does not cause _input calls, use_accumulated_input, flush_buffered_events, is_anything_pressed including simulated actions, TouchScreenButton.action. Removed unconfirmed claims about polling state after parse_input_event, next-frame behaviour of InputEventAction, key code matching, and third-party test frameworks.

Method: documentation only; no commands were run.
