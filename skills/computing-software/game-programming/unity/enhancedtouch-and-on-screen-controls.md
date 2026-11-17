---
id: computing-software.game-programming.unity.enhancedtouch-and-on-screen-controls
name: enhancedtouch-and-on-screen-controls
category: computing-software
field: game-programming
product: unity
tags: [unity, enhancedtouch, input-system, touch, on-screen-controls, mobile, game-programming]
level: practitioner
status: docs-checked
description: "Unity Input System 1.11 touch: EnhancedTouch fingers, touches and phases, activeTouches rules, touch simulation, and On-Screen Button and Stick control paths."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Touch.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/OnScreen.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/api/UnityEngine.InputSystem.EnhancedTouch.Touch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EnhancedTouch and on-screen controls

**Goal:** poll multi-touch with `EnhancedTouch` and drive virtual sticks and buttons (Input System 1.11).

## Touch support layers
- Low level: `Touchscreen` (based on the Pointer layout; `Touchscreen.current`; `primaryTouch` and a
  fixed-size `touches` array of `TouchControl`). High level: `EnhancedTouch.Touch`.
- Page note: do not use `Touchscreen` for polling; reading touch state directly in `Update` or
  `FixedUpdate` means the app will miss changes in touch state.
- Touch input is supported on Android, iOS, Windows and UWP.
- Actions: bind `<Pointer>/press` or `<Pointer>/delta` (primary touch plus other non-touch pointers);
  `<Touchscreen>/touch3/press` for one touch; `<Touchscreen>/touch*/press` for all touches. For one
  Action bound to multiple touches, set the Action type to pass-through.

## EnhancedTouch.Touch
- Polling API like `UnityEngine.Input.touches`. Has recording overhead, so call
  `EnhancedTouchSupport.Enable()` (for example in `Awake` or a `RuntimeInitializeOnLoadMethod`).
  `Touchscreen` itself does not need it. Accessing `activeTouches`, `activeFingers`, `fingers`, `screens`
  or the `onFingerDown`/`onFingerMove`/`onFingerUp` events without enabling throws
  `InvalidOperationException`.
- Finger: the Nth contact source on a Touchscreen (`Touch.activeFingers`, `Touch.fingers`: length is the
  maximum concurrent touches the system supports). Touch: one finger contact from `Began` to `Ended` or
  `Cancelled`, with `Moved`/`Stationary` between; all records share a `touchId` (`Touch.activeTouches`).
- `activeTouches`: touches on-going this frame or ended this frame. A touch that begins in a frame always
  has phase `Began`, even if it also moved or ended; a touch that begins and ends in the same frame shows
  `Began` then an `Ended` entry in the next frame, so there can be more active touches than hardware
  supports. Results may differ from `UnityEngine.Input.touches` (queues flush at different times).
- Properties include `began`, `ended`, `inProgress`, `phase`, `screenPosition`, `startScreenPosition`,
  `delta`, `pressure` (0 if unsupported), `radius`, `touchId`, `isTap`, `tapCount`, `history`, `finger`,
  `valid`. `history` is empty by default: `maxHistoryLengthPerFinger` is zero.
- `touchId` may be reused by the platform after a touch finishes; uniqueness is only guaranteed within
  `activeTouches`.
- Touch data is a circular buffer in unmanaged memory; `valid` goes false when old entries are reused and
  most other properties then throw `InvalidOperationException`.
- The Touch and Finger APIs do not generate GC garbage (arrays pre-allocated).
- Page example: `foreach (var touch in Touch.activeTouches) if (touch.began) ... else if (touch.ended)
  ...`.

## Touch simulation
`TouchSimulation.Enable()` or the `TouchSimulation` MonoBehaviour adds a virtual Touchscreen mirroring
Pointer devices (Mouse, Pen). In the Editor: Input Debugger Options > "Simulate Touch Input From Mouse or
Pen". Unity Remote can test mobile touch in the Editor.

## On-screen controls
- UI widgets that simulate input devices; no predefined visuals (set your own sprite or UI). Button and
  stick are built in; custom ones extend `OnScreenControl` (the `OnScreenButton` source is shown).
- Each uses a Control path (for example `<Gamepad>/buttonSouth`). The system creates one device per
  distinct device type referenced (a Gamepad and a Keyboard if both are used), when components are
  enabled, and removes them when disabled. `OnScreenControl.control` gives the target control.
- Button: UI Button object plus `OnScreenButton`, path to a `ButtonControl`; sets value 1 on pointer-down,
  0 on pointer-up.
- Stick: UI Image plus `OnScreenStick`, path to a `Vector2Control` (for example `<Gamepad>/leftStick`).
  Drags within a box centered on the pointer-down point with edge length Movement Range (50 means 25
  pixels each way). Implement `IPointerDownHandler`/`IPointerUpHandler` on the stick GameObject to be
  notified of touch start/stop.
- Isolated mode: because the stick sends events from the paired device, dynamic device switching (for
  example `PlayerInput` with `neverAutoSwitchControlSchemes` false) can alternate devices and make the
  stick jitter; Isolated Input Actions use a local set of actions. Defaults when unset: Pointer Down
  `<Mouse>/leftButton`, `<Pen>/tip`, `<Touchscreen>/touch*/press`, `<XRController>/trigger`; Pointer Move
  `<Mouse>/position`, `<Pen>/position`, `<Touchscreen>/touch*/position`.

## Checked
Date: 2026-11-07

Read in full: the Touch support manual page, the On-screen Controls manual page and the
`EnhancedTouch.Touch` API page including its member docs. The `Finger`, `TouchSimulation` and
`OnScreenStick` API pages were not opened.

Corrected: the draft said `activeTouches` is empty unless enabled; the API page says it throws
`InvalidOperationException`. Removed because the pages do not confirm it: `Touch.activeTouches.Count`
and the pinch-zoom formula, `Finger.index` and `Finger.screenPosition` use, "Exact Position With Dynamic
Origin" behaviour, `EventSystem.IsPointerOverGameObject` advice, the PlayerInput scheme-flipping gotcha
(only the isolated-mode jitter note is on the page), and the Verify list.

Method: documentation only; no commands were run.
