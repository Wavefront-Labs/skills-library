---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.ackermann-steering-geometry
name: ackermann-steering-geometry
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [ackermann, steering-geometry, steer-angle, tie-rod, steering-arm, turning-circle, anti-ackermann, steering-design, toe-out-on-turns]
level: practitioner
status: verified
description: "Set Ackermann steering geometry: compute ideal inner and outer wheel angles, choose steering arm and tie-rod layout, and judge percent Ackermann for the vehicle's use."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
  - "Gillespie, Fundamentals of Vehicle Dynamics (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ackermann steering geometry

## 1. Ideal Ackermann
At very low speed there is no tyre slip, so all wheels roll about a common centre on the rear-axle line. With wheelbase L and kingpin track t, the inner (delta_i) and outer (delta_o) steer angles satisfy
cot(delta_o) - cot(delta_i) = t / L (checked numerically against the common-centre geometry).
Turn radius at the rear axle midpoint is approximately L / tan(delta_mean) for small angle estimates; use a kinematic model for exact figures.

## 2. Geometry that produces it
Extend the line through each steering arm's kingpin axis foot to the steering arm ball joint; for 100% Ackermann those lines meet on the rear axle centreline. Angling the steering arms inward (toe-in of the arm line) increases Ackermann; parallel arms give 0%; arms angled outward give anti-Ackermann. With rack-and-pinion, the tie-rod length, rack position and arm angle together set it (see steering rack packaging).

## 3. Percent Ackermann
Percent Ackermann = actual toe-out difference / ideal toe-out difference at a given steer angle, x 100. It changes with steer angle because the linkage is nonlinear: plot it over the full range.

## 4. How much to use
- **Road cars:** commonly close to 100% (or somewhat less) at parking angles so tyres do not scrub; at highway speeds the slip angles are larger on the loaded outer tyre, so lower Ackermann or even parallel steer can be better for high-speed handling and tyre load use. Chosen by testing and tyre scrub considerations.
- **Racing:** often reduced or negative Ackermann because of high slip angles and load transfer; track-dependent.
Check the effect on steering torque at parking (scrub), on tyre wear (toe-out in turns), and on understeer feel at the limit.

## 5. Check and measure
Plot inner and outer wheel angles vs rack travel in a multibody model (Adams, CarSim); compare with ideal. Measure on a turntable or with toe-and-steer gauges. Verify steering ratio and turning circle requirement and bump steer interaction (tie-rod pivot heights).

## Verify
- [ ] Ideal and actual angle curves plotted over the full range.
- [ ] Percent Ackermann chosen with tyre wear and limit-handling in mind.
- [ ] Turning circle and clearance at lock confirmed.
- [ ] Bump steer re-checked after any tie-rod or arm change.
