---
id: social-sciences.psychology.developmental-psychology-research.infant-looking-time-and-longitudinal-designs
name: infant-looking-time-and-longitudinal-designs
category: social-sciences
field: psychology
product: developmental-psychology-research
tags: [developmental-psychology-research, developmental-psychology, psychology, infant-research, looking-time, habituation, violation-of-expectation, voe, preferential-looking, eye-tracking, fussiness, exclusion-rates, manybabies, longitudinal-design, cross-sectional, cohort-sequential, accelerated-longitudinal, attrition, missing-data, growth-curve, multilevel-models, age-appropriate-measures, parental-consent, child-research-ethics]
level: practitioner
status: draft
description: "Run infant looking-time studies (habituation, violation-of-expectation, preferential looking) and plan longitudinal or cohort-sequential designs with attrition handled."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Infant looking-time paradigms and longitudinal designs

**Goal:** get interpretable data from participants who cannot follow instructions,
and separate genuine developmental change from cohort, attrition and practice effects.

## 1. Looking-time paradigms
- **Habituation:** repeat a stimulus until looking drops below a criterion (commonly
  50% of the first 2–3 trials' mean, over a sliding window), then test novel vs
  familiar. Recovery of looking to the novel item implies discrimination.
- **Violation of expectation (VoE):** longer looking to an "impossible" outcome is
  taken as evidence the infant expected otherwise. Control for low-level perceptual
  novelty — the impossible event must not simply be more visually interesting.
- **Preferential looking / intermodal matching:** two displays side by side; proportion
  of looking to target. Counterbalance target side.
- **Familiarity vs novelty preference** can flip with age, exposure time and task
  complexity (Hunter & Ames model) — a "null" may be a transition point. Predict the
  direction in advance where possible.

## 2. Running sessions
- Infant on caregiver's lap; caregiver wears occluded glasses or headphones with
  masking so they can't cue the infant.
- Trial ends when the infant looks away for a criterion (e.g. 2 s continuous) or at a
  max duration. Use attention-getters between trials.
- Code looking **offline from video by two coders blind to condition**, or use eye
  tracking; report inter-coder reliability (e.g. r or ICC > .9 on a subset).
- Expect substantial exclusion (fussiness, inattention, parental interference,
  equipment failure) — 15–40% is common depending on age and paradigm. Define
  exclusion criteria before testing and report every reason.

## 3. Sample and replication
Infant effects are often small and samples historically tiny (n ≈ 16–24 per group).
Large collaborations such as ManyBabies have found smaller effects than single-lab
literature suggested. Power accordingly and consider multi-site collection.

## 4. Choosing a developmental design
| Design | Gives you | Weakness |
|---|---|---|
| Cross-sectional | Age differences, fast | Confounds age with cohort; no individual change |
| Longitudinal | Within-person change, individual trajectories | Slow, attrition, practice/test effects |
| Cohort-sequential (accelerated) | Several cohorts followed over overlapping ages — covers a long span quickly | Assumes cohorts converge; must test it |

## 5. Longitudinal practicalities
- Choose measures that are **age-appropriate yet comparable** across waves; if the
  instrument must change, plan linking items or invariance tests.
- Space waves around expected periods of change, not convenience.
- **Retention** is the project: collect multiple contacts, send birthday cards/updates,
  keep burden low, pay per wave. Track attrition and compare dropouts with stayers on
  baseline measures.
- Analyse with **multilevel growth models** or latent growth curves (R `lme4`,
  `lavaan`), using age at assessment (not wave number) as the time metric, and full
  information maximum likelihood or multiple imputation for missing waves (assumes
  missing at random — say whether that's plausible).
- Watch for **retest effects**: participants improve from practice; a refreshment
  sample at a later wave can estimate this.

## 6. Ethics
Parental informed consent plus the child's ongoing assent — stop if the child is
distressed, regardless of protocol. Store video securely; faces are identifiable data.

## Gotchas
- Small-n, high-exclusion studies with flexible criteria are fertile ground for false positives.
- Longer looking is ambiguous (surprise, interest, confusion); theory must justify the inference.
- Uncertain: habituation criteria and exclusion rates vary by lab; cite the convention used.

## Verify
- [ ] Looking coded blind with reliability reported.
- [ ] Exclusion criteria fixed in advance and all exclusions reported by reason.
- [ ] Perceptual confounds in VoE stimuli addressed.
- [ ] Design choice (cross-sectional / longitudinal / cohort-sequential) justified.
- [ ] Attrition analysed and missing-data assumption stated.
