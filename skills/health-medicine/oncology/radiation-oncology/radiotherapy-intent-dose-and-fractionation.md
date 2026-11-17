---
id: health-medicine.oncology.radiation-oncology.radiotherapy-intent-dose-and-fractionation
name: radiotherapy-intent-dose-and-fractionation
category: health-medicine
field: oncology
product: radiation-oncology
tags: [radiotherapy, radiation-therapy, radiation-oncology, fractionation, hypofractionation, stereotactic, sabr, sbrt, srs, palliative-radiotherapy, radical-radiotherapy, gross-tumour-volume, gtv, ctv, ptv, oar, organs-at-risk, icru-50, icru-62, icru-83, bed, eqd2, alpha-beta-ratio, linear-quadratic-model, dose-constraints, quantec, radiation-toxicity, radiation-dermatitis, re-irradiation]
level: advanced
status: gated
description: "Decide radiotherapy intent, dose and fractionation, define GTV/CTV/PTV and organs at risk per ICRU, compare schedules with BED/EQD2, and manage acute and late toxicity."
sources: ["ICRU Reports 50, 62 and 83 (volume definitions and IMRT prescribing/reporting)", "QUANTEC normal-tissue complication reviews (Int J Radiat Oncol Biol Phys, 2010)", "Perez and Brady's Principles and Practice of Radiation Oncology (textbook)", "Royal College of Radiologists: Radiotherapy dose fractionation (current edition)", "Hall and Giaccia, Radiobiology for the Radiologist (textbook)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

# Radiotherapy intent, dose and fractionation

**Goal:** choose a radiotherapy course whose intent, volume, dose and schedule fit the
tumour and the patient, and keep normal-tissue toxicity within accepted limits.

## 1. Fix the intent first
| Intent | Typical aim | Implication |
|---|---|---|
| **Radical / curative** | Tumour control | Full dose, conformal technique, daily image guidance, weeks of treatment acceptable |
| **Adjuvant / neoadjuvant** | Reduce recurrence or downstage around surgery | Sequencing agreed at MDT |
| **Palliative** | Symptom relief (pain, bleeding, obstruction, cord compression) | Short course, simple technique, minimal visits |
| **Ablative (SABR/SRS)** | Local control of small lesions, oligometastases | Very high dose per fraction, tight margins, strict QA |

Common palliative example: the ASTRO 2017 bone-metastases update (Lutz et al., Practical Radiation Oncology) keeps four schedules for unirradiated sites: 8 Gy in 1, 20 Gy in 5, 24 Gy in 6 or 30 Gy in 10, with similar pain relief; single fractions carry a higher re-treatment rate, and a painful site can be re-treated with 8 Gy. Confirm
schedules against current national dose-fractionation guidance (for example RCR).

## 2. Define the volumes (ICRU 50/62/83)
- **GTV** gross tumour volume: what can be seen or felt (imaging fused to planning CT:
  MRI, PET as indicated).
- **CTV** clinical target volume: GTV plus microscopic spread, including elective
  nodal regions where indicated; follow published contouring atlases.
- **ITV** internal target volume: accounts for internal motion (4D-CT for lung/liver).
- **PTV** planning target volume: adds set-up margin; size depends on immobilisation
  and image-guidance used.
- **OARs** organs at risk (spinal cord, brainstem, lungs, heart, rectum, parotids, etc.)
  with a **PRV** margin for serial organs like cord.

## 3. Choose dose and fractionation using radiobiology
The **linear-quadratic model** underpins schedule comparison:
- BED = n·d·(1 + d/(α/β)), where n = fractions and d = dose per fraction.
- EQD2 = BED / (1 + 2/(α/β)), the equivalent dose in 2 Gy fractions.
- LQ formulas are standard textbook forms (checked arithmetically: 30 Gy in 10 fractions (10 x 3 Gy) has BED10 39 Gy and EQD2 32.5 Gy). Conventional assumptions (Hall and Giaccia, (gated: unconfirmed, source is paywalled or blocked)): **α/β about 10 Gy** for most tumours and acute-reacting
  tissues; **about 3 Gy** for late-reacting normal tissue. Prostate and breast cancers
  are thought to have low α/β, which supports moderate hypofractionation.
- The model is less reliable at very high dose per fraction (SABR); use with caution.
- Overall treatment time matters for rapidly repopulating tumours (head and neck,
  cervix): avoid unplanned gaps; if gaps occur, compensate per local gap policy.

## 4. Respect normal-tissue constraints
Use consensus constraint sets (QUANTEC, disease-specific trial protocols, national
guidance). Examples often quoted: spinal cord maximum 50 Gy in conventional fractionation is associated with about 0.2% myelopathy risk (60 Gy about 6%, 69 Gy about 50%; QUANTEC figures as quoted in secondary reviews, primary paper not read); mean lung dose and lung V20 limits for thoracic plans; mean parotid dose
to preserve salivary function. Exact values depend on fractionation and protocol;
always check the current constraint document.

## 5. Manage toxicity
- **Acute** (during and up to ~90 days): skin reaction (RTOG/CTCAE grading), mucositis,
  oesophagitis, diarrhoea, cystitis, fatigue. Weekly on-treatment review.
- **Late** (months to years): fibrosis, xerostomia, radiation pneumonitis (typically
  1–6 months after thoracic RT), proctitis, cognitive change, secondary malignancy.
- **Re-irradiation** requires cumulative-dose assessment in EQD2 with recovery
  assumptions; specialist peer review.
- Concurrent chemotherapy, some targeted agents and immunotherapy can increase
  toxicity; check interactions before planning.

## Gotchas
- A beautiful plan on the wrong target: peer-review contours before planning.
- PTV margins assume the image-guidance protocol is followed; changing IGRT
  frequency invalidates them.
- BED comparisons across very different fraction sizes are approximations, not facts.
- Pacemakers/ICDs, connective-tissue disease, and prior RT need flagging at referral.

## Verify
- [ ] Intent documented and agreed at MDT; consent covers acute and late effects.
- [ ] GTV/CTV/PTV and OARs contoured per atlas and peer-reviewed.
- [ ] Dose/fractionation matches current guidance; EQD2 calculated where comparing.
- [ ] OAR constraints met or deviations justified and signed off.
- [ ] Weekly on-treatment review and gap-management plan in place.
