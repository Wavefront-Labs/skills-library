---
id: health-medicine.radiology-and-medical-imaging.pacs-and-imaging-informatics.pacs-worklist-hanging-protocols-and-prior-comparison
name: pacs-worklist-hanging-protocols-and-prior-comparison
category: health-medicine
field: radiology-and-medical-imaging
product: pacs-and-imaging-informatics
tags: [pacs, ris, imaging-informatics, worklist, hanging-protocol, prior-comparison, dicom, hl7, modality-worklist, accession-number, mpi, patient-merge, image-sharing, xds-i, vendor-neutral-archive, vna, viewer-setup, priority-flags, peer-review, downtime-procedures, radiology-workflow]
level: practitioner
status: draft
description: "Getting a PACS/RIS reading environment right: worklist priority rules, hanging protocols that auto-load priors, DICOM identity mismatches, external image import and downtime fallback."
sources: [DICOM standard PS3 (NEMA), IHE Radiology technical framework (SWF, XDS-I, PIR profiles), SIIM imaging informatics body of knowledge, RCR guidance on PACS and radiology IT]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PACS worklist, hanging protocols and prior comparison

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** the right study, on the right patient, opens with the right prior next to it, in
the right order of clinical urgency — so readers spend time reading, not hunting.

Vendor menus differ (e.g. Sectra, Philips, GE, Agfa, Fujifilm, Change Healthcare/Optum);
the concepts below are vendor-neutral. Status: draft — exact settings names unverified
per vendor.

## 1. How the pieces fit
- **RIS** holds orders, scheduling, reports. **Modality worklist (DICOM MWL)** pushes
  patient demographics + accession to the scanner. **PACS** stores and displays images;
  a **VNA** may archive across departments. **HL7** carries orders/results between EHR,
  RIS and PACS.
- **Accession number** links an order, its images and its report. Most "missing images"
  problems are an accession or patient-ID mismatch.

## 2. Worklist design
- Filters by modality, body part, subspecialty, location (ED, inpatient, outpatient) and
  **priority** (stat/critical, urgent, routine).
- Rules: stat ED and stroke studies float to the top with a visible timer; urgent
  inpatient next; outpatients by target turnaround.
- Show **study status** (in progress, complete, preliminary, final) and lock a study when
  opened so two people don't read it.
- Review turnaround metrics weekly; adjust rules rather than relying on readers
  cherry-picking.

## 3. Hanging protocols
- Define per modality + body part + number of series: e.g. CT chest — current axial lung
  and soft-tissue on the left, **matching prior** on the right, synced scrolling, MPR on
  demand.
- Mammography: standard CC/MLO mirror layout with priors.
- **Prior selection rules:** same body region, most recent, then relevant other modalities
  (e.g. PET for a CT chest). Too-strict rules hide useful priors; too-loose rules load the
  wrong body part.
- Default window/level presets per series; registration/sync across studies for
  follow-up measurements.

## 4. Identity and data-integrity problems
- **Wrong patient on images** (e.g. manually entered demographics at the modality): stop
  reading, notify PACS admin; corrections need a documented merge/split process with
  audit trail — never "fix" by renaming locally.
- Duplicate patients across sites → MPI (master patient index) reconciliation.
- Missing series: check modality send queue and PACS receive logs before re-scanning.

## 5. External images
- Import via image-sharing network (IHE XDS-I), cloud exchange, or CD/DVD.
- **Import reconciliation** (IHE PIR): map external IDs to local MRN/accession so priors
  link up; flag as "outside study" for reporting/billing rules.
- Scan external discs for malware per IT policy; never install viewers from discs on
  reading stations.

## 6. Downtime
- Planned and unplanned downtime procedures: modality local storage, temporary paper or
  standalone reporting, **reconciliation after recovery** (every study sent, every
  preliminary report re-entered and finalised).
- Test the downtime viewer quarterly.

## Gotchas
- Hanging protocol silently loading a prior from a different body part.
- Readers working around the worklist (cherry-picking) → stat studies wait.
- Local demographic edits creating orphan studies.
- Forgetting post-downtime reconciliation → reports never reach the EHR.

## Verify
- [ ] Stat studies appear at the top with timers; locking works.
- [ ] Hanging protocols tested on sample studies per modality, priors correct.
- [ ] Identity correction process documented and audited.
- [ ] External import maps to local IDs and is labelled.
- [ ] Downtime procedure tested; post-recovery reconciliation checklist exists.
