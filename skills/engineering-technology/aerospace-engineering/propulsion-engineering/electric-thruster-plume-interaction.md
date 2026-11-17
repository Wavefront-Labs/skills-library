---
id: engineering-technology.aerospace-engineering.propulsion-engineering.electric-thruster-plume-interaction
name: electric-thruster-plume-interaction
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [plume-interaction, plume-spacecraft-interaction, charge-exchange, contamination, electric-propulsion, spacecraft-charging]
level: practitioner
status: draft
description: "Assess thruster plume interactions with spacecraft: charge-exchange ion backflow, contamination, sputtering, momentum and torque from impingement, and placement mitigations."
sources:
  - "Goebel and Katz, Fundamentals of Electric Propulsion"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Plume spacecraft interaction

**Goal:** find and bound unwanted effects of thruster exhaust on the spacecraft.

## Electric thrusters
- **Beam divergence**: ions leave in a cone; any hardware in the cone (solar arrays, antennas, booms) is exposed to erosion and momentum transfer.
- **Charge-exchange ions**: fast beam ions swap charge with slow neutrals, producing slow ions that follow the electric field around and can backstream to the spacecraft, causing sputter erosion and deposition on surfaces.
- **Contamination**: eroded grid or cathode material and thruster-body sputter deposit on optics, solar cells and thermal-control surfaces.
- **Charging and EMI**: plume potential and neutraliser coupling affect spacecraft potential; radio-frequency noise can couple into communication links.

## Chemical thrusters
- Plume impingement on arrays and sensors gives force and torque, heat load, and contamination from unburnt droplets and particulates; reaction-control thruster placement avoids pointing into appendages.

## Procedure
1. Get thruster plume data (beam profile, divergence half-angle, ion energy) from the thruster maker.
2. Draw the plume cone on the spacecraft model including gimbal range and attitude.
3. Run a plume model (particle-in-cell or direct simulation Monte Carlo for chemical plumes) or use the supplier's empirical models.
4. Evaluate force, torque, erosion rate per year, deposition, and heating.
5. Apply mitigations: canting, repositioning, shields, thruster firing restrictions, array rotation.

## Gotchas
- Backflow is sensitive to background pressure, so ground-test data must be interpreted with chamber effects in mind.
- Thruster alignment error changes the torque seen by the attitude control.

## Verify
- [ ] No sensitive surface lies in the high-flux plume region at any gimbal and attitude combination in the operating plan.
