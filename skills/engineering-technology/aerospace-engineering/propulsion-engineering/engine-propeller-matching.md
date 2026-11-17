---
id: engineering-technology.aerospace-engineering.propulsion-engineering.engine-propeller-matching
name: engine-propeller-matching
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propeller-matching, engine-propeller-matching, constant-speed-propeller, fixed-pitch-propeller, power-absorption, propellers]
level: practitioner
status: draft
description: "Match engine power and torque to propeller power absorption for fixed-pitch and constant-speed propellers, finding operating rpm across the flight envelope."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Anderson, Introduction to Flight"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Engine-propeller matching

**Goal:** the operating rpm, power and thrust at each flight condition.

## Fixed pitch
1. Propeller power absorbed `P_prop = CP(J) rho n^3 D^5`.
2. Engine power available at that rpm and throttle `P_eng(n)`.
3. The operating point is the rpm where `P_prop = P_eng` for each speed; as speed rises `J` rises, `CP` falls, so rpm increases (static and climb conditions run at lower rpm than level flight).
4. A propeller pitched for climb over-revs in a dive; one pitched for cruise gives poor take-off thrust.

## Constant speed
1. The governor holds rpm by adjusting blade angle `beta` as power and speed change; operate in a range between low-pitch and high-pitch stops.
2. Choose the rpm and manifold pressure that give the required power; use propeller maps at the achieved `beta`.
3. Check that the blade can reach the low-pitch stop at take-off and the high-pitch stop at cruise.

## Practice
- Include gearbox ratio and its efficiency on geared engines.
- Check torque and power at hot and high conditions: engine power falls with density while the propeller sees the same non-dimensional behaviour.
- For turboprops the free turbine or reduction gearbox sets the propeller rpm, with the propeller governor and power lever scheduling.

## Gotchas
- Avoid operating in rpm ranges prohibited by the vibration (critical rpm) placard.
- Propeller diameter is limited by tip Mach, ground clearance and noise.

## Verify
- [ ] The matched operating points lie on both the engine and the propeller power curves.
