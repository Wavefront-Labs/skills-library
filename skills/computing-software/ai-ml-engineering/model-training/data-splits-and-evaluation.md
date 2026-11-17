---
id: computing-software.ai-ml-engineering.model-training.data-splits-and-evaluation
name: data-splits-and-evaluation
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-evaluation, train-test-split, validation-set, holdout, cross-validation, temporal-split, group-split, metrics, precision-recall, roc-auc, pr-auc, f1, rmse, baselines, learning-curves, calibration, reliability-diagram, brier-score, error-analysis, confidence-intervals, bootstrap, class-imbalance, overfitting, machine-learning]
level: practitioner
status: draft
description: "Design train/validation/test splits that mirror deployment, pick metrics tied to the decision, beat baselines, read learning curves, check calibration, do error analysis and report CIs."
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html
  - https://scikit-learn.org/stable/modules/calibration.html
  - https://developers.google.com/machine-learning/crash-course
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data Splits and Evaluation — numbers you can believe before launch

**Goal:** produce an offline evaluation whose numbers predict production performance, and know what the model gets wrong and how sure you are. Framework-agnostic; sklearn mechanics are in computing-software.ai-ml-engineering.scikit-learn.pipelines-and-cross-validation.

## 1. Design the split to mirror deployment
Ask: "When this model runs, what will it never have seen?" The split must withhold exactly that.
- **New time periods** (forecasting, fraud, churn): split by time. Train on the past, validate on the next period, test on the period after. Leave a gap equal to the label horizon so training labels do not overlap the validation window.
- **New entities** (new patients, users, stores): group split — every row of an entity in one side only.
- **i.i.d. rows**: stratified random split is fine.
- Typical sizes: 70/15/15 or 80/10/10, but size the test set by the precision you need (section 6), not by ratio. 2,000 test rows gives roughly ±2 percentage points on a ~50% accuracy.
- Deduplicate before splitting; near-duplicates across train and test (same image resized, same text with whitespace changes) inflate scores.
- The test set is touched **once**, at the end. If you iterate on it, it becomes a validation set and you need a new test set.

## 2. Choose the metric from the decision
- Imbalanced binary problems: use **PR-AUC (average precision)** and precision/recall at the operating threshold; accuracy and ROC-AUC look excellent at 1% prevalence even for weak models.
- Pick the threshold from costs: e.g. "recall ≥ 0.9 while flagging ≤ 5% of traffic". Report the metric at that threshold, not only threshold-free AUC.
- Regression: MAE when errors cost linearly, RMSE when large errors are disproportionately bad, MAPE only when targets stay well away from zero.
- Ranking/retrieval: recall@k, NDCG@k, MRR.
- Agree one primary metric and a few guardrail metrics (latency, per-segment performance) before training.

## 3. Always compare against baselines
- Trivial: majority class, mean/median, "same as last period", or the current rule-based system.
- Simple model: logistic/linear regression or a small gradient-boosted tree on a handful of features.
A complex model that beats the trivial baseline by a hair is not worth the operational cost. A model that beats the baseline by an implausible margin usually has leakage (see computing-software.ai-ml-engineering.feature-engineering.leakage-safe-feature-construction).

## 4. Read learning curves
Plot training and validation metric versus training-set size (and versus epochs).
- Both poor and close together: high bias — richer features or model.
- Training good, validation poor, gap closing as data grows: high variance — more data or regularisation helps.
- Validation curve flat as data doubles: more labels will not help; work on features or label quality.

## 5. Calibration
If downstream code uses probabilities (pricing, triage, expected-value thresholds), check calibration with a reliability diagram (10–15 bins) and Brier score. Boosted trees, SVMs and deep nets are often miscalibrated. Fix with Platt scaling (sigmoid) or isotonic regression fitted on held-out data — isotonic needs roughly a thousand or more calibration samples or it overfits. Recalibrate after resampling or class weighting, which distort probabilities.

## 6. Error analysis and uncertainty
- Slice metrics by segment (region, device, new vs. returning, input length). An aggregate gain can hide a regression on an important slice.
- Read 50–100 actual errors, tag them by cause (label noise, missing feature, ambiguous input, distribution gap) and count. Fix the largest bucket first.
- Report confidence intervals: bootstrap the test set (1,000+ resamples, 2.5th–97.5th percentiles). To compare two models, bootstrap the **paired** difference on the same examples; if the interval includes zero, you have not shown an improvement.
- With k-fold CV, report mean ± standard deviation across folds and keep the seed fixed when comparing.

## Verify
- [ ] The split withholds what production will not have seen (time, entity, or neither), with a gap for label horizon.
- [ ] No exact or near-duplicate rows cross train and test.
- [ ] The primary metric and operating threshold are written down and tied to a business cost.
- [ ] The model beats a trivial and a simple baseline by a margin larger than the bootstrap CI.
- [ ] Per-segment metrics and a calibration plot are in the evaluation report.
- [ ] The test set was evaluated once, after all model selection.
