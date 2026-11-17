---
id: computing-software.game-programming.unity.input-control-schemes-and-device-switching
name: input-control-schemes-and-device-switching
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-input-system, control-schemes, device-switching, game-programming]
level: practitioner
status: docs-checked
description: "How Unity Input System control schemes work: binding groups, binding masks, PlayerInput device-to-scheme matching, restricting devices, and per-device binding display strings."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/ActionBindings.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/PlayerInput.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control schemes and device switching

**Goal:** keep bindings for different device types separate and show prompts matching the device in use. Package
version 1.11 docs.

## What a control scheme is
A binding can belong to any number of binding groups, stored as a semicolon-separated string in `InputBinding.groups`
(for example `"Keyboard&Mouse;Gamepad"`). Groups can be used for any grouping, but are mostly used for control schemes.
To enable different sets of groups on an `InputActionMap` or `InputActionAsset`, set its `bindingMask`; the Input System
uses that to implement `InputControlScheme`s, which map bindings to different types of devices. `PlayerInput` uses
control schemes to enable a matching scheme for a new user based on the device they play on.

```csharp
// Restrict to the "Gamepad" group; MaskByGroup is used the same way for display and parameter overrides.
actions.bindingMask = InputBinding.MaskByGroup("Gamepad");
```
(The assignment follows the page's `InputBinding.MaskByGroup("Gamepad")` and `bindingMask` descriptions; the page does
not show this exact statement.)

## PlayerInput and devices
- Properties: **Actions**, **Default Control Scheme** (scheme enabled by default), **Default Action Map**,
  **Camera** (split-screen only), **Behavior**.
- If a PlayerInput has devices assigned, it matches them to the control schemes in its Action Asset and enables only
  schemes that match its devices.
- Each PlayerInput can have one or more devices. By default no two PlayerInputs share a device; to force sharing,
  assign devices when calling `PlayerInput.Instantiate`, or call `InputUser.PerformPairingWithDevice` on the
  PlayerInput's `InputUser` (`PlayerInput.user`).
- When several PlayerInputs use the same actions they make private copies; read input through callbacks or the
  PlayerInput's own copy, not `InputSystem.actions`, otherwise automatic device assignment will not work.
- Behaviors: Send Messages, Broadcast Messages, Invoke Unity Events, Invoke CSharp Events (`onActionTriggered`,
  `onDeviceLost`, `onDeviceRegained`). `DeviceLostMessage` / `DeviceRegainedMessage` report lost and recovered devices
  (for example a wireless device running out of battery).
- In Play mode each PlayerInput shows a Debug section with the user number (from zero), control scheme and devices.

## Restricting devices without PlayerInput
By default actions resolve bindings against all devices (`InputSystem.devices`). Restrict an `InputActionMap` or asset to
specific devices through its `devices` property, for example `actionMap.devices = new[] { Gamepad.all[0] };`.
`InputUser` and `PlayerInput` set this automatically from paired devices.

## Binding display strings for prompts
`InputActionRebindingExtensions.GetBindingDisplayString` gives the display text for an action or a binding index. An
overload returns `out deviceLayout, out controlPath`, which you can use to pick icons, for example checking
`InputSystem.IsFirstLayoutBasedOnSecond(deviceLayout, "Gamepad")` and switching on `controlPath` values such as
`buttonSouth` or `dpad/up`. Resolved controls can change at any time (for example when the user changes keyboard
layout), so display strings can change dynamically.

## Checked
Date: 2026-11-07.
Read in full: Input System 1.11 "Input Bindings" (ActionBindings, all sections: composites, rebinding, display strings,
Control Schemes, binding resolution, device choice, conflicts, initial state check) and "The Player Input component".
Neither page documents auto-switching.
Removed as unconfirmed: the scheme definitions "Keyboard&Mouse"/"Gamepad"/"Touch" and Optional device requirements,
`onControlsChanged`, the "auto-switch only with one PlayerInput" rule, `InputUser.listenForUnpairedDeviceActivity` /
`onUnpairedDeviceUsed` / `ActivateControlScheme`, deadzone and mouse-jitter remarks, the composite-scheme gotcha, and the
invented Verify checklist.
Method: documentation only; no commands were run.
