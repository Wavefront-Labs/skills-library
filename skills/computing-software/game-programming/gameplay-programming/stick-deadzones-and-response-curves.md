---
id: computing-software.game-programming.gameplay-programming.stick-deadzones-and-response-curves
name: stick-deadzones-and-response-curves
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, input-system, stick-deadzone, radial-deadzone, axial-deadzone, response-curve, analog-stick, gamepad, aim-sensitivity, outer-deadzone, game-programming]
level: practitioner
status: gated
description: "Process analog stick input properly: radial vs axial dead zones, scaled rescaling, outer dead zone, response curves for aiming, and per-device tuning."
sources: ["https://www.gamedeveloper.com/business/doing-thumbstick-dead-zones-right", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Processors.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stick dead zones and response curves

**Goal:** sticks that do not drift, reach full speed at full tilt, allow precise slow aim, and feel
the same on worn and new controllers.

## Why naive dead zones feel bad
- **Axial** (`if abs(x) < dz: x = 0` per axis): snaps movement to the axes near the centre; diagonals
  feel sticky. Fine for d-pad-like menu navigation only.
- **Radial without rescale** (`if len < dz: v = 0`): no drift, but output jumps from 0 to `dz` when
  leaving the zone, so the smallest movement is not small.

## Scaled radial dead zone (default for movement and aim)
```
v      = raw stick vector (-1..1 each axis)
len    = length(v)
inner  = 0.15        # drift threshold; measure on worn pads, 0.1-0.25 typical
outer  = 0.95        # many sticks never report exactly 1.0, especially on diagonals
if len < inner: return (0,0)
t      = clamp((len - inner) / (outer - inner), 0, 1)   # rescale to 0..1
return normalize(v) * t
```
Run in Python with inner 0.15 and outer 0.95: (0.14, 0) gives (0, 0); (0.151, 0) gives 0.00125, so output starts near zero rather than jumping to the dead-zone size; (0.95, 0) gives 1.0; a diagonal (0.7, 0.7) gives 0.707 per axis (length 1.0).
The outer dead zone guarantees full speed is reachable on every controller; also clamp `len` to 1
because square-gate sticks report up to ~1.41 on diagonals.

## Response curve (aim)
Apply after the dead zone, on the magnitude:
```
m = t ^ exponent          # exponent 1 = linear, 2-3 = precise near centre, fast at edge
out = direction * m
```
Variants used in shooters: a two-zone curve (linear up to 0.8, then accelerating "turn boost" after
holding full tilt for ~0.1-0.3 s). Expose curve type and exponent in the options menu; players expect
"Linear / Classic / Dynamic" style choices.

## Separate settings per use
- Movement: radial scaled, linear curve, inner ~0.15.
- Camera/aim: radial scaled, curve exponent ~2, separate X/Y sensitivity, optional invert Y.
- Menus: axial with hysteresis (enter at 0.5, release at 0.3) plus repeat delay ~0.4 s then ~0.1 s.
- Triggers: own inner dead zone (~0.05-0.1) and outer (~0.95).

## Engine mapping
- Unity Input System: `StickDeadzone` processor (`min`, `max`) scales a Vector2 so magnitudes below min give (0,0) and magnitudes above max are normalised to length 1 (Input System 1.11 manual); add a
  custom `InputProcessor<Vector2>` for curves.
- Unreal Enhanced Input: `Dead Zone` modifier (Type: Radial/Axial, Lower/Upper Threshold), `Response
  Curve - Exponential` modifier (gated: unconfirmed, source is paywalled or blocked).
- Godot: InputMap action deadzone per action; for vectors use `Input.get_vector(neg_x, pos_x, neg_y,
  pos_y, deadzone)` which is radial and rescaled (engine source: below the deadzone returns zero, above 1 normalises, otherwise inverse-lerps the length from (deadzone, 1) to (0, 1); a negative deadzone argument means the average of the four actions' deadzones).

## Verify
- [ ] Rest a worn controller on the desk: no movement for 60 s.
- [ ] Slowest stick deflection produces slow (not jump-start) movement.
- [ ] Full tilt on every diagonal reaches max speed (log magnitude == 1.0).
- [ ] Draw the processed vector on a debug overlay while circling the stick: smooth circle, no axis snapping.
