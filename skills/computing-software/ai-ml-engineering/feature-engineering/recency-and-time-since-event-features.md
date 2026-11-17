---
id: computing-software.ai-ml-engineering.feature-engineering.recency-and-time-since-event-features
name: recency-and-time-since-event-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, recency-features, time-since-event, rfm, days-since-last, point-in-time, customer-features]
level: practitioner
status: verified
description: "Build time-since-event and recency features (days since last purchase, login, failure; RFM) correctly as of each prediction time, with censoring, caps and decayed counts."
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html
  - https://docs.feast.dev/getting-started/concepts/point-in-time-joins
  - https://en.wikipedia.org/wiki/RFM_(market_research)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Time-since-event and recency features

Recency is often the strongest single predictor in churn, conversion, fraud and maintenance models: how long since the customer last bought, since the machine last failed, since the password changed.

## Compute as of the prediction time
For each prediction row `(entity, as_of)`, use only events with `event_ts < as_of`:
```python
events = events.sort_values("event_ts"); preds = preds.sort_values("as_of")
last = pd.merge_asof(preds, events[["customer_id", "event_ts"]].rename(columns={"event_ts": "last_purchase_ts"}),
                     left_on="as_of", right_on="last_purchase_ts", by="customer_id",
                     direction="backward", allow_exact_matches=False)
last["days_since_purchase"] = (last["as_of"] - last["last_purchase_ts"]).dt.total_seconds() / 86400
```
Checked: with `allow_exact_matches=False` an event at the same instant is excluded; entities with no prior event get NaT/NaN. SQL equivalent (runs in SQLite 3.50): `MAX(event_ts) FILTER (WHERE event_ts < p.as_of)` grouped per prediction row, or a lateral join.

Computing "days since last purchase" relative to *today* or the dataset end for training rows is the classic leakage bug.

## Never-happened (censoring)
No prior event gives NaN. Options: fill with time since entity creation (time-at-risk) plus a `never_purchased` flag; or a large cap value plus the flag. Avoid filling with 0 (means "just happened").

## Variants
- **Time since first event** (tenure), **time between last two events** (inter-event gap), ratio of current gap to typical gap (`days_since / median_gap`: "overdue" signal, strong for churn).
- **RFM**: Recency, Frequency (count in window), Monetary (sum in window); quantile-scored for segmentation.
- **Decayed counts**: `sum(exp(-(as_of - t_i)/tau))` over past events: smooth blend of recency and frequency; several taus (7, 30, 180 days).
- **Time since state change**: last plan change, last address change, last config deploy.

## Transformations
- `log1p(days_since)`: recency effects are usually strongest at small values.
- Cap at a horizon (e.g. 365 days) to limit outlier influence for linear models; trees do not need it.

## Serving
At serving time, compute against `now()` with the same definition (strictly before now, same time zone, same event types). Online feature stores keep `last_event_ts` per entity updated by streams; compute `now - last_event_ts` at request time (on-demand feature) rather than storing a stale "days since" value.

## Verify
For a sample of training rows, recompute recency manually from raw events with the row's as_of; ensure no event at or after as_of is used, and compare feature distributions between training and recent serving logs.
