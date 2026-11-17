---
id: computing-software.ai-ml-engineering.feature-engineering.automated-time-series-features-tsfresh
name: automated-time-series-features-tsfresh
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, tsfresh, time-series-features, automated-feature-extraction, feature-relevance, rolling-windows]
level: practitioner
status: draft
description: "Extract hundreds of time-series features automatically with tsfresh: long-format input, extraction settings, relevance filtering, rolled windows and leakage control."
sources:
  - https://tsfresh.readthedocs.io/en/latest/
  - https://tsfresh.readthedocs.io/en/latest/text/feature_extraction_settings.html
  - https://tsfresh.readthedocs.io/en/latest/text/forecasting.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Automated time-series features (tsfresh)

tsfresh computes a large library of per-series features (statistics, autocorrelation, FFT coefficients, entropy, peaks, trend) and filters them with hypothesis tests against the target.

## Input format
Long format: one row per (id, time, value), optionally several value columns (`kind`).
```python
from tsfresh import extract_features, select_features, extract_relevant_features
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters
from tsfresh.utilities.dataframe_functions import impute
X = extract_features(long_df, column_id="machine_id", column_sort="ts", column_value="vibration",
                     default_fc_parameters=EfficientFCParameters(), n_jobs=8)
impute(X)                                   # replaces NaN/inf from undefined features in place
X_sel = select_features(X, y)               # y indexed by machine_id; Benjamini-Yekutieli FDR control
```
- `MinimalFCParameters` for a quick test; `EfficientFCParameters` skips the most expensive; `ComprehensiveFCParameters` (default) computes ~800 features per series.
- Restrict to chosen calculators: `kind_to_fc_parameters = tsfresh.feature_extraction.settings.from_columns(X_sel)` and reuse that dict to extract only selected features for new data (much faster at inference).

## Classification/regression per series
Typical use: each id is one sample (a machine run, a patient stay, an ECG segment) with one label. Extract per id, select, then train any tabular model.

## Forecasting: rolled windows
```python
from tsfresh.utilities.dataframe_functions import roll_time_series
rolled = roll_time_series(df, column_id="store", column_sort="date", max_timeshift=28, min_timeshift=7)
Xr = extract_features(rolled, column_id="id", column_sort="date", column_value="sales", default_fc_parameters=MinimalFCParameters())
```
Each window `(store, end_date)` only contains data up to its end date: features describe the past at that time. Join targets from the next period(s).

## Leakage control
- `select_features` uses the target: run it inside the training fold only, not on all data, or validation scores are optimistic.
- Rolled windows must end before the prediction time; check the window ids.

## Cost
Comprehensive extraction on many long series is slow (hours). Use `n_jobs`, `chunksize`, Dask/Spark bindings (`tsfresh.convenience.bindings`), or downsample series first.

## Alternatives
`tsfel`, `catch22` (22 curated features, fast), `sktime`/`aeon` transformers (MiniRocket for classification is often stronger and faster than feature extraction).

## Verify
Compare CV score of the selected features vs a small hand-made set (mean, std, last value, slope); keep tsfresh only if it adds clear lift.
