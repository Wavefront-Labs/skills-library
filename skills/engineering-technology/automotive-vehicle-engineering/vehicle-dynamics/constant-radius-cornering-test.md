---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.constant-radius-cornering-test
name: constant-radius-cornering-test
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [constant-radius-test, constant-radius, skidpad, iso-4138, understeer-gradient, steady-state-test, steady-state-handling]
level: practitioner
status: gated
description: "Run and analyse a constant-radius cornering test to measure understeer gradient, roll gradient and limit behaviour, with data cleaning and plotting."
sources:
  - "ISO 4138 (steady-state circular driving behaviour, open-loop methods; confirm current edition at iso.org)"
  - "SAE J266, Steady-State Directional Control Test Procedures for Passenger Cars and Light Trucks (reaffirmed 2025; saemobilus.sae.org)"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Constant-radius cornering test

1. Mark a circle of known radius R (30-100 m typical (gated: unconfirmed, source is paywalled or blocked)); instrument steering wheel angle, lateral acceleration, yaw rate, roll angle, speed and sideslip if possible. The standards (ISO 4138, SAE J266) define methods and conditions; confirm the edition.
2. Drive at slowly increasing speed so lateral acceleration rises slowly enough to stay quasi-steady (a ramp of a minute or more to reach the limit (gated: unconfirmed, source is paywalled or blocked)), then repeat both directions and average.
3. Compute road-wheel angle `delta = steering_wheel_angle / steering_ratio` and plot `delta - L/R` against `ay`; slope in deg/g is the understeer gradient K. Plot roll angle vs ay for roll gradient.
4. Apply Ackermann reference `L/R` using the actual tracked radius from GPS rather than the marked circle if speed is small.
5. Report K at low ay (near-linear range) and describe the limit behaviour: understeer at limit, power-off response, any snap.

**Gotchas:** tyre warm-up, wind, track slope, steering ratio assumed constant when it is not.

## Verify
- [ ] Left and right directions agree within tolerance after sign correction.
- [ ] K matches the bicycle-model prediction within the measured spread.
