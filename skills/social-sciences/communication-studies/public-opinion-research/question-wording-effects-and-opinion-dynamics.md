---
id: social-sciences.communication-studies.public-opinion-research.question-wording-effects-and-opinion-dynamics
name: question-wording-effects-and-opinion-dynamics
category: social-sciences
field: communication-studies
product: public-opinion-research
tags: [public-opinion-research, public-opinion, polling, opinion-polls, questionnaire-design, question-wording, wording-effects, question-order-effects, context-effects, acquiescence-bias, agree-disagree-items, response-order-effects, primacy, recency, split-ballot, non-attitudes, dont-know-option, filter-questions, opinion-dynamics, policy-mood, dyad-ratios, repeated-cross-sections, trend-analysis, aapor, transparency-initiative, survey-mode-effects, cognitive-interviewing]
level: practitioner
status: draft
description: "Measuring opinion well: wording, order and response-option effects, split-ballot tests, non-attitudes, and modelling opinion change over time with repeated surveys."
sources: ["Schuman & Presser, Questions and Answers in Attitude Surveys (1981)", "Tourangeau, Rips & Rasinski, The Psychology of Survey Response (2000)", "Zaller, The Nature and Origins of Mass Opinion (1992)", "Stimson, Public Opinion in America: Moods, Cycles, and Swings", "AAPOR Code of Professional Ethics and Practices; Transparency Initiative"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Question wording effects and opinion dynamics

**Goal:** write opinion questions that measure what you intend, detect when wording
drives the answer, and analyse change in opinion over time without mistaking
measurement shifts for real movement.

## 1. Why answers move with wording
Respondents comprehend, retrieve, judge and map onto response options (Tourangeau et
al.). Many hold weak or no opinion on a topic, so they build an answer from whatever
the question makes accessible (Zaller). Classic effects:
- **Wording:** "forbid" vs "not allow" produce different totals for logically
  equivalent policies; "welfare" vs "assistance to the poor" differ sharply.
- **Order/context:** earlier questions prime later ones (asking about a scandal before
  approval lowers approval). Assimilation vs contrast effects.
- **Response-option order:** primacy in visual modes (web), recency in aural modes
  (phone).
- **Acquiescence:** agree/disagree formats inflate agreement; prefer
  **item-specific** wordings ("Is X more important, less important or as important...").
- **Explicit "don't know"/filter questions** reduce **non-attitudes** but can also
  push people with weak opinions out.
- **Mode effects:** interviewer modes increase socially desirable answers versus
  self-administered web.

## 2. Writing better items
- One idea per question (no double-barrels: "Do you support lower taxes and fewer
  services?").
- Balanced stems ("favour or oppose") and balanced options.
- Plain words; define unfamiliar policies neutrally.
- Pretest with **cognitive interviews** (think-aloud, probing on what terms meant).
- Reuse established items for comparability (e.g. from ANES, Pew, ESS) — but
  recognise their limitations.

## 3. Test wording with split-ballot experiments
Randomly assign respondents to alternative wordings or orders, then compare
distributions (chi-square, difference in proportions). This turns wording uncertainty
into a finding. Report all versions, not just the convenient one.

## 4. Opinion dynamics
- **Repeated cross-sections:** same question, new samples over time. Only compare
  across waves when wording, context (preceding questions), mode and population are
  constant — a mode switch (phone → web) can look like opinion change.
- **Panels** show individual-level stability and conversion; watch for panel
  conditioning and attrition.
- **Aggregate measures:** combine many series into a latent measure (Stimson's
  **policy mood** via the dyad-ratios algorithm; Bayesian dynamic models). They smooth
  item-specific noise.
- Model change with time-series tools (ARIMA, error-correction) and relate to events,
  media coverage or economic indicators; beware spurious trend correlations.
- **Thermostatic** responses: public preferences often move opposite to policy change.

## 5. Transparency
Report sponsor, field dates, population, mode, sample size and source, weighting,
full question wording and order, and margin of error / design effect (AAPOR Transparency
Initiative elements). Unreported wording is the most common reason polls get
misread.

## Verify
- [ ] Each item single-barrelled, balanced, and cognitively pretested.
- [ ] Key items tested via split-ballot or justified against established wording.
- [ ] Question order and context documented alongside wording.
- [ ] Over-time comparisons hold wording, context and mode constant (or adjust).
- [ ] Full methodological disclosure published with results.
