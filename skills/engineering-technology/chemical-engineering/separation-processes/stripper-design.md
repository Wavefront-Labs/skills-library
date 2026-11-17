---
id: engineering-technology.chemical-engineering.separation-processes.stripper-design
name: stripper-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-absorption-and-stripping, stripper-design, stripper, stripping-factor, steam-stripping, solvent-regeneration, desorption, gas-stripping, stripping-column, kremser-stripping]
level: practitioner
status: draft
description: "Design stripping columns (steam or inert gas): stripping factor, minimum stripping rate, solvent regeneration duty, temperature and pressure choice, and stage count."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stripper design

**Goal:** remove a volatile solute from a liquid with a stripping gas or steam.

## Equations (dilute, equilibrium y = m x)
- Stripping factor S = m V/L (the inverse of the absorption factor).
- Fraction removed: (x_in - x_out)/(x_in - y_in/m) = (S^(N+1) - S)/(S^(N+1) - 1).
- **Minimum stripping gas rate**: (V/L)_min = (x_in - x_out)/(m x_in - y_in) for clean gas (pinch at the rich liquid end).
- Typical design at 1.2 to 2 times the minimum.

## Choices
1. **Stripping agent**: steam (condenses, easy separation, adds heat, used for organics and also amine regeneration), air (cheap, but causes emission problems and oxidation), nitrogen or flue gas.
2. **Temperature**: higher temperature raises m (better stripping) at the cost of energy; pressure low helps.
3. **Regeneration loop**: for amine, the stripper reboiler duty is the largest operating cost; the lean loading target sets it.
4. **Steam stripping of wastewater**: check regulatory limits and downstream treatment for the stripped overhead.

## Procedure
1. Specify inlet and outlet liquid concentration.
2. Compute V/L_min and choose the multiple.
3. Compute N from Kremser or a rigorous model.
4. Size the column (trays or packing) as for absorbers.
5. Evaluate energy: sensible heat plus heat of desorption plus steam latent heat.

## Gotchas
- Fouling (scale, polymer) in reboilers of regenerators.
- Corrosion in amine systems at high loading and temperature.

## Verify
- [ ] Solute mass balance (liquid loss equals gas gain).
- [ ] Energy balance consistent with the simulator duty.
