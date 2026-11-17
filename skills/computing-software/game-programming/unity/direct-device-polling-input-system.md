---
id: computing-software.game-programming.unity.direct-device-polling-input-system
name: direct-device-polling-input-system
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-input-system, keyboard-current, gamepad-current, device-polling, game-programming]
level: practitioner
status: docs-checked
description: "Read Input System controls directly (Gamepad.current, ReadValue, IsActuated, EvaluateMagnitude), control types and paths, device removal and onDeviceChange (1.11)."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Devices.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Controls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Direct device polling with the Input System

**Goal:** read controls straight from devices (Input System package 1.11 docs) and handle device
connection changes.

## Reading controls
- Read a control's current value with `ReadValue()`, for example `Gamepad.current.leftStick.x.ReadValue()`.
  `InputControl.valueType` gives the value type; reads may apply Processors.
- Control types (page table): `AxisControl` (`Gamepad.leftStick.x`), `ButtonControl` (`Mouse.leftButton`;
  trigger buttons can have values other than 0 and 1, face buttons generally cannot), `KeyControl`
  (`Keyboard.aKey`; display name follows the system keyboard layout), `Vector2Control`
  (`Pointer.position`), `Vector3Control`, `QuaternionControl`, `IntegerControl`, `StickControl`
  (`Gamepad.rightStick`), `DpadControl`, `TouchControl` (`Touchscreen.primaryTouch`).
- Actuation: `IsActuated()` (moved away from default so it affects the value), e.g.
  `Gamepad.current.leftStick.IsActuated()`; `EvaluateMagnitude()` returns >= 0, or -1 when there is no
  meaningful magnitude, e.g. `leftStick.EvaluateMagnitude() > 0.25f`.
- Control paths: `<Gamepad>/leftStick/x`; look up with `gamepad["leftStick/x"]`, `gamepad["{Submit}"]`,
  `InputSystem.FindControls("*/{Submit}")`. A control has a name, optional display name (button west
  shows "Square" on a DualShock 4), aliases and usages (Submit is commonly on `buttonSouth`).
- History: `InputStateHistory<T>` records value changes (needs `Dispose`).
- Perf note: `InputControl<T>.value` returns `ref readonly` and avoids a copy only if assigned to a
  `ref readonly` variable.

## Devices
- `InputSystem.devices` lists all present devices. `InputSystem.onDeviceChange` signals
  `InputDeviceChange.Added`, `Removed`, `Disconnected`, `Connected` (and others).
- When a device is added the system calls `MakeCurrent`; a removed device instance stays valid in code
  but reading values from its controls throws exceptions.
- `InputSystem.disconnectedDevices` tracks disconnected devices, reused if they reconnect.
- Sensors start disabled and must be enabled to generate events (`InputSystem.EnableDevice`).
- Noisy controls can be excluded from making a device current (project setting); this avoids a PS4
  controller constantly becoming `Gamepad.current` due to sensor data.
- Focus: input is tied to application focus; on regaining focus devices get a sync request or a soft
  reset of controls not marked `dontReset`. `InputSystem.ResetDevice` resets controls.
- Editor domain reloads reset device state.

## Checked
Date: 2026-11-07

Read in full: the Devices page (including the custom device steps) and the Controls page. The Keyboard,
Gamepad, Mouse, Touch and Actions pages were not opened.

Removed because neither page confirms it: `Keyboard.current` being null where no keyboard exists,
`wasPressedThisFrame`, `wasReleasedThisFrame` and `isPressed` semantics, Update Mode and FixedUpdate
guidance, `Gamepad.all` / `Joystick.all` iteration advice, `Touchscreen.current.primaryTouch.position`,
mouse delta per-frame statements, `Keyboard.onTextInput`, the Active Input Handling setting, "most
recently used gamepad" for `current`, the advice on when to switch to Actions, and the Verify list.
The page only shows `Gamepad.current` in code samples.

Method: documentation only; no commands were run.
