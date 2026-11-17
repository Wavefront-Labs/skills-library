---
id: health-medicine.allied-health-technologies.medical-laboratory-technology.specimen-acceptance-qc-westgard-rules-and-critical-results
name: specimen-acceptance-qc-westgard-rules-and-critical-results
category: health-medicine
field: allied-health-technologies
product: medical-laboratory-technology
tags: [allied-health-technologies, medical-laboratory-technology, medical-laboratory-scientist, mls, mlt, biomedical-scientist, clinical-laboratory, specimen-rejection, haemolysis, hemolysis-index, order-of-draw, edta-contamination, levey-jennings, westgard-rules, internal-quality-control, iqc, eqa, proficiency-testing, delta-check, critical-values, panic-values, autoverification, lis, analyser-maintenance, clia]
level: practitioner
status: draft
description: "Clinical lab bench practice: specimen acceptance and rejection, pre-analytical errors, Levey-Jennings and Westgard QC, delta checks, autoverification, and critical-result phoning."
sources: [CLSI documents C24 (statistical QC), GP41 (venipuncture), GP33/EP-related guidance, Westgard multirule QC literature, CLIA regulations 42 CFR 493, ISO 15189:2022]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Specimen acceptance, QC with Westgard rules, and critical results

> General clinical/professional reference, not a substitute for your laboratory's SOPs, the analyser manufacturer's instructions, or accreditation requirements.

**Goal:** release only results that are right for the right patient — most lab errors
happen **before** the analyser (pre-analytical), and the QC system catches most of the rest.

## 1. Specimen acceptance
Check on receipt:
- **Two identifiers** on the tube matching the request; unlabelled or mislabelled
  specimens are rejected (re-collect) — never relabel someone else's tube.
- Correct tube type/additive, fill volume (citrate coagulation tubes ~90% fill),
  collection time, transport temperature and stability window.
- Visual/automated serum indices: **haemolysis** (false high K+, LDH, AST), **icterus**,
  **lipaemia**. Apply the analyser's index limits per test.
Common pre-analytical traps:
- **EDTA contamination** (wrong order of draw / decanting): very high K+, very low
  Ca2+, low ALP.
- Drip-arm contamination: glucose/electrolytes resembling the IV fluid.
- Delayed separation: falsely high K+, low glucose; refrigerated whole blood raises K+.
- Clotted EDTA/citrate samples invalidate counts and coagulation.

## 2. Daily analyser operation
Start-up maintenance and checks per manufacturer, reagent lot/expiry and on-board
stability, calibration when due or after reagent lot change, then **QC before patient
samples** (and at intervals defined by risk and run size).

## 3. QC and Westgard rules
- Plot QC on **Levey-Jennings** charts using lab-established mean and SD for each lot.
- Common multirule (Westgard) set:
  - **1-2s** warning → inspect other rules (some labs no longer use it as a trigger).
  - **1-3s** reject — random error.
  - **2-2s** reject — systematic (two consecutive on same side > 2SD).
  - **R-4s** reject — random (range across controls > 4SD in one run).
  - **4-1s**, **10-x** reject — systematic shift/trend.
- On rejection: **hold patient results**, troubleshoot (reagent, calibration, control
  material, instrument), correct, re-run QC, then re-test patients since last good QC as
  required. Document every action.
- Sigma-metric QC design (rules chosen by method performance) is increasingly used.
- **External quality assessment / proficiency testing:** treat samples like patients;
  investigate unacceptable results with root cause.

## 4. Result review
- **Delta checks:** large change from the patient's prior result → check identity and
  sample quality before release.
- Absurd/physiologically implausible values → re-run, check sample.
- Autoverification rules in the LIS release normal-range results; flagged results
  route to the technologist — know your rule set.

## 5. Critical results
- Defined list with thresholds (e.g. K+, Na+, glucose, Hb, platelets, INR, positive
  blood culture — local values).
- Phone to a responsible clinician within the defined time, **read-back** of patient,
  test and value, document recipient name and time. Escalate if unreachable.

## Gotchas
- Releasing a "repeat to confirm" before rechecking specimen ID.
- Changing QC means when a shift appears hides real drift.
- Point-of-care results outside the lab still need QC and oversight.

## Verify
- [ ] Specimen ID, tube, volume and serum indices checked; rejections documented.
- [ ] QC in range by Westgard rules before patient release; failures actioned.
- [ ] Delta-check and implausible results investigated.
- [ ] Critical results phoned with read-back and documented in time.
