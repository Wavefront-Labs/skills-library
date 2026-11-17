---
id: computing-software.ai-ml-engineering.feature-engineering.choosing-an-imputation-strategy
name: choosing-an-imputation-strategy
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, missing-data, imputation-strategy, imputation, group-imputation, leakage-safe-imputation]
level: practitioner
status: verified
description: "Pick an imputation strategy per feature from mechanism, model type and data size: drop, constant, median plus indicator, group-wise, model-based, or none, fitted leakage-safely."
sources:
  - https://scikit-learn.org/stable/modules/impute.html
  - https://scikit-learn.org/stable/auto_examples/impute/plot_missing_values.html
  - https://stefvanbuuren.name/fimd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing an imputation strategy

**Goal:** a deliberate, per-feature choice that's simple enough to reproduce at serving time and doesn't leak.

## Decision guide
| Situation | Strategy |
|---|---|
| Model handles NaN natively (HistGradientBoosting, XGBoost, LightGBM, CatBoost) | leave NaN; maybe add nothing |
| Linear / NN / distance models, numeric, missingness informative | median + missing indicator |
| Structural missing ("no value because none exists") | domain constant (0, "none") |
| Categorical | explicit "missing" category |
| Value strongly determined by other features (MAR), small-medium data | KNNImputer or IterativeImputer |
| Group-dependent value (price missing, depends on product category) | group-wise median (fitted on train) |
| Column > ~60-80% missing and indicator not predictive | drop the column |
| Rows missing the target | drop those rows (never impute the target for training) |
| Time series | forward-fill with limit (see time-series skill) |

## Group-wise imputation inside a pipeline
```python
class GroupMedianImputer(BaseEstimator, TransformerMixin):
    def __init__(self, group_col, cols): self.group_col, self.cols = group_col, cols
    def fit(self, X, y=None):
        self.medians_ = X.groupby(self.group_col)[self.cols].median()
        self.global_ = X[self.cols].median(); return self
    def transform(self, X):
        X = X.copy()
        fill = self.medians_.reindex(X[self.group_col]).set_index(X.index).fillna(self.global_)
        X[self.cols] = X[self.cols].fillna(fill); return X
```
Fitted per CV fold like any transformer; unseen groups (and groups whose median is NaN) fall back to the global median. Run on a DataFrame with an unseen group: works; it needs DataFrame input and a final estimator with `score` for `cross_val_score`.

## Leakage rules
- All learned imputation statistics fitted on training folds only (pipeline step).
- Don't impute using the target (e.g. per-class means) - that leaks labels.
- Time-ordered data: imputation statistics from the past only.

## Measure, don't assume
Compare strategies by downstream CV score, not by imputation accuracy. Fancy imputers frequently tie with median + indicator; prefer the simpler one when they do, because it's easier to replicate in serving code and to monitor.

## Verify
- [ ] Strategy per feature recorded (table in the feature docs).
- [ ] Imputation lives in the fitted pipeline used for serving.
- [ ] Alternative strategies benchmarked in CV for the important features.
