---
id: computing-software.ai-ml-engineering.scikit-learn.validation-and-learning-curves
name: validation-and-learning-curves
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, validation-curve, learning-curve, cross-validation, bias-variance, learningcurvedisplay]
level: practitioner
status: verified
description: "Diagnose under/overfitting and whether more data helps with validation_curve, learning_curve and their Display classes, and how to read them."
sources:
  - https://scikit-learn.org/stable/modules/learning_curve.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LearningCurveDisplay.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ValidationCurveDisplay.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validation curves and learning curves

**Goal:** decide with evidence whether to change model complexity or collect more data.

## Validation curve: score vs one hyperparameter
```python
from sklearn.model_selection import ValidationCurveDisplay
ValidationCurveDisplay.from_estimator(
    pipe, X, y, param_name="clf__max_depth", param_range=[2, 4, 6, 8, 12, 16, 30],   # numbers only
    cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="roc_auc", n_jobs=-1,
)
```
(`validation_curve` returns the raw `train_scores, test_scores` arrays, shape `(n_params, n_folds)`: `(3, 5)` in a test.) A `None` in `param_range` (unlimited depth) makes the display crash with `TypeError: ufunc 'isfinite' not supported for the input types` inside `fill_between`; use a large number instead. Decision tree test: mean train/validation AUC 0.717/0.680 at depth 2, 0.857/0.820 at depth 4, 0.963/0.823 at depth 8 (a growing gap).
- Both scores low: underfitting (high bias) - more capacity, better features.
- Train high, validation lower and falling as complexity rises: overfitting - regularise, simplify.
- The gap and the fold spread (shaded band) together tell you whether a difference between two settings is real.
- Use a log-spaced `param_range` for regularisation strengths (`np.logspace(-4, 2, 7)`).

## Learning curve: score vs training-set size
```python
from sklearn.model_selection import LearningCurveDisplay
LearningCurveDisplay.from_estimator(
    pipe, X, y, train_sizes=np.linspace(0.1, 1.0, 6), cv=5, scoring="roc_auc",
    n_jobs=-1, shuffle=True, random_state=0,
)
```
- Validation score still climbing at 100%: more data will help - worth the labelling cost.
- Curves converged and both low: more data will not help; the model/features are the bottleneck.
- Large persistent gap: variance problem; more data or regularisation.
- `return_times=True` on `learning_curve` gives fit times per size (`fit_times` shape `(n_sizes, n_folds)`), useful to extrapolate training cost. `train_sizes=np.linspace(0.1, 1.0, 3)` gave absolute sizes 160, 880 and 1600 for 2,000 rows with 5-fold CV.

## Gotchas
- Use the same CV splitter you use for model selection (`GroupKFold`, `TimeSeriesSplit`); default KFold on grouped or temporal data gives optimistic curves.
- For imbalanced classification, small `train_sizes` can in principle produce training subsets with one class; set `shuffle=True` and a stratified CV, or start sizes higher. (On 1,000 rows with 2% positives, sizes of 2% and 5% with `StratifiedKFold(5)` ran without error and gave mean AUC 0.81 and 0.77, so this is a risk to check, not a given.)
- `scoring` must match the metric you care about; accuracy curves can hide changes in minority-class performance.
- These curves are diagnostics, not model selection: pick hyperparameters with a search (or nested CV), not by eyeballing a single curve.

## Verify
- [ ] The diagnosis (bias vs variance vs data-limited) is written down with the curve.
- [ ] CV splitter respects groups/time.
- [ ] Decision (collect data / add capacity / regularise) follows from the shape, not from the best single point.
