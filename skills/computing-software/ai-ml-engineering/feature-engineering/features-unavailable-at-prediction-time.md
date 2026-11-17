---
id: computing-software.ai-ml-engineering.feature-engineering.features-unavailable-at-prediction-time
name: features-unavailable-at-prediction-time
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, prediction-time-availability, data-leakage, feature-availability, point-in-time, latency-of-data, temporal-leakage]
level: practitioner
status: draft
description: "Audit every feature for availability at the moment of prediction: data latency, backfilled values, post-event updates, as-of snapshots and building an availability map."
sources:
  - https://developers.google.com/machine-learning/crash-course/overfitting/data-leakage
  - https://docs.feast.dev/getting-started/concepts/point-in-time-joins
  - https://www.kaggle.com/code/alexisbcook/data-leakage
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Features unavailable at prediction time

A feature can be legitimate in concept and still leak if, at the real decision moment, its value is not yet known or is different from what the training table holds.

## Typical traps
- **Data latency**: transactions land in the warehouse with a 1-2 day delay; training uses the complete table, production sees partial data.
- **Overwritten records**: customer table stores the *current* address/status; training rows from last year join today's values (status "closed" leaks churn).
- **Backfilled or corrected values**: lab results revised later, chargebacks posted weeks after transaction, labels corrected manually.
- **Batch timing**: features computed nightly are up to 24 h stale at request time, but training joined them at exact event time.
- **Downstream process outputs**: "assigned investigator", "approved credit limit", "discharge code" exist only after the decision being predicted.
- **Aggregates over windows that extend past the prediction time** ("transactions this month" computed at month end).

## Build an availability map
For each feature, record:
| Feature | Source | When created | Available to the model at decision time? | Latency | Mutable? |
|---|---|---|---|---|---|
Ask data owners: when is the value written, can it change after, and is history kept?

## Fixes
- Use **as-of snapshots** or change-data-capture history (SCD type 2 tables with valid_from/valid_to) and join point-in-time.
- Simulate latency in training: as-of time = decision time minus known delay (`as_of = event_ts - pd.Timedelta("2D")` for warehouse features).
- Use the **same feature pipeline** for training and serving (feature store with point-in-time joins, or log features at serving time and train on the logs).
- Drop features that do not exist at decision time, however predictive.

## Detect
- Suspiciously high importance for operational fields (status codes, IDs assigned later, timestamps).
- Large gap between offline validation and online/shadow performance.
- Compare training feature values with values **logged at serving time** for the same entities: mismatches reveal latency or mutation.
- Backtest: rebuild the training set as of a past date using only data that existed then, and compare.

## Verify before launch
Run the model in shadow mode on live traffic, logging features as served; compute metrics once labels arrive and compare to offline numbers.
