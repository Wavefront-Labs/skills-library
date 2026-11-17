---
id: computing-software.ai-ml-engineering.feature-engineering.models-with-native-missing-value-support
name: models-with-native-missing-value-support
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, missing-data, native-missing-support, histgradientboosting, xgboost-missing, lightgbm-missing, catboost-nan-mode]
level: practitioner
status: verified
description: "Use models that handle missing values natively: how HistGradientBoosting, XGBoost, LightGBM, CatBoost and recent sklearn trees route NaNs, their options, and serving consistency."
sources:
  - https://scikit-learn.org/stable/modules/ensemble.html#missing-values-support
  - https://xgboost.readthedocs.io/en/stable/faq.html#how-to-deal-with-missing-values
  - https://lightgbm.readthedocs.io/en/latest/Advanced-Topics.html#missing-value-handle
  - https://catboost.ai/docs/en/concepts/algorithm-missing-values-processing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Models with native missing-value support

**Goal:** skip imputation where the model can learn what missingness means, and avoid the encodings that silently break it.

## How they handle NaN
- **scikit-learn HistGradientBoosting:** at each split, tries sending missing values left and right and keeps the better; if no missing values were seen in training for a feature, missing values at predict time go to the child with more samples.
- **scikit-learn DecisionTree / RandomForest / ExtraTrees:** DecisionTree, RandomForest and ExtraTrees all fit NaN without error on 1.9.1 (checked); older versions raise, so check your version's docs.
- **XGBoost:** sparsity-aware split finding learns a default direction per split for missing values. `missing=np.nan` by default; set `missing=-999` only if your data uses a sentinel.
- **LightGBM:** `use_missing=true` (default) learns direction; `zero_as_missing=true` treats zeros as missing (useful for sparse data, dangerous otherwise).
- **CatBoost:** `nan_mode="Min"` (default; missing treated as smaller than all values), `"Max"`, or `"Forbidden"`.

## Practices
- Feed real NaN, not sentinels like -999 or 0: a sentinel is a real value that the tree may group with genuinely small values, and it breaks if the model or feature is later used by linear models.
- Categorical NaN: LightGBM/CatBoost native categorical handling treats NaN as its own category or a special value - check behaviour; explicit "missing" category is the safe choice.
- Serving must reproduce NaN exactly: JSON `null` -> NaN, not None-to-0 conversions by a validation layer. Add a test that sends missing fields through the real API and compares predictions with offline scoring.
- Still consider a missing indicator for linear stacking/blending or explainability reports - SHAP for NaN values can be confusing to explain.

## When imputing anyway helps
Very high missing rates where you have strong domain knowledge of plausible values, or when a downstream consumer of the features (another model, a report) requires complete data.

## Verify
- [ ] No sentinel values in features passed to these models.
- [ ] Offline vs online predictions match for rows with missing fields.
- [ ] Benchmarked native-NaN vs imputed variants in CV.
