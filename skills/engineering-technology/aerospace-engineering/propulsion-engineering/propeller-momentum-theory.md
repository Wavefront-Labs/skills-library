---
id: engineering-technology.aerospace-engineering.propulsion-engineering.propeller-momentum-theory
name: propeller-momentum-theory
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, propellers, propeller-theory, momentum-theory, actuator-disc, ideal-efficiency, figure-of-merit, static-thrust]
level: practitioner
status: verified
description: "Apply actuator-disc momentum theory to propellers and rotors: ideal efficiency, static thrust and power, and figure of merit."
sources:
  - "Leishman, Principles of Helicopter Aerodynamics"
  - "McCormick, Aerodynamics Aeronautics and Flight Mechanics"
  - "Phillips, Mechanics of Flight"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Propeller momentum theory

**Goal:** an upper bound and a quick sizing relation.

## Axial flight
- Thrust `T = m_dot (V_e - V) = rho A (V + v_i) 2 v_i` with `v_i` the induced velocity at the disc.
- Ideal power `P = T (V + v_i)`; ideal efficiency `eta_i = V/(V + v_i) = 2/(1 + sqrt(1 + C_T))` where `C_T = T/(0.5 rho V^2 A)`.
- Efficiency falls as thrust loading rises: larger discs (diameter) at the same thrust improve efficiency.

## Static (hover) case
- `v_i = sqrt(T/(2 rho A))`; ideal power `P_i = T^(3/2)/sqrt(2 rho A)`.
- Figure of merit `FM = P_ideal/P_actual`, typically 0.6-0.8 for good rotors and propellers at static conditions (gated: unconfirmed, source is paywalled or blocked).

## Use
1. Pick disc area from tip-speed limits and ground clearance.
2. Compute `eta_i` for cruise `C_T`; actual efficiency is lower by profile and swirl losses (real propellers 0.8-0.87 at best cruise points (gated: unconfirmed, source is paywalled or blocked)).
3. Estimate power needed for static thrust at takeoff; compare with engine power.

## Gotchas
- Momentum theory ignores swirl, finite blade number, tip losses and profile drag.
- Static thrust on a fixed-pitch propeller is lower than ideal; use blade element methods or test data.

## Verify
- [ ] Numerical check: T 1000 N, V 50 m/s, rho 1.225, A 1 m^2 gives `V/(V+v_i)` = 0.875 from the thrust equation and from the `C_T` closed form. As `C_T -> 0`, `eta_i -> 1`; at static conditions the formulas reduce to the hover relations.
