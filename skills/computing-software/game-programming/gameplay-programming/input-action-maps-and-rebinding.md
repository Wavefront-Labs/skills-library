---
id: computing-software.game-programming.gameplay-programming.input-action-maps-and-rebinding
name: input-action-maps-and-rebinding
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, input-system, action-maps, rebinding, device-agnostic, control-scheme, multiplayer-local-input, dead-zone, input-buffering, controller-switching, accessibility, unity-input-system, unreal-enhanced-input, game-programming]
level: practitioner
status: draft
description: "Architect input as action maps with device-agnostic bindings, so rebinding, controller/keyboard switching mid-session, and local multiplayer all work without special-casing."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@latest", "https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input action maps and rebinding

**Goal:** structure input so gameplay code asks "was Jump pressed" rather than
"was Space or Gamepad button A pressed" — this is what makes rebinding, device
switching mid-session, and local multiplayer all fall out for free instead of
needing special-casing at every call site.

## Actions, not raw keys
Define **logical actions** (`Jump`, `Move`, `Fire`) once, each bound to one or
more physical inputs (keyboard key, gamepad button, mouse button) per
**control scheme**. Gameplay code reads `jumpAction.WasPressedThisFrame()` or
equivalent — it never checks `Input.GetKeyDown(KeyCode.Space)` directly. This
single indirection is the entire trick: rebinding becomes "change what's bound
to the Jump action," not "find every place Space is hardcoded and add a
settings-driven branch." Both Unity's Input System package (Action Maps,
InputActionAsset) and Unreal's Enhanced Input (Input Actions + Mapping
Contexts) are built around exactly this model; a custom engine should copy it
rather than reinvent per-key polling.

## Composite bindings and dead zones
Movement is rarely one key — a 2D `Move` action is usually a **composite**
binding combining 4 keys into a `Vector2` (WASD/arrows → `(x,y)`), or reads a
gamepad stick's analog axis directly. Analog axes need a **dead zone**
(ignore input below a small magnitude threshold — stick drift/imprecision
causes false micro-movement near zero) and a response curve (linear vs
exponential — exponential gives finer control near center for aiming,
linear/raw for movement). Get the dead zone wrong (too small) and a character
visibly creeps with the stick at rest; too large and small deliberate
movements get clamped to zero.

## Device switching mid-session
A player might plug in a gamepad mid-match, or touch the keyboard after using
a controller. Detect the **last device that produced input** (most input
systems expose this, e.g. Unity's `InputUser` / device-change events) and
switch the displayed button-prompt icons/control scheme accordingly — showing
"Press A" when the player is on keyboard (or vice versa) is a constant source
of user confusion and support tickets. Don't assume the device present at
startup is the device in use for the whole session.

## Local multiplayer: per-player device binding
Each local player must be locked to a specific device (or device pair) once
assigned — player 1's gamepad input must never leak into player 2's actions.
This needs an explicit **player-to-device map** set up during a join/lobby
screen (pressing a button on an unassigned device claims it for a new local
player) rather than a single global action set shared across players; both
major input systems support multiple simultaneous "input users"/player
contexts for this, but it has to be deliberately wired — the default single-
player setup doesn't do this automatically.

## Rebinding UI gotchas
- **Conflict detection**: rebinding Jump to a key already bound to Sprint
  should warn or block, not silently create a conflict only discovered during
  play.
- **"Press any key" capture** needs to exclude or specially handle Escape
  (cancel) and must distinguish "listening for a new binding" from "listening
  for gameplay input" — a rebind UI that's still receiving gameplay actions in
  the background causes the character to move while the player is trying to
  rebind.
- **Persisting bindings**: save the override as a diff from default bindings
  (most systems support exporting binding overrides as a JSON/string blob),
  not as a full re-authored action asset, so a game update adding a new action
  doesn't wipe the player's existing rebinds.

## Verify
- [ ] No gameplay code reads a raw key/button directly; every input path goes
      through a named action.
- [ ] Switching from gamepad to keyboard mid-session updates on-screen prompts
      without a restart.
- [ ] Analog dead zone tested at stick-rest (no drift) and at small deliberate
      movements (not clamped away).
- [ ] Local multiplayer: each player's device assignment confirmed exclusive —
      input on player 1's pad never affects player 2.
- [ ] Rebinding a control that conflicts with an existing binding is caught and
      surfaced to the player, not silently applied.
