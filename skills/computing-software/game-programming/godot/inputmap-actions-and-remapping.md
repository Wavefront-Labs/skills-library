---
id: computing-software.game-programming.godot.inputmap-actions-and-remapping
name: inputmap-actions-and-remapping
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-input, inputmap, input-actions, rebinding, input-get-vector, action-strength, game-programming, get-vector]
level: practitioner
status: docs-checked
description: "Use Godot InputMap actions for all input: defining actions, Input polling APIs, get_vector, and runtime key remapping saved to a ConfigFile."
sources: ["https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html", "https://docs.godotengine.org/en/stable/classes/class_inputmap.html", "https://docs.godotengine.org/en/stable/classes/class_input.html", "https://docs.godotengine.org/en/stable/classes/class_inputeventkey.html", "https://docs.godotengine.org/en/stable/classes/class_configfile.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# InputMap actions and remapping

**Goal:** gameplay code that only knows actions ("jump", "move_left"), devices bound in Project
Settings, and players able to rebind keys with the bindings persisted.

## Define actions
Project > Project Settings > Input Map: add `move_left`, `move_right`, `move_up`, `move_down`, `jump`,
`attack`; add events per action (key, joypad button, joypad axis, mouse button). Per-action
**deadzone** applies to analog inputs (`InputMap.add_action()` defaults to 0.2; the controllers tutorial
states 0.5 for the Input Map tab, so set it explicitly). Physical keycodes (`physical_keycode`) keep WASD in the same
place on AZERTY layouts; prefer them for movement.

## Polling
```gdscript
func _physics_process(delta: float) -> void:
    var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")  # radial deadzone, length <= 1
    velocity = dir * speed
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
    var throttle := Input.get_action_strength("accelerate")     # 0..1 for triggers
    move_and_slide()
```
`get_axis(neg, pos)` for one axis. `is_action_just_pressed` is true only on the frame (or physics tick)
where the press started: read one-shot actions where they are used. Inside input callbacks such as
`_input`, use `event.is_action_pressed()` instead.

## Runtime remapping
```gdscript
func rebind(action: StringName, new_event: InputEvent) -> void:
    # keep gamepad bindings, replace keyboard ones
    for ev in InputMap.action_get_events(action):
        if ev is InputEventKey: InputMap.action_erase_event(action, ev)
    InputMap.action_add_event(action, new_event)
    save_bindings()

# capture the next key press in a "press a key" dialog
func _input(event: InputEvent) -> void:
    if waiting_for_action and event is InputEventKey and event.pressed and not event.echo:
        rebind(waiting_for_action, event)
        waiting_for_action = &""
        get_viewport().set_input_as_handled()
```
Check for conflicts (same key bound to another action in the same context) before applying.

## Persisting
```gdscript
const PATH := "user://input.cfg"
func save_bindings() -> void:
    var cfg := ConfigFile.new()
    for action in ["jump", "attack", "move_left", "move_right"]:
        var keys: Array[int] = []
        for ev in InputMap.action_get_events(action):
            if ev is InputEventKey: keys.append(ev.physical_keycode)   # store plain ints
        cfg.set_value("keys", action, keys)
    cfg.save(PATH)

func load_bindings() -> void:
    var cfg := ConfigFile.new()
    if cfg.load(PATH) != OK: return
    for action in cfg.get_section_keys("keys"):
        for ev in InputMap.action_get_events(action):
            if ev is InputEventKey: InputMap.action_erase_event(action, ev)   # keep gamepad bindings
        for code in cfg.get_value("keys", action):
            var key_event := InputEventKey.new()
            key_event.physical_keycode = code
            InputMap.action_add_event(action, key_event)
```
Call `load_bindings()` from an autoload at startup. Provide "Reset to defaults" with
`InputMap.load_from_project_settings()`.

## Display names
`event.as_text()` returns a string representation of an event for display; map joypad buttons to
platform glyphs (Xbox/PlayStation icons) by `Input.get_joy_name(device)` for prompts.

## Verify
- [ ] No direct keycode checks in gameplay scripts (search for `KEY_`).
- [ ] Rebinding survives restart; reset restores defaults.
- [ ] Keyboard and gamepad both drive every action.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the InputMap, Input, InputEvent, InputEventKey and ConfigFile class pages: add_action deadzone default 0.2, action_get_events, action_erase_event, action_erase_events, action_add_event, load_from_project_settings, get_vector deadzone and length limit, is_action_just_pressed semantics, InputEventKey physical_keycode (an event mapping should set only one of keycode, physical_keycode or unicode), ConfigFile storing Variant values. The persistence example was changed to store integer key codes because storing InputEvent objects in ConfigFile is not documented.

Method: documentation only; no commands were run.
