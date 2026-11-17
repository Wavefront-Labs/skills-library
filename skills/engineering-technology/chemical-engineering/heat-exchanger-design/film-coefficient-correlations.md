---
id: engineering-technology.chemical-engineering.heat-exchanger-design.film-coefficient-correlations
name: film-coefficient-correlations
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-thermal-fundamentals, film-coefficient-correlations, dittus-boelter, sieder-tate, gnielinski, film-coefficient, nusselt-number, heat-transfer-correlation, laminar-flow, shell-side-coefficient, kern-method]
level: advanced
status: draft
description: "Select tube-side and shell-side film coefficient correlations (Dittus-Boelter, Sieder-Tate, Gnielinski, Kern, laminar) with validity ranges and viscosity corrections."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tube-side and shell-side film coefficient correlations

**Goal:** a film coefficient with the right correlation for the flow regime.

## Tube side
- **Turbulent, Re above about 10,000** (Dittus-Boelter): Nu = 0.023 Re^0.8 Pr^n, n = 0.4 heating, 0.3 cooling; for large property variation use Sieder-Tate: Nu = 0.027 Re^0.8 Pr^(1/3) (mu/mu_w)^0.14.
- **Transition** (2,300 to 10,000): avoid in design if possible; Gnielinski is commonly used: Nu = (f/8)(Re - 1000) Pr/[1 + 12.7 sqrt(f/8)(Pr^(2/3) - 1)], f the Darcy friction factor.
- **Laminar** (developing flow, Sieder-Tate): Nu = 1.86 (Re Pr d/L)^(1/3) (mu/mu_w)^0.14; fully developed laminar flow with constant wall temperature gives Nu = 3.66.
- Nu = h d/k.

## Shell side (Kern, simple estimate)
Nu = 0.36 Re_s^0.55 Pr^(1/3) (mu/mu_w)^0.14 using the equivalent diameter d_e of the tube layout and the crossflow mass velocity; accurate to roughly plus or minus 25 to 30%. For final design use Bell-Delaware (see `engineering-technology.chemical-engineering.heat-exchanger-design.bell-delaware-shell-side-method`).

## Procedure
1. Compute Re, Pr at bulk temperature (and at wall temperature for the viscosity ratio).
2. Select the correlation by the regime and geometry.
3. Evaluate h; also compute the pressure drop for the same condition (the two compete).
4. For viscous liquids check laminar and heat-up zones.

## Gotchas
- Fouled walls shift the wall temperature; the viscosity correction needs an iteration.
- Low velocity in tubes encourages fouling; tube-side velocity should typically be above about 1 m/s for liquids (water often 1 to 2 m/s), but below erosion limits.
- Correlations assume smooth tubes unless stated.

## Verify
- [ ] Compare with a rating program or an independent correlation within 20%.
- [ ] Velocity and Re within the validity range.
