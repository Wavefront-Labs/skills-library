---
id: computing-software.ai-ml-engineering.feature-engineering.time-series-feature-engineering
name: time-series-feature-engineering
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, time-series, lag-features, rolling-window, look-ahead-bias, seasonality, autocorrelation, feature-store, point-in-time-correctness, windowed-aggregation, trend-decomposition]
level: advanced
status: draft
description: "Build time-series features (lags, rolling windows, seasonality) without look-ahead bias, and handle point-in-time correctness for features joined from other tables."
sources:
  - https://otexts.com/fpp3/
  - https://www.tableau.com/analytics/what-is-time-series-analysis
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Time-series feature engineering without look-ahead bias

**Goal:** build lag, rolling-window, and seasonal features that a model could have actually computed at prediction time — the single discipline that separates a time-series model that looks great in backtesting from one that actually works in production.

## 1. Look-ahead bias is the central failure mode, and it's easy to introduce by accident
- **A rolling/aggregate feature must only use data from strictly before the prediction time** for the row it's attached to. `df['rolling_mean'] = df['value'].rolling(7).mean()` computed naively and then used as a same-row feature is **not** look-ahead-safe unless you explicitly shift it: pandas' `.rolling(7).mean()` for row `t` includes rows `t-6..t` — if `value` at row `t` is only known after the thing you're predicting at `t` happens, you've leaked the present into the feature. Shift by one (`.rolling(7).mean().shift(1)`) so the window ends at `t-1`, not `t`, whenever the feature is meant to represent "what was knowable before now."
- The same trap applies to **any aggregation joined from another table** (a customer's "average order value," a product's "7-day sales count") — if that aggregate is computed once over the *entire* table's history (including future-relative-to-the-prediction-row data) and then joined back, every row effectively knows about events that hadn't happened yet relative to it. This is **point-in-time correctness**: the join must use an as-of timestamp, matching each row to only the data available as of that row's own timestamp, not the latest available data as of today.
- Feature stores designed for this (Feast, Tecton, or a hand-rolled as-of join in SQL/Spark using a `point_in_time <= event_timestamp` condition) exist specifically because getting this right by hand, row by row, across many feature pipelines is error-prone — if your organization doesn't have one, at minimum write the as-of join explicitly and test it with a synthetic row where you know the right answer.
- Backtesting with k-fold cross-validation (shuffling rows into folds) is **wrong for time series** for the same reason — a fold can end up training on future data and validating on the past relative to it. Use **time-series-aware splits** (`sklearn.model_selection.TimeSeriesSplit`, or a simple expanding/rolling-origin split) that always train on a time window strictly before the validation window.

## 2. Useful feature families and their gotchas
- **Lag features** (`value.shift(k)` for various `k`): the simplest and often most predictive time-series features — but choosing lags blindly (lag-1 through lag-30, say) multiplies feature count and encourages overfitting on short histories; use domain knowledge (known seasonal cycle length, known business cadence — weekly, monthly) to choose a small, justified lag set first, then let feature-importance analysis suggest more only if there's enough data to support it.
- **Rolling statistics** (rolling mean/std/min/max over various windows): smooth noise and capture recent trend — but a rolling window needs to be long enough to be stable yet short enough to still be "recent"; too-short windows are themselves noisy, too-long windows lag real changes. Test a couple of window lengths against validation performance rather than picking one arbitrarily.
- **Calendar/seasonality features** (day-of-week, month, is-holiday, days-since-event): cheap to compute, frequently among the most predictive features for anything with human behavioral cycles (retail, traffic, energy demand) — don't skip these in favor of only numeric lags; a model with lags but no calendar features often misses a large, easily explainable seasonal signal.
- **Decomposition-based features** (trend/seasonal/residual via STL or classical decomposition): useful as a diagnostic (confirming what seasonality actually exists before hand-picking lag periods) and occasionally as features themselves (e.g. use only the residual, after removing a known seasonal/trend component, as a cleaner input) — but decomposition fit on the full series (including future-relative-to-each-row data) is itself a look-ahead-bias risk if used naively as a per-row feature; same discipline as rolling windows applies.

## 3. Missing data and cold-start
- Lag/rolling features are undefined for the first `k` rows of any series (a new entity — new customer, new store — has no history yet) — decide explicitly how to handle this: drop those rows from training (loses early-life data), impute with a population-level default (risks papering over genuinely different cold-start behavior), or build a separate cold-start model/feature set for entities with insufficient history. Silently leaving NaNs for a model that doesn't handle them (many linear models, some gradient boosting configs) either errors or silently drops rows in a way that skews the training distribution toward longer-history entities.
- Irregular/missing timestamps (gaps in the series) break naive `.shift()`/`.rolling()` assumptions, which assume a fixed, regular time index — resample to a regular frequency first (with an explicit fill/interpolation policy for gaps) before computing lag/rolling features, or compute features using explicit time-based windows (`.rolling("7D")` in pandas, not `.rolling(7)` rows) which are robust to irregular spacing.

## Verify
- [ ] Every rolling/lag feature confirmed to only use data strictly before its row's timestamp (shifted correctly, checked on a synthetic example with a known right answer).
- [ ] Any feature joined from another table uses a point-in-time/as-of join, not a join against the latest available aggregate.
- [ ] Train/validation splits are time-ordered (expanding or rolling-origin), not randomly shuffled k-fold.
- [ ] Calendar/seasonality features are included, not only numeric lags.
- [ ] Cold-start/missing-history rows have an explicit, deliberate handling policy, not silent NaNs or silent row drops.
- [ ] Rolling/lag features use time-based windows (not row-count windows) if the series has irregular timestamps.
