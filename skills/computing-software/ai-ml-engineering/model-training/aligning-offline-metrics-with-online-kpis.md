---
id: computing-software.ai-ml-engineering.model-training.aligning-offline-metrics-with-online-kpis
name: aligning-offline-metrics-with-online-kpis
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, offline-online-metrics, online-experiments, ab-testing, proxy-metrics, metric-validation, business-kpi]
level: practitioner
status: draft
description: "Make offline model metrics predict online business KPIs: choose proxy metrics, validate offline-online correlation across past launches, guardrails and counterfactual evaluation."
sources:
  - https://developers.google.com/machine-learning/guides/rules-of-ml
  - https://experimentguide.com/
  - https://arxiv.org/abs/1003.5956
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Aligning offline metrics with online KPIs

Teams ship models with better offline AUC that do nothing (or harm) online. Offline metrics are proxies; their value depends on how well they predict the online outcome.

## Why they diverge
- **Objective mismatch**: model optimises clicks, business wants retention or revenue.
- **Distribution mismatch**: offline data was logged by the old model (feedback loop / selection bias); new model's recommendations were never shown, so they have no labels.
- **Aggregate vs top-k**: AUC rewards global ranking; the product shows top 5. Use top-k metrics (NDCG@k, recall@k, precision at the operating threshold).
- **Latency and coverage**: a slower or less available model loses online despite accuracy.
- **Calibration**: downstream bidding/pricing uses probabilities; ranking metrics ignore calibration.
- **Interaction effects**: diversity, novelty, fatigue, and cannibalisation are not captured by per-item metrics.

## Build the bridge
1. Write down the decision chain: prediction -> action -> user behaviour -> KPI (Rules of ML rule #2: measure first, pick a simple observable objective).
2. Choose an offline metric that measures the action's quality at the operating point (top-k, threshold, cost-weighted).
3. **Validate the proxy**: for every past A/B test, record offline metric delta and online KPI delta; check correlation and sign agreement. A proxy that disagrees on sign in 30% of launches is not trustworthy.
4. Add offline guardrails: calibration, slice metrics, latency, prediction distribution shift vs current model.

## Counterfactual (off-policy) evaluation
When logs come from a stochastic policy with logged propensities, estimate a new policy's online reward offline with inverse propensity scoring (IPS) or doubly robust estimators (Li et al. 2011, replay method). Requires exploration in production (e.g. epsilon-greedy) and logging of action probabilities.

## Online confirmation
- Always A/B test meaningful changes with a pre-registered primary KPI, guardrails (latency, errors, complaint rate) and power analysis.
- Interleaving experiments for ranking: more sensitive than A/B for detecting preference between two rankers.
- Watch novelty effects: run long enough (at least one or two weekly cycles).

## Maintain
Keep a launch log table: model version, offline metrics, online results. Revisit the proxy when the product changes.
