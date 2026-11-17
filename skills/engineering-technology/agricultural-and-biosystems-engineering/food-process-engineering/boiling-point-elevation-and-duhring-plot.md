---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.boiling-point-elevation-and-duhring-plot
name: boiling-point-elevation-and-duhring-plot
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, boiling-point-elevation, duhring-plot, bpe, evaporator-temperature-drop, sugar-solution, hydrostatic-head]
level: practitioner
status: verified
description: "Account for boiling point elevation in evaporators: Duhring's rule, solute effect, hydrostatic head, and the loss of useful temperature difference."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Boiling point elevation and Duhring plot

**Goal:** know the true boiling temperature of a concentrated solution so the useful temperature difference and area are right.

## BPE
A dissolved solute lowers vapour pressure, so the solution boils above the pure water temperature at the same pressure. The boiling point elevation (BPE) grows with concentration, particularly at high solids. In sugar, juice and milk concentrates it can be a few kelvin at high concentration (ideal-solution estimate for 70 wt% sucrose: 0.512 x 6.8 mol/kg = 3.5 K), and the actual figure for your product should come from data or measurement.

## Duhring's rule
Plotting the boiling temperature of the solution against that of pure water at the same pressure gives nearly straight lines for each concentration. Duhring charts for common solutions (sodium chloride, sucrose and others) are published in food engineering and chemical engineering references; read the boiling temperature at the operating pressure.

## Other temperature losses
- Hydrostatic head: in tubes submerged in liquid, the pressure at the bottom is higher than at the surface, which raises the local boiling point; forced-circulation and rising-film evaporators lose more than falling-film.
- Pressure drop in vapour lines between effects.

## Use
Useful dT = (steam temperature) - (solution boiling temperature, including BPE and head effects). In multi-effect, subtract from the overall dT (`multiple-effect-evaporator-steam-economy`).

## Verify
- [ ] BPE source and concentration recorded.
- [ ] Observed boiling temperature at the outlet compared to the prediction.
- Unconfirmed: BPE values for your product.
