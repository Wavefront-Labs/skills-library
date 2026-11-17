---
id: health-medicine.pathology-and-laboratory-medicine.laboratory-quality-management.westgard-qc-proficiency-testing-and-preanalytic-control
name: westgard-qc-proficiency-testing-and-preanalytic-control
category: health-medicine
field: pathology-and-laboratory-medicine
product: laboratory-quality-management
tags: [laboratory-quality-management, pathology-and-laboratory-medicine, quality-control, iqc, internal-quality-control, westgard-rules, levey-jennings-chart, multirule-qc, sigma-metrics, total-allowable-error, proficiency-testing, eqa, external-quality-assessment, peer-comparison, pre-analytic-error, specimen-rejection, wrong-blood-in-tube, iso-15189, cap-accreditation, clia, document-control, nonconformance, capa, root-cause-analysis, quality-indicators, turnaround-time, audit]
level: practitioner
status: gated
description: "Keep lab results right: Westgard multirule QC with sigma-based design, proficiency testing/EQA follow-up, pre-analytic error control, nonconformance and CAPA, and accreditation readiness."
sources:
  - "Westgard JO. Basic QC Practices, 4th ed. Westgard QC 2016; westgard.com multirule reference"
  - "CLSI C24 Statistical Quality Control for Quantitative Measurement Procedures: Principles and Definitions, 4th ed."
  - "ISO 15189:2022 Medical laboratories — Requirements for quality and competence"
  - "CAP Laboratory Accreditation Program checklists; US CLIA regulations (42 CFR Part 493)"
  - "IFCC Working Group on Laboratory Errors and Patient Safety — model quality indicators"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Westgard QC, proficiency testing and pre-analytic error control

*General professional reference. QC frequency, rules and acceptance limits must be set per analyte and analyser according to your accreditation body (ISO 15189, CAP, CLIA or national scheme) and manufacturer instructions.*

**Goal:** detect analytical errors before results reach patients, prove accuracy against
peers, and shrink the pre-analytic phase where most laboratory errors actually happen.

## 1. Internal QC design
- Run control materials (at least two levels spanning decision points) at a defined frequency;
  plot on **Levey-Jennings charts** with the lab's own mean and SD (established from
  ≥ 20 data points on the current lot, not the manufacturer's range (gated: unconfirmed, source is paywalled or blocked)).
- **Westgard multirules** (common set):
  | Rule | Meaning | Usually signals |
  |---|---|---|
  | 1₂s | One control > 2 SD | **Warning** only — inspect other rules |
  | 1₃s | One control > 3 SD | Random error — reject |
  | 2₂s | Two consecutive (or both levels) > 2 SD same side | Systematic error — reject |
  | R₄s | One > +2 SD, another > −2 SD in the same run | Random error — reject |
  | 4₁s | Four consecutive > 1 SD same side | Systematic shift — reject or investigate |
  | 10x̄ | Ten consecutive same side of mean | Systematic shift — reject or investigate |
  Westgard's own page (westgard.com/mltirule.htm) classes 1₂s as the warning and the rest as rejection rules; R₄s applies within a run only, 4₁s and 10x̄ usually across runs, and the classic scheme only checks them after a 1₂s warning (not needed in computerised use).
- Do not use 1₂s as a rejection rule — it causes high false rejection and "repeat until it passes" habits.
- **Sigma metric** = (TEa − |bias|) / CV, using total allowable error from a chosen
  specification (biological variation, CLIA, RCPA). ≥ 6 sigma: simple rules, fewer controls; < 4 sigma:
  more controls and multirules, plus method improvement (gated: unconfirmed, source is paywalled or blocked).

## 2. When QC fails
1. Stop reporting on that analyte; hold results since the last good QC.
2. Look for the cause: reagent/calibrator lot, calibration, instrument maintenance, control material degradation.
3. Fix, recalibrate if needed, rerun QC — **not** just re-run the same control repeatedly.
4. **Assess impact**: re-test patient samples since the last acceptable QC; recall
   and correct released results where clinically significant; document.
5. Record as a nonconformance.

## 3. Proficiency testing / external quality assessment (EQA)
- Treat PT samples exactly like patient samples (same staff, same methods; no referral to another lab — 42 CFR 493.801 bars sending PT samples to another laboratory for any analysis you are certified to perform; confirmed in eCFR).
- Review every report, including passing results with bias trends.
- For unacceptable results: root-cause analysis (clerical, method, calibration, sample handling),
  corrective action, and look-back at patient results. Repeated failures can suspend testing under some regimes.
- Where no PT exists, use alternative assessment (split samples with another lab, etc.).

## 4. Pre-analytic error control (most errors live here)
Common failures: mislabelled or unlabelled specimens, **wrong blood in tube**, wrong tube or
order of draw, haemolysis, clotted samples, insufficient volume, delayed transport, wrong
temperature. Controls:
- Clear **rejection criteria** applied consistently; never relabel a specimen in the lab.
- Positive patient ID and bedside labelling (barcode label printers, electronic ordering).
- Delta checks and HIL indices to catch WBIT and artefacts.
- Track **quality indicators** (rejection rates by ward/collector, haemolysis rate,
  turnaround times, critical-value notification times) and feed back to wards.

## 5. Document control, nonconformance and CAPA
- Controlled SOPs with version, approval, review date; obsolete copies removed.
- Every nonconformance logged, risk-rated, root-caused (5 whys, fishbone), with
  **corrective and preventive action** and effectiveness check.
- Staff competency assessment and training records for every test performed.

## 6. Accreditation readiness
Mock inspections against the current checklist/standard, internal audits on a cycle,
management review of quality indicators, risk register, equipment maintenance and
calibration records, temperature logs, and evidence that issues were closed — inspectors
look for the loop being closed, not for zero problems.

## Gotchas
- New control lot without crossover runs = wrong mean and SD.
- QC passing does not detect pre-analytic errors or patient-specific interferences.
- Manufacturer control ranges are too wide to detect meaningful shifts.

## Verify
- [ ] Lab-specific mean/SD set; QC rules chosen by sigma/TEa, documented per analyte.
- [ ] QC failures stopped release and triggered patient-result look-back.
- [ ] PT/EQA results reviewed, failures root-caused with CAPA.
- [ ] Pre-analytic rejection criteria and quality indicators tracked and fed back.
- [ ] Documents controlled; nonconformances closed with effectiveness checks.
