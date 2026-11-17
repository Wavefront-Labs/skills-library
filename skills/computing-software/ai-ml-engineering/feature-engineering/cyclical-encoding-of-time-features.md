---
id: computing-software.ai-ml-engineering.feature-engineering.cyclical-encoding-of-time-features
name: cyclical-encoding-of-time-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, time-series, cyclical-encoding, sine-cosine-encoding, hour-of-day, day-of-week, periodic-features]
level: practitioner
status: verified
description: "Encode periodic features (hour, weekday, month, wind direction) with sine/cosine pairs, one-hot or periodic splines, and know which models need it and which do not."
sources:
  - https://scikit-learn.org/stable/auto_examples/applications/plot_cyclical_feature_engineering.html
  - https://developers.google.com/machine-learning/crash-course/numerical-data
  - https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.SplineTransformer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cyclical encoding of time features

**Goal:** make 23:00 close to 00:00 and December close to January for models that otherwise see them as far apart.

## Sine/cosine pair
```python
import numpy as np
def cyc(x, period):
    return np.sin(2 * np.pi * x / period), np.cos(2 * np.pi * x / period)
df["hour_sin"], df["hour_cos"] = cyc(df.ts.dt.hour + df.ts.dt.minute / 60, 24)
df["dow_sin"], df["dow_cos"] = cyc(df.ts.dt.dayofweek, 7)
df["doy_sin"], df["doy_cos"] = cyc(df.ts.dt.dayofyear - 1, 365.25)
```
- Always use **both** sin and cos: sin alone maps 06:00 and 18:00 to opposite values but 03:00 and 09:00 to the same value.
- Computed: sin(2*pi*h/24) is 0.707 for both 03:00 and 09:00, and +1/-1 for 06:00/18:00.
- Use fractional values (hour + minute/60) for smoothness.
- Day-of-month has variable period (28-31); use day-of-year or a "fraction of month" `(day-1)/days_in_month`.
- Also works for angles (wind direction, compass heading).

## Alternatives
| Encoding | Pros | Cons |
|---|---|---|
| sin/cos | 2 columns, smooth, wraps | one harmonic: can only model a single smooth bump per cycle |
| one-hot | any shape | no smoothness, 24/7/12 columns, no wrap |
| periodic splines (`SplineTransformer(extrapolation="periodic")`) | smooth, flexible shape, wraps | more columns |
| multiple harmonics (sin/cos of 2x, 3x frequency) | Fourier series, flexible | more columns |
For linear models with a daily pattern that has two peaks (commute times), one sin/cos pair underfits; use splines or more harmonics.

## Which models need it
- Linear models, neural nets, distance-based models (KNN, clustering): yes.
- Tree ensembles: usually no - they can split raw hour into ranges; sin/cos may even hurt slightly because a split on one of the two columns is less natural. Keep raw values too and let validation decide.

## Gotchas
- Time zone: compute hour in the local time that drives behaviour, not UTC, for human-activity patterns.
- DST shifts create 23/25-hour days; local-time features handle them, UTC features don't.

## Verify
- [ ] Both sin and cos included for each cycle.
- [ ] Ablation: raw vs cyclical vs spline compared in CV for the chosen model.
- [ ] Time zone of derived features documented.
