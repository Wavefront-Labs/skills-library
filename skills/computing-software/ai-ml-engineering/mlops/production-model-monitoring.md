---
id: computing-software.ai-ml-engineering.mlops.production-model-monitoring
name: production-model-monitoring
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-monitoring, data-drift, concept-drift, prediction-drift, psi, population-stability-index, ks-test, kolmogorov-smirnov, training-serving-skew, label-delay, shadow-deployment, canary-release, retraining-triggers, evidently, alerting, model-performance, observability, feature-monitoring, ab-testing]
level: advanced
status: draft
description: "Monitor deployed ML models: log inputs/predictions, detect data and prediction drift with PSI/KS thresholds, handle delayed labels, roll out via shadow and canary, and set retraining triggers."
sources:
  - https://docs.evidentlyai.com/
  - https://cloud.google.com/vertex-ai/docs/model-monitoring/overview
  - https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Production Model Monitoring — knowing a model has gone stale before users do

**Goal:** detect when a deployed model's inputs, outputs or accuracy change, decide whether it matters, and roll new versions out safely.

## 1. Log what you will need later
For every prediction, log: request id, timestamp, model name + version, the **feature values as the model saw them** (after preprocessing), the prediction/score and the threshold decision. Join labels later by request id. Without logged features you cannot diagnose skew; without the version you cannot attribute regressions. Sample (e.g. 1–10%) if volume is high, but keep it random and record the sampling rate. Mask or drop personal data the monitoring does not need.

## 2. Monitor in layers
1. **Service health**: latency p50/p99, error rate, throughput — standard SRE alerts.
2. **Data quality**: null rate, out-of-range values, unseen categories, schema changes per feature. Most "model" incidents are an upstream pipeline change, and these checks catch them first.
3. **Training–serving skew**: compare serving feature distributions to the training set on day one. A big gap immediately after launch is a preprocessing bug, not drift.
4. **Drift**: input feature and prediction distributions versus a reference window.
5. **Performance**: the real metric once labels arrive.

## 3. Drift statistics and starting thresholds
**Population Stability Index** per feature, binned on reference deciles:
`PSI = Σ (cur% − ref%) × ln(cur% / ref%)`. Industry rules of thumb: < 0.1 stable, 0.1–0.25 moderate shift (investigate), > 0.25 significant shift. Add a small epsilon to empty bins or PSI becomes infinite.

**Kolmogorov–Smirnov** (`scipy.stats.ks_2samp`) for continuous features. Gotcha: with tens of thousands of rows, the p-value flags trivially small shifts. Alert on the KS statistic (e.g. > 0.1) or an effect size, not p < 0.05. For categoricals use chi-squared or PSI on categories, or Jensen–Shannon / Wasserstein distance.

Practical rules:
- Use a reference window from training/validation data or a known-good production period; compare daily or weekly windows.
- Weight alerts by feature importance — drift in an unused feature is noise.
- Prediction drift (score distribution, positive rate) is often the single most useful early signal when labels are delayed.
- Expect seasonality; compare to the same period last year or use a rolling reference to avoid weekly false alarms.
These thresholds are conventions, not laws — tune them against incidents you actually observed.

## 4. Living with label delay
Labels for fraud chargebacks, churn or loan default can arrive weeks to months later. Then:
- Track proxies now (prediction drift, complaint rates, manual-review overturn rates).
- Compute true performance on **matured cohorts** (e.g. predictions from 60 days ago), and plot it by prediction date.
- Beware feedback loops: if the model blocks transactions, you never see labels for blocked ones; keep a small random holdout (exploration) to measure true performance.

## 5. Safe rollout: shadow and canary
- **Shadow**: the candidate receives a copy of live traffic, predictions are logged but not acted on. Compare score distributions, agreement rate and latency with the champion — no user risk.
- **Canary**: route a small share (1–5%) of traffic to the candidate, watch guardrail metrics, then step up (e.g. 5 → 25 → 50 → 100%) with automatic rollback on breach.
- **A/B test** when you need a causal estimate of business impact; size it in advance.
Registry aliases make promotion and rollback a single pointer change: computing-software.ai-ml-engineering.mlflow.experiment-tracking-and-model-registry.

## 6. Retraining triggers
Combine:
- **Scheduled** retrain (weekly/monthly) for domains with steady change.
- **Event** triggers: performance on matured labels below an agreed floor, or sustained high-importance drift (e.g. PSI > 0.25 for 3 consecutive windows).
- **Never auto-promote blindly**: retrained candidates pass the same frozen evaluation and per-segment checks (computing-software.ai-ml-engineering.model-training.data-splits-and-evaluation) and a shadow period before taking traffic.
If drift is caused by a broken upstream feed, retraining on the broken data makes things worse — fix the data first.

Tooling: Evidently, NannyML (performance estimation without labels), whylogs, or managed monitors in SageMaker, Vertex AI and Azure ML. Dashboards in Grafana work fine for the simple statistics.

## Verify
- [ ] Every logged prediction has request id, model version, post-processing features and score.
- [ ] Data-quality checks (nulls, ranges, new categories) alert before drift checks.
- [ ] Drift alerts use effect sizes (PSI, KS statistic) with documented thresholds, not raw p-values.
- [ ] Performance is computed on matured-label cohorts and plotted by prediction date.
- [ ] A candidate model has run in shadow and passed canary guardrails before full traffic.
- [ ] Rollback to the previous version is a single, tested action.
