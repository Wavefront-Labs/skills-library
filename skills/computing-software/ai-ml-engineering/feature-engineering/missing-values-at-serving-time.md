---
id: computing-software.ai-ml-engineering.feature-engineering.missing-values-at-serving-time
name: missing-values-at-serving-time
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, serving-missing-values, training-serving-skew, imputation, fallback-values, online-inference]
level: practitioner
status: draft
description: "Handle missing features at prediction time: train-serve parity for imputation, upstream outages vs genuine missingness, defaults from training stats, indicators and alerting."
sources:
  - https://developers.google.com/machine-learning/guides/rules-of-ml
  - https://scikit-learn.org/stable/modules/impute.html
  - https://docs.feast.dev/getting-started/concepts/feature-retrieval
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Handling missing values at serving time

**Two different situations:**
1. **Genuine missingness** that also occurred in training (user never set a field). The model learned how to handle it.
2. **Serving-only missingness**: an upstream service timed out, a feature store key is absent for a new entity, a pipeline lagged. Training never saw this pattern, so predictions can be badly wrong.

## Parity rules
- Ship imputation inside the model artifact (sklearn Pipeline, TF preprocessing layers), never reimplemented in the service.
- Missing representation must match: NaN vs None vs empty string vs 0; JSON nulls must become NaN before the pipeline.
- Defaults come from training statistics (median, most frequent) stored with the model, not computed on the live batch.

## New entities and feature-store misses
- Cold-start entities: features like "30-day spend" are legitimately 0 or missing. Make sure training includes new entities with the same representation (simulate first-day snapshots).
- Distinguish "no history" from "lookup failed": return a flag from the feature retrieval layer.

## Upstream failures
- Decide per feature: impute with training default, use a fallback model trained without that feature group, or refuse to score (return a safe default/decision to manual review).
- Robustness training: randomly drop feature groups during training (feature dropout) so the model degrades gracefully.
- Emit a metric per feature for missing rate at serving; alert when it exceeds the training rate.

## Verify
- [ ] Contract test: send requests with each critical feature absent/null; responses are valid and logged with a degraded-mode flag.
- [ ] Dashboard compares serving missing rates per feature with training rates.
