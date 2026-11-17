---
id: computing-software.ai-ml-engineering.feature-engineering.purged-embargoed-time-series-cv
name: purged-embargoed-time-series-cv
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, purged-cv, embargo, time-series-cross-validation, data-leakage, timeseriessplit-gap]
level: practitioner
status: gated
description: "Prevent leakage in time-series validation: overlapping label windows, purging training rows near test folds, embargo periods, TimeSeriesSplit gap and walk-forward design."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
  - https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086
  - https://otexts.com/fpp3/tscv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Purged and embargoed time-series CV

**Leak:** when labels span a window (e.g. "churn in next 30 days", "return over next 5 days") or features use rolling windows, training rows close to the test period share information with test rows even under a chronological split.

## Simple fix: a gap
```python
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5, gap=30, test_size=60)    # rows sorted by time; units = rows
```
(Checked on 500 rows, `gap=30, test_size=60`: the gap leaves 30 unused rows between train end and test start.) `gap` drops that many samples between train and test. Set it to at least the label horizon (and the longest feature lookback if features use future-aligned aggregates). With one row per day this is days; with many rows per day, compute splits on time boundaries instead of row counts.

## Purging and embargo (Lopez de Prado, Advances in Financial Machine Learning (gated: unconfirmed, source is paywalled or blocked))
- **Purge:** remove training samples whose label window [t_start, t_end] overlaps any test sample's label window.
- **Embargo:** additionally drop training samples immediately after the test period (a fraction of the period), since serial correlation leaks backward when training data follows test data (relevant for combinatorial/k-fold CV on time series).
- Implementations: write a custom splitter yielding indices by timestamp comparisons. `PurgedKFold` exists in Hudson & Thames' `mlfinlab`, which is now proprietary ("all rights reserved" on its GitHub page), so do not assume a free install.

## Walk-forward design
Expanding or rolling training window, then predict the next period, step forward. Mirrors production retraining cadence; report metrics per fold to see degradation over time.

## Group plus time
For entity data (customers), also prevent the same entity's near-duplicate snapshots from crossing the boundary; combine time cutoffs with group logic.

## Verify
- [ ] For each fold, assert `max(train_label_end) < min(test_feature_start)` (or the embargo boundary).
- [ ] Compare scores with and without the gap: a big drop with the gap means the old setup leaked.
