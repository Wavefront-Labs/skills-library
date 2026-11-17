---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.bp-validation-iso-81060-2
name: bp-validation-iso-81060-2
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [bp-validation, blood-pressure-measurement, oscillometry, iso-81060-2, clinical-validation, auscultatory-reference, same-arm-sequential, accuracy-criteria]
level: advanced
status: gated
description: "Plan a clinical validation of an automated sphygmomanometer per ISO 81060-2: subject numbers and distributions, reference measurement, pairing and the two accuracy criteria."
sources: ["ISO 81060-2 Non-invasive sphygmomanometers - Clinical investigation of intermittent automated measurement type (2018 edition and amendment 1 2020; confirm current edition)", "AAMI/ESH/ISO Universal Standard (ISO 81060-2) validation statements in Stergiou et al., A universal standard for the validation of blood pressure measuring devices (Hypertension 2018)", "https://discovery.ucl.ac.uk/id/eprint/10048123/ (AAMI/ESH/ISO universal standard consensus statement, free PDF)", "ISO 14155 Clinical investigation of medical devices for human subjects"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clinical validation per ISO 81060-2

**Goal:** show that an automated cuff blood pressure device meets the accuracy criteria against a reference method in a defined population.

Clinical investigations need ethics approval and compliance with ISO 14155 and local regulation; the sample size, sex and BP-range requirements below were read in the AAMI/ESH/ISO consensus statement (Stergiou et al. 2018, free PDF); the criterion limits are from the paywalled standard and must be confirmed in the current edition.

## Design (general population, same-arm sequential method)
- **Subjects:** at least 85 adults for the general-population study (per the consensus statement), with at least 30% male and at least 30% female. Reference systolic readings: at least 5% at or below 100 mmHg, at least 5% at or above 160 mmHg, at least 20% at or above 140 mmHg. Reference diastolic: at least 5% at or below 60 mmHg, at least 5% at or above 100 mmHg, at least 20% at or above 85 mmHg. For a device with n cuffs each cuff is tested on at least 1/(2n) of subjects, and at least 40% of subjects have arm circumference in the upper half and at least 40% in the lower half of the cuff range.
- **Reference:** two trained observers reading simultaneously (Y-tube double stethoscope) by auscultation with a mercury or accurate non-mercury sphygmomanometer, blinded to the device reading and to each other; Korotkoff K1 for systolic and K5 for diastolic. The test device cuff is not used for the reference.
- **Measurements:** same-arm sequential method, alternating R0, T0, R1, T1, R2, T2, R3, T3, R4 (R reference, T test device). R0 and T0 are not used in the analysis. Each of T1-T3 is compared with the average of the reference readings before and after it, giving three paired comparisons per subject (255 pairs for 85 subjects). A subject is excluded if the reference differs by more than 12 mmHg systolic or 8 mmHg diastolic in any 2 of R1-R4; observer disagreement above 4 mmHg triggers a repeat pair (maximum 8 pairs).
- Use the same cuff placement and rest between readings (device time restrictions); document arm, cuff size, and posture.

## Accuracy criteria
- **Criterion 1:** the mean difference (test minus reference) over all pairs is within plus or minus 5 mmHg and the standard deviation is no greater than 8 mmHg (gated: unconfirmed, source is paywalled or blocked).
- **Criterion 2:** the standard deviation of the per-subject mean differences (averaging each subject's three paired differences) must be below a limit that depends on criterion 1's standard deviation, given in a table in the standard (a larger criterion 1 standard deviation allows a different threshold).
Both systolic and diastolic pressures are analysed separately.

## Other populations
The consensus statement accepts a minimum of 35 subjects (45 for pregnancy) for a special population provided an independent 85-subject general-population study has already passed; special populations are age under 3, pregnancy, arm circumference over 42 cm and atrial fibrillation. The statement says there is no agreed procedure for atrial fibrillation. Confirm current requirements in the standard and its amendment.

## Practice points
- Train observers, check the reference device and keep an audit trail for all readings.
- Pre-register the analysis plan; do not exclude data without protocol-defined rules.
- Report outliers and device error messages.

## Verify
- [ ] Subject distributions meet each table requirement before analysis.
- [ ] Statistical analysis reproduces criterion 1 and 2 values using the raw data.
- [ ] Study report follows ISO 14155 and the 81060-2 reporting items.
