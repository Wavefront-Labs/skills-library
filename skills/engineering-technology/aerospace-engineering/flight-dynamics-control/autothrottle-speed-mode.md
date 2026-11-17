---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.autothrottle-speed-mode
name: autothrottle-speed-mode
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [autothrottle, speed-hold, mach-hold, thrust-control, autopilot-modes, mode-logic]
level: practitioner
status: draft
description: "Design an autothrottle speed or Mach hold loop with feedforward, anti-windup, thrust limits, engine lag handling and clear mode logic with the pitch axis."
sources:
  - "Blakelock, Automatic Control of Aircraft and Missiles"
  - "Stevens and Lewis, Aircraft Control and Simulation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Autothrottle

**Goal:** hold speed with thrust while pitch holds flight path or altitude.

## Structure
- Speed error to thrust command: PI with feedforward `T_ff` from the drag and path angle (trim thrust) so the integrator only cleans up error.
- Add flight-path acceleration feedback (longitudinal acceleration) to damp speed and reduce overshoot.
- Output: engine thrust or power command (EPR, N1, torque) with rate and position limits that match the engine's schedule and limits.

## Mode logic (speed on thrust vs speed on pitch)
1. Climb and cruise: thrust is set to a limit or hold level, pitch holds speed in climb; or thrust holds speed in cruise with pitch on altitude.
2. Descent: idle thrust with pitch for speed, or thrust to hold speed on a path.
3. Approach: thrust holds approach speed with pitch on glide path.
4. Flare and landing: thrust retard.
Every mode change must be annunciated and consistent; ambiguity about which axis holds speed has been a recurring contributor to incidents, which is why mode annunciation and monitoring are design drivers.

## Procedure
1. Identify the engine response: spool time constant (several seconds from idle) and delays.
2. Pick the loop bandwidth well below engine lag so the loop does not chase it.
3. Implement anti-windup on the limits and a thrust-rate limit.
4. Add protection: minimum speed protection (alpha-based) and a floor on thrust in approach.
5. Test in turbulence and wind shear.

## Gotchas
- Throttle lever back-driving and manual override logic must be unambiguous to the crew.
- Thrust asymmetry on multi-engine aircraft must be limited.

## Verify
- [ ] A 10 knot step command gives monotonic speed response and thrust remains within its limits.
