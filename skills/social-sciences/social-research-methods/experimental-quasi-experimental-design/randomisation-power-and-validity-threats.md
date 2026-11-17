---
id: social-sciences.social-research-methods.experimental-quasi-experimental-design.randomisation-power-and-validity-threats
name: randomisation-power-and-validity-threats
category: social-sciences
field: social-research-methods
product: experimental-quasi-experimental-design
tags: [experimental-quasi-experimental-design, experimental-design, randomised-controlled-trial, rct, field-experiment, randomisation, block-randomisation, stratified-randomisation, cluster-randomisation, power-analysis, minimum-detectable-effect, mde, icc, quasi-experiment, interrupted-time-series, nonequivalent-control-group, regression-discontinuity, internal-validity, external-validity, construct-validity, shadish-cook-campbell, attrition, contamination, spillover, hawthorne, pre-registration, intention-to-treat, compliance]
level: practitioner
status: verified
description: "Design a study of people that supports a causal claim: choose RCT or quasi-experiment, randomise properly, size it with an MDE, and close off validity threats before fielding."
sources: ["Shadish, Cook & Campbell, Experimental and Quasi-Experimental Designs for Generalized Causal Inference (Houghton Mifflin 2002)", "Gerber & Green, Field Experiments (Norton 2012)", "Glennerster & Takavarasha, Running Randomized Evaluations (Princeton 2013)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Experimental and quasi-experimental design — randomise, size, defend

**Goal:** a design where the comparison group really shows what would have happened
without the intervention, large enough to detect an effect worth detecting.

## 1. Pick the design by what you control
| You can… | Design |
|---|---|
| Randomly assign individuals | Individual RCT (block/stratify on strong predictors) |
| Only assign groups (classes, clinics, villages) | Cluster RCT |
| Roll out gradually to everyone | Stepped-wedge or randomised phase-in |
| Not randomise; assignment by a cutoff score | Regression discontinuity |
| Not randomise; long series before/after | Interrupted time series with a comparison series |
| Not randomise; treated and untreated groups with pre-data | Nonequivalent groups with pretest, difference-in-differences |
Weakest commonly used: post-only comparison with no pretest. Avoid it if any alternative exists.

## 2. Randomisation done properly
- Generate the allocation with a seeded script (R `set.seed()`; Stata `set seed`), save it,
  and keep it away from the people recruiting (**allocation concealment**).
- **Block / stratify** on 1–3 variables that predict the outcome (baseline score, site);
  it raises precision and protects balance in small samples.
- Check balance on baseline covariates with standardised differences rather than
  significance tests; imbalance after proper randomisation is chance, not failure — adjust
  for pre-specified covariates.
- Record the unit of randomisation: analysing individuals when you randomised clusters
  overstates precision.

## 3. Power and the MDE
Fix α (0.05), power (0.80), and the **minimum detectable effect** you care about, ideally
from policy relevance or prior studies — not from what makes n affordable.
- Individual, two arms, equal split, standardised outcome: MDE ≈ 2.8 × √(4/N) SD
  (2.8 ≈ 1.96 + 0.84). So N = 400 → MDE ≈ 0.28 SD.
- Clusters: multiply variance by the design effect `1 + (m − 1)·ICC`. With 20 per cluster
  and ICC 0.10, deff = 2.9 — almost three times the sample for the same MDE. **More
  clusters beat bigger clusters.**
- A baseline covariate with correlation r to the outcome shrinks required N by about (1 − r²).
- Tools: R `pwr`, Stata `power`, Optimal Design / PowerUp! for multilevel designs, or
  simulation (most honest for complex designs).

## 4. Threats to validity — checklist
- **Internal:** selection, history, maturation, testing, instrumentation, regression to the
  mean, **attrition** (differential dropout), **contamination/spillover** between arms.
- **Construct:** does the treatment as delivered match the concept? Measure fidelity and dose.
- **Statistical conclusion:** low power, fishing across many outcomes, violated
  independence (clusters).
- **External:** would the effect hold for other people, places, delivery agencies, scale?
For each threat write the design feature that answers it (e.g. spillover → randomise at
school, not classroom, level).

## 5. Field logistics
- **Pre-register** hypotheses, primary outcome, and analysis plan (OSF, AEA RCT Registry,
  or ClinicalTrials.gov for health outcomes) before outcome data exist.
- Ethics approval before recruitment
  (social-sciences.social-research-methods.research-ethics-human-subjects.consent-risk-and-ethics-committee-applications).
- Same data collection, same timing, same enumerators for both arms; blind assessors where
  possible.
- Monitor compliance; analyse **intention-to-treat** as primary, with complier effects
  (IV using assignment) as secondary.

## Gotchas
- Re-randomising until balance "looks good" invalidates standard inference unless you use
  the matching re-randomisation procedure in the analysis.
- An "active control" that is half the treatment produces null results by design.
- Hawthorne/John Henry effects: control groups that know they are controls change behaviour.

## Verify
- [ ] Design choice justified from what you can control.
- [ ] Seeded, saved, concealed allocation; unit of randomisation = unit of analysis.
- [ ] MDE stated in outcome units and judged meaningful; ICC sourced for clusters.
- [ ] Every validity threat mapped to a design response.
- [ ] Pre-registration time-stamped before outcomes collected.
- [ ] ITT primary analysis planned.

*Checked 2026-10-19: statsmodels TTestIndPower gives MDE 0.281 SD for N=400 (rule gives 0.28; 1.96+0.84=2.80); deff 1+19*0.10 = 2.9; 1-r^2 = 0.75 at r=0.5. The MDE rule assumes equal allocation and no covariates; check with software for anything more complex.*
