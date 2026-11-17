---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.thruster-layout-design
name: thruster-layout-design
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [thruster-layout, reaction-control, thruster-placement, plume-impingement, six-dof-control, propulsion-subsystem]
level: practitioner
status: draft
description: "Lay out reaction control and orbit thrusters for six-degree-of-freedom control with redundancy, avoiding plume impingement and centre-of-mass coupling."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Fortescue et al., Spacecraft Systems Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Thruster layout

**Goal:** thruster positions and directions that give required forces and torques with failure tolerance.

## Principles
- Three-axis torque needs at least four thrusters for attitude control with pairs; typical designs use 8 to 12 for full redundancy and 24 for redundant translation and rotation.
- Pairs fired together give a pure torque with no net force; place pairs symmetrically about the centre of mass.
- Orbit-control thrusters fire through the centre of mass; any offset adds a disturbance torque to be countered by attitude control or by gimbal.
- Centre of mass moves as propellant is used; check the torque coupling at beginning and end of life.

## Procedure
1. List the manoeuvres: orbit raising, station keeping, desaturation, attitude slews.
2. Compute required force and torque and the minimum impulse bit from pointing accuracy.
3. Position the thrusters on the spacecraft body, considering the field of view of sensors, solar arrays and antennas.
4. Evaluate plume impingement (force, torque, heating, contamination) with a plume model (see electric-thruster-plume-interaction).
5. Assign firing logic (thruster selection tables) for each axis, including one- and two-failure cases.
6. Validate by simulation, including thruster misalignment and thrust variation.

## Gotchas
- Cant angles reduce plume impingement on arrays but give cosine loss.
- Thruster misalignment of a fraction of a degree produces significant disturbance torque for long burns.
- Fuel line routing and thermal constraints for catalyst beds.

## Verify
- [ ] The control allocation shows every commanded axis achievable after the first thruster failure.
