---
id: health-medicine.radiology-and-medical-imaging.nuclear-medicine-and-pet.fdg-pet-ct-reading-and-pitfalls
name: fdg-pet-ct-reading-and-pitfalls
category: health-medicine
field: radiology-and-medical-imaging
product: nuclear-medicine-and-pet
tags: [nuclear-medicine, pet, pet-ct, fdg, 18f-fdg, suv, suvmax, deauville-score, lugano-classification, perci, physiological-uptake, brown-fat, false-positive, blood-glucose, patient-preparation, mip, attenuation-correction, psma-pet, tracer-selection, oncology-imaging]
level: practitioner
status: draft
description: "Reading FDG PET-CT: patient prep and glucose checks, a systematic MIP-then-fused read, SUV caveats, Deauville scoring for lymphoma, and the physiological uptake that fools people."
sources: [EANM procedure guidelines for FDG PET/CT tumour imaging v2.0 2015, Lugano classification Cheson 2014, SNMMI procedure standard for FDG PET/CT, PERCIST Wahl 2009]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FDG PET-CT reading and pitfalls

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** produce a PET-CT report that separates true disease from physiological and
inflammatory uptake, with reproducible numbers for response assessment.

## 1. Was the scan done right? (check before reading)
- **Fasting ≥ 4–6 h**; blood glucose recorded — EANM suggests rescheduling above about
  11 mmol/L (200 mg/dL) for oncology; follow local limits. Recent insulin drives FDG
  into muscle and fat.
- **Uptake time ~ 60 min** (± 5–10 min, and the same on follow-up scans for
  comparability).
- Injected activity, weight and height recorded correctly — **SUV is wrong if weight is
  wrong**.
- Recent chemotherapy, G-CSF (diffuse marrow/splenic uptake), radiotherapy, surgery,
  biopsy, infection — note dates.
- Warm room / beta-blocker if brown fat was a problem previously.

## 2. Read in a fixed order
1. **MIP (rotating maximum-intensity projection)** — global pattern, asymmetry,
   unexpected foci.
2. **Fused PET-CT** slice by slice, every region: head/neck, thorax, abdomen, pelvis,
   skeleton, limbs in field.
3. **Non-attenuation-corrected (NAC) images** when a focus sits near metal or dense
   contrast (attenuation-correction artefact).
4. **CT component as a diagnostic CT** — incidental findings, lung nodules too small
   for PET resolution (< ~8 mm can be falsely PET-negative).

## 3. Physiological and benign uptake to know
Brain, myocardium (variable), **brown fat** (neck, supraclavicular, paravertebral —
symmetric, fat density on CT), tonsils/Waldeyer ring, vocal cord (unilateral palsy →
contralateral cord avid), thymus in young adults, bowel (diffuse; metformin causes
intense colonic uptake), urinary tract, endometrium/ovary mid-cycle, muscles (talking,
chewing, recent exercise), post-surgical and post-radiotherapy inflammation,
sarcoid/granulomatous disease, infection, injection site extravasation.

## 4. Quantification
- **SUVmax** is noisy (single voxel); **SUVpeak** (1 mL sphere) and SUL (lean-body-mass
  normalised; PERCIST) are more reproducible.
- Compare like with like: same scanner/reconstruction where possible, same uptake time,
  same normalisation. Report reference uptake (liver, mediastinal blood pool).
- Small lesions under-read SUV (partial volume effect).

## 5. Lymphoma: Deauville 5-point scale (Lugano)
1 no uptake; 2 ≤ mediastinal blood pool; 3 > mediastinum but ≤ liver; 4 moderately
> liver; 5 markedly > liver (2–3× liver) and/or new lesions. Interim/end-of-treatment
scores **1–3 = complete metabolic response** in most contexts (3 may be treated as
inadequate in de-escalation trials — follow the protocol). X = new area unlikely
lymphoma.

## 6. Tracer choice — FDG isn't always right
Low-FDG tumours: well-differentiated neuroendocrine (use **Ga-68 DOTATATE**), prostate
(**PSMA PET**), mucinous and lobular breast, some HCC, RCC. Choose the tracer to the
question.

## Gotchas
- Wrong weight entry → every SUV on the report wrong.
- Calling malignancy on G-CSF marrow uptake or post-biopsy inflammation.
- Calling "no metabolic activity" in a sub-centimetre lung nodule.
- Comparing SUV across scanners with different reconstruction (EARL harmonisation helps).

## Verify
- [ ] Glucose, uptake time, weight and confounding treatments recorded.
- [ ] MIP, fused, NAC and diagnostic CT all reviewed.
- [ ] Each reported lesion has location, SUV metric used, size and comparison.
- [ ] Lymphoma studies scored with Deauville and reference regions stated.
- [ ] Physiological/benign explanations considered and stated where relevant.
