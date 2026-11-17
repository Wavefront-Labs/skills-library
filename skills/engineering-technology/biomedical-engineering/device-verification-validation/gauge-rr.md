---
id: engineering-technology.biomedical-engineering.device-verification-validation.gauge-rr
name: gauge-rr
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [gauge-rr, test-method-validation, measurement-system-analysis, msa, anova-gauge-rr, repeatability, reproducibility, ndc]
level: practitioner
status: gated
description: "Run a gauge R and R study for device measurements: crossed ANOVA design, number of parts and operators, %study variation and %tolerance, ndc and attribute agreement."
sources: ["AIAG Measurement Systems Analysis Reference Manual (4th edition)", "Montgomery, Introduction to Statistical Quality Control (measurement system capability)", "ISO 13485 Medical devices - Quality management systems (monitoring and measuring equipment)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gauge R&R (repeatability and reproducibility)

**Goal:** determine whether a measurement method is capable of detecting variation in the characteristic and checking it against its tolerance.

## Design (crossed study for non-destructive tests)
- **10 parts** chosen to span the process variation (include parts near both limits), **3 operators**, **2-3 replicates** per operator per part, run in random order and blind to part identity.
- Use the actual fixture, software and measurement conditions.

## Analysis (ANOVA method preferred)
- Variance components: repeatability (equipment variation within an operator), reproducibility (between operators), operator-by-part interaction, and part-to-part variation.
- Report **%Study Variation** = measurement-system standard deviation / total standard deviation, and **%Tolerance** = 6 x measurement-system standard deviation / (USL - LSL).
- **Number of distinct categories (ndc)** = 1.41 x (part SD / measurement system SD); aim for at least 5.

## Typical acceptance guidance (AIAG; the 10%/30% bands, ndc of 5 and the 10 parts x 3 operators design are from the paywalled MSA manual (gated: unconfirmed, source is paywalled or blocked))
- Below 10% of tolerance or study variation: acceptable.
- 10-30%: may be acceptable depending on importance, cost, risk and agreed plan.
- Above 30%: not acceptable; improve the method.
Criteria are guidance; set the acceptance rule in the test method validation protocol (see tmv-procedure) and base it on risk.

## Special cases
- **Destructive tests** (tensile, burst, seal peel) cannot be repeated on the same part: use a nested design with homogeneous batches, or similar parts as surrogates, and note the limits.
- **Attribute measurement** (pass/fail, visual inspection): attribute agreement analysis with kappa statistics; compare to a reference decision; acceptable kappa often above 0.75-0.9 (gated: unconfirmed, source is paywalled or blocked).
- **Linearity, bias and stability** studies complement R&R with reference standards.

## Gotchas
- Selecting parts all near nominal hides capability for detecting out-of-tolerance parts.
- Operators who know the readings; randomise and blind.
- Treating R&R passing as proof of accuracy; check bias with a reference.

## Verify
- [ ] Study uses production fixtures and a range of parts.
- [ ] Results (%tolerance, %study variation, ndc) recorded against predefined acceptance.
- [ ] Re-run when equipment, software or operators change.
