---
id: natural-sciences.applied-industrial-rd.formulation-science.doe-screening-for-new-formulations
name: doe-screening-for-new-formulations
category: natural-sciences
field: applied-industrial-rd
product: formulation-science
tags: [formulation-science, applied-industrial-rd, formulation, design-of-experiments, doe, screening-design, fractional-factorial, plackett-burman, definitive-screening-design, mixture-design, simplex-lattice, response-surface, central-composite, jmp, minitab, design-expert, factor-ranges, interactions, replicates, centre-points, randomisation, stability, scale-up, compatibility, prototype-iteration]
level: advanced
status: draft
description: "Develop a new formulation with designed experiments: set responses and ranges, choose screening, mixture or response-surface designs, randomise, model, confirm, check stability and scale-up."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DoE screening for new formulations

**Goal:** find a formulation that meets a target profile with far fewer trials than
one-factor-at-a-time, and understand the interactions that will matter at scale-up.

## 1. Define before you mix
- **Target product profile:** measurable responses with specs (viscosity 3,000–5,000
  mPa·s at 25 °C, pH 5.5 ± 0.3, no phase separation after 4 weeks at 40 °C, cost ≤ X/kg).
- **Factors:** ingredient levels and process variables (mixing shear, order of
  addition, temperature, cooling rate). Process factors often matter as much as ingredients.
- **Ranges:** wide enough to see an effect, narrow enough to stay feasible. Run a
  couple of "corner" scouting batches first — if extremes don't form a product at
  all, the design wastes runs.
- **Measurement capability:** know the repeatability of each test; if the
  method's noise is bigger than the effect you care about, fix the method first.

## 2. Pick the design type
- **Screening (many factors, find the vital few):** fractional factorial
  (resolution IV keeps main effects clear of two-factor interactions),
  Plackett–Burman (main effects only, interactions confounded), or
  **definitive screening designs** (3 levels, detect curvature, efficient for
  6–15 factors).
- **Mixture designs** when components must sum to 100% (e.g. a solvent blend or
  oil phase): simplex-lattice, simplex-centroid, or D-optimal with constraints. Don't
  use an ordinary factorial on components that must sum to a fixed total — changing
  one changes the others.
- **Combined mixture-process designs** when both matter (more runs; often D-optimal).
- **Optimisation:** response surface (central composite, Box–Behnken) on the 2–4
  factors that screening found important.

Software: JMP, Minitab, Design-Expert, or R (e.g. `FrF2`, `rsm`, `mixexp`) /
Python (`pyDOE3`, `statsmodels`).

## 3. Running the trials
- **Randomise run order** to protect against drift (raw-material lot, ambient
  humidity, operator learning). If something can't be randomised (e.g. a slow
  temperature change), use blocking or a split-plot design, and analyse it as such.
- Include **centre points** (3–5) to estimate pure error and detect curvature.
- Use one raw-material lot per ingredient for the study where possible; record lots.
- Record everything about process: batch size, equipment, times, temperatures.

## 4. Analysis
- Fit the model, check residual plots (normality, constant variance, run-order
  trends), and look at effect sizes, not only p-values.
- Use transforms (e.g. log viscosity) if variance grows with the mean.
- Watch for aliasing: in fractional designs, an "effect" may be an interaction in disguise.
- Use desirability functions or overlay plots to find a region meeting all specs —
  a robust region is better than a single sharp optimum.

## 5. Confirm and de-risk
- **Confirmation runs** at the predicted optimum (≥2–3 batches); compare to the
  prediction interval.
- **Stability:** accelerated (e.g. 40 °C/75% RH), real-time, freeze–thaw cycles,
  light exposure, packaging compatibility. Accelerated data are indicative, not proof.
- **Scale-up readiness:** identify scale-dependent factors (shear, heat transfer,
  addition rate, mixing time); test at pilot scale on equipment that resembles production.
- Document a **design space** and critical parameters for handover to production.

## Gotchas
- Too narrow ranges → nothing significant; too wide → runs fail and break the model.
- Ingredient interactions (e.g. an electrolyte collapsing a thickener) dominate
  many formulations — screening designs that can't see interactions miss them.
- Lab mixers don't reproduce production shear; a "robust" lab optimum can fail at scale.

## Verify
- [ ] Responses, specs and test-method repeatability defined first.
- [ ] Design type matches the problem (screening, mixture, RSM).
- [ ] Runs randomised with centre points and lots recorded.
- [ ] Model residuals checked; aliasing considered.
- [ ] Optimum confirmed by fresh batches and placed on stability and pilot trials.

*Draft note:* stability conditions follow common ICH-style practice; your sector's
regulations may set different conditions.
