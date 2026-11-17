---
id: computing-software.ai-ml-engineering.feature-engineering.exponentially-weighted-features
name: exponentially-weighted-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, ewm-features, exponential-moving-average, time-series, halflife, recency-weighting]
level: practitioner
status: verified
description: "Create exponentially weighted features: pandas ewm with span/halflife/times, per-entity EWMs without leakage, irregular timestamps, and choosing decay rates."
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
  - https://pandas.pydata.org/docs/user_guide/window.html#exponentially-weighted-window
  - https://otexts.com/fpp3/ses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Exponentially weighted features

**Why:** recent behaviour matters more than old behaviour. An EWM summarizes the whole history with decaying weights in one number, smoother than fixed windows and without a hard cutoff.

## Basic
```python
df = df.sort_values("ts")
df["sales_ewm_7"] = df["sales"].ewm(span=7, adjust=False).mean().shift(1)   # shift: exclude current value
df["sales_ewm_hl14"] = df["sales"].ewm(halflife=14, adjust=False).mean().shift(1)
```
- `span=N`: alpha = 2/(N+1), roughly comparable to an N-period moving average.
- `halflife=h`: weight halves every h periods (most interpretable).
- `adjust=False` gives the recursive form (matches online updates); `adjust=True` normalizes early weights.
- `.shift(1)` so the feature at time t uses only data up to t-1 (forecasting/leakage safety).

## Per entity
```python
df = df.sort_values(["store_id", "ts"])
df["sales_ewm"] = (df.groupby("store_id")["sales"]
                     .transform(lambda s: s.ewm(halflife=7, adjust=False).mean().shift(1)))
```

## Irregular timestamps
Event data with uneven gaps: use time-based decay so a 30-day gap counts more than a 1-day gap:
```python
s = df.set_index("ts")["amount"]
ewm = s.ewm(halflife="7D", times=s.index).mean()   # `times` requires adjust=True (adjust=False raises)
```

## Online serving
The recursive form updates in O(1). For regular steps with `adjust=False`: `ewm_new = alpha * x + (1 - alpha) * ewm_old`. For the irregular `times=` form (which is `adjust=True`) that formula does NOT match pandas; keep two numbers per entity and decay both by `d = 0.5 ** (dt / halflife)`: `num = num * d + x; den = den * d + 1; ewm = num / den` (matched pandas exactly in a test). Store the state per entity in the online store; make sure batch training reproduces the same update rule.

## Choosing decay
Create several half-lives (e.g. 1, 7, 30 days) and let the model choose; combinations (short minus long EWM) capture trend/momentum. EWM variance (`ewm().std()`) captures volatility.

## Verify
- [ ] Recompute the feature for one entity with a manual loop; values match; no row uses its own target-period value.
