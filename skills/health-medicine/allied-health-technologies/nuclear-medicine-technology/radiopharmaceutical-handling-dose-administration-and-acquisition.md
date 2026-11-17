---
id: health-medicine.allied-health-technologies.nuclear-medicine-technology.radiopharmaceutical-handling-dose-administration-and-acquisition
name: radiopharmaceutical-handling-dose-administration-and-acquisition
category: health-medicine
field: allied-health-technologies
product: nuclear-medicine-technology
tags: [allied-health-technologies, nuclear-medicine-technology, nuclear-medicine, nmt, radiopharmaceutical, tc-99m, technetium, f-18-fdg, pet-ct, spect, gamma-camera, dose-calibrator, generator-elution, molybdenum-breakthrough, radiochemical-purity, unit-dose, extravasation, misadministration, alara, time-distance-shielding, daily-qc, uniformity-flood, cor, suv]
level: practitioner
status: draft
description: "Nuclear medicine technologist practice: dose calibrator and camera QC, Tc-99m prep and purity checks, dose verification and injection, FDG patient prep, acquisition setup and radiation protection."
sources: [SNMMI procedure standards and technologist scope of practice, US NRC 10 CFR Part 35 (and equivalent national regulations), EANM procedure guidelines, IAEA nuclear medicine resources manual]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Radiopharmaceutical handling, dose administration and acquisition

> General clinical/professional reference, not a substitute for your licence conditions, radiation safety officer, package inserts or departmental procedures. Regulatory limits differ by country.

**Goal:** the right radiopharmaceutical, in the right activity, to the right patient,
acquired correctly — while keeping staff and public dose ALARA.

## 1. Daily quality control
- **Dose calibrator:** constancy check with a long-lived source (e.g. Cs-137) daily;
  linearity, accuracy and geometry on their scheduled intervals.
- **Gamma camera:** extrinsic or intrinsic **uniformity flood** daily before patients;
  centre-of-rotation and resolution checks on schedule for SPECT.
- **PET:** daily detector check / blank scan per vendor; periodic SUV calibration with a
  phantom — PET SUVs are only as good as the cross-calibration with the dose calibrator.
- Survey meters: battery and check-source response before use. Record everything.

## 2. Generator and kit preparation (Tc-99m)
- Elute the Mo-99/Tc-99m generator aseptically; assay the eluate.
- **Mo-99 breakthrough** check on each elution (regulatory limit 0.15 µCi Mo-99 per
  mCi Tc-99m at administration in the US); Al3+ breakthrough per policy.
- Reconstitute kits per insert (activity, volume, incubation/heating), aseptic technique
  in the shielded hood.
- **Radiochemical purity** testing (thin-layer chromatography) for kits where required;
  free pertechnetate shows as thyroid/stomach/salivary uptake on images.
- Label vials and syringes: agent, activity, volume, time, initials.

## 3. Dose administration
1. Two identifiers; confirm exam, agent and prescribed activity (adult or weight-based
   paediatric).
2. **Assay the dose** in the calibrator before administration; within the prescribed
   range (often ±20%) or per the written directive. Recalculate for decay if delayed.
3. Pregnancy and breastfeeding status — some agents require interrupting breastfeeding
   for a specified time.
4. Use shielded syringe; secure IV access with saline flush; for tracers where
   **extravasation** spoils quantification (FDG, bone agents), confirm patency and image
   the injection site if in doubt.
5. Record time, activity, site and residual activity.
Wrong patient, wrong agent, or activity outside limits = possible **reportable
medical event** — report via the RSO immediately.

## 4. Patient preparation examples
- **FDG PET:** fast 4–6 h, blood glucose check (thresholds commonly < ~11 mmol/L / 200 mg/dL
  — policy varies), quiet warm uptake room 60 min, avoid talking/chewing/exercise,
  void before scanning.
- **Myocardial perfusion:** caffeine abstinence before pharmacological stress
  (vasodilator agents).
- **Thyroid/I-131:** iodine-containing contrast and certain medications interfere.

## 5. Acquisition
Collimator matched to energy (LEHR for Tc-99m, medium/high energy for In-111, I-131),
energy window centred on the photopeak, patient as close to the detector as possible,
correct matrix, counts/time per protocol. Check for motion and repeat if needed.

## 6. Radiation protection
**Time, distance, shielding**: tongs, syringe and vial shields, L-block. Wear ring and
body dosimeters. Survey and wipe-test work areas; store waste for decay with labels.
Handle spills per the spill kit procedure.

## Gotchas
- Forgetting decay correction for delayed injections leads to under-dosing.
- Dose calibrator setting on the wrong isotope gives wrong activity.
- Patient urine contamination is the commonest artefact on bone scans.

## Verify
- [ ] Calibrator, camera and survey-meter QC done and logged before first patient.
- [ ] Eluate and kit purity checks recorded.
- [ ] Dose assayed, within range, administered to correctly identified patient.
- [ ] Prep conditions met (glucose, fasting, medication holds).
- [ ] Waste, surveys and dosimetry handled per licence.
