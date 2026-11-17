---
id: engineering-technology.chemical-engineering.reactor-design.external-mass-transfer-and-weisz-prater
name: external-mass-transfer-and-weisz-prater
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-catalytic-reactors, external-mass-transfer-and-weisz-prater, weisz-prater, mears-criterion, external-mass-transfer, film-diffusion, diffusion-limitation, catalyst-testing, kinetic-regime, damkohler]
level: advanced
status: verified
description: "Test for external and internal mass-transfer limitations in catalytic data using the Mears and Weisz-Prater criteria, and correct or redesign experiments accordingly."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External mass transfer and the Weisz-Prater criterion

**Goal:** make sure measured kinetics are intrinsic before they enter a reactor model.

## Criteria
- **Weisz-Prater (internal diffusion)**: Phi_WP = (-r_A,obs) rho_c R^2 / (D_e C_As), with rho_c the catalyst density, R the particle radius and C_As the surface concentration. If Phi_WP is much less than 1 (a value below about 0.3 is often used as a threshold in textbooks (gated: unconfirmed, source is paywalled or blocked)), internal diffusion limitation is negligible.
- **Mears (external)**: (-r'_A,obs) rho_b R n / (k_c C_Ab) < 0.15 means external diffusion is negligible (criterion from Mears, Ind. Eng. Chem. Process Des. Dev. 10(4):541-547, 1971, title Crossref-confirmed; the 0.15 value itself (gated: unconfirmed, source is paywalled or blocked)) (n is the reaction order, rho_b the bed density, k_c the mass transfer coefficient).
- **Mears for heat effects** has a similar form; check textbooks for the exact heat-transfer criterion.

## Experimental checks
1. Vary the total flow rate at constant space velocity (W/F): if conversion changes, external transfer limits.
2. Crush the catalyst to smaller sizes: if rate per mass increases, internal diffusion limits.
3. Compare the apparent activation energy at low versus high T: a drop signals diffusion limitation.

## Estimating k_c
From correlations (for a packed bed, j-factor or Sh = 2 + 0.6 Re^0.5 Sc^(1/3) (Ranz-Marshall form (gated: unconfirmed, source is paywalled or blocked)) for isolated spheres; for beds use the Wakao-Funazkri (Chem. Eng. Sci. 33:1375-1384, 1978, Crossref-confirmed) or Ranz-Marshall type correlations); document the source and range.

## Gotchas
- Criteria are order-of-magnitude screens; borderline cases need direct tests.
- Wall effects and channeling in small lab reactors look like mass-transfer limits.

## Verify
- [ ] Both criteria evaluated at the most severe condition (highest T and rate).
- [ ] Experimental flow and size checks agree with the criteria.
