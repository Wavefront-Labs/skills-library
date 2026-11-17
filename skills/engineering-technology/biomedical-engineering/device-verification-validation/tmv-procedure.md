---
id: engineering-technology.biomedical-engineering.device-verification-validation.tmv-procedure
name: tmv-procedure
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [tmv, test-method-validation, method-validation, measurement-system, test-method-qualification]
level: practitioner
status: draft
description: "Validate a test method for verification use: purpose, attributes, accuracy, precision, range, robustness, protocol, acceptance criteria and revalidation triggers."
sources: ["ISO 13485 validation of processes and measurement equipment clauses (confirm edition)", "AIAG Measurement Systems Analysis reference manual (confirm edition)", "https://www.iso.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Test method validation procedure

**Goal:** show a test method measures the characteristic accurately and precisely enough for the decision based on it.

## Procedure
1. **Define purpose and requirement:** the characteristic, specification limits, and the measurement tolerance needed (a rule of thumb is that measurement variation should consume a small fraction of the specification tolerance; set the target in your procedure).
2. **Choose attributes** to validate: accuracy (bias) against a reference or standard, precision (repeatability and reproducibility across operators, days, equipment; see gauge-rr), linearity and range, resolution, robustness to small setup variations (specimen alignment, speed, temperature), specificity or interference where relevant.
3. **Write the validation protocol** with samples spanning the range (including at and around the limit), operator numbers, replicates, acceptance criteria, and statistical analysis.
4. **Execute and analyse:** percentage of tolerance consumed by repeatability and reproducibility, bias versus reference, capability of the test (discrimination).
5. **Report:** state the validated range and conditions and the limits of use.
6. **Revalidation triggers:** change of equipment, fixture, software, operator qualification, or specification; periodic review.
7. For attribute (go or no-go) tests, use attribute agreement analysis and detection probability.

## Verify
- [ ] Protocol approved before execution with predefined acceptance criteria.
- [ ] Report states the validated range and fixtures.
- [ ] Equipment calibration current; operators trained.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
