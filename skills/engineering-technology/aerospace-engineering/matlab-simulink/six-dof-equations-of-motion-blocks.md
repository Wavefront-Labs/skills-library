---
id: engineering-technology.aerospace-engineering.matlab-simulink.six-dof-equations-of-motion-blocks
name: six-dof-equations-of-motion-blocks
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, aerospace-blockset, eom-6dof, six-dof, equations-of-motion, quaternion, body-axes, flat-earth]
level: practitioner
status: docs-checked
description: "Choose among the Aerospace Blockset 6DOF blocks (Euler angles, quaternion, wind axes, ECEF) and connect forces, moments and mass properties without frame mistakes."
sources:
  - "https://www.mathworks.com/help/aeroblks/6dofeulerangles.html"
  - "https://www.mathworks.com/help/aeroblks/6dofwindquaternion.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# 6DOF equations-of-motion blocks

**Goal:** a correct rigid-body core for an aircraft or vehicle model.

## Choosing the block
- **6DOF (Euler Angles):** the Euler-rate inversion contains tan(theta) and 1/cos(theta), so it is undefined at pitch of +/-90 degrees.
- **6DOF (Quaternion):** quaternion attitude; use for aerobatic or high-pitch cases.
- **6DOF Wind (Quaternion / Wind Angles):** states are wind-axis quantities (airspeed, angle of attack, sideslip, wind orientation); handy for aerodynamic work.
- **6DOF ECEF (Quaternion):** the Earth-centred variant.
- **Simple Variable Mass** and **Custom Variable Mass** 6DOF variants handle mass and inertia change (fuel burn); the fixed-mass block assumes constant mass and inertia.

## Inputs
Inputs `Fxyz` (force at the centre of mass, body frame) and `Mxyz` (moment about the centre of mass, body frame). Parameters: mass type (Fixed, Simple Variable or Custom Variable), mass, inertia, initial states. The Units parameter selects Metric (MKS), English (ft/s) or English (kts); check it matches your data.

## Procedure
1. Build aerodynamic forces and moments from coefficients in the body or stability axes and transform to body axes.
2. Add thrust (with its offset moment) and gravity. The Euler Angles page does not say whether the block includes gravity, so confirm in your release that it is applied exactly once.
3. Add atmosphere and wind.
4. Initialise by trim (see trim skill) not by guessing states.

## Gotchas
- Applying gravity twice or in the wrong frame.
- Using Euler angle block with near-vertical flight.

## Verify
- [ ] Zero-force test: with only gravity, the vehicle falls with the local gravitational acceleration on the right axis.
- [ ] Torque-free rotation conserves angular momentum.

## Checked
2026-11-01. Confirmed on the MathWorks 6DOF (Euler Angles) and 6DOF Wind (Quaternion) pages: Fxyz and Mxyz body-frame inputs, Units options, mass types, constant-mass assumption, the variant list, tan/cos terms in the Euler rates, wind-axis states. Removed: body-axis sign convention, the 9.81 figure, the textbook source and the claim that the block can optionally include gravity (the page does not say).
Method: documentation only; no commands were run.
