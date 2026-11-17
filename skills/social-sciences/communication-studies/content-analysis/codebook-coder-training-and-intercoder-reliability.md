---
id: social-sciences.communication-studies.content-analysis.codebook-coder-training-and-intercoder-reliability
name: codebook-coder-training-and-intercoder-reliability
category: social-sciences
field: communication-studies
product: content-analysis
tags: [content-analysis, quantitative-content-analysis, codebook, coding-scheme, coder-training, intercoder-reliability, krippendorffs-alpha, cohens-kappa, percent-agreement, scotts-pi, unitising, constructed-week-sampling, media-sampling, news-content, computational-content-analysis, dictionary-methods, supervised-learning, topic-models, llm-coding, validation, gold-standard, irr, krippendorff-r, reliability-subsample]
level: practitioner
status: draft
description: "Running a quantitative content analysis: unitising, sampling, writing a codebook, training coders, Krippendorff's alpha and validating computational coding."
sources: ["Krippendorff, Content Analysis: An Introduction to Its Methodology (4th ed., 2018)", "Neuendorf, The Content Analysis Guidebook (2nd ed., 2017)", "Riffe, Lacy, Watson & Fico, Analyzing Media Messages", "Lombard, Snyder-Duch & Bracken, 'Content Analysis in Mass Communication: Assessment and Reporting of Intercoder Reliability' (2002)", "Grimmer & Stewart, 'Text as Data' (2013)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Codebook, coder training and intercoder reliability

**Goal:** turn a body of messages (news articles, ads, tweets, TV segments) into
reliable, valid numeric data that others could reproduce with your codebook.

## 1. Define units and sample
- **Sampling unit** (an article, a broadcast, a post), **coding unit** (the whole item,
  each paragraph, each claim) and **context unit** (what coders may read to decide).
  Write all three down; unclear units are a major source of disagreement.
- Sampling news over time: **constructed-week sampling** (randomly pick one Monday,
  one Tuesday... from the period) is more efficient than consecutive days because news
  varies by weekday. For social media, document the API/query, time window and
  deduplication.

## 2. Write the codebook
For each variable: name, definition, values with **operational rules**, examples and
**near-miss counterexamples**, and a decision rule for ambiguous cases ("if both
present, code the dominant one, defined as..."). Include "not applicable" and "cannot
tell" codes. Pair with a coding form (spreadsheet or survey tool) that enforces valid
values.

## 3. Train coders
1. Walk through the codebook together on practice items not in the sample.
2. Code independently, compare, discuss disagreements, revise the codebook.
3. Repeat until pilot reliability is acceptable.
4. Freeze the codebook; then code the reliability sample.
Gotcha: researchers coding their own hypotheses risk bias — use coders blind to
hypotheses where possible.

## 4. Measure intercoder reliability
- Use a **reliability subsample** coded independently by ≥2 coders (often 10–20% of
  items, or a minimum of ~50–100+ units depending on variable rarity).
- **Percent agreement** alone is not enough — it ignores chance agreement and is
  inflated for rare categories.
- **Krippendorff's alpha** handles any number of coders, missing data and nominal/
  ordinal/interval levels. Common thresholds: α ≥ .80 reliable; .667–.80 only for
  tentative conclusions (Krippendorff's guidance). Cohen's kappa for two coders on
  nominal data.
- Report reliability **per variable**, not averaged. Rare categories can give low α
  even with high agreement — sample more instances of them.
- Tools: R `irr` or `krippendorffsalpha`; Python `krippendorff`; ReCal online.
- After the reliability check, coders split the rest; spot-check drift periodically.

## 5. Computational content analysis
- **Dictionaries** (e.g. sentiment lexicons): fast but domain-sensitive; validate on
  your corpus.
- **Supervised classifiers** (from logistic regression to fine-tuned transformers):
  train on human-coded data; report precision/recall/F1 on a held-out set.
- **Topic models** (LDA, STM): exploratory; labels are the researcher's
  interpretation.
- **LLM-assisted coding:** treat the model as a coder — fixed prompt and model version,
  compute agreement against a human gold standard, check per-category errors.
  *Rapidly evolving practice; reliability across model versions is not guaranteed.*

## Verify
- [ ] Sampling, coding and context units defined in the codebook.
- [ ] Codebook includes examples, counterexamples and ambiguity rules.
- [ ] Reliability subsample coded independently after training, codebook frozen.
- [ ] Krippendorff's alpha (or kappa) reported per variable with thresholds.
- [ ] Any automated coding validated against human codes on held-out data.
