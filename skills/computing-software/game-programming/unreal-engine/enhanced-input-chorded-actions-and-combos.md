---
id: computing-software.game-programming.unreal-engine.enhanced-input-chorded-actions-and-combos
name: enhanced-input-chorded-actions-and-combos
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, chorded-action, enhanced-input, combo-trigger, input-triggers, game-programming]
level: practitioner
status: draft
description: "Build modifier-key chords and timed input combos with Unreal Enhanced Input Chorded Action and Combo triggers, including blocking the unchorded action and timing windows."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Plugins/EnhancedInput/UInputTriggerChordAction/", "https://docs.unrealengine.com/5.3/en-US/API/Plugins/EnhancedInput/UInputTriggerCombo/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enhanced Input chorded actions and combos

**Goal:** Shift+E does something different from E, and Down, Forward, Punch triggers a special.

## Chords
1. Create `IA_Modifier` (bool) mapped to Left Shift / gamepad LB.
2. Create `IA_SpecialInteract` mapped to E with trigger **Chorded Action**, Chord Action = `IA_Modifier`.
   It fires only while the modifier action is triggered.
3. Plain `IA_Interact` on the same E key in the **same mapping context** is blocked automatically
   while the chord is active: Enhanced Input injects a `UInputTriggerChordBlocker` into other mappings
   that share the chorded key. Across different contexts there is no automatic blocking, so keep
   chord and plain mappings together.
Order matters: the modifier action must be evaluated before the chorded action; keep it earlier in the
mapping context.

## Combos
`IA_Hadouken` with trigger **Combo**: list Combo Actions in order (`IA_Down`, `IA_Forward`, `IA_Punch`)
with Time To Press Key per step and a Trigger Event (Triggered, Started). Cancel actions (any action
that resets the combo) are configurable. The combo action itself needs a mapping (any key; commonly the
last step's key).

```cpp
EIC->BindAction(IA_Hadouken, ETriggerEvent::Triggered, this, &AMyChar::DoSpecial);
```

## Gotchas
- Chords evaluate per frame: tapping both keys simultaneously can register the unchorded action first
  if the modifier is not yet triggered. Test on frame-perfect input.
- Combo step actions must be in an active mapping context; they need their own mappings.
- Fighting-game style buffers with motion inputs often outgrow Combo triggers; a custom input buffer
  component reading action values per frame gives tighter control.

## Verify
- [ ] `showdebug enhancedinput` shows the plain action not triggered while the chord fires.
- [ ] Combo succeeds within the time window and fails after it.
