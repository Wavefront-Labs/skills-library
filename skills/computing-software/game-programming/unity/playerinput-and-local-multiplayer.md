---
id: computing-software.game-programming.unity.playerinput-and-local-multiplayer
name: playerinput-and-local-multiplayer
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-input-system, playerinput-component, playerinputmanager, local-multiplayer, split-screen, device-pairing, game-programming]
level: practitioner
status: docs-checked
description: "Use PlayerInput for per-player actions and device pairing, and PlayerInputManager for join behaviours and split-screen in Unity local multiplayer."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/PlayerInput.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/PlayerInputManager.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PlayerInput and local multiplayer

**Goal:** couch co-op where each controller joins as its own player with its own copy of the actions.

## PlayerInput
One `PlayerInput` represents one player: the link between that player's devices, Actions, and methods or callbacks. Each
`PlayerInput` corresponds to one `InputUser` (`PlayerInput.user`). Properties: Actions, Default Control Scheme, Default Action
Map (None means no Actions are enabled at start), Camera (only needed for split-screen), Behavior.

- When several `PlayerInput` components use the same Actions, each automatically creates a private copy. In code for a
  `PlayerInput` read that component's actions, not `InputSystem.actions` (the singleton copy): reading the singleton bypasses the
  per-player device filtering and automatic device assignment stops working.
- It enables and disables Actions itself. On first enable it enables the Default Action Map. Use
  `PlayerInput.currentActionMap` and `SwitchCurrentActionMap` to inspect or change the map. `DeactivateInput` disables the
  player's input; `ActivateInput` re-enables it (and enables the default map if one exists). Disabling the component disables
  the current map and disassociates paired devices.

### Notification behaviours
| Behavior | What it does |
|---|---|
| Send Messages | `GameObject.SendMessage` on the same GameObject; action "Jump" becomes method `OnJump()` |
| Broadcast Messages | `BroadcastMessage` down the hierarchy (same or child GameObject) |
| Invoke Unity Events | one `UnityEvent` per message type, wired in the Inspector; receives the same argument as started/performed/canceled callbacks (`InputAction.CallbackContext`) |
| Invoke CSharp Events | plain C# events: `onActionTriggered` (all actions), `onDeviceLost`, `onDeviceRegained`; registered in script, not configurable in the Inspector |

With Send/Broadcast Messages a method can take no argument, or an `InputValue` (`value.Get<Vector2>()`). The `InputValue` is
only valid during the callback; storing it and calling `Get<T>()` later does not work correctly.

General notifications: `DeviceLostMessage` (for example a wireless device out of battery) and `DeviceRegainedMessage`.

### Device assignment
A `PlayerInput` with devices assigned matches them to the Control Schemes in its Action asset and enables only matching
schemes. By default no two `PlayerInput` components get the same device; to force sharing, assign devices manually via
`PlayerInput.Instantiate` or call `InputUser.PerformPairingWithDevice` on the player's `InputUser`. The Input System
supports shared devices such as left/right keyboard splits and hot seat.

### UI input
Assign an `InputSystemUIInputModule` to the UI Input Module field (both using the same `InputActionAsset`) so the same
Action and device configuration drives the UI. With `MultiplayerEventSystem` components, several UI instances can be on screen,
each controlled by a separate player.

## PlayerInputManager
Manages creation and lifetime of `PlayerInput` instances as players join and leave. Properties: Notification Behavior, Join
Behavior, Player Prefab (must have one `PlayerInput` in its hierarchy), Joining Enabled By Default, Limit Number of Players
with Max Player Count.

Join behaviours:
- Join Players When Button Is Pressed: a button press on a device not paired to any player joins a player using that device.
- Join Players When Join Action Is Triggered: joins only when the control matches a specific action you define.
- Join Players Manually: call `JoinPlayer` explicitly; alternatively create GameObjects with `PlayerInput` components and the
  Input System joins them automatically.

Split-screen: with Enable Split-Screen on, the manager divides the screen between active players; the Camera property on the
`PlayerInput` prefab must be set. Extra options: Maintain Aspect Ratio, Set Fixed Number (if above zero, always that many
rectangles), Screen Rectangle (normalised area).

Notifications: `PlayerJoinedMessage` and `PlayerLeftMessage`, each passing the `PlayerInput`. They follow the manager's
Notification Behavior, like `PlayerInput`. The package has a "Simple Multiplayer" sample.

## Verify
- [ ] Each controller drives only its own player.
- [ ] The split-screen prefab has its Camera field set.

## Checked
Date: 2026-11-09. Read in full: Input System 1.11 manual pages "The Player Input component" and "The Player Input Manager
component". Removed as not on those pages: the "slow and typo-prone" verdict on Send Messages, caching actions in `Awake`,
`onControlsChanged` and Auto-Switch behaviour, the explicit `JoinPlayer` argument list, the two-schemes-on-one-keyboard recipe,
pause on disconnect advice, and the claim about a prefab placed in the scene pairing with every device.
Method: docs-checked 2026-11-09 against the two Input System manual pages named above.
