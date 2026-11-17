---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.differential-types-and-selection
name: differential-types-and-selection
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [differential-types, differential, limited-slip, torsen, locking-differential, torque-vectoring, electronic-lsd, driveline-components, bias-ratio]
level: practitioner
status: draft
description: "Choose among open, limited-slip, locking and torque-vectoring differentials by traction need, handling effect and cost, and know their failure modes and verification tests."
sources:
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
  - "Gillespie, Fundamentals of Vehicle Dynamics (chapter list)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Differential types and selection

## 1. Why a differential
Left and right wheels travel different distances in a turn, so the axle needs a speed difference. An open differential splits torque equally, so the wheel with less grip limits total traction.

## 2. Types
| Type | How it biases torque | Pros | Cons |
|---|---|---|---|
| Open | none | cheap, smooth, light | one-wheel spin on split mu |
| Clutch-pack LSD | preload plus ramp-loaded clutches | strong lock, tunable preload | wear, noise, can push understeer on power |
| Helical (Torsen-type) | gear friction, torque-sensitive | no wear parts, smooth | needs some torque on both wheels, bias ratio limited |
| Viscous | shear of fluid by speed difference | simple | slow response, ageing, heat-sensitive |
| Locking (mechanical/electric) | locks both axle shafts | max traction off-road | driveline wind-up on high mu, steering effects |
| Electronically controlled LSD / torque vectoring | clutch, brake, or dual motors | active handling and traction | cost, control complexity, safety case |
Electric axles with two motors (or an e-axle with torque vectoring) can vary left-right torque electronically without a mechanical differential.

## 3. Selection method
1. List needs: split-mu launch, track use, snow, off-road, or purely economy.
2. Quantify traction demand: axle torque available vs mu x load on the lightly loaded wheel (inside wheel in a corner under load transfer).
3. Evaluate handling: locking adds understeer on power-on corners and can cause snap behaviour on lift-off; verify with a tuned simulation (CarSim, Adams) and test.
4. Check interaction with ESC/TCS: a brake-based electronic LSD shares hardware with ESC; coordinate with the ESC supplier.
5. Compare cost, mass, oil and NVH (clutch LSD chatter, gear rattle).

## 4. Torque bias
Torque bias ratio (TBR) = high-traction-side torque / low-traction-side torque. Open diff TBR = 1. Use supplier datasheets for the real value of helical and clutch designs.

## 5. Tests
Split-mu straight-line launch, constant-radius power-on and lift-off, low-speed tight circle for binding or chatter, durability on a dynamometer with a torque spectrum.

## Verify
- [ ] Traction need quantified with load transfer.
- [ ] Handling effect (power-on and lift-off) checked in simulation and test.
- [ ] ESC/TCS coordination and diagnostic strategy defined.
- [ ] Wear, preload and fluid life verified on the durability cycle.
