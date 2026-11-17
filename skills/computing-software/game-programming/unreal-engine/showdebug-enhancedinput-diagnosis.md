---
id: computing-software.game-programming.unreal-engine.showdebug-enhancedinput-diagnosis
name: showdebug-enhancedinput-diagnosis
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, enhanced-input, showdebug-enhancedinput, input-debugging, mapping-context-priority, game-programming]
level: practitioner
status: draft
description: "Diagnose Unreal Enhanced Input problems with showdebug enhancedinput, input.+key injection, mapping context priorities, consumed keys and trigger states."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/EnhancedInput/UEnhancedInputLocalPlayerSubsystem"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnosing Enhanced Input with showdebug

**Goal:** find out quickly why an action doesn't fire, fires twice, or fires in the wrong context.

## Tools
- Console `showdebug enhancedinput`: overlay listing active mapping contexts (with priority), each
  action's current value and trigger state (None/Ongoing/Triggered), and the keys mapped.
- `showdebug devices` (5.x): connected input devices and their types.
- `Input.+key Gamepad_FaceButton_Bottom` / `Input.-key ...` (EnhancedInput console commands) to inject
  presses; useful on PC without a pad.
- `log LogEnhancedInput Verbose` for mapping rebuilds and warnings.

## Checklist when an action doesn't fire
1. Is the mapping context added? (`Subsystem->AddMappingContext(IMC, Priority)` on the local player;
   for pawns, contexts are often added in `PawnClientRestart`/possess — check it ran on the client.)
2. Is the binding made? `EnhancedInputComponent->BindAction(IA, ETriggerEvent::Triggered, ...)` and is
   the input component the one being processed (pawn's `SetupPlayerInputComponent` called after
   possession).
3. Is a higher-priority context consuming the key? Higher priority contexts win; with
   `bConsumeInput` on the action (default true) lower contexts don't receive that key.
4. Trigger states: a Hold trigger never reaches Triggered on a quick tap; bind `Completed` or `Canceled`
   accordingly. Debug overlay shows Ongoing vs Triggered.
5. Value type: Axis2D action bound to a single key without Swizzle/Negate modifiers gives X only.
6. UI input mode: `SetInputMode(FInputModeUIOnly)` stops game input entirely.

## Double firing
- Same IMC added twice is ignored, but two IMCs mapping the same key to the same action fire twice
  if neither consumes.
- Binding in both C++ and Blueprint to `Triggered` = two callbacks.
- `Triggered` fires **every frame** while held for Down/no-trigger mappings; use `Started` for
  one-shot presses or add a Pressed trigger.

## Verify
- [ ] Overlay shows expected contexts after possession, respawn and UI open/close.
- [ ] Input injection reproduces the bug deterministically.
