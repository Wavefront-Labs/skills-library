---
id: natural-sciences.chemistry.analytical-chemistry.analytical-method-validation
name: analytical-method-validation
category: natural-sciences
field: chemistry
product: analytical-chemistry
tags: [analytical-chemistry, method-validation, ich-q2, ich-q2-r2, ich-q14, eurachem, usp-1225, specificity, selectivity, linearity, range, accuracy, recovery, spike-recovery, precision, repeatability, intermediate-precision, reproducibility, lod, loq, limit-of-detection, limit-of-quantitation, robustness, system-suitability, calibration-curve, hplc, quantitative-analysis, iso-17025, gmp, glp]
level: practitioner
status: gated
description: "Validate a quantitative analytical method per ICH Q2: specificity, linearity and range, accuracy, precision, LOD/LOQ, robustness, with acceptance criteria and a protocol."
sources: ["ICH Q2(R2) Validation of Analytical Procedures (2023)", "Eurachem Guide: The Fitness for Purpose of Analytical Methods (2nd ed., 2014)", "USP General Chapter <1225> Validation of Compendial Procedures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analytical method validation

**Goal:** documented evidence that a method (e.g. HPLC assay, impurity test, ICP
trace analysis) measures the right analyte, at the right level, with known
accuracy and precision — fit for its stated purpose.

## 1. Write the protocol first
Before any validation run, record: the method (frozen version), its purpose
(assay, impurity, limit test, identification), the parameters to test,
experiments, number of replicates and **acceptance criteria**. Validating first and
choosing criteria afterwards is the classic audit finding. Which characteristics you
need depends on the purpose (ICH Q2 table: identification needs specificity only;
a quantitative impurity test needs nearly everything).

## 2. Characteristics and typical experiments
- **Specificity / selectivity:** analyse blank matrix, placebo, known impurities,
  degradation products (forced degradation: acid, base, peroxide, heat, light; Q2(R2) asks for stability-indicating proof via forced degradation samples where necessary).
  Show the analyte response is free of interference (resolution, peak purity by
  DAD/MS).
- **Linearity & range:** ≥ 5 concentrations across the range (ICH Q2(R2) section 3.2.2.1, confirmed; assay range 80% to 120% of declared content or specification, Q2(R2) Table 2, confirmed; impurity range from reporting level to ~120% of specification (gated: unconfirmed, source is paywalled or blocked)). Plot response vs
  concentration, report slope, intercept, r, **and residuals** — r ≥ 0.999 can hide
  curvature; a residual plot cannot.
- **Accuracy:** spike known amounts into matrix at ≥ 3 levels × 3 replicates (9
  determinations (gated: unconfirmed, source is paywalled or blocked)); report % recovery and confidence interval. Or compare with a
  certified reference material or an independent method.
- **Precision:**
  - repeatability: ≥ 6 determinations at 100% of test concentration, or ≥ 9 covering the reportable range, e.g. 3 concentrations × 3 replicates (Q2(R2) 3.3.2.1, confirmed), same analyst/day;
  - intermediate precision: different days, analysts, instruments/columns;
  - reproducibility: between labs (method transfer/collaborative studies).
  Report RSD; assay methods often aim at ≤ 1–2% (gated: unconfirmed, source is paywalled or blocked), trace methods accept much more.
- **LOD / LOQ:** by signal-to-noise (3:1 for DL, at least 10:1 for QL, Q2(R2) 3.2.3.2, confirmed) or from the calibration:
  LOD = 3.3σ/S, LOQ = 10σ/S (Q2(R2) 3.2.3.3, confirmed) (σ = SD of the response or intercept, S = slope).
  **Confirm LOQ experimentally** with replicates at that level meeting precision/accuracy targets.
- **Robustness:** deliberately vary parameters (the example ranges pH ± 0.2, column temperature ± 5 °C,
  flow ± 10%, mobile-phase composition ± 2% are (gated: unconfirmed, source is paywalled or blocked); different column lot) — ideally by a
  small factorial design during development (ICH Q14 puts this earlier).
- **System suitability:** criteria checked every run (resolution, tailing, plate count,
  injection precision) derived from validation data.

## 3. Report
Summarise each characteristic vs its acceptance criterion, all raw data traceable,
deviations explained. Any later change to the method triggers a risk assessment
and possibly partial revalidation.

## Gotchas
- Spiking a standard into solvent is not accuracy in matrix — matrix effects (ion
  suppression in LC-MS, interferences in ICP) are the point.
- Using the same standard solution to build the curve and check accuracy hides
  weighing errors; prepare independent stock solutions.
- Heteroscedastic data over wide ranges (trace work) need weighted regression (1/x or 1/x² (gated: unconfirmed, source is paywalled or blocked)).
- *Uncertainty note:* acceptance limits quoted here are typical for pharmaceutical
  assays; regulated fields (food, environmental, clinical) have their own guidance
  and numbers. ICH Q2(R2) wording was updated in 2023; check the current text.

## Verify
- [ ] Protocol with acceptance criteria signed before validation runs.
- [ ] Specificity shown against blanks, impurities and degradation products.
- [ ] Linearity residual plot shows no trend; range covers intended use.
- [ ] Accuracy from ≥ 9 determinations in matrix; precision at two levels (repeatability, intermediate).
- [ ] LOQ verified with real replicates; system suitability criteria defined.
