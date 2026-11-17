---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.understeer-gradient-handling-balance
name: understeer-gradient-handling-balance
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [vehicle-dynamics, handling, understeer, oversteer, understeer-gradient, cornering-stiffness, bicycle-model, characteristic-speed, critical-speed, iso-4138, iso-8855, steady-state-cornering, constant-radius, roll-stiffness-distribution, load-transfer, tyre-load-sensitivity, pacejka, magic-formula, compliance-steer, roll-steer, yaw-rate-gain, kc-testing]
level: practitioner
status: gated
description: "Predict, measure and tune steady-state handling balance: understeer gradient from axle cornering stiffness, ISO 4138 constant-radius testing, and the levers that shift it."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics (SAE)"
  - "Milliken & Milliken, Race Car Vehicle Dynamics (SAE)"
  - "ISO 4138 (steady-state circular driving) and ISO 8855 (vehicle axis system)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Understeer gradient and handling balance

**Goal:** put a number on how much a car understeers in the linear range, predict it
from tyre and chassis data, measure it repeatably, and know which hardware moves it.

## 1. The linear bicycle model
In steady-state cornering at lateral acceleration a_y (in g), road-wheel steer is
```
δ = L/R + K · a_y          K = Wf/Cαf − Wr/Cαr     [rad/g]
```
Wf, Wr are axle loads (N); Cαf, Cαr are **axle** cornering stiffnesses (N/rad, both tyres).
K > 0 understeer, K = 0 neutral, K < 0 oversteer.

- Characteristic speed (understeer car, yaw-rate gain peaks here):
  `v_char = sqrt(57.3 · L · g / K)` with K in deg/g.
- Critical speed (oversteer car, becomes unstable): same expression with −K.

**Worked example:** 1500 kg, L = 2.70 m, 58/42 weight split → Wf = 8535 N, Wr = 6180 N.
Front axle Cα = 120 kN/rad, rear 130 kN/rad.
K = 8535/120000 − 6180/130000 = 0.0711 − 0.0475 = 0.0236 rad/g = **1.35 deg/g**.
v_char = sqrt(57.3 · 2.70 · 9.81 / 1.35) ≈ 33.5 m/s ≈ 121 km/h (arithmetic recomputed; yaw-rate gain there is half the neutral-steer value).

That number is the *tyre-only* gradient. A real car measures higher because of load
transfer, roll steer, compliance steer and aligning torque — see step 3.
Production passenger cars commonly land somewhere around 2–5 deg/g measured (gated: unconfirmed, source is paywalled or blocked); treat that
as an orientation band, not a target, because it is brand- and segment-dependent.

## 2. Measure it (ISO 4138)
ISO 4138 offers constant-radius, constant-steer-angle and constant-speed methods (gated: unconfirmed, source is paywalled or blocked). The
constant-radius method is the most common:
1. Mark a circle (100 m radius is a common choice; check the current edition for allowed
   radii (gated: unconfirmed, source is paywalled or blocked)). Warm tyres; set pressures cold and record them.
2. Drive the circle at increasing speed in small steps up to the limit, holding each
   point steady for a few seconds. Log steering-wheel angle, speed, yaw rate, a_y.
3. Run both directions and average to cancel crown and asymmetry.
4. Plot steering-wheel angle / overall steering ratio vs a_y. The slope in the linear
   range (typically up to ~0.3–0.4 g) is K. Beyond that, the curve shape tells you limit
   balance: steepening = progressive understeer, flattening or reversing = limit oversteer.

Use the ISO 8855 axis system and state it; sign conventions differ between SAE J670 and
ISO and are a frequent source of "the model says oversteer" arguments.

## 3. Effective cornering stiffness — why the model under-predicts
- **Tyre load sensitivity:** Cα grows less than linearly with vertical load (in Pacejka's
  Magic Formula, the slope at zero slip is BCD and it saturates with Fz). Lateral load
  transfer therefore *reduces* axle Cα; the axle with more load transfer loses more.
- **Roll stiffness distribution:** more front roll stiffness → more front load transfer →
  lower effective Cαf → more understeer. This is the main tuning knob (anti-roll bars).
- **Roll steer and compliance steer:** rear toe-in on the outside wheel under load adds
  understeer and stability; front toe-out under lateral force adds understeer too.
- **Aligning torque and steering compliance** add apparent understeer at the hand wheel.
Fold these into effective axle stiffnesses in the bicycle model, fitted to K&C rig data.

## 4. Levers, roughly in order of cost
| Lever | Direction for more understeer |
|---|---|
| Tyre pressures | raise rear / lower front (small effect, quick test) |
| Anti-roll bars | stiffer front or softer rear |
| Tyre size/construction | wider or stiffer-compound rear |
| Rear roll / compliance steer | more toe-in on the loaded outer rear |
| Weight distribution | more mass forward (expensive late in a programme) |
ESC can mask a poor passive balance on the road, but not on a homologation K&C rig or in
the linear range customers feel — get the passive balance right first.

## Gotchas
- Don't mix units: Cα per tyre vs per axle doubles K.
- A low K with high yaw-rate gain feels darty; check the yaw-rate gain and response time
  as well as K.
- Temperature and wear move tyre Cα by double-digit percent; compare runs on the same set.

## Verify
- [ ] K computed from axle (not single-tyre) cornering stiffness with consistent units.
- [ ] Measured K taken from the linear range, averaged across both directions.
- [ ] Sign convention (ISO 8855 vs SAE) stated on every plot.
- [ ] Difference between model and measured K explained by load transfer, roll and
      compliance steer — not fudged.
- [ ] Any tuning change confirmed with a repeat ISO 4138 run on the same tyres.
