---
id: computing-software.ai-ml-engineering.feature-engineering.group-aggregate-features
name: group-aggregate-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, aggregation-features, groupby-features, entity-features, window-aggregates, featuretools]
level: practitioner
status: verified
description: "Build group aggregate features: per-entity counts, means, ratios to group statistics, multiple time windows, leakage-safe computation and serving consistency."
sources:
  - https://pandas.pydata.org/docs/user_guide/groupby.html
  - https://featuretools.alteryx.com/en/stable/getting_started/afe.html
  - https://docs.feast.dev/getting-started/concepts/feature-view
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Group aggregate features

**Typical wins:** transaction amount vs the customer's average, user activity counts over 7/30/90 days, merchant fraud rate, product's average rating.

## Patterns
```python
g = tx.groupby("customer_id")["amount"]
tx["cust_amt_mean"] = g.transform("mean")
tx["cust_amt_std"] = g.transform("std")
tx["amt_z_vs_cust"] = (tx["amount"] - tx["cust_amt_mean"]) / tx["cust_amt_std"].replace(0, np.nan)
tx["cust_tx_count"] = g.transform("count")
tx["cust_merchant_nunique"] = tx.groupby("customer_id")["merchant_id"].transform("nunique")
```
Useful families: count, sum, mean, std, min/max, nunique, last value, time since first/last event, ratio of current value to group mean, share of category within group.

## Time-aware windows (the usual correct version)
Aggregates must use only events **before** the prediction time:
```python
tx = tx.sort_values(["customer_id", "ts"]).set_index("ts")
roll = tx.groupby("customer_id")["amount"].rolling("30D", closed="left")   # excludes current row
tx["cust_amt_30d_sum"] = roll.sum().reset_index(level=0, drop=True)
tx["cust_tx_30d_cnt"] = roll.count().reset_index(level=0, drop=True)
```
With `closed="left"` the first event of an entity has no earlier rows, so sum is NaN (not 0): `fillna(0)` for sum/count. The assignment above works because the rolling result has the same row order and index as `tx` (checked, including duplicate timestamps across customers); if in doubt use `.to_numpy()` on the sorted frame.

Whole-history `transform` like the first block leaks future rows into training features; use it only for static snapshots computed strictly before the label period.

## Target-based aggregates
Group mean of the label (e.g. merchant fraud rate) is target encoding: compute out-of-fold or with time cutoffs, smooth with priors for small groups.

## Serving consistency
The same definitions must run online. Options: precompute in a feature store (batch or streaming materialization), or compute on request from a recent-events store. Define windows once (SQL/feature view) and reuse for training via point-in-time joins.

## Cardinality and sparsity
Small groups produce noisy statistics: add the count as a feature, shrink means toward the global mean, or require minimum support.

## Verify
- [ ] For a sample row, recompute aggregates by hand from events strictly before its timestamp; match the pipeline output.
