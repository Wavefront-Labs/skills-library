---
id: health-medicine.internal-medicine.adult-differential-diagnosis.building-and-narrowing-a-differential
name: building-and-narrowing-a-differential
category: health-medicine
field: internal-medicine
product: adult-differential-diagnosis
tags: [adult-differential-diagnosis, internal-medicine, clinical-reasoning, differential-diagnosis, ddx, problem-representation, illness-scripts, semantic-qualifiers, diagnostic-schema, pre-test-probability, likelihood-ratio, bayes, anchoring, premature-closure, cognitive-bias, diagnostic-timeout, must-not-miss, vindicate, hospital-medicine]
level: practitioner
status: draft
description: "Build an adult differential: one-line problem representation, schema-driven ddx, must-not-miss list, pre-test probability, tests chosen by likelihood ratio, and a debiasing timeout."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building and narrowing an adult differential diagnosis

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** go from a pile of findings to a ranked, testable differential that names the
most likely diagnosis, the dangerous ones you must exclude, and the test that best
separates them.

## 1. Write the problem representation (one sentence)
Compress the case into: **who** (age, key risk factors) + **tempo** (hyperacute /
acute / subacute / chronic / episodic) + **syndrome** (the key clinical pattern) using
**semantic qualifiers** (unilateral vs bilateral, constant vs intermittent, painful vs
painless, febrile vs afebrile).
- Weak: "65-year-old with shortness of breath, cough, and some leg swelling."
- Strong: "65-year-old smoker with heart failure presenting with subacute progressive
  exertional dyspnoea, orthopnoea and bilateral pitting oedema, afebrile."
If you can't write this sentence, you haven't finished the history.

## 2. Generate candidates with a schema, not memory
Pick one organising frame per problem:
- **Anatomic** (chest pain: wall, pleura, lung, heart, aorta, oesophagus, abdomen).
- **Physiologic** (hyponatraemia by tonicity → volume status → urine osm/Na).
- **Mnemonic sweep** for undifferentiated problems — VINDICATE (vascular, infectious,
  neoplastic, drugs, inflammatory/idiopathic, congenital, autoimmune, trauma,
  endocrine/metabolic). Always ask "drugs?" explicitly; medication effects are among the
  most-missed causes.
Then match candidates against **illness scripts** (epidemiology, time course, key
features, mechanism) and keep the 3–6 that fit.

## 3. Rank in three columns
| Most likely | Must not miss | Treatable/less likely but worth testing |
|---|---|---|
| fits the script best | lethal if missed (PE, dissection, MI, sepsis, SAH, ectopic, cord compression) | cheap to exclude |

The "must-not-miss" column is ranked by consequence, not probability.

## 4. Estimate pre-test probability, then test with intent
- Assign a rough probability (low <10%, intermediate, high >~70%) — use validated scores
  where they exist (Wells, PERC, HEART, CURB-65, Centor). Thresholds vary by source;
  check the current version you use locally.
- Choose tests by **likelihood ratio**: LR+ >10 or LR– <0.1 shift probability a lot;
  LR 0.5–2 barely moves it. A sensitive test (high sensitivity, low LR–) rules *out*
  when negative ("SnOut"); a specific test rules *in* when positive ("SpIn").
- Rule of thumb (Fagan nomogram approximation): LR 2 ≈ +15 percentage points, LR 5 ≈
  +30, LR 10 ≈ +45; LR 0.5 ≈ –15, 0.2 ≈ –30, 0.1 ≈ –45 (valid roughly for mid-range
  pre-test probabilities).
- Before ordering, ask: **will any result change management?** If not, don't order it.

## 5. Debias before you commit — the diagnostic timeout
Ask aloud or in the note:
1. What else could this be? (forces against **premature closure**)
2. Does anything **not fit**? Unexplained findings are the most valuable data.
3. Am I **anchored** on the triage label or the referral diagnosis?
4. Could **two** processes coexist? (Hickam's dictum is common in multimorbid adults.)
5. Have I seen the patient myself, or just the chart (**diagnostic momentum**)?

## Gotchas
- Older adults present atypically: sepsis as delirium or falls; MI without chest pain.
- Normal vitals at one time point do not exclude a deteriorating process — trend them.
- A diagnosis "confirmed" by a low-specificity test (e.g. D-dimer, troponin leak in
  CKD) is not confirmed.
- Write the differential in the note with reasoning; it lets the next clinician
  revise instead of inherit.

## Verify
- [ ] One-sentence problem representation with semantic qualifiers is written.
- [ ] Differential has a must-not-miss column with a plan for each item.
- [ ] Every test ordered has a stated question and would change management.
- [ ] A diagnostic timeout was done; unexplained findings are listed.
- [ ] Working diagnosis is labelled as working, with what would make you reconsider.
