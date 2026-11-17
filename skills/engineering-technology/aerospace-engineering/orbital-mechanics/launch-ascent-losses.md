---
id: engineering-technology.aerospace-engineering.orbital-mechanics.launch-ascent-losses
name: launch-ascent-losses
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [ascent-losses, gravity-loss, drag-loss, steering-loss, launch-delta-v, launch-and-rendezvous]
level: practitioner
status: gated
description: "Budget launch ascent delta-v: orbital speed plus gravity, drag and steering losses, minus Earth rotation, for a typical LEO insertion."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Sutton and Biblarz, Rocket Propulsion Elements"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ascent losses

**Goal:** the real delta-v a launcher needs, compared with orbital speed.

## Budget terms
- Orbital speed at about 200 km altitude is 7.78 km/s (recomputed, mu = 398,600 km3/s2).
- **Gravity loss**: `integral(g sin(gamma) dt)` along the flight, where `gamma` is the flight path angle above horizontal; lower thrust-to-weight raises it because the vehicle spends longer fighting gravity.
- **Drag loss**: `integral(D/m dt)`, small for large vehicles that exit the dense atmosphere quickly.
- **Steering loss**: thrust not aligned with velocity (pitch programme, gravity turn, angle-of-attack).
- **Rotation gain**: Earth's equatorial speed of about 0.465 km/s (2 pi R / sidereal day, recomputed 0.4651) helps an eastward launch from the equator; scales with `cos(latitude)` and launch azimuth (see launch-azimuth-and-inclination).
- Typical total delta-v to low Earth orbit is about 9.3 to 9.5 km/s, depending on vehicle and trajectory (gated: unconfirmed, source is paywalled or blocked).

## Procedure
1. Start from orbital speed at the target altitude.
2. Add gravity, drag and steering losses from a trajectory simulation or heuristic values (about 1.0 to 1.5 km/s gravity, 0.1 to 0.2 km/s drag are typical (gated: unconfirmed, source is paywalled or blocked), to be replaced by simulation).
3. Subtract rotation gain.
4. Convert to propellant with the rocket equation (see rocket-equation-and-staging).

## Gotchas
- Using ideal delta-v for a stage with low initial thrust-to-weight understates the propellant.
- Throttling for maximum dynamic pressure adds a small loss.
- Air-launched or high-altitude starts change the budget.

## Verify
- [ ] The sum of the terms for a known launcher is within a few percent of its published payload capability.
