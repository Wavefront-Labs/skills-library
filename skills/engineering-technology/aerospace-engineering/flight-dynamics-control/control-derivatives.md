---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.control-derivatives
name: control-derivatives
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [control-derivatives, elevator-effectiveness, aileron-effectiveness, rudder-effectiveness, control-power, adverse-yaw]
level: practitioner
status: draft
description: "Estimate control derivatives for elevator, aileron and rudder using flap effectiveness, and check control power and adverse yaw against requirements."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Roskam, Airplane Flight Dynamics and Automatic Flight Controls"
  - "USAF DATCOM"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Control derivatives

**Goal:** moment and force per unit control deflection.

## Elevator, rudder
- `CL_de = eta * (S_t/S) * CL_alpha_t * tau_e`.
- `Cm_de = -eta * V_H * CL_alpha_t * tau_e` (negative for a conventional tail).
- `Cn_dr = -eta_v * V_V * CL_alpha_v * tau_r`, `Cy_dr = eta_v * (S_v/S) * CL_alpha_v * tau_r` (signs per convention).
- `tau` is the control-surface effectiveness factor, read from charts versus flap-to-chord ratio (about 0.5 to 0.7 for a 30 percent chord surface; confirm with a chart), and reduced by gaps, aerodynamic balance, and boundary layer.

## Aileron
- `Cl_da` from strip theory integrating the surface's span station contribution: `Cl_da = (2 CL_alpha_w tau c_root / (S b)) * integral(y * c(y)/c_root dy)` form, with taper correction.
- Adverse yaw `Cn_da`: opposite of the roll direction because of induced drag asymmetry; ailerons with differential travel, Frise hinges or rudder interconnects reduce it.

## Requirements check
1. Roll rate after full aileron: time to bank 30 degrees or roll rate per the requirement relevant to your category.
2. Pitch control: rotation at the lowest speed with forward CG, landing flare.
3. Directional: crosswind landing and minimum control speed with one engine out.
4. Nonlinear: control saturation and hinge-moment limits at high dynamic pressure.

## Gotchas
- Effectiveness drops at high Mach and with flow separation; derivatives are not constant.
- Hinge moments determine actuator size and stick force.

## Verify
- [ ] A check against tunnel or CFD data at one deflection reproduces the derivative within the stated tolerance.
