---
id: computing-software.game-programming.godot.touch-input-and-gestures
name: touch-input-and-gestures
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-input, inputeventscreentouch, inputeventscreendrag, multitouch, game-programming]
level: practitioner
status: docs-checked
description: "Handle Godot touch input: InputEventScreenTouch/ScreenDrag with finger indices, emulate touch from mouse, pinch and pan gestures, TouchScreenButton and virtual joysticks."
sources: ["https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html", "https://docs.godotengine.org/en/stable/classes/class_inputeventscreentouch.html", "https://docs.godotengine.org/en/stable/classes/class_touchscreenbutton.html", "https://docs.godotengine.org/en/stable/classes/class_projectsettings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Touch input and gestures

**Goal:** reliable multitouch controls (virtual stick + buttons, pinch-zoom, drag) on phones and
tablets.

## Events
- `InputEventScreenTouch`: `index` (finger id), `position`, `pressed`, `double_tap`, `long_press`, `canceled`.
- `InputEventScreenDrag`: `index`, `position`, `relative`, `velocity`, `pressure`.
- Desktop gesture events (trackpads): `InputEventMagnifyGesture`, `InputEventPanGesture`.
Project Settings > Input Devices > Pointing: `emulate_touch_from_mouse` (default false; test touch on
desktop) and `emulate_mouse_from_touch` (default true: touches also generate mouse events; disable if
you handle touch directly to avoid double handling). Emulated events carry `device` -1
(`DEVICE_ID_EMULATION`).

## Tracking fingers
```gdscript
var touches := {}   # index -> position
func _unhandled_input(e):
    if e is InputEventScreenTouch:
        if e.pressed: touches[e.index] = e.position
        else: touches.erase(e.index)
    elif e is InputEventScreenDrag:
        touches[e.index] = e.position
        if touches.size() == 2: _pinch()
```
Pinch: compare distance between the two fingers to the previous frame's distance; zoom by the ratio.

## Virtual joystick
Track the finger that started inside the stick area by `index`; ignore other fingers. Output a
normalised vector with a dead zone; feed it into the same movement code as gamepad
(`Input.action_press("move_left", strength)` or a shared input abstraction).

## Built-in helpers
- `TouchScreenButton` (Node2D): maps a touch area to an action (`action`); unlike `Button` it supports
  multitouch out of the box, so several can be pressed at once. `visibility_mode =
  VISIBILITY_TOUCHSCREEN_ONLY` hides it on non-touch devices.

## Gotchas
- `canceled` touches (system gesture, notification shade) must release held actions.
- Safe areas: `DisplayServer.get_display_safe_area()` returns the safe-area rectangle to keep controls out of notches.

## Verify
- [ ] Move with stick and press jump simultaneously on a device.
- [ ] Swipe down notification shade mid-move: character stops (no stuck input).

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the Using InputEvent tutorial and class pages: InputEventScreenTouch and InputEventScreenDrag properties, InputEventMagnifyGesture and InputEventPanGesture exist, project settings input_devices/pointing/emulate_touch_from_mouse (false) and emulate_mouse_from_touch (true), InputEvent.DEVICE_ID_EMULATION, TouchScreenButton action, multitouch and VISIBILITY_TOUCHSCREEN_ONLY, DisplayServer.get_display_safe_area. Removed unconfirmed remarks about Button multitouch and stretch-mode coordinates.

Method: documentation only; no commands were run.
