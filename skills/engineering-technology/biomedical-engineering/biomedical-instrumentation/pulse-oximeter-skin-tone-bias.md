---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.pulse-oximeter-skin-tone-bias
name: pulse-oximeter-skin-tone-bias
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [oximeter-bias, skin-pigmentation, pulse-oximetry-accuracy, occult-hypoxemia, spo2-bias]
level: advanced
status: gated
description: "Understand and test pulse oximeter accuracy across skin pigmentation: mechanism, evidence of overestimation, test design, labelling and regulatory attention."
sources: ["Sjoding et al., Racial Bias in Pulse Oximetry Measurement, N Engl J Med 2020;383:2477-2478", "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pulse-oximeters-medical-purposes-non-clinical-and-clinical-performance-testing-labeling-and", "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pulse-oximeters-premarket-notification-submissions-510ks-guidance-industry-and-food-and", "ISO 80601-2-61 (confirm edition)", "https://www.fda.gov"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pulse oximeter accuracy across skin tones

**Goal:** make accuracy claims that hold across the intended population, and test them that way.

## Evidence
- Retrospective studies, including a widely cited 2020 study, found that pulse oximeters can overestimate arterial oxygen saturation in patients with darker skin pigmentation, so low blood oxygen can be missed (occult hypoxaemia) more often than in lighter-skinned patients.
- Mechanisms include greater melanin absorption altering the optical path and calibration derived mostly from lighter-skinned volunteers. Skin-tone self-report and the Fitzpatrick scale are imperfect measures; objective colorimetric methods are used in research.

## Design and test implications
1. Include subjects across a wide range of measured skin pigmentation in the hypoxia (desaturation) calibration and validation study, with objective skin colour measurement; FDA's 2013 final 510(k) guidance recommends 10 or more subjects, 200 or more paired points and at least 2 darkly pigmented subjects or 15% of the pool, whichever is larger; FDA's January 2025 draft guidance (Pulse Oximeters for Medical Purposes, non-binding, not for implementation) asks for clinical data showing performance across pigmentation levels. Check fda.gov for whether the draft has been finalised.
2. Report accuracy (ARMS or bias and limits; ISO 80601-2-61 criteria (gated: unconfirmed, source is paywalled or blocked)) per pigmentation subgroup, not only overall.
3. Algorithm: check for pigmentation-dependent bias at low saturation; consider calibration or multi-wavelength approaches.
4. Labelling: disclose limits (for example that readings can be less accurate with darker skin, poor perfusion, motion), and clinical advice to rely on arterial blood gas where doubt matters.
5. Post-market: monitor complaints and published comparisons.

## Verify
- [ ] Study cohort pigmentation distribution reported using an objective measure.
- [ ] Subgroup bias analysed with confidence intervals.
- [ ] Labelling and risk file updated with the limitation.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
