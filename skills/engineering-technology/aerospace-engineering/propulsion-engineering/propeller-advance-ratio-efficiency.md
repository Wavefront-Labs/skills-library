---
id: engineering-technology.aerospace-engineering.propulsion-engineering.propeller-advance-ratio-efficiency
name: propeller-advance-ratio-efficiency
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [advance-ratio, propeller-efficiency, propeller-coefficients, helical-tip-mach, propellers]
level: practitioner
status: gated
description: "Use advance ratio, thrust and power coefficients to read propeller efficiency, and check helical tip Mach number at the design point."
sources:
  - "Anderson, Introduction to Flight"
  - "Hartman and Biermann, NACA propeller test reports"
  - "Raymer, Aircraft Design: A Conceptual Approach"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Advance ratio and propeller efficiency

**Goal:** read a propeller's performance from non-dimensional coefficients.

## Definitions (`n` in revolutions per second, `D` diameter)
- Advance ratio `J = V / (n D)`.
- Thrust coefficient `CT = T / (rho n^2 D^4)`.
- Power coefficient `CP = P / (rho n^3 D^5)`.
- Efficiency `eta = J * CT / CP`.
- Helical tip Mach `M_h = sqrt(V^2 + (pi n D)^2) / a`.

## Behaviour
- At `J = 0` (static) efficiency is zero by this definition although thrust is high; static thrust is compared with `CT0`.
- A fixed-pitch propeller gives its best efficiency at one `J`; take-off (low `J`) and cruise (high `J`) cannot both be optimal. A constant-speed propeller adjusts blade angle to hold rpm and efficiency across `J`.
- Efficiency peaks at a `J` where blade angle and the flow angle match, then falls sharply at high `J`.

## Procedure
1. From flight speed and chosen rpm get `J`.
2. Read `CT`, `CP`, `eta` from the propeller chart (for the blade angle) or from blade-element results (see propeller-blade-element-theory).
3. Compute thrust `T = CT rho n^2 D^4` and power absorbed.
4. Check `M_h`: efficiency drops as the tip approaches transonic conditions, and noise rises; many designs hold tip Mach below roughly 0.85 to 0.9 at take-off power (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Charts use specific definitions (rps vs rpm, `CP` vs `Cs`); always confirm.
- Spinner and nacelle blockage change installed thrust.

## Verify
- [ ] `eta` from the formula equals thrust power over shaft power computed independently (algebraically `J CT/CP = (T V)/P`, checked; the UIUC propeller database cites McCormick for its standard coefficient definitions).
