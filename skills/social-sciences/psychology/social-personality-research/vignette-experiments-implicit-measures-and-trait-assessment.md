---
id: social-sciences.psychology.social-personality-research.vignette-experiments-implicit-measures-and-trait-assessment
name: vignette-experiments-implicit-measures-and-trait-assessment
category: social-sciences
field: psychology
product: social-personality-research
tags: [social-personality-research, social-psychology, personality-psychology, psychology, vignette-experiment, factorial-survey, attitude-measurement, implicit-measures, iat, implicit-association-test, d-score, amp, affect-misattribution, evaluative-priming, big-five, ffm, bfi-2, hexaco, ipip, tipi, social-desirability, demand-characteristics, deception, debriefing, prolific, mturk, online-samples]
level: practitioner
status: draft
description: "Design social-psychology vignette experiments, use implicit measures (IAT, AMP) with their reliability limits, and assess Big Five traits with validated short forms."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vignette experiments, implicit measures and trait assessment

**Goal:** measure attitudes, social judgements and personality in ways that survive
social-desirability bias and the replication scrutiny social/personality psychology
has had since the 2010s.

## 1. Vignette experiments
A vignette describes a person or situation; you vary one or more attributes and
measure judgements.
- **Vary only the manipulated attribute.** Changing a name to signal ethnicity also
  signals class, age and familiarity — pretest names/cues for those confounds.
- **Factorial survey** designs vary several attributes at once (e.g. 2 × 3 × 2);
  each participant may rate several vignettes, so analyse with multilevel models
  (vignettes nested in respondents).
- Use **multiple stimulus versions** per condition and treat stimuli as a random
  factor — otherwise you generalise from one vignette to a whole category
  ("stimulus sampling").
- Keep vignettes short and realistic; add a comprehension check on the key fact.
- Between-subjects manipulation of a sensitive attribute hides the hypothesis better
  than within-subjects (where participants see the contrast).

## 2. Implicit measures
- **IAT:** categorise stimuli with shared response keys; scored with the improved
  **D-score** algorithm (Greenwald et al. 2003). Counterbalance block order.
- **AMP (affect misattribution procedure)** and **evaluative priming** are alternatives.
- Know the limits: IAT test–retest reliability is modest (often cited around .5), and
  meta-analyses find weak prediction of individual behaviour. Use implicit measures for
  group-level questions and process research, **not** for diagnosing individuals.
- Changes in implicit scores after interventions are often short-lived and don't
  reliably change behaviour (Forscher et al. 2019 meta-analysis) — design follow-ups.
- Ready-made: Project Implicit materials, Inquisit, or jsPsych/PsychoPy IAT templates.

## 3. Explicit attitudes and social desirability
- Use multi-item scales, not single feeling thermometers, where reliability matters.
- Anonymity, self-administration and indirect questioning reduce desirability bias;
  list experiments and randomised response can estimate sensitive prevalence.
- Social-desirability scales as "controls" are of doubtful validity — don't rely on them.

## 4. Trait assessment
- **Big Five:** BFI-2 (60 items; BFI-2-S 30, BFI-2-XS 15), IPIP-NEO (public domain),
  NEO-PI-3 (licensed). **HEXACO** adds Honesty–Humility.
- Ultra-short forms (TIPI, 10 items) are fine as covariates but have low internal
  consistency by design and poor facet coverage — don't use them for main outcomes.
- Report reliability per domain (see social-sciences.psychology.psychometrics).
- Traits are moderately stable; for "state" research use experience sampling with
  multilevel analysis.

## 5. Deception and debriefing
Deception needs ethics approval and justification that no non-deceptive design
works. Debrief fully and check for suspicion with a funnel debrief ("What do you
think the study was about?") — decide in advance whether suspicious participants are excluded.

## 6. Online samples
Prolific, MTurk/CloudResearch: use attention checks, bot/duplicate screening,
fair pay, and limits on "professional" participants who've seen standard paradigms.

## Gotchas
- Classic effects (ego depletion, some priming effects, power posing) failed large
  replications — check Many Labs / registered replication reports before building on one.
- Personality–outcome correlations of r ≈ .1–.3 are typical and meaningful; don't
  oversell or dismiss them.
- Uncertain: reliability figures above are summary values from the literature; check
  for your specific measure and population.

## Verify
- [ ] Vignette manipulation pretested for confounds; multiple stimuli per condition.
- [ ] Analysis treats participants and stimuli as random where applicable.
- [ ] Implicit measure used for group-level inference only, scoring algorithm named.
- [ ] Trait measure length matches its role (outcome vs covariate).
- [ ] Deception justified, debrief and suspicion probe done.
