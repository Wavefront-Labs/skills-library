---
id: health-medicine.family-and-general-medicine.geriatric-care.comprehensive-geriatric-assessment-frailty-and-falls
name: comprehensive-geriatric-assessment-frailty-and-falls
category: health-medicine
field: family-and-general-medicine
product: geriatric-care
tags: [family-and-general-medicine, geriatric-care, geriatrics, geriatric-medicine, older-adults, elderly, comprehensive-geriatric-assessment, cga, frailty, clinical-frailty-scale, cfs, rockwood, efi, electronic-frailty-index, falls, falls-risk, falls-assessment, timed-up-and-go, tug, orthostatic-hypotension, postural-hypotension, gait-and-balance, sarcopenia, polypharmacy, deprescribing, stopp-start, beers-criteria, fall-risk-increasing-drugs, cognitive-screening, delirium, 4at, osteoporosis, frax, advance-care-planning, primary-care]
level: practitioner
status: draft
description: "Run a primary-care comprehensive geriatric assessment: grade frailty (CFS/eFI), work up falls (TUG, orthostatics, FRIDs), screen cognition and turn findings into a care plan."
sources: ["https://www.nice.org.uk/guidance/ng249/chapter/Recommendations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

*General clinical/professional reference, not patient-specific advice and not a substitute for independent clinical judgement, current local guidelines, or verified prescribing references.*

# Comprehensive geriatric assessment, frailty and falls in primary care

**Goal:** turn "an older patient who is not coping" into a named set of problems across
medical, functional, psychological and social domains, each with an owner and an action —
rather than a list of disconnected single-disease reviews.

## 1. Identify who needs it
- Case-find frailty opportunistically: **Clinical Frailty Scale (CFS)** 1–9 judged on
  function two weeks before any acute illness; ≥5 = mildly frail. Population tools such as
  the **electronic Frailty Index (eFI)** flag candidates but are not a diagnosis.
- Triggers: a fall, new dependence, recurrent admissions, polypharmacy, carer
  concern, "slowing down", unexplained weight loss.
- Do not apply CFS to stable single disabilities in younger people (validation is in ≥65s;
  ambiguity noted in CFS v2.0 guidance).

## 2. The CGA domains (structure the visit around them)
| Domain | Minimum content |
|---|---|
| Medical | Problem list, continence, nutrition (weight trend, MUST), vision/hearing, pain, mouth/teeth |
| Medicines | Full reconciliation incl. OTC; STOPP/START or Beers review; anticholinergic burden |
| Function | ADLs (Barthel) and IADLs; mobility aid use; gait |
| Cognition and mood | 4AT if acute change (delirium first), then Mini-Cog/6CIT/MoCA; PHQ-9 or GDS-15 |
| Social | Who lives at home, carers and carer strain, finances, home hazards, driving |
| Future planning | Goals, advance care planning, lasting power of attorney/health proxy |

Multidisciplinary input (OT, physio, pharmacist, social care) is what makes CGA effective;
a doctor-only CGA is a reduced version — say so in the record.

## 3. Falls workup (any fall, or ≥2 falls/year, or gait concern)
1. **History:** circumstances, prodrome (syncope vs trip), injury, long lie, fear of falling.
2. **Gait/balance/strength:** observed gait and a validated test such as Timed Up and Go
   (cut-offs vary by source; use your local pathway).
3. **Lying and standing BP** (NICE NG249 includes it in the cardiovascular examination). Repeat
   standing readings catch delayed drops; use your local definition of orthostatic hypotension.
4. **Fall-risk-increasing drugs (FRIDs):** sedatives, antipsychotics, antidepressants,
   opioids, antihypertensives with postural drop, alpha-blockers, sulfonylureas/insulin
   (hypos), anticholinergics.
5. **Cardiovascular:** ECG; consider arrhythmia if unexplained or syncopal.
6. **Bone health:** osteoporosis risk assessment (see the NICE osteoporosis guideline). NICE NG249 finds insufficient evidence for vitamin D supplements specifically to lower falls risk; advise following NHS vitamin D advice.
7. **Vision, feet and footwear, continence (night-time urgency), home hazards.**

Interventions recommended by NICE NG249: a progressive falls-prevention exercise programme
(balance, coordination, strength, power), structured medication review (psychotropics
especially), home-hazard assessment and intervention (ideally by an OT), referral for
cataract surgery when cataract impairs vision, and cognitive behavioural interventions for
fear of falling not helped by exercise.

## 4. Turn it into a plan
Write a problem-based **care and support plan**: each problem → action → who → review date.
Share it with the patient, carer and community team. Record CFS, falls risk and ACP status
in coded fields so they surface next time (see
`health-medicine.family-and-general-medicine.ehr-charting.problem-oriented-encounter-notes-and-inbox-management`).
For a deeper medicines review, see
`health-medicine.internal-medicine.multimorbidity-and-pharmacotherapy.structured-polypharmacy-review`.

## Gotchas
- **Delirium masquerades as dementia.** Screen with 4AT before any cognitive test after
  an acute change; don't diagnose dementia during an acute illness.
- Lying/standing BP is often skipped or done too early after standing; repeat readings catch delayed drops.
- Guideline targets (HbA1c, BP) for robust adults cause harm in frailty: relax them and
  document why.
- Deprescribe one drug at a time with a review date; taper benzodiazepines, antidepressants,
  PPIs and beta-blockers rather than stopping abruptly.
- Frailty scores are dynamic — recalculate after recovery from acute illness.
- Uncertainty: TUG cut-offs and CFS use in under-65s vary by source; check your local pathway.
- Falls content here follows NICE NG249 (published April 2025); the CFS thresholds, STOPP/START and Beers content above were not checked in this review.

## Verify
- [ ] CFS recorded with the date and baseline it refers to.
- [ ] Every CGA domain addressed or explicitly deferred.
- [ ] Lying/standing BP at 1 and 3 min documented after any fall.
- [ ] FRIDs reviewed; each change has a monitoring/review date.
- [ ] Bone-health decision recorded.
- [ ] Care plan shared, with named owners and an ACP conversation offered.
