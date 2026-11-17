---
id: social-sciences.communication-studies.media-effects-research.framing-agenda-setting-and-exposure-measurement
name: framing-agenda-setting-and-exposure-measurement
category: social-sciences
field: communication-studies
product: media-effects-research
tags: [media-effects-research, media-effects, framing, framing-effects, equivalence-framing, emphasis-framing, agenda-setting, mccombs-shaw, priming, most-important-problem, exposure-measurement, self-reported-exposure, over-reporting, digital-trace-data, web-tracking, browser-panel, linkage-analysis, panel-design, cross-lagged-panel, random-intercept-clpm, ri-clpm, selective-exposure, survey-experiment, effect-decay, pretreatment-effects, manipulation-check]
level: advanced
status: draft
description: "Studying media effects: framing experiments, agenda-setting (content-plus-survey linkage), measuring exposure beyond self-report, and panel designs."
sources: ["McCombs & Shaw, 'The Agenda-Setting Function of Mass Media' (1972)", "Chong & Druckman, 'Framing Theory' Annual Review of Political Science (2007)", "Prior, 'The Immensely Inflated News Audience' (2009)", "de Vreese & Neijens, 'Measuring Media Exposure in a Changing Communications Environment' (2016)", "Hamaker, Kuiper & Grasman, 'A Critique of the Cross-Lagged Panel Model' (2015)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Framing, agenda-setting and exposure measurement

**Goal:** show whether and how media content changes what people think about and how
they think about it — with valid exposure measures and designs that support the
causal claim.

## 1. Framing experiments
- Distinguish **equivalence framing** (logically identical: "90% survival" vs "10%
  mortality") from **emphasis framing** (highlighting different considerations: a
  rally as "free speech" vs "public safety"). Most political communication is emphasis
  framing.
- Design: randomise respondents to realistic articles/posts differing only in the
  frame; include a no-frame control. Hold length, source and images constant.
- Measure the outcome (opinion) *and* the mechanism: belief importance or accessible
  considerations (open-ended "what comes to mind").
- **Gotchas:** effects often **decay** within days — add a follow-up wave; **pre-
  treatment** — people already exposed in the real world respond less; **competitive
  framing** (both sides' frames) usually shrinks effects; strong manipulation checks
  can themselves prime the frame — place them after outcomes.

## 2. Agenda-setting
"Media tell people what to think *about*." Classic test: correlate issue salience in
media with public salience.
- **Media agenda:** content analysis of issue attention over time (see
  social-sciences.communication-studies.content-analysis.codebook-coder-training-and-intercoder-reliability).
- **Public agenda:** the "most important problem" (MIP) survey question.
- **Linkage:** match individuals' outlets to those outlets' content (linkage analysis)
  or use time series (VAR/Granger tests) with appropriate lags.
- Attribute (second-level) agenda-setting: which attributes of an issue/candidate are
  made salient.

## 3. Measuring exposure
Self-reported exposure is badly inflated and noisy (Prior); people misremember how
much news they consume, especially online.
- Improve self-report: ask about specific outlets/programmes, shorter recall windows,
  "list-frequency" techniques.
- **Digital trace data:** browser/app tracking panels, data donations (people
  uploading platform data downloads), smart TV logs. Consent and privacy are central;
  trackers miss other devices.
- Combine: traced exposure for a subsample to calibrate self-report.

## 4. Observational designs
- **Panel surveys** observe change within people. Classic cross-lagged panel models
  confound stable between-person differences with within-person effects; prefer
  **random-intercept CLPM** or fixed-effects panel models.
- **Selective exposure:** people choose congenial media, so correlations between use
  and attitudes overstate effects. Use within-person change, natural experiments
  (e.g. channel rollout, outages), or instrumental designs.
- Field experiments: incentivised exposure (paying people to switch news sources or
  deactivate social media) give causal estimates in real settings.

## 5. Reporting effects
Report effect sizes with CIs and their durability; small average effects can still be
politically consequential, while lab effects may overstate real-world influence.

## Verify
- [ ] Frame type (equivalence vs emphasis) named; stimuli differ only in the frame.
- [ ] Follow-up wave or argument about effect duration included.
- [ ] Media and public agendas measured independently and linked with stated lags.
- [ ] Exposure measure validated or triangulated beyond simple self-report.
- [ ] Panel models separate within- from between-person variance.
