---
id: engineering-technology.chemical-engineering.heat-exchanger-design.fluid-allocation-and-fouling-factors
name: fluid-allocation-and-fouling-factors
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-shell-and-tube-selection, fluid-allocation-and-fouling-factors, fluid-allocation, tube-side, shell-side, fouling-factor, fouling-resistance, tema-fouling, cleanability]
level: practitioner
status: draft
description: "Allocate fluids to tube or shell side and select fouling resistances, using corrosion, pressure, fouling, viscosity and cleanability guidance."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fluid allocation and fouling factors

**Goal:** a sensible tube-side vs shell-side assignment and defensible fouling allowances.

## Allocation guidance
Put on the **tube side**: the corrosive fluid (cheaper than alloy shells), the high-pressure fluid (small diameter tubes bear pressure better), the toxic or hazardous fluid (fewer leak paths at the shell), the fouling fluid when the tubes can be cleaned mechanically or chemically, and the cooling water.
Put on the **shell side**: the viscous fluid (baffled crossflow promotes turbulence at lower Re), the lower-flow stream, the condensing vapour (usually), and fluids that need low pressure drop; a clean fluid if the shell cannot be cleaned.
When guidance conflicts, evaluate both and choose from cost and the rating.

## Fouling resistances
1. Use client standards first; otherwise the tabulated values in the TEMA standards or handbooks. As an order of magnitude: treated cooling water about 0.00018 to 0.00035 m2 K/W; clean light hydrocarbon liquids about 0.00009 to 0.00018; heavy fouling services much higher. These numbers vary with source, temperature and velocity; confirm.
2. Note that the fouling factor is the design allowance for the interval between cleanings, not a physical constant.
3. Keep velocities high enough to limit deposition, wall temperatures low enough to avoid scaling or coking.
4. Consider an installed spare or a bypass for heavily fouling duties.

## Excess area
Report percent over-surface: (A_with_fouling - A_clean)/A_clean; very large values (above about 30 to 50%) suggest fouling allowances dominate and that operating practice should address fouling instead.

## Gotchas
- Over-specified fouling factors cause overdesign, which lowers velocity and increases fouling in practice.
- Fouling in boiling and condensing duties acts differently.

## Verify
- [ ] Allocation logic documented per stream.
- [ ] Fouling sources cited; clean and dirty cases both checked for pressure drop.
