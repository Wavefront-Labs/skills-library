---
id: computing-software.ai-ml-engineering.model-training.cost-sensitive-evaluation-and-thresholds
name: cost-sensitive-evaluation-and-thresholds
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, model-evaluation, cost-sensitive-evaluation, decision-threshold, expected-cost, profit-curve, business-metrics]
level: practitioner
status: verified
description: "Translate business costs into evaluation: cost matrices, expected cost and profit curves, the optimal threshold for calibrated probabilities, and capacity-limited top-k decisions."
sources:
  - https://scikit-learn.org/stable/modules/classification_threshold.html
  - https://scikit-learn.org/stable/auto_examples/model_selection/plot_cost_sensitive_learning.html
  - https://cseweb.ucsd.edu/~elkan/rescale.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost-sensitive evaluation and thresholds

**Goal:** pick the model and threshold that maximise business value, not accuracy or F1.

## Cost matrix
Write the costs down with the business owner, per decision:
| | Predicted positive (act) | Predicted negative (don't act) |
|---|---|---|
| Actually positive | benefit or cost of TP (e.g. -$50 saved churner minus $5 offer) | cost of FN (lost customer $200) |
| Actually negative | cost of FP (wasted $5 offer) | 0 |

Expected cost per decision = sum over cells of (rate x cost). Evaluate every candidate model at its best threshold on this, using validation data with the real class prior.

## Optimal threshold for calibrated probabilities
Act when `p * cost_FN > (1 - p) * cost_FP` (benefit of acting exceeds cost), i.e. threshold
```
t* = cost_FP / (cost_FP + cost_FN)       (Elkan, 2001; with TP/TN costs: (c_FP - c_TN) / (c_FP - c_TN + c_FN - c_TP))
```
FP $5, FN $200 -> t* = 5/205 = 0.0244: act on anyone with > 2.4% churn probability. This only holds if probabilities are calibrated.

## Tune it empirically
```python
from sklearn.model_selection import TunedThresholdClassifierCV
from sklearn.metrics import make_scorer, confusion_matrix
def gain(y, y_pred):
    tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
    return 45 * tp - 5 * fp - 200 * fn
clf = TunedThresholdClassifierCV(model, scoring=make_scorer(gain), cv=5).fit(X, y)
clf.best_threshold_
```
Ran on a 2,000-row, 10%-positive synthetic set with logistic regression: `best_threshold_` was 0.030 (close to the analytic 0.024; the empirical value depends on calibration and sample), and `make_scorer(gain, response_method="predict")` gave the same threshold. The `gain` function above takes the usual `(y_true, y_pred)` and scores hard predictions at each candidate threshold.
Plot gain vs threshold (a profit curve); flat regions mean the exact threshold matters little, sharp peaks mean you need tight calibration and monitoring.

## Capacity constraints
If ops can only call 500 customers a week, the decision is top-k, not a threshold. Evaluate precision@k / gain@k at that k, and compare models by value captured in the top k.

## Gotchas
- Costs often vary per example (loan size, customer value): use example-dependent costs (`gain = sum(value_i ...)`) rather than a single matrix.
- Class prior shifts move the optimal threshold; re-tune on recent data.
- Report the business metric alongside ROC-AUC/PR-AUC so stakeholders see the trade-off in their units.

## Verify
- [ ] Cost matrix signed off by the business owner.
- [ ] Threshold chosen on validation data, profit curve saved.
- [ ] Expected value on test set reported in currency/units.
