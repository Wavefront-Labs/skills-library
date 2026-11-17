---
id: health-medicine.clinical-research-operations.edc-and-ctms-systems.edc-ctms-etmf-validation-and-audit-trails
name: edc-ctms-etmf-validation-and-audit-trails
category: health-medicine
field: clinical-research-operations
product: edc-and-ctms-systems
tags: [edc-and-ctms-systems, clinical-research-operations, edc, electronic-data-capture, ctms, clinical-trial-management-system, etmf, tmf-reference-model, irt, epro, medidata-rave, oracle-clinical-one, veeva-vault, redcap, 21-cfr-part-11, eu-gmp-annex-11, audit-trail, electronic-signature, computerised-system-validation, csv, gamp-5, uat, role-based-access, ich-e6-r3]
level: practitioner
status: verified
description: "Work in EDC, CTMS and eTMF platforms compliantly: 21 CFR Part 11 / EU Annex 11 controls, role-based access, audit-trail review, UAT for study builds, and TMF Reference Model filing."
sources:
  - "21 CFR Part 11 (Electronic Records; Electronic Signatures)"
  - "FDA Guidance: Electronic Systems, Electronic Records, and Electronic Signatures in Clinical Investigations — Questions and Answers (2024)"
  - "EMA Guideline on computerised systems and electronic data in clinical trials (2023)"
  - "EudraLex Volume 4, Annex 11: Computerised Systems"
  - "ISPE GAMP 5: A Risk-Based Approach to Compliant GxP Computerized Systems (2nd ed., 2022)"
  - "TMF Reference Model (current version)"
  - "ICH E6(R3) Guideline for Good Clinical Practice (Step 4, January 2025), data governance section"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# EDC, CTMS and eTMF: validation, access and audit trails

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** use trial systems (EDC, IRT, ePRO, CTMS, eTMF — Medidata Rave, Oracle Clinical
One, Veeva Vault, REDCap and peers) so that every record is attributable, every change is
traceable, the study build does what the protocol says, and the TMF tells the trial's
story without gaps.

## 1. Know which system holds what
| System | Holds | Key compliance point |
|---|---|---|
| EDC | eCRF data, queries, investigator e-signature | Audit trail on every data point; casebook sign-off |
| IRT/IWRS | Randomisation, kit assignment, supply | Blinding: unblinded roles strictly separated |
| ePRO/eCOA | Participant-entered data | Site must not edit participant data; data-change requests via vendor |
| CTMS | Sites, visits, enrolment, monitoring reports, actions, payments | Operational record; feeds oversight |
| eTMF | Essential records | Filing to TMF Reference Model zones/sections/artifacts |

## 2. Validation and study build (sponsor/CRO side)
- Platform validated by vendor and qualified by sponsor using a risk-based approach
  (GAMP 5 2nd ed.); the **study build** is validated per study.
- UAT: test scripts traced to the protocol and edit-check spec — visit structure,
  dynamic forms, derivations, every edit check (positive and negative case), IRT
  randomisation and stratification, role permissions. Record expected vs actual, defects,
  retest, and sign-off **before** go-live.
- Mid-study changes (post-amendment) go through change control and regression UAT; know
  whether a migration touches existing data.

## 3. Access control
- Named accounts only, never shared; role-based access matched to the delegation log
  (CRA read/SDV, CRC entry, PI sign, DM query).
- Training completed before access; access removed promptly when people leave (check at
  every monitoring visit; target e.g. ≤ 5 working days, per SOP).
- Unblinded roles (pharmacist, unblinded monitor) segregated in IRT and EDC.

## 4. Electronic records and signatures
21 CFR Part 11 controls (with FDA's narrowed scope and enforcement discretion), EU Annex 11
and the EMA 2023 guideline converge on:
- **Audit trail:** 21 CFR 11.10(e) requires secure, computer-generated, time-stamped audit trails recording date/time of operator entries and actions that create, modify or delete records, without obscuring earlier data, retained as long as the records. ICH E6(R3) 4.2.2 adds that initial entries and later changes are documented "including, where appropriate, the reason for the change", that audit trails are not disabled or modified except in rare, logged cases, and are interpretable for review.
- **E-signatures:** the signed record shows printed name, date/time and meaning (11.50(a)); non-biometric signatures use at least two distinct identification components such as ID code and password (11.200(a)(1)) and are used only by their genuine owners; users certify to FDA that e-signatures are the legally binding equivalent of handwritten ones (11.100(c)).
- ICH E6(R3) 4.2.3: review of trial data, audit trails and other metadata should be a planned, risk-based activity adapted to the trial. The EMA computerised-systems guideline (adopted 7 Mar 2023, effective 10 Sep 2023 per an EMA inspection annex) and FDA's Part 11 Q&A guidance have their own wording on audit-trail review and investigator control of data: read the current texts (not retrieved in full for this review).

## 5. Audit-trail review in practice
Pick critical data (primary endpoint, eligibility, SAEs, dosing) and look for:
- Changes long after entry, or after SDV/lock attempts.
- Bulk changes by one user in a short window.
- Entries outside site working hours or from unexpected roles.
- Repeated changes to the same value toward eligibility thresholds.
Document the review, findings and follow-up.

## 6. eTMF filing
- File contemporaneously (target e.g. within 30 days of finalisation — set in the TMF plan).
- Metadata: artifact type per TMF Reference Model, site, country, document date, version.
- QC a sample for correct artifact, legibility, signatures, completeness; track
  completeness against the expected-document list per milestone.
- Certified copies of paper originals per a defined process before destruction.

## Gotchas
- Spreadsheets used for trial decisions are computerised systems too.
- System-generated "reason for change" defaults ("data entry error") hide the real reason.
- Data exports for analysis must be versioned; uncontrolled copies are not the record.
- Decommissioning a system: archive data and audit trails readable for the full retention period.

## Verify
- [ ] UAT evidence signed before go-live and after each build change.
- [ ] User list reconciled to delegation log; leavers removed.
- [ ] Audit trails captured, unalterable and reviewed for critical data.
- [ ] E-signatures carry name, date/time and meaning.
- [ ] eTMF completeness and QC metrics within TMF plan targets.
