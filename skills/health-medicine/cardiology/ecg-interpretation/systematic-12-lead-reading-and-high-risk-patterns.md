---
id: health-medicine.cardiology.ecg-interpretation.systematic-12-lead-reading-and-high-risk-patterns
name: systematic-12-lead-reading-and-high-risk-patterns
category: health-medicine
field: cardiology
product: ecg-interpretation
tags: [cardiology, ecg-interpretation, ekg, 12-lead-ecg, ecg-reading, rhythm-analysis, axis, pr-interval, qrs-duration, qtc, bazett, fridericia, stemi, stemi-equivalents, posterior-mi, de-winter, wellens, sgarbossa, lbbb, rbbb, av-block, mobitz, wpw, pre-excitation, brugada, long-qt, hyperkalaemia, pericarditis, lvh, occlusion-mi]
level: practitioner
status: draft
description: "Reading the 12-lead ECG systematically (rate, rhythm, axis, intervals, morphology) and recognising high-risk patterns: STEMI equivalents, Wellens, conduction disease, pre-excitation, Brugada, long QT."
sources: [Fourth Universal Definition of Myocardial Infarction 2018, AHA/ACCF/HRS recommendations for standardisation and interpretation of the ECG, ESC ACS guidelines 2023, Smith/Meyers occlusion MI literature, Sgarbossa and modified (Smith) Sgarbossa criteria]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Systematic 12-lead reading and high-risk patterns

> General clinical/professional reference, not patient-specific advice. ECGs are interpreted in clinical context and against prior tracings; computer interpretations are not reliable for the high-risk patterns below.

**Goal:** never miss the trace that needs action in minutes, by reading every ECG the same
way and then actively hunting for the dangerous patterns.

## 1. Check the recording
Name/time, calibration (10 mm/mV, 25 mm/s), lead placement (see
`health-medicine.allied-health-technologies.cardiovascular-and-neurodiagnostic-technology.ecg-holter-and-eeg-acquisition-quality`),
artefact. Lead I negative with upright aVR → probable limb-lead reversal.

## 2. The system
1. **Rate:** 300 / large squares between R waves, or count QRS in 10 s × 6.
2. **Rhythm:** P before every QRS? P morphology (upright in II)? Regular/irregular?
   Narrow or wide QRS?
3. **Axis:** leads I and aVF (both positive = normal; I positive/aVF negative → check II
   for left axis deviation).
4. **Intervals:** PR 120–200 ms; QRS < 120 ms; **QTc** (Fridericia preferable at fast
   rates; ~> 470 ms men / 480 ms women prolonged; > 500 ms high risk).
5. **Morphology:** P waves (atrial enlargement), Q waves, R-wave progression, LVH voltage
   criteria, bundle branch pattern.
6. **ST segments and T waves:** elevation, depression, inversion, hyperacute T waves.
7. **Compare** with previous ECGs.

## 3. Ischaemia patterns
- **STEMI criteria** (J point, two contiguous leads): ≥ 1 mm in most leads; V2–V3
  ≥ 2 mm men ≥ 40 y, ≥ 2.5 mm men < 40 y, ≥ 1.5 mm women. Look for reciprocal depression.
- **STEMI equivalents / occlusion MI without classic elevation:**
  - **Posterior MI:** ST depression V1–V3 with tall R/upright T → record V7–V9.
  - **De Winter:** upsloping ST depression with tall symmetrical T waves in precordial leads (LAD occlusion).
  - **Hyperacute T waves** (broad, bulky relative to QRS).
  - **ST elevation in aVR with widespread ST depression:** left main/multivessel
    ischaemia (or other causes of diffuse subendocardial ischaemia).
  - **LBBB or paced rhythm with suspected MI:** modified (Smith) Sgarbossa criteria
    (concordant ST elevation ≥ 1 mm, concordant ST depression V1–V3, or discordant
    ST/S ratio ≥ 25%).
- **Wellens pattern:** deep symmetric or biphasic T waves in V2–V3 in a pain-free patient
  after chest pain → critical proximal LAD stenosis; avoid stress testing; urgent angiography.
- Right ventricular infarct with inferior STEMI: record V4R.

## 4. Conduction disease
- First-degree AV block (PR > 200 ms): usually benign.
- **Mobitz I (Wenckebach):** progressive PR prolongation, often nodal and benign.
- **Mobitz II** (constant PR, dropped QRS) and **complete heart block** (AV
  dissociation): risk of asystole → pacing assessment.
- Bifascicular block + syncope → investigate for intermittent high-grade block.

## 5. Other high-risk patterns
- **Pre-excitation (WPW):** short PR, delta wave, wide QRS. AF with pre-excitation (fast,
  irregular, wide, varying QRS) — avoid AV nodal blockers.
- **Brugada type 1:** coved ST elevation ≥ 2 mm with negative T in V1–V2 (high leads help).
- **Long QT** (congenital or drug-induced); **short QT**; **ARVC** (epsilon waves,
  T inversion V1–V3 beyond childhood); HCM (deep Q waves, LVH, giant T inversion apical variant).
- **Hyperkalaemia:** peaked T → PR prolongation and P flattening → wide QRS → sine wave.
- **Pericarditis:** diffuse concave ST elevation with PR depression (PR elevation in aVR),
  no reciprocal changes except aVR/V1.
- Tachycardia: wide-complex regular tachycardia is **VT until proven otherwise**.

## Gotchas
- Trusting the machine read "normal ECG" — it misses subtle occlusion MI and posterior MI.
- Calling diffuse ST elevation "early repolarisation" without comparison or serial ECGs.
- Measuring QT in a lead with prominent U waves; use II or V5 and the tangent method.

## Verify
- [ ] Recording quality and lead placement checked.
- [ ] All seven steps documented, including QTc.
- [ ] Active search done for STEMI equivalents, Wellens and high-grade block.
- [ ] Compared with prior ECGs; serial ECGs ordered when symptoms persist.
- [ ] Time-critical findings escalated immediately.
