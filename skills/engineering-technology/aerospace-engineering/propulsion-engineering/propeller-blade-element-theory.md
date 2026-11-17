---
id: engineering-technology.aerospace-engineering.propulsion-engineering.propeller-blade-element-theory
name: propeller-blade-element-theory
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, propellers, propeller-theory, blade-element, bemt, prandtl-tip-loss, qprop, xrotor]
level: advanced
status: docs-checked
description: "Compute propeller performance with blade element methods: momentum first cut, airfoil inputs, Reynolds and Mach effects, and use of QPROP or XROTOR for design and analysis."
sources:
  - "https://web.mit.edu/drela/Public/web/qprop/"
  - "https://web.mit.edu/drela/Public/web/qprop/qprop_doc.txt"
  - "https://web.mit.edu/drela/Public/web/xrotor/"
  - "https://www.grc.nasa.gov/www/k-12/airplane/propth.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Blade element methods for propellers

**Goal:** thrust, torque and efficiency of a given propeller geometry.

## Method
1. First cut with simple momentum theory: treat the propeller as a disk; thrust is the pressure jump times disk area, `F = 0.5 * rho * A * (Ve^2 - V0^2)` with exit velocity `Ve` and flight speed `V0`. This is an ideal number that ignores losses such as tip losses; a detailed propeller theory is needed for those.
2. Detailed analysis: divide the blade into radial stations, each with chord, blade angle `beta` and airfoil data. Blades are twisted because the tip moves faster than the hub.
3. For a measured propeller, a station blade angle follows from pitch `p` at radius `r`: `beta = arctan(p / (2 pi r))`.
4. Run a blade-element/vortex code (below) rather than hand-coding the induced-velocity iteration.

## Tools
- QPROP (Mark Drela, MIT) predicts the performance of propeller-motor combinations, with a blade-element/vortex aerodynamic model that stays accurate to the static-thrust case. Its companion QMIL generates minimum-induced-loss propeller geometries and windmill geometries.
- XROTOR is an interactive program for the design and analysis of ducted and free-tip propellers and windmills; the QPROP documentation can serve as its basic documentation.
- QPROP motor type 1 is a brushed DC model from `Kv`, `R` and zero-load current `Io`; other motor models go in a user subroutine. Non-electric power sources can use the "voltage" as throttle or fuel flow.
- QPROP needs a detailed prop file (blade count, radius, `CL(alpha)` with `CLmax` and `CLmin` limits, a quadratic `CD(CL)` with a power-law Reynolds scaling, and chord and `beta` by radius); diameter and pitch alone are not enough.
- Output includes local `Cl`, `Cd`, Reynolds and Mach numbers by radius, and advance ratio `V/(w R)`.

## Practice
- The lift curve is modified by the local compressibility factor `sqrt(1 - M^2)`, and Reynolds number changes `Cd`: use airfoil data from XFOIL or similar at the right Reynolds number.
- Measure the real propeller; crude geometry input gives crude output.
- Compare with test data for the same propeller.

## Checked
2026-11-01. Confirmed in the QPROP user guide and web page, the XROTOR page and the NASA Glenn propeller momentum theory page: the items listed above. Removed as unconfirmed: the named blade-element force equations, the Adkins-Liebeck and Prandtl tip-loss attribution, Reynolds and tip Mach number ranges, the `J = 0` convergence remark, and the efficiency-curve checklist.
Method: documentation only; no commands were run.
