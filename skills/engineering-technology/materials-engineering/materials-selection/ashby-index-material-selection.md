---
id: engineering-technology.materials-engineering.materials-selection.ashby-index-material-selection
name: ashby-index-material-selection
category: engineering-technology
field: materials-engineering
product: materials-selection
tags: [materials-engineering, materials-selection, ashby, ashby-chart, material-property-chart, performance-index, material-index, selection-index, specific-stiffness, specific-strength, lightweight-design, cost-performance, trade-off, substitution, screening, ranking, granta, ces-edupack, granta-edupack, matweb, eco-audit, embodied-energy, embodied-carbon, multi-objective, penalty-function, shape-factor, design-requirements]
level: practitioner
status: gated
description: "Pick materials with Ashby's method: translate function, constraints, objective into a performance index (E^1/2/rho etc.), screen on property charts, rank, check cost."
sources:
  - "Ashby, Materials Selection in Mechanical Design (Butterworth-Heinemann)"
  - "Ashby, Shercliff and Cebon, Materials: Engineering, Science, Processing and Design"
  - "Callister and Rethwisch, Materials Science and Engineering: An Introduction"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ashby index material selection — from requirements to a ranked shortlist

**Goal:** replace "we always use 6061" with a traceable decision: derive the property
combination that actually governs performance, screen the whole materials universe,
and hand over a short ranked list with cost and risk noted.

## 1. Translate the design requirement
Write four lines before touching any data:
- **Function** — what the part does (tie, beam, panel, shaft, pressure vessel, spring).
- **Constraints** — non-negotiable limits: max service temperature, must be weldable,
  stiffness or strength must be met, corrosion environment, food contact, etc.
- **Objective** — the one thing to minimise or maximise (mass, cost, embodied carbon, volume).
- **Free variables** — what the designer may change (usually a section dimension, and the material).

## 2. Derive the performance index
Write the objective equation (e.g. mass m = A·L·ρ), write the constraint equation
(e.g. stiffness S = C·E·I/L³), eliminate the free variable, and group the material
properties. The group to **maximise** is the index M. Standard results (all derived by hand and checked: beam stiffness m ∝ ρ/E^1/2 from S ∝ E·A²/L³; panel E^1/3, strength σf^1/2; column E^1/2; tie E and σf; spring σf²/E; log-log slopes 1, 2 and 3 follow from the exponents):

| Component, loading, free variable | Stiffness-limited | Strength-limited |
|---|---|---|
| Tie in tension, area free | E/ρ | σf/ρ |
| Beam in bending, square/round section size free | E^1/2/ρ | σf^2/3/ρ |
| Panel/plate in bending, thickness free | E^1/3/ρ | σf^1/2/ρ |
| Column in buckling, section size free | E^1/2/ρ | — |
| Spring, max elastic energy per volume | — | σf²/E |
| Cheapest version | replace ρ with Cm·ρ (Cm = cost per kg) | same |

σf is yield strength for metals, tensile strength for ceramics/composites per Ashby's
convention. If the shape is also free, multiply in a shape factor (φ) — a hollow tube
can be several times more efficient in bending than a solid bar of the same material.

## 3. Screen, then rank
1. **Screen** on constraints: delete everything outside the temperature, environment,
   processability and toughness limits (attribute limits, not indices).
2. **Plot** the index on a log-log property chart (E vs ρ etc.). The index becomes a
   straight line: slope 1 for E/ρ, slope 2 for E^1/2/ρ, slope 3 for E^1/3/ρ. Slide the
   line toward the top-left until roughly 5–10 candidate families remain above it.
3. **Rank** survivors by M numerically. Example for a light stiff beam (E^1/2/ρ, E in
   GPa, ρ in Mg/m³, typical handbook values (gated: unconfirmed, source is paywalled or blocked)): CFRP quasi-isotropic ~ 70^0.5/1.6 ≈ 5.2;
   wood along grain ~ 12^0.5/0.6 ≈ 5.8; Al alloy ~ 70^0.5/2.7 ≈ 3.1; steel
   ~ 210^0.5/7.8 ≈ 1.9. Same-stiffness steel beam is therefore roughly 1.7× heavier
   than aluminium (computed from the unrounded indices 3.10 and 1.86: 1.67) — not 2.9× as the density ratio suggests.
4. **Document** the supporting information for the top 3–5: datasheets, track record,
   failure analyses in similar products, supply chain, joining, recyclability.

## 4. Multiple objectives and cost
- If two indices conflict (mass vs cost), plot one against the other and look at the
  **trade-off surface** (Pareto front); choose with an exchange constant α (e.g. €/kg
  saved — high for aerospace, near zero for a garden chair) in a penalty function
  Z = Cost + α·mass.
- If two constraints both bind (stiffness and strength), compute mass for each and
  take the larger for each material ("active constraint" method).
- Add the eco-objective when required: embodied energy or CO₂ per kg × mass, plus
  use-phase effects. Software such as Ansys Granta EduPack/Selector does this;
  a spreadsheet works for under ~30 candidates.

## 5. Substitution studies
When replacing an existing material, compute the index ratio new/old for the binding
constraint, multiply by price ratio, then add the **process** and **joining** cost
changes — they often dominate. Re-qualify fatigue, creep and corrosion, which indices
ignore.

## Gotchas
- **Wrong free variable, wrong index.** A beam where only height is free gives a
  different exponent than one with fixed aspect ratio. Re-derive; do not copy.
- **Database values are ranges.** Charts show families; final design needs the
  specific grade, temper, product form and supplier minimum (often an A- or B-basis
  allowable for structures), not typical values.
- **Anisotropy.** Composite and wood values are directional; quasi-isotropic laminate
  stiffness is roughly a third to half of the unidirectional value (computed 0.39 for standard-modulus carbon/epoxy with CLT).
- **Price volatility.** Cm can move ±50% in a year (illustrative (gated: unconfirmed, source is paywalled or blocked)); record date and source.
- Indices ignore manufacturability, minimum gauge, and environmental degradation.

## Verify
- [ ] Function, constraints, objective and free variable are written down explicitly.
- [ ] The index was derived (or checked) for this loading and free variable.
- [ ] Constraint screening was done before ranking on the index.
- [ ] Final candidates use grade-specific design values, not chart midpoints.
- [ ] Cost (and carbon if required) is included, with price source and date.
