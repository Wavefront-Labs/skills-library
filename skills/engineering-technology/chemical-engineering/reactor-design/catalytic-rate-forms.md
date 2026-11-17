---
id: engineering-technology.chemical-engineering.reactor-design.catalytic-rate-forms
name: catalytic-rate-forms
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-kinetics-and-rate-laws, catalytic-rate-forms, langmuir-hinshelwood, eley-rideal, mars-van-krevelen, rate-limiting-step, adsorption-constant, heterogeneous-catalysis, catalytic-kinetics, lhhw]
level: advanced
status: draft
description: "Write catalytic rate forms (Langmuir-Hinshelwood, Eley-Rideal, Mars-van Krevelen) from a mechanism with a rate-limiting step, and fit adsorption constants sensibly."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalytic rate forms and adsorption models

**Goal:** a mechanism-based rate expression with the right form and physically sensible parameters.

## Procedure
1. Propose a mechanism: adsorption of reactants, surface reaction, desorption of products (single or dual site).
2. Choose the **rate-limiting step** and write the rate for it; other steps at equilibrium give surface coverage expressions.
3. Eliminate coverages with the site balance (sum of coverages = 1).

## Common forms
- **Single-site surface reaction controlling** (A <-> B): -r_A = k K_A P_A / (1 + K_A P_A + K_B P_B).
- **Adsorption of A controlling**: rate = k (P_A - P_B/K) / (1 + ...) with a different denominator.
- **Dual-site bimolecular (Langmuir-Hinshelwood)** A + B: -r_A = k K_A K_B P_A P_B / (1 + K_A P_A + K_B P_B)^2.
- **Eley-Rideal** (gas B reacts with adsorbed A): -r_A = k K_A P_A P_B / (1 + K_A P_A + ...).
- **Dissociative adsorption**: square-root terms such as (K P)^0.5.
- **Mars-van Krevelen** (redox oxidation catalysts): two-step rate with catalyst oxidation and reduction in series; the rate limits at low or high oxygen pressure.

## Fitting
1. Collect data over a range of partial pressures and temperatures, including product addition.
2. Fit candidate models with nonlinear regression; reject any with negative or temperature-increasing adsorption constants. Adsorption is exothermic, so K should decrease with T.
3. Discriminate by residuals and parameter significance, not only R-squared.

## Gotchas
- Too many parameters for the data range lead to unidentifiable constants; reduce.
- Rate per catalyst mass, per surface area or per volume: keep it consistent and record the basis.
- Equilibrium constants for reversible reactions must obey thermodynamics.

## Verify
- [ ] Reverse reaction consistent with the thermodynamic K at test conditions.
- [ ] All fitted adsorption enthalpies negative and of reasonable size.
