---
id: computing-software.ai-ml-engineering.feature-engineering.count-and-frequency-encoding
name: count-and-frequency-encoding
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, frequency-encoding, count-encoding, categorical-encoding, high-cardinality]
level: practitioner
status: verified
description: "Encode categoricals by count or frequency: computing on training data only, unseen categories, collisions between equal counts, normalization over time and when it helps trees."
sources:
  - https://feature-engine.trainindata.com/en/latest/user_guide/encoding/CountFrequencyEncoder.html
  - https://contrib.scikit-learn.org/category_encoders/count.html
  - https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Count and frequency encoding

**Idea:** replace each category with how often it appears (count) or its share (frequency). Captures popularity/rarity in one numeric column; works well with tree models on high-cardinality fields (device model, merchant, zip code).

## Implementation
```python
from feature_engine.encoding import CountFrequencyEncoder
enc = CountFrequencyEncoder(encoding_method="frequency", variables=["merchant_id", "device_model"],
                            unseen="encode")         # unseen -> 0 instead of error/NaN
X_train_enc = enc.fit_transform(X_train); X_test_enc = enc.transform(X_test)
```
Pandas equivalent:
```python
freq = X_train["merchant_id"].value_counts(normalize=True)
X_test["merchant_freq"] = X_test["merchant_id"].map(freq).fillna(0.0)
```

Feature-engine 1.9.4: the default is `unseen="ignore"`, which yields NaN and then raises `ValueError` on transform; `unseen="encode"` returns 0 (checked).

## Rules
- Fit on training data only (inside the CV pipeline); counts from the full dataset leak test distribution information.
- Unseen categories get 0 (or a small floor) consistently in training simulation and serving.
- Frequency (normalized) is more stable than raw counts when training and serving volumes differ; for time-evolving data, compute counts over a trailing window as of prediction time.

## Limitations
- Different categories with the same count become indistinguishable; combine with other encodings (target encoding, or keep native categorical for the top-N).
- Says nothing about the target relationship; for linear models it is a weak feature unless popularity matters.
- Popularity shifts over time (new merchants grow): monitor drift on the encoded values.

## Variants
Rank encoding (rank of frequency), log-count (`log1p(count)`) for heavy tails, and count within segments (category count per country).

## Verify
- [ ] Compare CV score with one-hot (top-N) and target encoding on the same folds; check unseen-category rate on recent data.
