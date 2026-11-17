---
id: computing-software.game-programming.unreal-engine.enhanced-input-triggers-and-modifiers
name: enhanced-input-triggers-and-modifiers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, enhanced-input, input-triggers, input-modifiers, swizzle-axis, hold-trigger, game-programming]
level: practitioner
status: docs-checked
description: "How Enhanced Input modifiers pre-process values and triggers decide firing: explicit, implicit and blocker types, trigger states, custom subclasses and the Hold trigger."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced Input triggers and modifiers

**Goal:** WASD, sticks and hold actions built from data; write custom ones when needed.

## Modifiers (Enhanced Input page)
- Pre-processors that alter the raw value before it reaches Input Triggers. The plugin ships modifiers for changing axis
  order, dead zones and converting axial input to world space. Useful for sensitivity, smoothing over frames, or behaviour
  based on player state.
- Each mapping lists modifiers; the value returned by one goes to the next modifier, or to the first trigger.
- WASD on one Axis2D action: W/Up Swizzle Input Axis Values (YXZ or ZXY); A/Left Negate; S/Down Negate plus Swizzle
  (YXZ or ZXY); D/Right none. Keys give 0.0 or 1.0 on X, so Negate flips sign and Swizzle moves X to Y.
- Custom: subclass `UInputModifier` (C++ or a Blueprint child) and override `ModifyRaw_Implementation(const
  UEnhancedPlayerInput* PlayerInput, FInputActionValue CurrentValue, float DeltaTime)`, which returns an
  `FInputActionValue`. The player input gives access to the owning controller and game state. The page's example is
  Lyra's aim-inversion modifier reading a shared setting.

## Triggers
- Decide whether processed input activates the action. Most check the input (minimum actuation, short taps, holds,
  press or release); Chorded Action is the exception and only fires with another Input Action. By default any input
  activity triggers every tick.
- Trigger types: Explicit succeeds the input if it succeeds; Implicit needs it and all other implicit triggers to
  succeed; Blocker fails the input if it succeeds. Page logic: no implicits and no explicits fires unless value is 0; with
  only explicits, at least one fired; with only implicits, all fired; with both, all implicits and at least one explicit;
  blockers override everything.
- A trigger returns None (conditions unmet), Ongoing (partly met) or Triggered (all met).
- Action-level trigger events to bind: Started, Ongoing, Triggered, Completed, Canceled. Page examples: a Press and
  Release trigger sends Triggered on release; the first press of Double tap calls Started once; Press and hold is Ongoing
  while held before the duration; Canceled if released before the hold completes. Ongoing may fire every tick while the
  action is evaluated.
- Custom: extend the base Input Trigger, or Input Trigger Timed Base (checks the input was held for a length of time and
  returns Ongoing; it never returns Triggered itself). Override `GetTriggerType` and `UpdateState` (player input,
  current value, delta time; returns None, Ongoing or Triggered).
- The page shows `UInputTriggerHold`: `HoldTimeThreshold` (default 1.0, ClampMin 0), `bIsOneShot` (default false). Its
  `UpdateState_Implementation` triggers once `HeldDuration >= HoldTimeThreshold`; with `bIsOneShot` later frames
  return `ETriggerState::None`. `GetSupportedTriggerEvents` returns `ETriggerEventsSupported::Ongoing`.

## Checked
Date: 2026-11-07. Read in full: the Enhanced Input page (Input Modifiers, Directional Input, Input Triggers, Trigger
States sections and the Hold source listings), unversioned en-us page. The second source (UInputTrigger API page)
returned no text and was dropped.
Removed as not on the page: the modifier list (Dead Zone settings, Scalar, Response Curve, FOV Scaling, Smooth), the
trigger table (Pressed, Released, Hold And Release, Tap, Pulse, Combo "5.2+"), Radial 0.2 and mouse-look advice, the
mapping-before-action modifier order, `GetElapsedTime`/`GetTriggeredTime`, the interact-UI binding sample and the Verify
checklist. Tap, Pulse and Combo triggers are not described there.
Method: documentation only; no commands were run.
