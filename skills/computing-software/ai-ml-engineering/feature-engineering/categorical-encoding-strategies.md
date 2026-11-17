---
id: computing-software.ai-ml-engineering.feature-engineering.categorical-encoding-strategies
name: categorical-encoding-strategies
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, categorical-encoding, one-hot-encoding, target-encoding, label-encoding, high-cardinality, hashing-trick, ordinal-encoding, embeddings, mean-encoding, leakage]
level: practitioner
status: verified
description: "Pick the right categorical encoding by cardinality and model type, and avoid target-encoding leakage, unseen-category crashes, and unnecessary dimensionality from one-hot."
sources:
  - https://contrib.scikit-learn.org/category_encoders/
  - https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Categorical encoding strategies — by cardinality, model, and leakage risk

**Goal:** turn categorical features into numbers that help the model rather than silently leaking the target or exploding dimensionality, matched to both the feature's cardinality and the model family that will consume it.

## 1. Match the encoding to cardinality and model family
- **One-hot encoding**: correct default for **low-cardinality** categoricals (roughly under a few dozen distinct values) with linear models, and generally fine for tree models too, though trees handle cardinality natively via splits. Past a few hundred categories, one-hot blows up dimensionality — sparse representation keeps memory manageable, but a linear model now has that many more coefficients to fit with no more data, and nearest-neighbor/distance-based methods degrade as dimensionality grows (curse of dimensionality).
- **Ordinal/label encoding** (map each category to an arbitrary integer): fine for tree-based models, which split on thresholds and don't assume the integers carry a meaningful order — but actively wrong for linear/distance-based models, which will interpret the arbitrary integer ordering as meaningful magnitude (category 5 is not "more" than category 2 just because label-encoding assigned it a higher number).
- **High-cardinality** (IDs, zip codes, product SKUs — hundreds to millions of distinct values): one-hot and ordinal both break down. Use **target/mean encoding** (replace each category with a statistic of the target computed over training rows with that category — see leakage warning below), the **hashing trick** (hash categories into a fixed number of buckets, accepting some collision risk, when the category space is unbounded or unknown ahead of time, e.g. streaming new user IDs), or **learned embeddings** (a low-dimensional dense vector per category, trained jointly with a neural network) when enough data exists to train them well.

## 2. Target encoding's leakage trap — the thing that makes validation lie
- **Target/mean encoding computed over the full training set and then applied to that same training set leaks the target into its own feature** — a category with only 2 rows in training gets a mean-encoded value computed from exactly those 2 rows' targets, which the model then "predicts" suspiciously well because the feature was partly derived from the answer. This inflates training (and often validation, if the leak is systemic) metrics in a way that collapses on real unseen data.
- The fix is the same discipline as any leakage-prone transform (see computing-software.ai-ml-engineering.feature-engineering.leakage-safe-feature-construction): compute target encodings **within cross-validation folds** (fit the encoding on the training fold only, apply to the held-out fold), or use **smoothing/regularization toward the global mean** for low-count categories (a Bayesian-style blend: `(category_mean * n + global_mean * k) / (n + k)`), or add noise, so that rare categories don't get an encoding that's effectively memorizing their own target. `category_encoders.TargetEncoder` and similar libraries implement smoothing but still require fold-correct fitting to avoid the within-fold leak.
- For time-series/sequential data, use only **past** data to compute the encoding for a given row (an expanding or rolling window), never future rows relative to that row — the same look-ahead bias that applies to any time-aware feature.

## 3. The unseen-category problem
- Any fitted encoder (one-hot, target, ordinal) that sees a **category at inference time it never saw during training** needs an explicit, deliberate policy: scikit-learn's `OneHotEncoder(handle_unknown="ignore")` zeros out the unseen category's columns rather than erroring; target encoders typically fall back to the global mean for unseen categories. `category_encoders.TargetEncoder` returned the global mean for an unseen level (checked), and `OneHotEncoder()` default raises `ValueError` on one. Whichever you pick, **test it deliberately** by holding out at least one category from training and confirming inference behaves as expected — an encoder that throws on unseen categories in production (the default for many hand-rolled or older-config encoders) turns a routine new-category appearance (a new product SKU, a new zip code) into a hard outage rather than a graceful degraded prediction.
- Log the rate of unseen categories in production — a rising rate often signals upstream data drift (a new category genuinely appearing more, e.g. after a product launch) worth knowing about even if the encoder handles it gracefully.

## Verify
- [ ] Encoding choice matches both cardinality and the downstream model family (ordinal for trees only, one-hot for low cardinality, target/hashing/embeddings for high cardinality).
- [ ] Any target/mean encoding is fit per-CV-fold (or with an equivalent out-of-fold scheme), never fit on the same rows it's applied to for training.
- [ ] Low-count categories in target encoding are smoothed toward the global mean, not left as a raw small-sample average.
- [ ] Unseen-category behavior at inference is explicit and tested (not left to throw by accident), and the unseen-category rate is monitored in production.
- [ ] For time-ordered data, encodings use only past rows relative to each encoded row.
