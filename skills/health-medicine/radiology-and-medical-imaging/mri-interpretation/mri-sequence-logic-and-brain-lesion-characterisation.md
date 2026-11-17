---
id: health-medicine.radiology-and-medical-imaging.mri-interpretation.mri-sequence-logic-and-brain-lesion-characterisation
name: mri-sequence-logic-and-brain-lesion-characterisation
category: health-medicine
field: radiology-and-medical-imaging
product: mri-interpretation
tags: [radiology, mri, neuroradiology, t1, t2, flair, dwi, adc, swi, gre, gadolinium, contrast-enhancement, ring-enhancement, restricted-diffusion, t2-shine-through, lesion-characterisation, brain-tumour, abscess, multiple-sclerosis, mcdonald-criteria, mri-artefacts, mri-safety]
level: practitioner
status: draft
description: "Reading brain MRI by sequence logic: what each sequence shows, the DWI/ADC check, SWI for blood and calcium, enhancement patterns, and a structured differential for a focal lesion."
sources: [Osborn's Brain Imaging Pathology and Anatomy 3rd ed, MAGNIMS-CMSC-NAIMS consensus on MRI in MS 2021, McDonald criteria 2017, ACR Manual on MR Safety 2024]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MRI sequence logic and brain lesion characterisation

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** know what each sequence is for, then use the combination of signals to narrow
a focal brain lesion to a short, ranked differential.

## 1. What each sequence tells you
| Sequence | Bright | Use it for |
|---|---|---|
| T1 | Fat, subacute blood (methaemoglobin), gadolinium, melanin, protein, some calcium | Anatomy; pre/post-contrast comparison |
| T2 | Fluid, oedema, most pathology | Lesion detection |
| FLAIR | Pathology with CSF suppressed | Periventricular/cortical lesions, SAH, meningitis |
| DWI + **ADC** | Restricted diffusion (bright DWI, **dark ADC**) | Acute infarct, abscess, cellular tumour, epidermoid |
| SWI/GRE | Blooms dark: blood products, calcium, iron, air | Microbleeds, haemorrhagic transformation, DAI |
| T1 post-gad | Blood–brain barrier breakdown | Tumour, infection, active demyelination |

- **Always read DWI with ADC.** Bright DWI with bright ADC = **T2 shine-through**, not
  restriction.
- SWI phase images distinguish calcium from blood (opposite phase; vendor-dependent
  convention — check yours).
- Pre-contrast T1 is mandatory to call enhancement: intrinsic T1 brightness can mimic it.

## 2. Characterising a focal lesion — the questions
1. **Where:** intra-axial vs extra-axial (CSF cleft, dural tail, buckled grey matter →
   extra-axial, e.g. meningioma). Grey vs white matter; vascular territory?
2. **How many:** single vs multiple (multiple → metastases, abscesses, demyelination,
   emboli).
3. **Signal:** T1, T2/FLAIR, DWI/ADC, SWI.
4. **Enhancement pattern:** none / solid / ring / open-ring / leptomeningeal / dural.
5. **Mass effect and oedema** relative to lesion size.
6. **Patient:** age, immune status, known cancer, acute vs chronic symptoms.

## 3. Ring-enhancing lesion — classic discriminators
- **Abscess:** smooth thin ring, **restricted diffusion in the centre**, T2-dark rim.
- **High-grade glioma:** thick irregular ring, central necrosis does *not* restrict,
  infiltrative T2/FLAIR signal crossing corpus callosum.
- **Metastasis:** often multiple, at grey–white junction, oedema out of proportion.
- **Tumefactive demyelination:** **open ring** (incomplete, open toward cortex), less
  mass effect than expected.
- Others: lymphoma (immunocompromised — ring; immunocompetent — solid, restricts,
  periventricular), resolving haematoma, subacute infarct.

## 4. White-matter lesions and MS
- Supportive features: periventricular lesions perpendicular to ventricles (Dawson's
  fingers), juxtacortical/cortical, infratentorial, spinal cord; **central vein sign**
  on SWI.
- McDonald 2017: dissemination in space (≥ 1 T2 lesion in ≥ 2 of 4 typical regions) and
  in time (simultaneous enhancing and non-enhancing lesions, or a new lesion on follow-up).
- Non-specific small deep white-matter foci in older or vascular-risk patients are usually
  small-vessel disease — avoid over-calling MS.

## 5. Artefacts and safety
- Susceptibility from metal/dental work, motion, flow (pulsation in posterior fossa),
  chemical shift. Know what yours look like before calling pathology.
- Screen implants against conditional labels (field strength, SAR limits); gadolinium:
  check renal function for group I agents, document prior reactions.

## Gotchas
- Calling restriction without checking ADC.
- Calling enhancement without a pre-contrast T1.
- Missing a small extra-axial lesion because only brain windows on axial were reviewed.
- Over-reading non-specific white-matter hyperintensities as demyelination.

## Verify
- [ ] Every sequence reviewed, including DWI with ADC and SWI.
- [ ] Location, number, signal, enhancement, mass effect recorded for each lesion.
- [ ] Differential ranked and tied to clinical context.
- [ ] Recommendation (biopsy, follow-up interval, spectroscopy/perfusion) stated.
