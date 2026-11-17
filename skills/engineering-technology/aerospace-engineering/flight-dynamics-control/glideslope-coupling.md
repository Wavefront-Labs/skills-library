---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.glideslope-coupling
name: glideslope-coupling
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [glideslope, ils, glideslope-capture, autoland-approach, gain-scheduling, autopilot-modes]
level: practitioner
status: draft
description: "Design glideslope capture and tracking for coupled ILS approaches: deviation-to-pitch law, gain scheduling with range, capture logic and flare hand-off."
sources:
  - "Blakelock, Automatic Control of Aircraft and Missiles"
  - "ICAO Annex 10 (ILS standards)"
  - "Nelson, Flight Stability and Automatic Control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Glideslope coupling

**Goal:** fly the ILS glide path automatically from capture to flare.

## Signal
The ILS glide slope receiver gives angular deviation from the glide path (difference in depth of modulation, converted to degrees). The nominal glide path angle is about 3 degrees. The same angular error is a smaller linear distance close to the antenna, so loop gain must scale.

## Law
- Pitch command from the glide path error `epsilon` (and its integral and the rate): `theta_cmd = K_e * epsilon + K_i * integral(epsilon) + K_edot * epsilon_dot` (or equivalent flight-path-angle command).
- Gain scheduling: reduce `K_e` as range falls (or with radio altitude) to keep the linear-cross-track loop gain roughly constant.
- Speed control during the approach is by autothrottle (see autothrottle-speed-mode).

## Capture logic
1. Arm the mode while below the glide path (or from above if the aircraft is configured for it).
2. Capture when the deviation and its rate meet the threshold (the capture point is computed so the aircraft turns onto the path with little overshoot).
3. Monitor signal quality and mode transitions (annunciation).
4. Hand over to the flare law at the specified radio altitude.

## Gotchas
- Beam bends and reflections give noise at short range; filter but account for the lag.
- Capture from above, or with high closure, needs different logic.
- Certification for automatic approach and landing uses the authority's criteria (for example FAA and EASA all-weather operations requirements) and requires system safety assessment; this skill is practice guidance.

## Verify
- [ ] In simulation with beam noise and wind shear, path deviation at the decision height stays within the required limit.
