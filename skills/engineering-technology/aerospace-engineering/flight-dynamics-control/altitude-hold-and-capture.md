---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.altitude-hold-and-capture
name: altitude-hold-and-capture
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, autopilot, autopilot-modes, altitude-hold, altitude-capture, vertical-speed, mode-logic, pitch-command-limit]
level: practitioner
status: draft
description: "Design altitude capture and hold modes: outer-loop structure, capture logic, pitch and vertical-speed limits, and smooth transitions between climb and hold."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Stevens, Lewis and Johnson, Aircraft Control and Simulation"
  - "Federal Aviation Administration advisory circular 91-85B (RVSM authorization), https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_91-85B.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Altitude hold and capture

**Goal:** acquire and hold a selected altitude with passenger-acceptable motion.

## Structure
- Inner loop: pitch attitude (or flight path angle) hold with a pitch damper.
- Outer loop: altitude error `h_err = h_cmd - h` -> commanded vertical speed or pitch -> inner loop. Add `h_dot` feedback for damping.
- Mode logic: altitude select (climb or descend to target) -> altitude capture (when `|h_err|` falls below a threshold proportional to vertical speed, for example `|h_err| < k |h_dot|`) -> altitude hold.

## Design steps
1. Choose the capture law: an exponential approach `h_dot_cmd = (h_cmd - h)/tau`, with `tau` of the order of 10 s, limited to a maximum vertical speed and normal acceleration (for example 0.05-0.1 g).
2. Select outer-loop gains for the bandwidth at least a factor of 3-5 below the pitch attitude loop.
3. Smooth transitions: initialise integrators, rate-limit command changes, avoid pitch kicks at mode change.
4. Use barometric altitude (and compensate for lag and static source error); in RVSM airspace the altitude-keeping performance and equipment need operational approval (see FAA AC 91-85B for part 91 RVSM, and the equivalent authority material elsewhere).
5. Add speed protection logic so a climb does not stall the aircraft (autothrottle interaction).

## Gotchas
- Altimeter lag creates oscillation if the outer loop is too fast.
- Gust and turbulence disturb vertical speed measurement; filter appropriately.

## Verify
- [ ] Capture from a 1000 ft climb shows no overshoot beyond the specified tolerance and acceptable load factor.
