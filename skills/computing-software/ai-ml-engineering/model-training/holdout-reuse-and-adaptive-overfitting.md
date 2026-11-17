---
id: computing-software.ai-ml-engineering.model-training.holdout-reuse-and-adaptive-overfitting
name: holdout-reuse-and-adaptive-overfitting
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, holdout-reuse, adaptive-overfitting, test-set-hygiene, data-splits, leaderboard-overfitting]
level: practitioner
status: draft
description: "Protect the test set from adaptive overfitting: when repeated evaluation leaks, lockbox test sets, refreshing holdouts, limiting peeks, and reporting honestly after reuse."
sources:
  - https://www.science.org/doi/10.1126/science.aaa9375
  - https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets
  - https://arxiv.org/abs/1902.10811
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Holdout reuse and adaptive overfitting

**Mechanism:** every time a decision (feature, hyperparameter, architecture, threshold) is made by looking at a dataset's score, information about that dataset leaks into the model. After hundreds of iterations, the "test" score is optimistic, like a Kaggle public leaderboard.

## Hygiene rules
1. **Three roles:** training data; validation data (used freely for decisions); a **lockbox test set** evaluated rarely, ideally once per major release.
2. **Log every test evaluation** (who, when, which model). If the test set was consulted for a decision, it has become validation data; say so.
3. **Do not tune thresholds, early stopping or calibration on the test set.**
4. **Refresh:** for ongoing products, build a new test set from newer data each quarter; this also measures temporal drift.
5. **Teams:** keep test labels with one owner or behind an evaluation service that returns aggregate metrics only, rate-limited.

## Signs you have overfit the validation set
- Validation score keeps improving while a fresh holdout or online metric does not.
- Gains are smaller than the validation set's noise (see test-set sizing), yet were accepted.
- Many small "improvements" stacked from tiny validation differences.

## Mitigations when reuse is unavoidable
- Use k-fold CV for decisions instead of one fixed validation split.
- Require improvements to exceed a noise threshold (e.g. 2 SE, or bootstrap CI excluding zero).
- Reusable holdout ideas (Thresholdout: only reveal whether validation and training scores differ beyond a noisy threshold) for heavy adaptive analysis.
- Report final numbers on a never-seen sample (new time period) when possible.

## Verify
- [ ] Evaluation log shows test-set access count; final report states whether the test set was used for any decision.
