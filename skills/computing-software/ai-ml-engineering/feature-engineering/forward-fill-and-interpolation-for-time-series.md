---
id: computing-software.ai-ml-engineering.feature-engineering.forward-fill-and-interpolation-for-time-series
name: forward-fill-and-interpolation-for-time-series
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, missing-data, forward-fill, interpolation, time-series-gaps, resampling, look-ahead-bias]
level: practitioner
status: verified
description: "Fill gaps in time series without leaking the future: resample to a regular grid, forward-fill with limits, causal interpolation, gap-length features and imputed flags."
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ffill.html
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html
  - https://pandas.pydata.org/docs/user_guide/timeseries.html#resampling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forward-fill and interpolation for time series gaps

**Goal:** a regular, gap-handled series where every filled value only uses information available at that time.

## Make the grid explicit
```python
s = df.set_index("ts").sort_index()["temp"]
s = s.resample("5min").mean()                    # regular grid; empty buckets become NaN
```
Per-entity data: `df.groupby("sensor_id").resample("5min", on="ts").mean()`, so fills never cross entities.

## Causal filling (safe for features)
```python
filled = s.ffill(limit=6)                        # carry last value forward up to 30 minutes
gap_len = s.isna().groupby(s.notna().cumsum()).cumsum()   # consecutive missing steps so far
was_imputed = s.isna() & filled.notna()
```
- `limit` caps how many consecutive steps are filled, but it fills the FIRST `limit` steps of a longer gap and leaves the rest NaN (checked: a gap of 5 with `limit=2` gets 2 filled); `interpolate(limit=3)` behaves the same, so a long outage is still partly filled. Mask long gaps explicitly if that matters.
- `limit` stops a stale value from being carried through a long outage; beyond it, keep NaN and let the model (or a downstream rule) handle it.
- Add `was_imputed` and `gap_len` features: a reading carried for 2 hours means something different from a fresh one.
- State-like variables (account status, price list, setpoint) are naturally forward-filled; physical measurements usually tolerate only short fills.

## Interpolation (careful)
```python
s.interpolate(method="time", limit=3, limit_area="inside")
```
Linear/time interpolation uses the **next** observation, i.e. the future. Fine for offline analysis, cleaning historical training *targets* when you explicitly accept it, or reconstruction after the fact - **not** for features computed at prediction time, where the next value doesn't exist yet. Training on interpolated features and serving with forward-filled ones creates train/serve skew. Same for `bfill` and centred rolling windows.

## Seasonal gaps
For long gaps in strongly seasonal series, fill with the value from the same time last period (`s.fillna(s.shift(freq="7D"))`) or a seasonal-naive model, and mark it imputed.

## Gotchas
- Duplicated timestamps break `resample`/`reindex`: deduplicate (aggregate) first.
- Time zones and DST: resample in UTC, derive local-time features afterwards.
- Irregular event data (transactions) should usually be aggregated (counts, sums -> 0 when no events), not forward-filled.

## Verify
- [ ] No fill method uses future values for prediction-time features.
- [ ] Fill limits set per variable type; imputed flags present.
- [ ] Training and serving use the identical gap-handling code.
