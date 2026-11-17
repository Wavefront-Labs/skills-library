---
id: creative-arts.game-design.systems-and-mechanics.control-schemes-and-remapping
name: control-schemes-and-remapping
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-and-mechanics, control-remapping, input-design, control-scheme, accessibility, controller-layout]
level: practitioner
status: docs-checked
description: "Design default control schemes per device and full input remapping: binding model, conflicts, alternates, toggle/hold options and platform guidelines."
sources:
  - https://gameaccessibilityguidelines.com/allow-controls-to-be-remapped-reconfigured/
  - https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/107
  - https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/manual/ActionBindings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control schemes and remapping

**Goal:** sensible defaults on every device, and every action rebindable by every player.

## Default scheme
1. List actions by frequency and urgency; put the most frequent on the easiest inputs
   (face buttons, right trigger, WASD plus mouse).
2. Follow genre conventions unless you have a reason; conventions are free learning.
3. Avoid requiring simultaneous button presses (Xbox guideline 107 advises against them).
4. Group related actions.

## Remapping model
- Bind **actions**, not keys: Xbox Accessibility Guideline 107 suggests remapping game
  actions rather than individual controls. In the Unity Input System, binding overrides
  are applied with the `ApplyBindingOverride` APIs and can be saved and restored as JSON
  with `SaveBindingOverridesAsJson` and `LoadBindingOverridesFromJson`, so player
  overrides stay separate from the defaults.
- Interactive rebinding in Unity is `PerformInteractiveRebinding()`.
- Offer **toggle or auto-hold** for controls that are normally held (sprint, fire,
  accelerate), invert each stick's x and y axis individually, and give per-control
  sensitivity adjustment.
- Remapping must cover all controls, and tutorial prompts, hints and controller maps must
  show the current mapping.
- Provide a set of presets plus a custom option that allows full remapping.

## Guidelines
- Game Accessibility Guidelines: allow controls to be remapped/reconfigured; console
  system-level remapping is a safety net, not a substitute for in-game remapping, and
  in-game prompts can reflect the current mapping.
- Xbox Accessibility Guideline 107 (Input): players should be able to remap all controls
  in the game itself, including the Esc key on PC games, regardless of platform-level
  remapping.

## Gotchas
- Hardcoded key checks in UI break remaps; audit for raw key reads.
- Tutorial prompts must read the live binding, not the default.
- Combos defined as specific physical keys become impossible after remap.

## Verify
- [ ] Every action, including menus, rebindable on each device.
- [ ] Toggle/auto-hold, per-stick invert and sensitivity options.
- [ ] Prompts and glyphs follow the current binding.

## Checked
Checked 2026-11-09 against Game Accessibility Guidelines (remap page), Xbox Accessibility
Guideline 107 on Microsoft Learn (first 120 lines read: goal, implementation guidelines
and start of mobile section), and the Unity Input System 1.8 ActionBindings manual
(override and rebinding API names; page searched, not read in full). Removed: the Unreal
Enhanced Input reference, conflict-swap and dead-zone advice, per-device alternate
bindings, hold-time adjustment, reset-per-device and the reserved pause/home rule (no
readable source).
Method: documentation only; no commands were run.
