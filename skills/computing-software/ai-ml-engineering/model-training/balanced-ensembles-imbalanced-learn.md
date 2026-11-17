---
id: computing-software.ai-ml-engineering.model-training.balanced-ensembles-imbalanced-learn
name: balanced-ensembles-imbalanced-learn
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, balanced-random-forest, easyensemble, imbalanced-learn, class-imbalance, rusboost]
level: practitioner
status: gated
description: "Use imbalanced-learn ensembles: BalancedRandomForest, EasyEnsemble, BalancedBagging and RUSBoost, with pipelines that resample inside CV and probability correction caveats."
sources:
  - https://imbalanced-learn.org/stable/ensemble.html
  - https://imbalanced-learn.org/stable/references/generated/imblearn.ensemble.BalancedRandomForestClassifier.html
  - https://imbalanced-learn.org/stable/common_pitfalls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Balanced ensembles (BalancedRandomForest, EasyEnsemble)

**Idea:** instead of resampling once (throwing away majority data), each ensemble member is trained on a different balanced sample, so all majority examples get used across members.

## Options
| Estimator | Mechanism |
|---|---|
| `BalancedRandomForestClassifier` | each tree's bootstrap is undersampled to balance classes |
| `BalancedBaggingClassifier(estimator=...)` | bagging any base model on balanced bootstraps |
| `EasyEnsembleClassifier` | AdaBoost learners, each on a balanced random undersample |
| `RUSBoostClassifier` | random undersampling inside each boosting round |

```python
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.model_selection import cross_validate, StratifiedKFold
brf = BalancedRandomForestClassifier(n_estimators=500, sampling_strategy="all", replacement=True,
                                     bootstrap=False, n_jobs=-1, random_state=0)
cross_validate(brf, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=0),
               scoring=["average_precision", "roc_auc", "balanced_accuracy"])
```
(On imbalanced-learn 0.14.2 these three arguments are already the defaults (`sampling_strategy="all"`, `replacement=True`, `bootstrap=False`; read from the signature) and no warning appeared; older releases (0.12 era) changed these defaults and warned (gated: unconfirmed, source is paywalled or blocked), so setting them explicitly keeps results stable across versions.) Ran on a 3,000-row, 5%-positive synthetic set: `BalancedRandomForestClassifier` CV average precision 0.912; `BalancedBaggingClassifier(estimator=DecisionTreeClassifier())`, `EasyEnsembleClassifier` (members are Pipelines of `RandomUnderSampler` + `AdaBoostClassifier`) and `RUSBoostClassifier` all fit.

## Resampling inside CV
Ensembles handle this internally. For explicit samplers use `imblearn.pipeline.Pipeline` (not sklearn's) so SMOTE/undersampling runs only on training folds:
```python
from imblearn.pipeline import make_pipeline
from imblearn.under_sampling import RandomUnderSampler
pipe = make_pipeline(preprocess, RandomUnderSampler(random_state=0), LogisticRegression())
```

## Probabilities are distorted
Balanced training inflates predicted positive probabilities relative to the true base rate. Rank metrics (PR-AUC, ROC-AUC) are fine; for decisions or expected-value calculations, recalibrate (CalibratedClassifierCV on untouched validation data, wrapping the fitted model in `FrozenEstimator` on scikit-learn 1.6+; `cv="prefit"` is rejected on 1.9.1) or apply prior correction.

## When to prefer alternatives
Gradient boosting with `scale_pos_weight`/class weights and a tuned threshold often matches or beats balanced ensembles with less complexity (a common finding, not tested here (gated: unconfirmed, source is paywalled or blocked)). Compare on PR-AUC using the same folds.

## Verify
- [ ] Table: plain RF, class-weighted RF, BalancedRF, boosting with weights, by PR-AUC and recall at target precision.
