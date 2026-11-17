---
id: engineering-technology.chemical-engineering.separation-processes.bubble-and-dew-point-calculations
name: bubble-and-dew-point-calculations
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-vle-and-flash, bubble-and-dew-point-calculations, bubble-point, dew-point, antoine-equation, raoults-law, modified-raoult, vle-iteration, saturation-temperature, bubble-pressure]
level: practitioner
status: verified
description: "Compute bubble and dew points for ideal and non-ideal mixtures with Antoine vapour pressures and activity coefficients, using convergent iteration schemes."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bubble and dew point calculations

**Goal:** the temperature (at fixed P) or pressure (at fixed T) where a liquid starts to boil or vapour starts to condense.

## Ideal mixtures
- **Bubble point**: sum x_i K_i = 1, with K_i = P_i^sat(T)/P.
- **Dew point**: sum y_i / K_i = 1.
Antoine form: log10 P_sat = A - B/(C + T) with consistent units (check the constants' units: mmHg and Celsius for many tables; bar and Kelvin for others).

## Algorithm for bubble T at fixed P
1. Guess T (mole-fraction-weighted boiling points).
2. Compute K_i; evaluate g(T) = sum x_i K_i - 1.
3. Update T by Newton or by the common trick: T_new from the pure-component reference, using the equation P = sum x_i P_i^sat(T) and a reference component j: P_j^sat(T) = P / sum(x_i P_i^sat / P_j^sat), then invert Antoine.
4. Iterate until |g| < 1e-6.
Dew point is analogous with the sum y_i/K_i = 1.

## Non-ideal liquid (modified Raoult)
K_i = gamma_i(T, x) P_i^sat / P (low pressure, ideal vapour). Inner loop updates gamma_i with the current T and x (for bubble point x is known so gamma needs only T); for dew point x is unknown and an extra loop is needed.

## High pressure
Use an EoS: K_i = phi_i^L/phi_i^V, iterate on K (successive substitution with acceleration).

## Gotchas
- Units in Antoine constants are the most frequent source of error.
- Dew point of a mixture with noncondensables or water needs care: the water dew point of humid gas is the partial-pressure condition, not a mixture bubble point.

## Verify
- [ ] Pure-component limits give the normal boiling point at 1 atm.
- [ ] Bubble point T < dew point T at the same composition and pressure.
