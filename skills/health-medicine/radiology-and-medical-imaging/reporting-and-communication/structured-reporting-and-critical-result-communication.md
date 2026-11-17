---
id: health-medicine.radiology-and-medical-imaging.reporting-and-communication.structured-reporting-and-critical-result-communication
name: structured-reporting-and-critical-result-communication
category: health-medicine
field: radiology-and-medical-imaging
product: reporting-and-communication
tags: [radiology, radiology-report, structured-reporting, report-template, impression, critical-results, urgent-findings, closed-loop-communication, unexpected-findings, incidental-findings, fleischner, addendum, discrepancy, mdt, rads-systems, bi-rads, li-rads, pi-rads, ti-rads, hedging, acr-practice-parameter]
level: practitioner
status: draft
description: "Writing radiology reports that get acted on: structure, a decisive impression, RADS categories, closed-loop critical and unexpected result communication, and addendum/discrepancy practice."
sources: [ACR Practice Parameter for Communication of Diagnostic Imaging Findings 2020, RCR Standards for the communication of radiological reports and fail-safe alert notification 2016, RSNA RadReport template library, Fleischner Society 2017 guidelines]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Structured reporting and critical-result communication

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** a report the referrer reads in 15 seconds and acts on correctly, and a
communication trail that guarantees urgent findings reached a responsible person.

## 1. Report structure
1. **Clinical indication** (as received, plus key history found).
2. **Technique:** modality, contrast (agent, volume, phase), limitations.
3. **Comparison:** date and modality of priors — or "none available".
4. **Findings:** by organ system or template; pertinent negatives that answer the
   question ("no pulmonary embolism to subsegmental level").
5. **Impression / conclusion:** the part most people read.

Templates (RSNA RadReport, society templates) reduce omissions; free text is fine for
nuance — hybrid works best.

## 2. Writing the impression
- **Answer the question first**, then the most important other findings, ranked.
- Numbered, short, decisive: "1. Acute appendicitis without perforation."
- Give a **specific recommendation** with test and interval only when it's evidence-
  based (e.g. Fleischner for incidental lung nodules, ACR white papers for incidental
  adrenal/renal/liver lesions), not reflexive "clinical correlation recommended".
- Use a **RADS category** where one applies (BI-RADS, LI-RADS, PI-RADS, TI-RADS,
  Lung-RADS, O-RADS) — they map to management.
- Calibrated hedging: if uncertain, say how likely ("probably", "cannot exclude") and
  what would resolve it. Avoid stacking hedges.

## 3. Critical and urgent results
- Define tiers locally, e.g.:
  - **Critical (minutes):** tension pneumothorax, aortic dissection, large PE with RV
    strain, intracranial haemorrhage, misplaced NG tube, free air.
  - **Urgent (hours):** new mass suggestive of malignancy, abscess, impending fracture.
  - **Unexpected significant (days):** incidental cancer requiring follow-up.
- **Closed-loop:** direct conversation (phone or in person) with a clinician who can act;
  confirm read-back. A report in the system or a voicemail alone is not communication.
- **Document** in the report: who, role, date, time, method: "Discussed with Dr X
  (ED registrar) by phone at 14:32."
- Use the electronic fail-safe alert system for unexpected cancer findings so the
  follow-up can't be lost when the patient leaves hospital.

## 4. Addenda and discrepancies
- New information or a correction after sign-off → **addendum**, never silent edit.
  If clinically significant, communicate the change directly as for a critical result.
- Discrepancy meetings (REALM / peer learning): anonymised, learning-focused; log
  errors without blame.

## 5. MDT input
Prepare by re-reviewing images (not just the report), stating stage/measurements with
the staging system, and recording the imaging opinion given in the MDT outcome.

## Gotchas
- Burying the critical finding in the middle of the findings section.
- Measurements without image/series numbers → follow-up readers can't find them.
- "Correlate clinically" with no defined action.
- Laterality errors — read back "left/right" in the impression before signing.
- Dictation/voice-recognition errors ("no" ↔ "new"); proofread every impression.

## Verify
- [ ] Clinical question answered in line 1 of the impression.
- [ ] Comparison stated; measurements have series/image numbers.
- [ ] Recommendations cite a guideline and give test + interval.
- [ ] Critical/urgent results communicated closed-loop and documented with time.
- [ ] Report proofread for laterality and negation errors.
