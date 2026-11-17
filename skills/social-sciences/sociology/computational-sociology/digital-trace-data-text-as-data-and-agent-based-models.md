---
id: social-sciences.sociology.computational-sociology.digital-trace-data-text-as-data-and-agent-based-models
name: digital-trace-data-text-as-data-and-agent-based-models
category: social-sciences
field: sociology
product: computational-sociology
tags: [computational-sociology, computational-social-science, sociology, digital-trace-data, social-media-data, web-scraping, apis, platform-terms, data-donation, text-as-data, topic-models, stm, structural-topic-model, word-embeddings, dictionary-methods, supervised-classification, llm-annotation, validation, agent-based-models, abm, netlogo, mesa, schelling-model, calibration, sensitivity-analysis, odd-protocol, python, r-language]
level: advanced
status: draft
description: "Use digital trace data, text-as-data and agent-based models for sociology: collect within platform terms, validate measures, and calibrate ABMs against data."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Digital trace data, text-as-data and agent-based models

**Goal:** use large-scale digital data and simulation for sociological questions
without mistaking volume for representativeness or a model's output for evidence.

## 1. Digital trace data
- **Access routes:** official APIs (research access programmes have been cut back or
  made paid on several major platforms since 2023 — check the current state before
  designing a study), the EU DSA researcher-access provisions (Art. 40, still being
  implemented), data donation (users export their own data packages and share them),
  browser plugins with consent, and scraping public pages.
- Scraping: read the terms of service and robots.txt, rate-limit, store only what you
  need, and get ethics review — "public" does not mean "consented to research".
- **Bias:** platform users aren't the population; active users aren't all users; bots
  and coordinated accounts inflate counts; the platform's algorithm shapes what is
  visible ("algorithmic confounding", Salganik's *Bit by Bit*). Describe the data-generating
  process before analysing.
- Data drift: platform changes (feature launches, moderation policy) create breaks in
  time series that look like social change.

## 2. Text as data
Pipeline: define the concept → build corpus → preprocess → measure → **validate** → analyse.
| Method | Use | Validation |
|---|---|---|
| Dictionaries (e.g. LIWC, custom) | Quick, transparent | Check precision on a hand-coded sample; off-the-shelf dictionaries often fail in new domains |
| Topic models (LDA, STM via `stm`) | Discovery, themes with covariates | Read top documents per topic; stability across K and seeds |
| Embeddings | Semantic dimensions, cultural meaning (Kozlowski et al.) | Check against known benchmarks |
| Supervised classifiers / fine-tuned transformers | Measuring a defined category at scale | Hold-out test set coded by humans; report F1 per class |
| LLM zero/few-shot annotation | Fast coding | Compare with human coders on a sample; prompt and model version recorded — outputs change across versions |
Grimmer & Stewart's rule: all quantitative text models are wrong — validate them.
Preprocessing choices (stemming, stopwords, n-grams) can change results; report them.

## 3. Agent-based models (ABM)
- Use when macro patterns emerge from interacting individuals (segregation — Schelling;
  diffusion; norms; opinion dynamics).
- Tools: NetLogo (fast prototyping, teaching), Mesa (Python), or custom code.
- Document with the **ODD protocol** (Overview, Design concepts, Details) so others can
  reimplement it.
- **Sensitivity analysis:** sweep parameters (Latin hypercube or full grid), run many
  replications per setting (stochastic models need distributions, not single runs).
- **Calibration/validation:** match stylised facts or empirical distributions
  (pattern-oriented modelling; approximate Bayesian computation). An ABM that reproduces
  a pattern shows a sufficient mechanism, not the actual one.

## 4. Reproducibility
Freeze data snapshots with dates; version code; record random seeds; share code and
derived (non-identifying) data. Raw platform data often can't be shared — share IDs
for rehydration where allowed.

## Gotchas
- Big n makes everything significant — focus on effect sizes and measurement validity.
- Re-identification from "anonymised" posts is easy via search; paraphrase quotes.
- Uncertain: platform access policies change quickly — verify before relying on any API.

## Verify
- [ ] Data access is within terms and ethics approval covers it.
- [ ] Population, platform and algorithmic biases described.
- [ ] Every text measure validated against human coding with metrics reported.
- [ ] ABM documented with ODD, sensitivity analysis and multiple runs per setting.
- [ ] Seeds, model versions and data snapshot dates recorded.
