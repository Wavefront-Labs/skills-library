---
id: computing-software.ai-ml-engineering.feature-engineering.rare-and-unseen-category-handling
name: rare-and-unseen-category-handling
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, categorical-encoding, rare-categories, unseen-categories, min-frequency, handle-unknown, infrequent-categories]
level: practitioner
status: gated
description: "Group rare categorical levels and handle categories unseen at training time: OneHotEncoder min_frequency and handle_unknown, OrdinalEncoder unknown values, lookups."
sources:
  - https://scikit-learn.org/stable/modules/preprocessing.html#infrequent-categories
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rare and unseen category handling

**Goal:** stop rare levels from overfitting and unseen levels from crashing or silently corrupting predictions in production.

## Rare levels at fit time
```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
ohe = OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=20, max_categories=50,
                    sparse_output=False)
```
- `min_frequency` (int count or float fraction) folds rare levels into one `infrequent` column; `max_categories` caps the total including that column.
- `ohe.infrequent_categories_` lists what was grouped - log it, because "infrequent" may contain your most important new product.
- `OrdinalEncoder(min_frequency=..., handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=-2)` does the same for tree models (scikit-learn >= 1.3 for infrequent support).
- Checked: with `min_frequency=20`, `x` and `y` (3 and 2 rows) shared one infrequent code (2) and unseen gave -1. `encoded_missing_value` only applies if NaN was present at fit; a NaN first seen at predict time gets `unknown_value` (-1), not -2.
- Choose the threshold so each level has enough rows for its coefficient or leaf statistics to be stable (dozens of rows, more for noisy targets).

## Unseen levels at predict time
| Encoder setting | Behaviour on unseen value |
|---|---|
| `OneHotEncoder(handle_unknown="error")` (default) | raises - crashes serving |
| `handle_unknown="ignore"` | all-zero row for that feature |
| `handle_unknown="infrequent_if_exist"` | maps to the infrequent column if one exists, else all zeros |
| `OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)` | -1 |
| `TargetEncoder` | global target mean |

Prefer mapping unseen to the infrequent bucket: the model has learned something about "rare stuff", whereas all-zeros is a combination it may never have seen.

## Other stacks
- pandas `category` dtype: LightGBM's Python package remembers the training category lists and re-maps new frames (checked: a test column with a different category list gave identical predictions), but still set `pd.Categorical(x, categories=train_categories)` explicitly for other libraries, where codes may shift without any error (gated: unconfirmed, source is paywalled or blocked).
- Keras `StringLookup(num_oov_indices=1)` maps unseen strings to the OOV index.

## Monitoring
Track the rate of unseen/infrequent values per feature in production. A rising rate (new SKUs, new country) is a retraining trigger and an early drift signal.

## Verify
- [ ] Pipeline predicts on a row with a never-seen category without error.
- [ ] Infrequent-category list reviewed and stored with the model.
- [ ] Production unseen-rate metric exists and is alerted.
