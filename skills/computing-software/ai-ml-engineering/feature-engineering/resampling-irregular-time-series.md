---
id: computing-software.ai-ml-engineering.feature-engineering.resampling-irregular-time-series
name: resampling-irregular-time-series
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, time-resampling, pandas-resample, irregular-time-series, aggregation, asfreq, time-series]
level: practitioner
status: draft
description: "Resample irregular event or sensor data to a fixed frequency with pandas resample: choosing aggregations, label/closed edges, filling gaps, time zones and per-entity resampling."
sources:
  - https://pandas.pydata.org/docs/user_guide/timeseries.html#resampling
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html
  - https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Resampling irregular series to a fixed frequency

Most forecasting and sequence models expect regular time steps. Events (transactions, clicks, sensor readings at random intervals) must be aggregated to a grid.

## Basic downsampling
```python
s = df.set_index("ts").sort_index()                     # DatetimeIndex required
hourly = s.resample("1h").agg(amount_sum=("amount", "sum"), n_events=("amount", "size"),
                              temp_mean=("temp", "mean"), temp_last=("temp", "last"))
```
Choose aggregation by meaning:
| Signal | Aggregation |
|---|---|
| Flows (sales, counts, rainfall) | sum, count |
| Levels / states (temperature, price, inventory) | mean, last, or time-weighted mean |
| Extremes (latency, load) | max, quantile |
| Prices (finance) | OHLC: `resample("5min")["price"].ohlc()` |

## Edges and labels
- `closed` and `label` decide whether `10:00` covers `[10:00, 11:00)` (default for most frequencies, labelled by left edge) or `(9:00, 10:00]`. For features used at prediction time, label each bucket by its **end** so you never use a bucket before it is complete: `resample("1h", label="right", closed="right")`.
- Weekly/monthly anchors: `"W-MON"`, `"MS"` (month start), `"ME"` (month end; pandas 2.2+ aliases).
- `origin`/`offset` align buckets (e.g. trading day starting 09:30).

## Gaps
- Empty buckets: sum -> 0 (correct for flows), mean -> NaN. Decide explicitly: `hourly["amount_sum"].fillna(0)` vs forward-fill levels `hourly["temp_last"].ffill(limit=3)`.
- Upsampling (coarse to fine): `s.resample("1min").asfreq()` then `interpolate(method="time")` or `ffill()`; never interpolate across long outages without an indicator.
- Add `n_events` / a "was observed" flag so models can tell real zeros from missing data.

## Per entity
```python
out = (df.set_index("ts").groupby("sensor_id").resample("15min")["value"].mean().reset_index())
```
Ensures every entity gets its own grid; use `.reindex` with a full date range per entity if leading/trailing gaps must exist.

## Time zones and DST
Convert to UTC for storage (`tz_convert("UTC")`); resample daily in local time when the business day is local (`tz_convert("Europe/London").resample("1D")`). DST days have 23 or 25 hours: hourly-to-daily sums are correct, but "24 rows per day" assumptions break.

## Time-weighted mean for levels
Readings at irregular times bias plain means toward dense periods. Upsample with `ffill` to a fine grid then average, or integrate with `np.trapezoid` (NumPy 2.0+; `np.trapz` was removed) per bucket.

## Verify
Totals preserved for flows (`df.amount.sum() == hourly.amount_sum.sum()`), no future data in any bucket's label, and plots of raw vs resampled series for a few entities.
