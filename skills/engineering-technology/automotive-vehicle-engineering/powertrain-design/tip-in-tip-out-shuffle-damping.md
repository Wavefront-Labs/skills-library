---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.tip-in-tip-out-shuffle-damping
name: tip-in-tip-out-shuffle-damping
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [shuffle-damping, tip-in, tip-out, driveline-oscillation, lash-crossing, active-damping, driveability, surge, jerk]
level: practitioner
status: gated
description: "Control driveline shuffle and lash-crossing clunk at tip-in and tip-out with torque shaping and active speed-difference damping; measure surge and jerk to tune it."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems (chapter list)"
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tip-in / tip-out shuffle damping

**Symptom:** a longitudinal surge (low-frequency shuffle) after a pedal step, and a clunk when torque reverses through gear lash.

## 1. Understand the mechanism
The driveline is a torsional spring-mass system: engine/flywheel inertia, shaft and tyre compliance, vehicle mass. Its first mode is typically in the low single-digit to about 10 Hz range (gated: unconfirmed, source is paywalled or blocked), lower in high gears; confirm on your vehicle by measurement. A sharp torque step excites it. Lash (backlash in gears, splines, diff) creates a nonlinear free-flight phase then an impact at torque sign change.

## 2. Measure first
Instrument: longitudinal acceleration at the seat rail, engine speed, wheel (or output shaft) speed, pedal, gear. Plot the twist proxy = engine speed / ratio - wheel speed, and acceleration vs time after a tip-in. Record frequency, decay and peak jerk. Repeat in each gear, warm and cold.

## 3. Torque shaping (feed-forward)
- Limit torque rate through the **lash zone**: slow the ramp as torque crosses zero, then speed up once contact is made. Detect lash state from estimated twist.
- Pre-filter the demand (notch at the shuffle frequency, or a smooth profile) so the step does not contain energy at the mode.

## 4. Active damping (feedback)
Feed back the speed difference across the compliance (estimated twist rate) with a gain to the torque request, typically via a band-pass around the shuffle frequency, so torque oscillates in anti-phase to the surge. Constraints: sensor latency, actuator bandwidth (engine torque response, motor current loop), gear-dependent frequency (schedule gain and centre frequency by gear and clutch state). EVs have fast torque, which makes this easier but also makes raw demand harsher.

## 5. Tune and verify
Tune on a repeatable manoeuvre (a fixed pedal step at a given speed and gear). Success is a measured decay within a few cycles and peak jerk below the programme target, without a noticeable response delay.

## Failure modes
- Damping gain too high amplifies sensor noise or interacts with ABS/TCS torque interventions.
- Filter introduces delay the driver feels as lag.
- Clunk returns when aged or cold parts change lash; calibrate across temperature and mileage.

## Verify
- [ ] Shuffle frequency measured per gear.
- [ ] Peak jerk and decay recorded before/after on the same manoeuvre.
- [ ] Hot, cold, low-mu and ABS/TCS interaction tested.
