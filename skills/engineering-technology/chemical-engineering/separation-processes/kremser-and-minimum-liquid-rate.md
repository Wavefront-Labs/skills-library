---
id: engineering-technology.chemical-engineering.separation-processes.kremser-and-minimum-liquid-rate
name: kremser-and-minimum-liquid-rate
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-absorption-and-stripping, kremser-and-minimum-liquid-rate, kremser-equation, absorption-factor, minimum-liquid-rate, absorber-design, gas-absorption, equilibrium-stages, operating-line, solvent-rate]
level: practitioner
status: verified
description: "Size absorbers with the Kremser equation and minimum liquid-to-gas ratio: absorption factor, stage count versus solvent rate and typical 1.2 to 2 times minimum."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kremser equation and minimum liquid rate

**Goal:** stage count and solvent flow for a dilute-gas absorber.

## Minimum liquid-to-gas ratio
For dilute solute with equilibrium y = m x and solvent entering at x_in: (L/V)_min = (y_in - y_out)/(y_in/m - x_in), assuming the exit liquid reaches equilibrium with the inlet gas (pinch at the rich end). Use mole ratios (Y, X) with solute-free flows when the solute is not dilute.

## Kremser equation (constant A, dilute)
Absorption factor A = L/(m V). The fraction of solute absorbed:
(y_in - y_out)/(y_in - m x_in) = (A^(N+1) - A)/(A^(N+1) - 1)  (A not equal to 1).
For A = 1: fraction = N/(N + 1).

## Procedure
1. Fix the recovery target.
2. Choose L/V at a multiple of the minimum, commonly 1.2 to 2.0 times (gated: unconfirmed, source is paywalled or blocked) (a higher ratio reduces stages but increases solvent regeneration cost); plot cost versus L/V.
3. Compute the stage count N from the Kremser equation, convert to packed height (see `engineering-technology.chemical-engineering.separation-processes.packed-absorber-height-ntu-htu`) or to trays with efficiency.
4. Check the temperature rise: absorption heat raises liquid temperature, increasing m; cooling or an interstage cooler may be needed.
5. Verify with a rigorous model.

## Worked check
Remove 95% of a dilute solute with m = 1.0 and clean solvent: with A = 1.4, (A^(N+1) - A)/(A^(N+1) - 1) = 0.95 gives A^(N+1) (1 - 0.95) = A - 0.95, so A^(N+1) = 0.45/0.05 = 9, N + 1 = ln 9/ln 1.4 = 6.53, N = 5.5 stages (recomputed: 5.53; check (9 - 1.4)/(9 - 1) = 0.95).

## Gotchas
- Kremser assumes constant A; real absorbers change L and V along the tower.
- Concentrated solute or chemical reaction (amine) needs rigorous methods.

## Verify
- [ ] Mass balance on the solute closes.
- [ ] Column temperature profile consistent with the m value used.
