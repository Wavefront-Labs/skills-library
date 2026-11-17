---
id: social-sciences.management-and-organisational-research.consumer-behaviour-research.running-consumer-judgement-experiments
name: running-consumer-judgement-experiments
category: social-sciences
field: management-and-organisational-research
product: consumer-behaviour-research
tags: [consumer-behaviour-research, consumer-behavior, consumer-psychology, between-subjects-experiment, manipulation-check, attention-check, mediation, moderation, process-model, hayes-process, prolific, mturk, cloudresearch, qualtrics, preregistration, aspredicted, osf, willingness-to-pay, field-experiment, journal-of-consumer-research, jcr, jcp, demand-effects, open-science, power-analysis]
level: practitioner
status: draft
description: "Design, run and report academic consumer-judgement experiments: manipulation and attention checks, online panels, preregistration, power, mediation/moderation and consequential DVs."
sources:
  - "Pieters (2017), Meaningful mediation analysis, Journal of Consumer Research"
  - "Hayes, Introduction to Mediation, Moderation, and Conditional Process Analysis (3rd ed.)"
  - "Simmons, Nelson & Simonsohn (2011), False-positive psychology, Psychological Science"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running consumer judgement experiments

**Goal:** produce causal evidence about how consumers judge and choose (e.g. "scarcity
cues raise willingness to pay because they signal popularity") that holds up in a
top consumer journal's review and replicates. For commercial pricing and conjoint
research see sales-marketing.market-research-consumer-insights.pricing-research.van-westendorp-gabor-granger-and-conjoint.

## 1. Design
- **Manipulate one construct cleanly.** Write the two (or more) conditions so they
  differ only in the focal factor; hold product, price, length and layout constant.
- **Between-subjects** by default (avoids carry-over and hypothesis guessing);
  within-subjects only where the theory is about comparison.
- **DV choice.** Self-report attitude scales are cheap but weak; reviewers increasingly
  want a *consequential* DV: real choice between products, incentive-compatible WTP
  (BDM auction, a lottery that pays one choice), click-through, or a field outcome.
- **Process evidence.** Measure the proposed mediator *after* the manipulation and
  before or after the DV (state which and why), and plan a moderation study that turns
  the mechanism off — "moderation-of-process" designs are often more persuasive than
  statistical mediation alone.
- **Multi-study package.** Typical JCR/JCP papers have 3–6 studies: a clean lab/online
  test, a mechanism study, a boundary condition, and ideally one field study.

## 2. Sample and power
- Online panels: Prolific, CloudResearch Connect / MTurk Toolkit. Quality varies by
  panel and over time — check recent methodological papers rather than trusting a past rule.
- Power for the *smallest effect you care about*, not the pilot's inflated estimate.
  For 2-cell designs, ~100+ per cell is a common modern floor; interactions need far
  more (an attenuated interaction can need roughly 4× the main-effect N — a rough rule).
  Use G*Power or simulation.
- Preregister on AsPredicted or OSF: hypotheses, N and stopping rule, exclusions, DV,
  analysis. Label exploratory analyses as such.

## 3. Build and run (Qualtrics or similar)
- Randomise with the survey flow randomiser, "evenly present elements".
- **Attention checks** before the manipulation (instructed-response items); exclusions
  based on post-manipulation checks can bias the sample.
- **Manipulation check** to show the manipulation moved the intended construct — and,
  ideally, a discriminant check that it did not move a rival construct.
- Block duplicate IPs/devices, add a bot check, and record time on the stimulus page.
- Ask a funnel debrief ("what do you think this study was about?") to gauge demand effects.

## 4. Analysis and reporting
- Primary test exactly as preregistered (t-test/ANOVA/logit). Report effect sizes with CIs.
- Mediation: bootstrapped indirect effect (PROCESS model 4, or `lavaan`/`mediation`
  in R). Remember the X→M→Y path is correlational for M→Y; say so.
- Moderated mediation: PROCESS model 7/14 etc.; probe with floodlight (Johnson-Neyman)
  for continuous moderators.
- Report all conditions, all measures and all studies run for the project (file-drawer
  disclosure), and post materials, data and code.

## Gotchas
- Covariates added post hoc to rescue significance = p-hacking.
- Students and panelists may know the paradigm (e.g. decoy effects); vary stimuli.
- Hypothetical WTP inflates values versus incentive-compatible measures.
- Single-stimulus designs confound the effect with the product; use several stimuli
  and treat stimulus as a random factor where possible.

## Verify
- [ ] Conditions differ only in the focal factor (a colleague checked blind).
- [ ] Preregistration timestamp precedes data collection; N and exclusions match it.
- [ ] Manipulation check passed; attention checks placed pre-manipulation.
- [ ] At least one consequential or incentive-compatible DV across the package.
- [ ] Mechanism supported by both mediation and a moderation-of-process study.
