---
id: health-medicine.allied-health-technologies.radiation-therapy-delivery.patient-setup-immobilisation-and-image-guided-verification
name: patient-setup-immobilisation-and-image-guided-verification
category: health-medicine
field: allied-health-technologies
product: radiation-therapy-delivery
tags: [allied-health-technologies, radiation-therapy-delivery, radiation-therapist, radiotherapy, therapeutic-radiographer, linac, linear-accelerator, igrt, cbct, kv-imaging, portal-imaging, immobilisation, thermoplastic-mask, vac-lok, tattoos, setup-tolerance, action-level, couch-shift, sgrt, surface-guidance, timeout, record-and-verify, mosaiq, aria, dibh, bladder-filling]
level: practitioner
status: draft
description: "Radiation therapist daily delivery: timeout and record-and-verify checks, immobilisation, setup to marks, CBCT/kV matching against tolerances, couch shifts, anatomy changes and when to stop."
sources: [AAPM TG-142 and TG-179 (IGRT QA), ASTRO Safety is No Accident, ASRT radiation therapy practice standards, UK Royal College of Radiologists/SCoR IGRT guidance (On Target)]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patient setup, immobilisation and image-guided verification

> General clinical/professional reference, not a substitute for the departmental protocol, the treatment prescription, physics instructions or the treating radiation oncologist.

**Goal:** every fraction delivers the planned dose to the planned place. Most serious
radiotherapy incidents are setup, identification or data-transfer errors, not machine
failures.

## 1. Before the patient enters
- Machine morning QA passed (physics sign-off).
- Open the patient in **record-and-verify (R&V)**: correct plan, fraction number, field
  list, prescribed fraction dose, any notes/alerts (pacemaker, bolus, bladder protocol,
  DIBH, special instructions).
- Check for **plan changes or adaptive replans** since the last fraction.

## 2. Timeout
At the console and at the couch, two therapists confirm: patient identity (two
identifiers + photo), site, laterality, plan/field set, immobilisation, accessories
(bolus, wedge, applicator), imaging protocol. Never skip it for a "regular" patient.

## 3. Immobilisation and setup
- Reproduce the simulation position exactly: thermoplastic mask (head and neck),
  vacuum bag, breast board angles, knee/foot supports — indexed to the couch at the
  recorded positions.
- Align skin marks/tattoos with the room lasers; level the patient (no rotation)
  before shifts. **Surface-guided RT (SGRT)** systems can replace or supplement marks.
- Apply planned shifts from reference marks to isocentre as documented; two people check.
- Prep protocols: comfortably full bladder / empty rectum for pelvis, breath-hold
  coaching for DIBH (left breast), fasting for some upper abdominal sites.

## 4. Image guidance
1. Acquire per protocol (kV pair, CBCT, MV portal; daily or as specified).
2. Match to the planning reference on the protocol structures: bone, soft tissue,
   fiducial markers or the target itself, with the correct region of interest.
3. Compare shifts to **tolerance/action levels** in the protocol (e.g. a few mm and
   a few degrees — site-specific). Within tolerance → apply and treat. Outside → re-setup
   and re-image; repeated large shifts → stop and contact physics/oncologist.
4. Assess anatomy, not just alignment: weight loss (loose mask), tumour shrinkage,
   bladder/rectal filling, lung changes. Flag for review or replan.
5. Watch for **wrong-isocentre matches** (vertebral level misidentification is a classic).

## 5. Delivery
- Room clear; monitor patient on CCTV and intercom; beam hold for motion, coughing or
  breath-hold loss.
- Never override an interlock or R&V tolerance without a documented authorisation.
- Record delivered fraction, imaging decision and shifts; note skin reactions and
  side effects for review clinic.

## 6. Stop and escalate if
Identity doubt, plan mismatch, R&V override request, out-of-tolerance shifts that won't
resolve, unexpected machine behaviour, patient deterioration, pregnancy disclosure, or
a pacemaker issue. Incidents and near misses go to the local reporting system.

## Gotchas
- Re-used mask that no longer fits after weight loss → systematic shifts.
- Treating with bolus missing or present when not planned changes skin dose.
- Changes to the planning image mid-course must be linked to the correct reference.

## Verify
- [ ] Morning QA passed; R&V plan and fraction confirmed.
- [ ] Two-person timeout completed with photo ID.
- [ ] Immobilisation indexed and reproduced; shifts double-checked.
- [ ] Image match on the right anatomy, shifts within tolerance, anatomy changes flagged.
- [ ] Delivery, imaging decision and side effects documented.
