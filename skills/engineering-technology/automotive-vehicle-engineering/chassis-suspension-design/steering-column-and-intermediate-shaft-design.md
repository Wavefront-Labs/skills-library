---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.steering-column-and-intermediate-shaft-design
name: steering-column-and-intermediate-shaft-design
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [steering-column, intermediate-shaft, collapsible-column, universal-joint, cardan-joint, tilt-telescope, steering-design, steering-crash-performance, steering-isolation]
level: practitioner
status: gated
description: "Design a steering column and intermediate shaft: universal joint angles and phasing, tilt and telescope range, crash collapse stroke, torsional stiffness and isolation."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
  - "FMVSS 203 and 204 (driver impact protection; steering control rearward displacement) and UN Regulation 12; confirm current texts"
  - "https://www.law.cornell.edu/cfr/text/49/571.203"
  - "https://www.ecfr.gov/current/title-49/part-571/section-571.204"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Steering column and intermediate shaft design

## 1. Function chain
Steering wheel - column (tilt/telescope, lock, switches, airbag) - upper universal joint - intermediate shaft - lower joint - rack or gearbox input. Package constraints (cowl, pedals, crossbeam) dictate the angles.

## 2. Universal joint kinematics
A single Cardan joint transmits angular velocity non-uniformly: output speed varies twice per revolution (checked numerically), with the fluctuation growing with joint angle. Two joints in series cancel this if (a) the intermediate shaft yokes are in phase (aligned) and (b) the two joint angles are equal and in the same plane (Z or W arrangement). If they are in different planes (spatial layout), use the phasing angle that minimises the net speed error; compute it in a multibody or kinematic model. Keep operating angles modest (supplier catalogues give limits) because torque ripple becomes felt steering roughness.

## 3. Compliance and isolation
- **Torsional stiffness:** high enough that the driver feels the road through the system; low stiffness adds lag and reduces on-centre feel (see on-centre feel).
- **Isolation:** rubber couplings or slip joints at the rack end reduce road shock and noise transmission; compromise with feel.
- **Bending modes:** column first mode must be above the engine and road excitation frequencies to avoid steering wheel shake; check with modal tests.

## 4. Adjustability
Tilt and telescope ranges ergonomic requirements; lock mechanism strength (clamp load, friction) against driver and crash loads; positive lock under crash.

## 5. Crash behaviour
Energy-absorbing (collapsible) column: in a frontal crash the column strokes under driver load so the wheel and airbag work with the occupant; limit rearward displacement of the column into the cabin (FMVSS 204 limits rearward displacement of the steering column and shaft upper end to 127 mm (5 in) in a 48 km/h barrier crash; UN R12 has equivalent driver-protection requirements, text not checked (gated: unconfirmed, source is paywalled or blocked); confirm applicable edition and test). Define collapse force-stroke curve with the airbag and belt system.

## Verify
- [ ] Joint angles and phasing analysed over the full steering and column adjustment range.
- [ ] Torsional stiffness and first bending mode measured and met.
- [ ] Lock, adjust and crash collapse performance tested against the applicable regulations.
- [ ] Isolation does not degrade on-centre feel beyond the target.
