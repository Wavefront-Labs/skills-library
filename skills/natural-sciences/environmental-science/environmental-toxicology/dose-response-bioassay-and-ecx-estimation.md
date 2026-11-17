---
id: natural-sciences.environmental-science.environmental-toxicology.dose-response-bioassay-and-ecx-estimation
name: dose-response-bioassay-and-ecx-estimation
category: natural-sciences
field: environmental-science
product: environmental-toxicology
tags: [environmental-toxicology, ecotoxicology, bioassay, dose-response, concentration-response, ec50, lc50, ec10, ecx, noec, loec, log-logistic, probit, drc, r, oecd-202, daphnia-magna, oecd-201, algae, oecd-203, fish-acute, test-validity, measured-concentrations, solvent-control, hormesis, bioaccumulation, ecological-risk]
level: practitioner
status: draft
description: "Run an aquatic bioassay (e.g. OECD 202 Daphnia) and estimate EC50/EC10 properly: concentration spacing, controls, validity criteria, log-logistic fitting in R drc, and why NOEC is out."
sources: [OECD Test Guidelines 201, 202, 203, OECD (2006) Current approaches in the statistical analysis of ecotoxicity data, Ritz et al. 2015 PLOS ONE drc package]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dose-response bioassays and ECx estimation

**Goal:** generate a concentration-response curve for a contaminant on a test organism
and report an effect concentration (EC50, EC10) with a confidence interval that a
reviewer or regulator will accept.

## 1. Design the test
- **Pick a standard guideline** when one exists — it fixes organism age, duration,
  endpoints and validity criteria. Common ones: OECD 202 *Daphnia* acute immobilisation
  (48 h, neonates <24 h old), OECD 201 freshwater algae growth inhibition (72 h, growth
  rate), OECD 203 fish acute (96 h).
- **Range-finder first:** a few concentrations spaced by ×10 to locate the effect zone.
- **Definitive test:** at least **five concentrations** in a geometric series (factor
  ≤3.2, often 2), bracketing 0–100% effect, plus control. For ECx regression, more
  concentrations with fewer replicates beats few concentrations with many replicates.
- **Replication:** OECD 202 uses ≥20 animals per concentration, typically 4 × 5.
  Randomise vessel positions.
- **Solvent control** if a carrier (e.g. acetone, DMSO ≤0.1 mL/L) was needed — it must
  not differ from the dilution-water control.

## 2. Measure, don't assume, exposure
Analytically confirm concentrations at the start and end (and for unstable or volatile
substances, in between). If measured values drop below 80% of nominal, express results
on **geometric-mean measured** concentrations, as the guidelines direct. Record pH,
dissolved oxygen and temperature in every vessel.

## 3. Check validity before analysis
Each guideline sets criteria — e.g. OECD 202: control immobilisation ≤10%, dissolved
oxygen ≥3 mg/L at the end. OECD 201: control biomass growth ≥16-fold in 72 h and limits
on control CV. A test that fails validity is repeated, not "interpreted".

## 4. Fit the curve
In R with the `drc` package:
```r
library(drc)
m <- drm(immobile/total ~ conc, weights = total, data = d,
         fct = LL.2(), type = "binomial")   # 2-parameter log-logistic, quantal data
summary(m); plot(m, type = "all")
ED(m, c(10, 50), interval = "delta")         # EC10, EC50 with 95% CI
```
- **Quantal** data (dead/alive): binomial with `LL.2` or probit (`LN.2`).
- **Continuous** data (growth rate, reproduction): `LL.3`/`LL.4` with `type="continuous"`;
  compare fits with `mselect()` and check residuals.
- Report the model, parameters, ECx with 95% CI, and whether the CI was bounded by
  tested concentrations. An EC10 extrapolated below the lowest tested concentration is
  not a finding.

## 5. NOEC/LOEC — know the critique
Hypothesis-test endpoints (NOEC = highest concentration not significantly different
from control, via Dunnett or Williams tests) depend on spacing and replication, have no
CI, and reward poor designs. OECD's 2006 guidance and most current literature prefer
ECx (typically EC10 or EC20). Some regulatory frameworks still request NOEC, so report
both if needed and explain.

## 6. From bioassay to risk
Ecological risk assessments combine endpoints across species — assessment factors on the
lowest endpoint, or a **species sensitivity distribution (SSD)** giving an HC5. For
bioaccumulation, the separate OECD 305 fish test gives BCF/BMF; that is a different
design (uptake and depuration phases).

## Gotchas
- **Hormesis** (stimulation at low dose) breaks monotone models; use Brain-Cousens
  (`BC.4`/`BC.5`) or report it rather than forcing a log-logistic fit.
- Zero concentration can't be log-transformed; `drc` handles it, hand-rolled probit
  in Excel often does not.
- Poorly soluble substances: effect may plateau at the solubility limit — state it.
- Over-dispersion in quantal data (replicate vessels differ) widens real CIs; check it.

## Verify
- [ ] ≥5 concentrations bracketing the response; controls (and solvent control) included.
- [ ] Validity criteria from the guideline met and reported.
- [ ] Exposure analytically confirmed; nominal vs measured basis stated.
- [ ] Model choice justified, residuals checked, ECx with 95% CI inside tested range.
- [ ] Raw data per vessel archived for reanalysis.
