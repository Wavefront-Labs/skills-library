---
id: engineering-technology.biomedical-engineering.device-verification-validation.measurement-uncertainty
name: measurement-uncertainty
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [measurement-uncertainty, uncertainty-budget, calibration-uncertainty, gum, test-uncertainty-ratio]
level: advanced
status: gated
description: "Build a measurement uncertainty budget: sources, type A and B evaluation, combination, expanded uncertainty, test uncertainty ratio and using uncertainty in pass-fail decisions."
sources: ["JCGM 100 Guide to the expression of uncertainty in measurement (GUM) (2008 edition, confirmed on bipm.org; JCGM 106:2012 covers decision rules and guard bands)", "ISO/IEC 17025 General requirements for the competence of testing and calibration laboratories (confirm edition)", "https://www.bipm.org/en/committees/jc/jcgm/publications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Calibration and measurement uncertainty

**Goal:** state how well a measured value is known so pass-fail decisions near a limit are sound.

## Method (GUM)
1. **Specify the measurand** and the measurement model.
2. **List uncertainty sources:** instrument calibration and resolution, repeatability, reference standard, environment (temperature), fixture alignment, operator, software and data processing.
3. **Evaluate standard uncertainties:** Type A from statistics of repeated observations (standard deviation of the mean); Type B from certificates, specifications and judgement, converting limits to standard uncertainty (a rectangular distribution of half-width a gives a divided by the square root of 3).
4. **Combine** in quadrature (root sum of squares) after weighting by sensitivity coefficients to get the combined standard uncertainty.
5. **Expanded uncertainty** U = k times combined, with k about 2 for roughly 95 percent coverage for a normal distribution.
6. **Traceability:** calibrations of instruments to national standards with stated uncertainty.

## Use
- **Test uncertainty ratio (TUR):** specification tolerance divided by the instrument's uncertainty; practice sets a target (often 4 to 1 in calibration practice (gated: unconfirmed, source is paywalled or blocked); confirm company and standard requirements).
- **Decision rules:** with a pass requirement near a limit, apply a guard band equal to some fraction of the expanded uncertainty, or state the rule used (simple acceptance or guard-banded acceptance).
- Report uncertainty with results where decisions are close.

## Verify
- [ ] Budget lists all significant contributors with distributions and sources.
- [ ] Calibration certificates give uncertainty and traceability.
- [ ] Decision rule applied to marginal results is documented.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
