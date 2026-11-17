---
id: health-medicine.pathology-and-laboratory-medicine.laboratory-information-systems.lis-autoverification-interfaces-and-digital-pathology
name: lis-autoverification-interfaces-and-digital-pathology
category: health-medicine
field: pathology-and-laboratory-medicine
product: laboratory-information-systems
tags: [laboratory-information-systems, lis, lims, pathology-and-laboratory-medicine, anatomic-pathology-lis, specimen-tracking, barcode, chain-of-custody, autoverification, auto-validation, clsi-auto10, auto15, delta-check, critical-values, result-verification, hl7, hl7-v2, oru, orm, fhir, loinc, snomed-ct, ucum, middleware, instrument-interface, astm, interface-validation, digital-pathology, whole-slide-imaging, wsi, dicom-wsi, primary-diagnosis-validation, cap-wsi-validation, downtime-procedures, epic-beaker, cerner-pathnet, sunquest]
level: practitioner
status: draft
description: "Running an LIS safely: specimen tracking, autoverification rules, HL7/LOINC interfaces and their validation, critical-value workflows, downtime plans, and validating whole-slide imaging."
sources:
  - "CLSI AUTO10 Autoverification of Clinical Laboratory Test Results; CLSI AUTO15 Autoverification of Medical Laboratory Results for Specific Disciplines"
  - "HL7 Version 2.5.1 Implementation Guide: Lab Results Interface (LRI); HL7 FHIR R4 DiagnosticReport/Observation resources"
  - "Regenstrief Institute. LOINC Users' Guide; SNOMED International documentation"
  - "Evans AJ et al. Validating Whole Slide Imaging Systems for Diagnostic Purposes in Pathology: CAP Guideline Update. Arch Pathol Lab Med 2022"
  - "Pantanowitz L, Henricks WH, Beckwith BA. Medical laboratory informatics. Clin Lab Med 2007; Pantanowitz L et al. Pathology Informatics: Theory and Practice"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# LIS autoverification, interfaces and digital pathology

*General professional reference. Vendor screens and configuration differ between products (e.g. Epic Beaker, Oracle Health PathNet, Sunquest, Clinisys and others) — this skill describes vendor-neutral workflows; exact menu paths are not given and should be taken from your vendor documentation. Validation requirements follow your accreditation body.*

**Goal:** make the laboratory information system move the right result to the right
patient's record quickly and safely: every specimen tracked, routine results released
automatically only when safe, interfaces that cannot silently corrupt data, and a plan for when the system is down.

## 1. Specimen tracking
- Barcoded labels at collection tied to the order (positive patient ID); scan at each
  step (receipt, accessioning, aliquoting, analysis, storage) to create a **chain of custody**.
- Anatomic pathology: track specimen → block → slide with 2D barcodes; scanners at the
  grossing station, embedding, microtomy and sign-out reduce mix-ups.
- Track **in-lab and total turnaround times** from these timestamps; set alerts for overdue specimens.

## 2. Autoverification (auto-validation)
Rules that release results without manual review when all checks pass; exceptions go to a
technologist queue. Typical rule elements (CLSI AUTO10/AUTO15):
- Instrument flags and error codes absent; QC acceptable for the run.
- Result within the analytical measurement range (dilution needed?).
- **HIL indices** below analyte-specific limits.
- **Delta check** against the patient's previous result within a time window.
- Critical-value range → hold for manual call, never auto-release silently.
- Consistency rules (e.g. anion gap, calculated vs measured values).
**Validate every rule before go-live** with test cases for each branch (pass and fail),
document, and **re-validate after any change** (software update, new analyser, new reference interval).
Monitor the autoverification rate and look at a sample of auto-released results periodically.

## 3. Interfaces
- Orders (HL7 v2 **ORM/OML**) in and results (**ORU**) out between EHR and LIS; analyser
  interfaces (ASTM or HL7) often through **middleware**. FHIR APIs increasingly used for
  newer integrations.
- Code results with **LOINC** (test identity), units in **UCUM**, and specimen/diagnoses
  with **SNOMED CT** where adopted; consistent coding is what makes data usable across systems.
- **Interface validation:** for each test, send results end to end and compare what the
  clinician sees in the EHR with the instrument value — value, units, reference interval,
  flags, comments, corrected-result behaviour, and long text (truncation is a classic failure).
- Monitor interface queues and error logs daily; a stuck queue means results not delivered.

## 4. Critical values and result corrections
- Critical-value list agreed with clinicians; LIS prompts documentation of who was called,
  when, by whom, and read-back confirmation.
- **Corrected reports** must clearly show the original and corrected value and notify the
  recipient — never silently overwrite.

## 5. Downtime procedures
Planned and unplanned downtime: pre-printed labels/requisitions, manual result reporting
forms, a priority order for back-entry, verification of interfaced results after recovery,
and regular downtime drills.

## 6. Digital pathology / whole-slide imaging (WSI)
- Scanner, image management system and viewer, integrated with the AP LIS (case list,
  slide barcode → image linkage).
- **Validate for primary diagnosis** per the CAP guideline: commonly at least 60 cases
  per application (e.g. H&E), representative of the case mix, compared with glass after a
  washout period (≥ 2 weeks), aiming for high intraobserver concordance; separate validation
  for frozen sections, cytology, IHC if used.
- Watch for scan failures: out-of-focus areas, missed tissue (faint or small fragments),
  pen marks — QC each scan before sign-out. Some materials (e.g. cytology with depth, birefringence) remain challenging.
- Standards: DICOM WSI supports interoperability; storage planning is substantial.
- AI tools: validate locally and understand intended use before relying on them.

## Gotchas
- A reference-interval change in the LIS not mirrored in the EHR shows misleading flags.
- Autoverification rules quietly break after software upgrades — re-test.
- Free-text comments may be truncated or lost across interfaces.
- Barcode label quality (printer, size) causes scanning failures that staff work around unsafely.

## Verify
- [ ] Specimen barcodes scanned at each step; TAT dashboards live.
- [ ] Each autoverification rule validated with pass/fail test cases and re-validated after changes.
- [ ] Interfaces validated end to end for value, units, flags, comments and corrections.
- [ ] Critical-value and corrected-report workflows documented in the LIS.
- [ ] Downtime procedure tested.
- [ ] WSI validated per current CAP guideline before primary diagnosis use.
