---
id: computing-software.ai-ml-engineering.feature-engineering.leakage-audits-and-adversarial-validation
name: leakage-audits-and-adversarial-validation
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, data-leakage, adversarial-validation, leakage-audit, too-good-to-be-true, feature-timestamps, distribution-shift]
level: practitioner
status: draft
description: "Audit features for leakage and train/test shift: single-feature AUC screening, feature availability timestamps, adversarial validation classifiers and what to do with offenders."
sources:
  - https://www.kaggle.com/learn/data-leakage
  - https://dl.acm.org/doi/10.1145/2382577.2382579
  - https://scikit-learn.org/stable/common_pitfalls.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Leakage audits and adversarial validation

**Goal:** catch features that encode the answer or won't exist at prediction time, before a "great" model fails in production.

## Red flags
- Validation metric suspiciously high (AUC 0.99 on a task where experts struggle).
- One feature dominates importance by a wide margin.
- Performance collapses on a later time period or in shadow deployment.

## Single-feature screen
```python
from sklearn.metrics import roc_auc_score
for c in num_cols:
    auc = roc_auc_score(y, X[c].fillna(X[c].median()))
    if max(auc, 1 - auc) > 0.9:
        print("check", c, round(auc, 3))
```
Then ask, for each flagged feature: **when is this value known relative to the prediction time?** Classic leaks: `account_closed_date` for churn, `refund_amount` for fraud, "number of follow-up visits" for a diagnosis, IDs or row order that correlate with label because of how data was assembled (Kaufman et al., "Leakage in data mining").

## Feature availability audit
Maintain for each feature: source table, the timestamp it becomes available, and whether it is updated after the event. Features from tables that are overwritten in place (current status, latest balance) leak the future when joined to historical labels - use snapshot/as-of joins.

## Adversarial validation (train vs test / train vs production)
```python
Xa = pd.concat([X_train.assign(_is_test=0), X_test.assign(_is_test=1)])
p = cross_val_predict(HistGradientBoostingClassifier(), Xa.drop(columns="_is_test"), Xa._is_test, cv=5, method="predict_proba")[:, 1]
print(roc_auc_score(Xa._is_test, p))     # ~0.5 = indistinguishable
```
- AUC well above 0.5: the sets differ. Feature importances of this classifier show which columns (timestamps, IDs, drifted features).
- Use it with production samples to check whether your validation set represents what the model will see.
- Remedies: drop or fix the shifting feature, re-split by time, weight training samples by `p/(1-p)` to resemble test, or choose validation rows most test-like.

## Verify
- [ ] Every high single-feature AUC explained or removed.
- [ ] Feature availability timestamps documented.
- [ ] Adversarial AUC train vs recent production data reported.
