---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.wheel-bearing-and-hub-load-calculation
name: wheel-bearing-and-hub-load-calculation
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [wheel-bearing, hub-bearing, hub-loads, bearing-life, l10-life, iso-281, wheel-end, knuckle, duty-cycle, bearing-preload]
level: practitioner
status: verified
description: "Calculate wheel bearing and hub loads from cornering, braking and vertical cases, equivalent load duty cycle and L10 life, and check preload, sealing and knuckle stiffness."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "ISO 281 (rolling bearing dynamic load ratings and rating life; confirm edition)"
  - "https://en.wikipedia.org/wiki/Rolling-element_bearing"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Wheel bearing and hub load calculation

## 1. Load cases at the tyre contact patch
For each case give vertical Fz, lateral Fy, longitudinal Fx at the contact patch, with the lever arms:
- Cornering (for example a quasi-static limit corner at the tyre's peak friction), with load transfer.
- Braking (front axle with brake-force distribution; see brake force distribution).
- Driving traction at peak torque.
- Combined, plus bump and curb-strike (shock cases with high Fz and Fy).
Take values from vehicle dynamics simulation or measurement with wheel force transducers.

## 2. Bearing reactions
Treat the hub as a beam on two bearing rows (or a double-row unit): the lateral force Fy acting at the rolling radius above the contact patch, offset from the bearing centre, produces a moment M = Fy x r_loaded + Fz x offset (signs per geometry). Solve for radial and axial load on each row. Use the unit supplier's tools or a bearing program (for nonlinear contact angle and preload) for accuracy.

## 3. Equivalent load and life
Basic rating life L10 (millions of revolutions) = (C/P)^p with p = 3 for ball bearings and 10/3 (3.33) for roller bearings, at 90 percent reliability, where C is the dynamic load rating and P the equivalent dynamic load (from the ISO 281 factors; the life method is described in ISO 281). For varying loads, combine cases weighted by time or distance fraction:
P_eq = (sum(q_i x P_i^p))^(1/p) with q_i the fraction of revolutions in case i.
Convert revolutions to km with rolling circumference. Required L10 distance, reliability and safety factor come from the customer standard; for hub bearings a high target is typical because of the safety function.

## 4. Other design checks
- **Preload and clearance:** preload set by the nut or orbital forming; excessive preload overheats and shortens life; too little allows fretting and play.
- **Sealing:** contamination (water, salt, brake dust) is a main life limiter; verify with a salt-spray and mud test.
- **Stiffness:** bearing and knuckle stiffness affect camber compliance (see compliance steer) and brake judder sensitivity.
- **ABS target ring:** magnetic encoder in the seal needs air-gap control.
- **Torque on axle nut and spline/hub joints.**

## 5. Test
Bearing rig test on a representative load spectrum, durability on proving ground, post-test teardown of bearing, seal and grease.

## Verify
- [ ] Load cases include shock cases and measured wheel forces where available.
- [ ] L10 computed on the real spectrum with the customer-specified target and factor.
- [ ] Preload, sealing and stiffness checked.
- [ ] Rig and vehicle durability evidence recorded.
