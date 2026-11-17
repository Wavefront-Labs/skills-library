---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.accelerator-pedal-map-design
name: accelerator-pedal-map-design
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [pedal-map, accelerator-pedal, driver-demand, driveability, pedal-interpretation, one-pedal-driving, driving-modes, torque-demand]
level: practitioner
status: draft
description: "Design the accelerator pedal map that turns pedal position and vehicle speed into wheel or engine torque demand with progressive feel, drive modes and rate limits."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems (chapter list)"
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Accelerator pedal map design

**Goal:** a predictable, proportional relationship between pedal and acceleration that suits each drive mode, with no surprises at tip-in, part-load or zero crossing.

## 1. Decide what the pedal commands
Most modern vehicles interpret the pedal as **driver demand** (wheel torque or acceleration), not a throttle angle. Define demand at the wheel, then convert to engine/motor torque per gear and ratio. This keeps feel consistent across gears.

## 2. Build the map
A 2-D table: pedal position (0-100%) x vehicle speed -> wheel torque demand (or demand as a fraction of available torque at that speed).
- Pedal 0%: zero or small negative demand (engine braking or regen level), speed-dependent.
- Low pedal (0-15%): fine resolution, gentle slope, so parking and creep are controllable.
- Mid pedal: roughly linear to the available torque envelope, so equal pedal changes give similar acceleration changes.
- Top: demand reaches full torque slightly before 100% pedal so the driver need not bury the pedal (the margin is a programme choice).
Normalise to the torque available at that speed so the top of the pedal always means "all there is".

## 3. Drive modes
Economy/Normal/Sport differ in map shape (concave = less response at low pedal; convex = more), rate limits, and regen level. Provide the mode as a table selector and interpolate when the mode changes.

## 4. Rate limiting and filtering
Limit rate of demand rise to protect the driveline (see lash crossing in `tip-in-tip-out-shuffle-damping`) but keep response perceptible; use asymmetric limits (faster up than down, or the reverse per feel target). Filter pedal noise lightly; do not add lag the driver feels as delay.

## 5. EV one-pedal behaviour
Negative demand at lift-off: define a regen torque vs speed curve, a smooth fade to zero near standstill, and the blend with friction brakes. Cap deceleration by traction and by the regulatory requirements on stop-lamp activation (confirm the regulation applicable in your market).

## 6. Calibrate by drive plus measurement
Objective: acceleration vs pedal at several speeds and gears; time to a reference speed from a fixed pedal; jerk at tip-in. Subjective rating by trained drivers on a defined scale, then tune the table cells that correlate.

## Verify
- [ ] Demand is normalised to available torque at each speed.
- [ ] Monotonic map: no cell causes demand to fall as pedal rises.
- [ ] Rate limits tested for lash crossing and wheel slip on low-mu.
- [ ] Mode switch interpolation tested while driving.
- [ ] Regen/lift-off levels agree with brake-light and regulatory requirements.
