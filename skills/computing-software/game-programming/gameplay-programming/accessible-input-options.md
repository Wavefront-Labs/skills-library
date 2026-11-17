---
id: computing-software.game-programming.gameplay-programming.accessible-input-options
name: accessible-input-options
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, input-accessibility, accessibility, remapping, game-programming]
level: practitioner
status: draft
description: "Implement accessible input: full remapping, hold-to-toggle, single-switch and one-handed layouts, adjustable timing windows and QTE alternatives."
sources: ["https://gameaccessibilityguidelines.com/", "https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/107"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accessible input options

**Goal:** let players with limited mobility, dexterity or reaction speed play, following the Game
Accessibility Guidelines and Xbox Accessibility Guideline 107 (input).

## Baseline features (cheap if planned early)
- **Full remapping** of every action on every device, including menu navigation; allow the same key
  on two actions only when contexts differ. Store bindings per action, not per key.
- **Hold vs toggle** per action (sprint, aim, crouch, interact-hold). Implement as an input-layer
  transform so gameplay sees the same logical "held" state either way.
- **Repeated-press alternatives:** button-mash prompts get a "hold instead" option.
- **Adjustable timing:** QTE windows, double-tap windows and combo leniency scaled by a setting;
  option to auto-complete QTEs.
- **Stick sensitivity, dead zones and invert** per axis; aim assist strength levels.
- **Copilot / two-controller merge:** two devices drive one player (Xbox Copilot does this at OS
  level; support it by reading all devices for player 1 when enabled).

## Architecture
```text
device -> raw events -> remap table -> accessibility transforms (toggle, hold-to-repeat,
          timing scale) -> logical actions -> gameplay
```
Keep transforms out of gameplay code: gameplay should never check "is toggle mode on".

## Gotchas
- Hard-coded keys in UI prompts or tutorials break after remapping; always render prompts from the
  binding table.
- Simultaneous-press requirements (L3+R3) exclude single-hand players; provide a single-button alternative.
- Save settings before the first gameplay scene, and expose them from the first boot screen.

## Verify
- Play the first hour with only a keyboard's left half, then with one controller hand.
- Check against the GAG basic/intermediate input items and XAG 107 checklist.
