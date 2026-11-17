---
id: computing-software.game-programming.unity.input-debugger-device-troubleshooting
name: input-debugger-device-troubleshooting
category: computing-software
field: game-programming
product: unity
tags: [unity, input-debugger, input-system, devices, troubleshooting, game-programming]
level: practitioner
status: docs-checked
description: "Diagnose Unity Input System problems with the Input Debugger: device list, live control values, event comparison, enabled actions, users, layouts and remote Player devices."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Debugging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input Debugger and device troubleshooting

**Goal:** find out quickly whether a problem is the device, the bindings or the action state. Package version 1.11 docs.

## Open it
Window > Analysis > **Input Debugger**. The tree has: Devices (current devices plus unsupported/unrecognized ones),
Layouts, Actions, Users, Settings, Metrics.
- **Actions** is visible only in Play mode and only if at least one Action is enabled; it lists enabled Actions and the
  Controls they are bound to (click the arrow next to an Action). Actions that belong to InputUsers appear under Users
  instead.
- **Users** is visible only when InputUser instances exist; each `PlayerInput` implicitly creates one. It shows each
  user's paired Devices, active Control Schemes and Actions.

## Workflow
1. **Is the device there?** Check the Devices list, and the unsupported/unrecognized list.
2. **Do controls change?** Double-click a Device. The Controls section shows real-time state, so you can verify the data
   the Input System receives is what you expect. Buttons: **HID Descriptor** (HID devices only) and **State** (a
   non-updating snapshot window). If values move here but the game ignores them, look at bindings and action state.
3. **Inspect events.** The Events section lists the Device's input events; double-click one to see full Device state at
   that time. Select several, right-click, Compare for a side-by-side difference.
4. **Is the action enabled and bound?** Look in Actions (or Users for PlayerInput actions) to see whether the Action is
   listed and which Controls it resolved to.
5. **Does a layout exist?** The Layouts list shows all registered Control and Device layouts, the database of supported
   hardware.

## Code
```csharp
// Record events (dispose the trace; it uses unmanaged resources)
var trace = new InputEventTrace();
trace.Enable();
foreach (var eventPtr in trace) Debug.Log("Got some event: " + eventPtr);
trace.Dispose();

// See events as they are processed; eventPtr.handled = true stops further processing
InputSystem.onEvent += (eventPtr, device) => { /* ... */ };
```
The page also offers a Visualizers sample (Package Manager > Input System > Import in project) with
`InputControlVisualizer` and `InputActionVisualizer` components to watch Controls and Actions on screen.

## Remote debugging
The Input Debugger can connect to a Player on another computer or device through PlayerConnection, the same mechanism the
Profiler uses. Open the **Remote Devices** drop-down, then enable **Show remote devices**; the Devices list then splits
into Local and Remote sections. Only Devices and events from Players are visible, not Actions or input users.

## Editor testing aids
- Device Simulator: mouse and pen input on the simulated screen become touchscreen input via its own touchscreen device,
  and native mouse and pen devices are disabled.
- Unity Remote (iOS/Android) adds remote Devices (`InputDevice.remote` true): Touchscreen, Accelerometer, and gyro-based
  sensors if present. Joysticks and gamepads are not supported over Unity Remote.

## Checked
Date: 2026-11-07.
Read in full: Input System 1.11 "Debugging" page, including both code blocks. The Layouts and HID pages that the draft also
cited were not opened for this version, so they were removed from sources and every claim depending on them was removed:
custom layout JSON and `InputSystem.RegisterLayout`, generic HID handling, and example control paths such as
`<DualSenseGamepadHID>/touchpadButton`.
Removed as unconfirmed by the Debugging page: `supportedDevices` filtering, OS permission and Bluetooth advice, the
`onDeviceChange` / `activeControl` snippets, and the Run In Background, Background Behavior and Play Mode Input Behavior
gotchas. The invented Verify checklist was dropped.
Method: documentation only; no commands were run.
