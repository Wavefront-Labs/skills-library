---
id: engineering-technology.chemical-engineering.separation-processes.rachford-rice-flash-calculation
name: rachford-rice-flash-calculation
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-vle-and-flash, rachford-rice-flash-calculation, rachford-rice, flash-calculation, isothermal-flash, vapor-fraction, k-values, vle, phase-split, two-phase-flash]
level: practitioner
status: verified
description: "Solve isothermal flash with the Rachford-Rice equation: single-phase test, bracketed root finding, phase compositions and an ideal-K worked check."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rachford-Rice flash calculation

**Goal:** vapour fraction and phase compositions for a feed at given T and P.

## Equations
With feed mole fractions z_i, K-values K_i = y_i/x_i and vapour fraction psi = V/F:
f(psi) = sum z_i (K_i - 1) / (1 + psi (K_i - 1)) = 0
then x_i = z_i / (1 + psi (K_i - 1)), y_i = K_i x_i.

## Procedure
1. Compute K_i at T and P (ideal: K = P_sat(T)/P; otherwise from the chosen model, iterating if K depends on composition).
2. **Single-phase test**: f(0) = sum z_i K_i - 1. If f(0) <= 0 the feed is all liquid (at or below the bubble point). f(1) = 1 - sum z_i/K_i. If f(1) >= 0 it is all vapour (at or above the dew point).
3. Otherwise a root exists between psi_min = 1/(1 - K_max) and psi_max = 1/(1 - K_min), and the physical root is in [0, 1]. f is monotonically decreasing, so bisection or Newton with bracketing is safe.
4. Compute x and y; check sum x = sum y = 1.
5. For non-ideal K, update K from x, y and repeat until K converges.

## Worked check
Equimolar benzene/toluene (z = 0.5 each) at a temperature where K_B = 1.5 and K_T = 0.6: f(psi) = 0.5(0.5)/(1 + 0.5 psi) + 0.5(-0.4)/(1 - 0.4 psi) = 0, so 0.25(1 - 0.4 psi) = 0.2(1 + 0.5 psi), i.e. 0.25 - 0.1 psi = 0.2 + 0.1 psi, giving psi = 0.25 (recomputed numerically, root 0.2500). Then x_B = 0.5/(1 + 0.125) = 0.444, y_B = 0.667, x_T = 0.5/(1 - 0.1) = 0.556, y_T = 0.333.

## Gotchas
- Newton from psi = 0.5 can step outside the bracket; clamp.
- Near-critical or trace components make K sensitive; use an EoS.
- Three-phase systems need a separate algorithm.

## Verify
- [ ] Mass balance: F z_i = V y_i + L x_i for each i.
- [ ] Results agree with a simulator flash block.
