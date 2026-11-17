---
id: computing-software.game-programming.godot.mouse-capture-and-mouse-look
name: mouse-capture-and-mouse-look
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-input, mouse-capture, mouse-look, mouse-mode-captured, inputeventmousemotion, first-person-camera, sensitivity, game-programming]
level: intro
status: docs-checked
description: "Implement first-person mouse look in Godot: capturing the mouse, relative motion without delta-time scaling, yaw/pitch split, pitch clamping and focus handling."
sources: ["https://docs.godotengine.org/en/stable/classes/class_input.html#enum-input-mousemode", "https://docs.godotengine.org/en/stable/classes/class_inputeventmousemotion.html", "https://docs.godotengine.org/en/stable/tutorials/inputs/mouse_and_input_coordinates.html", "https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mouse capture and mouse look

**Goal:** a first-person camera that feels like any PC shooter: raw, frame-rate independent, no
gimbal flip, cursor released for menus.

## Scene
```
Player (CharacterBody3D)      <- rotates around Y (yaw)
  Head (Node3D)               <- rotates around X (pitch)
    Camera3D
```
Splitting yaw and pitch across two nodes avoids roll and gimbal issues.

## Script
```gdscript
extends CharacterBody3D
@export var sensitivity := 0.0025   # radians per pixel (expose in settings)
@onready var head: Node3D = $Head

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
        rotate_y(-event.screen_relative.x * sensitivity)
        head.rotate_x(-event.screen_relative.y * sensitivity)
        head.rotation.x = clamp(head.rotation.x, deg_to_rad(-89), deg_to_rad(89))
    elif event.is_action_pressed("ui_cancel"):
        Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
    elif event is InputEventMouseButton and event.pressed and Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
        Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
        get_viewport().set_input_as_handled()
```

## Rules
- Use the motion since the last event (`relative`, or `screen_relative`) rather than `position`: in
  captured mode `event.position` is the screen centre. **Do not multiply by delta**: mouse deltas are
  already distances; scaling by frame time makes aim depend on frame rate.
- Apply rotation in the input callback (or accumulate and apply in `_process`), not in
  `_physics_process`, otherwise look updates only at the physics rate and feels laggy.
- `relative` is scaled by the project's content scale factor (stretch mode), so sensitivity changes with
  window size; the documentation recommends `screen_relative` and `screen_velocity` for mouselook so
  movement behaves the same across multiple resolutions.
- Invert Y and separate X/Y sensitivity as settings; store in ConfigFile.

## Mouse modes
| Mode | Behaviour |
|---|---|
| `MOUSE_MODE_VISIBLE` | Normal cursor. |
| `MOUSE_MODE_HIDDEN` | Hidden but not locked. |
| `MOUSE_MODE_CAPTURED` | Hidden, position locked at the centre of the window; use relative motion. |
| `MOUSE_MODE_CONFINED` / `_CONFINED_HIDDEN` | Cursor confined to the game window, visible / hidden. |
Release capture on pause menus and when the window loses focus
(`NOTIFICATION_APPLICATION_FOCUS_OUT`). On the web, browsers only allow capturing the cursor (and entering full screen) as a response to a
JavaScript input event: do it from within `_input` or `_unhandled_input` while handling the event;
querying the `Input` singleton is not sufficient.

## Verify
- [ ] Turning 360 degrees takes the same mouse distance at 30 and 240 fps.
- [ ] Pitch never flips past straight up/down.
- [ ] Escape frees the cursor; clicking recaptures without firing.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Mouse and input coordinates tutorial (captured mode position is the screen centre; screen_relative recommended for mouselook), the Input and InputEventMouseMotion class pages (mouse modes, relative scaled by stretch settings, screen_relative), the Node class page (NOTIFICATION_APPLICATION_FOCUS_OUT) and the Exporting for the Web page (cursor capture needs an active input event).

Method: documentation only; no commands were run.
