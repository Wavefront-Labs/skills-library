---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.bushing-rate-selection
name: bushing-rate-selection
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [bushing-rates, bushing, rubber-bush, radial-stiffness, axial-stiffness, hydrobush, dynamic-stiffness]
level: practitioner
status: gated
description: "Select suspension bushing rates in radial, axial and conical directions from compliance and NVH targets, with static versus dynamic stiffness and nonlinearity."
sources:
  - "Reimpell, Stoll and Betzler, The Automotive Chassis"
  - "Harrison, Vehicle Refinement"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Bushing rate selection

1. Start from the K&C and NVH targets: compliance steer, lateral compliance, longitudinal compliance for ride comfort (a soft longitudinal rate absorbs road impacts) versus stiff laterally for precision.
2. Axes: radial (perpendicular to the sleeve), axial, torsional and conical; design the shape (voids, inner sleeve) to give different stiffnesses in each direction.
3. Rate nonlinearity: progressive with load; specify rate at defined preload and amplitude; hysteresis and damping of the rubber (loss angle) matter for noise.
4. Static vs dynamic: dynamic stiffness at 100-200 Hz is higher than static (a factor 1.2 to 2 depending on compound (gated: unconfirmed, source is paywalled or blocked)); specify both.
5. Fluid-filled (hydro) bushes give damping at low frequency (e.g. 10-15 Hz wheel-hop/brake shudder (gated: unconfirmed, source is paywalled or blocked)) while staying soft at higher frequencies.
6. Geometry effect: bush axis angle changes compliance steer; bush location in the lower arm affects toe change.
7. Process: set the targets, simulate in Adams with bushes, tune on a K&C rig and in the car; durability and temperature drift (rubber stiffens in cold).

**Gotchas:** rate measured at one temperature and amplitude only.

## Verify
- [ ] Bush supplier curves at specified amplitude/frequency/temperature meet the spec.
- [ ] K&C compliance results meet the target after bush selection.
