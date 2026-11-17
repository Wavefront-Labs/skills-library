---
id: computing-software.game-programming.godot.gamepad-joypad-input
name: gamepad-joypad-input
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-input, joypad, gamepad, joy-connection-changed, sdl-gamecontrollerdb, deadzone, local-multiplayer, button-prompts, game-programming]
level: practitioner
status: docs-checked
description: "Support gamepads in Godot: joypad events and axes, per-action deadzones, connection signals, device ids for local multiplayer, mappings and button prompts."
sources: ["https://docs.godotengine.org/en/stable/tutorials/inputs/controllers_gamepads_joysticks.html", "https://docs.godotengine.org/en/stable/classes/class_input.html", "https://docs.godotengine.org/en/stable/classes/class_inputevent.html", "https://github.com/gabomdq/SDL_GameControllerDB"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gamepad (joypad) input

**Goal:** controllers work out of the box, hot-plugging is handled, multiple local players each get
their own device, and prompts show the right glyphs.

## Bind to actions
In the Input Map add Joypad Button / Joypad Axis events to actions alongside keys. Godot uses SDL
gamepad naming (`JOY_BUTTON_A` = 0 is the bottom action button: Sony Cross, Xbox A, Nintendo B; since
Godot 4.5 SDL 3 handles controllers on Windows, macOS and Linux, while Android and Web still use
Godot's own code). Axis events specify direction (e.g. Left Stick Left = `JOY_AXIS_LEFT_X`, negative).
Each action has a **deadzone**; the tutorial states a default of 0.5 in the Input Map tab while
`InputMap.add_action()` defaults to 0.2, so set it explicitly for stick actions.

```gdscript
var move := Input.get_vector("move_left", "move_right", "move_up", "move_down")  # combined keyboard + stick
var aim := Vector2(Input.get_joy_axis(0, JOY_AXIS_RIGHT_X), Input.get_joy_axis(0, JOY_AXIS_RIGHT_Y))
```
`Input.get_vector()` applies a circular deadzone (an explicit 5th argument, or the average of the four
actions' deadzones if omitted); handling axes one by one gives a less ideal deadzone shape.

## Hot-plugging
```gdscript
func _ready() -> void:
    Input.joy_connection_changed.connect(_on_joy_changed)

func _on_joy_changed(device: int, connected: bool) -> void:
    if connected:
        print("Connected: ", Input.get_joy_name(device), " guid ", Input.get_joy_guid(device))
    else:
        pause_game_and_prompt_reconnect(device)
```
`Input.get_connected_joypads()` lists devices at startup; the order is not guaranteed to be the same
after a restart.

## Local multiplayer
Every `InputEvent` carries a `device` ID (joypad index for gamepads; keyboard and mouse use their own
reserved IDs, and -1 marks emulated mouse or touch input). For per-player control, handle events
manually: check `event.device` in `_unhandled_input` and route to the player that owns that device.

## Unknown controllers
Godot uses SDL's game controller database plus community mappings to determine gamepad names and
mappings from the device GUID (`Input.get_joy_guid()`). Add a mapping in SDL format with
`Input.add_joy_mapping("<SDL mapping string>", true)`; the second argument updates already connected
devices.

## Prompts
Detect last used device type: on any `InputEventJoypadButton/Motion` set `using_gamepad = true`, on
key/mouse events false; swap UI glyphs accordingly. Pick glyph sets from `Input.get_joy_name(device)`,
which returns the name from the SDL controller database (for example `PS4 Controller`).

## Vibration
`Input.start_joy_vibration(device, weak_magnitude, strong_magnitude, duration)` (magnitudes 0.0 to 1.0;
duration 0 means until stopped); `Input.stop_joy_vibration(device)` stops it early. Offer a slider to
reduce or disable vibration.

## Verify
- [ ] Unplug/replug a controller mid-game: game pauses and resumes with the same player mapping.
- [ ] Two controllers drive two players independently.
- [ ] Prompts switch between keyboard and gamepad glyphs on first input from each.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the controllers tutorial and the Input, InputEvent, InputMap and @GlobalScope class pages: SDL 3 since 4.5 with custom code on Android and Web, JOY_BUTTON_A meaning, deadzone default (tutorial 0.5 versus InputMap.add_action 0.2), get_vector deadzone behaviour, joy_connection_changed(device, connected), get_connected_joypads ordering note, get_joy_name/get_joy_guid, add_joy_mapping(mapping, update_existing), start_joy_vibration and stop_joy_vibration, InputEvent.device and DEVICE_ID_EMULATION = -1. Removed unsupported claims about device -1 meaning all devices, keyboard being device 0, Steam Input and glyph name substrings.

Method: documentation only; no commands were run.
