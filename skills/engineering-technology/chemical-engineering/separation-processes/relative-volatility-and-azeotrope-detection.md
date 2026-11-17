---
id: engineering-technology.chemical-engineering.separation-processes.relative-volatility-and-azeotrope-detection
name: relative-volatility-and-azeotrope-detection
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-vle-and-flash, relative-volatility-and-azeotrope-detection, relative-volatility, azeotrope, minimum-boiling-azeotrope, maximum-boiling-azeotrope, xy-diagram, infinite-dilution, separation-feasibility, alpha]
level: practitioner
status: verified
description: "Use relative volatility curves and activity coefficients to detect azeotropes and pinch zones, estimate whether simple distillation is feasible, and plan the follow-up."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relative volatility and azeotrope detection

**Goal:** determine whether the key separation is feasible by ordinary distillation and how hard it is.

## Relative volatility
alpha_ij = K_i/K_j = (y_i/x_i)/(y_j/x_j). For ideal mixtures alpha = P_i^sat/P_j^sat, which varies with T but usually mildly. Separation difficulty: alpha above about 1.5 is easy; between 1.1 and 1.3 requires many stages; below about 1.1 usually needs another technique or a very tall column (rule-of-thumb bands (gated: unconfirmed, source is paywalled or blocked)).

## Azeotropes
- At an azeotrope x = y and alpha = 1. For modified Raoult: gamma_1 P_1^sat = gamma_2 P_2^sat at the azeotropic composition.
- **Minimum-boiling** (positive deviation, gamma > 1): the azeotrope boils below both pure components (ethanol-water, about 89 mol% ethanol at 1 atm (gated: unconfirmed, source is paywalled or blocked)); the azeotrope leaves at the top.
- **Maximum-boiling** (negative deviation): the azeotrope boils above both (for example HCl-water); the azeotrope leaves at the bottom.
- Screening from infinite-dilution activity coefficients: alpha_12 at x_1 -> 0 is gamma_1^inf P_1^sat/P_2^sat and at x_1 -> 1 is P_1^sat/(gamma_2^inf P_2^sat). If one end is above 1 and the other below 1, alpha crosses 1 and a binary azeotrope exists; if an end value is close to 1, expect a pinch there. (Derived from alpha = gamma_1 P_1^sat/(gamma_2 P_2^sat) with modified Raoult.)

## Procedure
1. Compute alpha across composition at column pressure using the validated model.
2. Plot xy and Txy; look for crossing of the diagonal.
3. Check pressure dependence: calculate azeotrope composition at two pressures (see `engineering-technology.chemical-engineering.separation-processes.pressure-swing-distillation`).
4. Estimate minimum stages by the Fenske equation using the average alpha (valid away from an azeotrope).
5. If alpha tends to 1 near one end (pinch), expect very large stage numbers at high purity.

## Gotchas
- Data scatter near an azeotrope can hide whether alpha crosses 1; check with direct data.
- Azeotropes in multicomponent mixtures need residue curve maps.

## Verify
- [ ] xy diagram checked against literature for the key binary.
- [ ] Azeotrope presence or absence recorded with the data source.
