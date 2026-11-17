---
id: computing-software.ai-ml-engineering.feature-engineering.leakage-safe-feature-construction
name: leakage-safe-feature-construction
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, data-leakage, target-leakage, point-in-time-correctness, as-of-join, merge-asof, target-encoding, out-of-fold, targetencoder, time-window-aggregates, rolling-features, feature-store, feast, get-historical-features, online-offline-skew, training-serving-skew, label-horizon, entity-timestamp, sql-window-functions, machine-learning, out-of-fold-features]
level: advanced
status: docs-checked
description: "Build features that only use information available at prediction time: point-in-time joins, out-of-fold target encoding, time-window aggregates, and feature stores such as Feast."
sources:
  - https://docs.feast.dev/
  - https://scikit-learn.org/stable/common_pitfalls.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html
  - https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Leakage-Safe Feature Construction — only what you would have known then

**Goal:** every training row's features use only data that existed at that row's prediction time, so offline metrics match production.

## 1. Anchor every row in time
Each training example needs an **entity key** (customer id) and a **prediction timestamp** (when the model would have scored it), separate from the **label timestamp** (when the outcome became known). Write the label definition with an explicit horizon: "churned within 30 days after `prediction_ts`". Every feature query then becomes "as of `prediction_ts`".

Classic leaks to hunt for:
- Columns updated after the event: `account_status = closed`, `total_refunds`, "last_login" snapshotted today.
- IDs or row order that encode the label (case numbers assigned after diagnosis, sorted files).
- Aggregates computed over the full table, including the future.
- Snapshot tables joined on key only — you get today's value, not the value at prediction time.
A model that looks too good (a sudden implausible jump in AUC after adding one feature) is leaking until proven otherwise. Inspect top feature importances for anything that "knows" the outcome.

## 2. Point-in-time (as-of) joins
For each (entity, prediction_ts) take the latest feature value with `feature_ts <= prediction_ts` (strictly `<` if the value was only available after a processing delay).
```python
import pandas as pd
train = pd.merge_asof(labels.sort_values("prediction_ts"),
                      feats.sort_values("feature_ts"),
                      left_on="prediction_ts", right_on="feature_ts",
                      by="customer_id", direction="backward",
                      tolerance=pd.Timedelta("30D"))
```
In SQL, join on `f.feature_ts <= l.prediction_ts` and keep the max `feature_ts` per row with `ROW_NUMBER() OVER (PARTITION BY l.row_id ORDER BY f.feature_ts DESC) = 1`.
Gotcha: **availability latency.** If a nightly batch lands at 06:00 for the previous day, a 01:00 prediction cannot use yesterday's value. Use the time the data *landed*, not the event time, or subtract the pipeline lag.

## 3. Time-window aggregates
"Transactions in the last 7/30/90 days" must be computed relative to each row's `prediction_ts`, over `(prediction_ts − window, prediction_ts]`. In SQL use window frames over event time (e.g. `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW`, syntax varies by engine) and make sure the current event's own outcome is not inside the frame. In pandas, `groupby(...).rolling("7D", on="ts", closed="left")` excludes the current row. Build the same code path for training (backfill) and serving so definitions cannot diverge.

## 4. Target encoding without leakage
Replacing a high-cardinality category with its mean target leaks the row's own label if computed on the same rows. Do it **out-of-fold**: split training data into K folds; encode fold k using statistics from the other folds; encode validation/test with statistics from the full training set. Add smoothing toward the global mean so rare categories (say < 20 rows) are not memorised.
scikit-learn ≥ 1.3 provides `sklearn.preprocessing.TargetEncoder`, whose `fit_transform` does internal cross-fitting (`cv=5` default) — note that `fit(X).transform(X)` is **not** the same and leaks. Keep it inside a Pipeline so CV refits it per fold (computing-software.ai-ml-engineering.scikit-learn.pipelines-and-cross-validation). For temporal data, encode using only earlier periods (expanding mean shifted by one).

## 5. Feature stores (Feast and similar)
A feature store keeps one definition per feature and serves it two ways: an **offline** store for point-in-time correct training sets and an **online** store (Redis, DynamoDB, ...) for low-latency serving.
```python
from feast import FeatureStore
fs = FeatureStore(repo_path="<PROJECT_ROOT>/feature_repo")
train_df = fs.get_historical_features(
    entity_df=labels[["customer_id", "event_timestamp"]],
    features=["customer_stats:txn_count_30d", "customer_stats:avg_amount_30d"]).to_df()
online = fs.get_online_features(features=[...], entity_rows=[{"customer_id": 42}]).to_dict()
```
- `get_historical_features` performs the as-of join using the entity dataframe's `event_timestamp`; each feature view's `ttl` limits how stale a value may be.
- Run `feast apply` after changing definitions and `feast materialize-incremental <END_TS>` to load the online store; stale materialisation is a common cause of online/offline skew.

## 6. Prove it
Log served feature values at prediction time and compare them with the offline values recomputed for the same entity and timestamp. Differences beyond float noise are skew — monitor them continuously (computing-software.ai-ml-engineering.mlops.production-model-monitoring).

## Verify
- [ ] Every training row has an entity key, `prediction_ts` and a label horizon, and labels start after `prediction_ts`.
- [ ] All feature joins are as-of joins that respect data landing latency.
- [ ] Window aggregates exclude the current event's outcome and anything after `prediction_ts`.
- [ ] Target encoding is out-of-fold (or `TargetEncoder.fit_transform` inside a Pipeline).
- [ ] Offline-recomputed features match logged online features for a sample of production requests.
- [ ] Removing the single most important feature does not drop performance to near-baseline without a business explanation.

## Checked

2026-11-02. Checked against pandas.merge_asof (by, left_on/right_on, direction, tolerance, sorted keys), scikit-learn TargetEncoder (added in 1.3, cv=5 default, fit_transform uses cross fitting and fit(X, y).transform(X) differs) and the common pitfalls page, and Feast docs (quickstart, point-in-time joins, CLI reference): get_historical_features with an entity dataframe, get_online_features, feast apply, feast materialize-incremental, ttl on feature views, offline and online stores. Removed: the list of comparable products (not in the fetched pages) and the specific AUC example numbers (replaced by a generic statement).

Method: documentation only; no commands were run.
