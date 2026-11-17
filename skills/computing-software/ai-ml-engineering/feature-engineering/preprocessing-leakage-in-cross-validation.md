---
id: computing-software.ai-ml-engineering.feature-engineering.preprocessing-leakage-in-cross-validation
name: preprocessing-leakage-in-cross-validation
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, data-leakage, preprocessing-leakage, feature-selection-bias, smote-leakage, imblearn-pipeline, cross-validation]
level: practitioner
status: gated
description: "Stop preprocessing from leaking validation data: scalers, imputers, encoders, feature selection, SMOTE and vocabularies fitted inside CV folds with Pipeline and imblearn."
sources:
  - https://scikit-learn.org/stable/common_pitfalls.html#data-leakage
  - https://www.pnas.org/doi/10.1073/pnas.102102699
  - https://imbalanced-learn.org/stable/common_pitfalls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preprocessing leakage in cross-validation

**Goal:** CV scores that match real out-of-sample performance because every learned transform sees only training folds.

## The mistake
```python
X_scaled = StandardScaler().fit_transform(X)          # uses all rows
X_sel = SelectKBest(k=50).fit_transform(X_scaled, y)  # uses labels of all rows!
cross_val_score(LogisticRegression(), X_sel, y, cv=5)  # optimistic
```
Feature selection with labels before CV is the worst offender: on pure noise data with thousands of features, it produces high CV accuracy (Ambroise & McLachlan, 2002, showed this selection bias on gene-expression data (gated: unconfirmed, source is paywalled or blocked); reproduced here: on pure noise with 100 rows x 5,000 features, selecting 50 before CV gave 0.94 accuracy, the same selection inside a Pipeline gave 0.31).

## The fix: everything learned goes in the pipeline
```python
pipe = make_pipeline(StandardScaler(), SelectKBest(k=50), LogisticRegression())
cross_val_score(pipe, X, y, cv=5)
```
Learned transforms to keep inside: scalers, imputers (their means/medians), encoders (category lists, target encoding), PCA, feature selection, text vectorizers (vocabulary and IDF), outlier removal, discretizer bin edges, any statistic computed from data.

## Resampling (SMOTE, undersampling)
Must apply only to training folds, never to validation:
```python
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
pipe = ImbPipeline([("scale", StandardScaler()), ("smote", SMOTE(random_state=0)), ("clf", LogisticRegression())])
cross_val_score(pipe, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="average_precision")
```
The sklearn `Pipeline` rejects samplers ("All intermediate steps should be transformers...", checked); imblearn's skips resampling at predict time. Oversampling before splitting puts synthetic copies of validation points into training.

## Stateless transforms are fine outside
Log transforms, fixed arithmetic (ratio of two columns), date parts - anything not fitted to data - can be done before splitting.

## Hyperparameter tuning
Tuning on the same CV you report is also optimistic; use nested CV or a final untouched test set.

## Verify
- [ ] No `.fit` or `.fit_transform` on the full dataset before the CV split.
- [ ] Resampling only in an imblearn pipeline.
- [ ] Sanity check: shuffle labels; CV score drops to chance.
