---
id: computing-software.data-engineering.data-quality.metric-anomaly-detection
name: metric-anomaly-detection
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-observability, dq-anomaly-detection, volume-anomaly, seasonality, z-score, mad, prophet, alert-thresholds]
level: practitioner
status: gated
description: "Detect anomalies in data quality metrics (row counts, null rates, sums, freshness): robust baselines, seasonality, z-score and MAD thresholds, minimum history, and tuning false alarms."
sources:
  - https://otexts.com/fpp3/
  - https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
  - https://facebook.github.io/prophet/docs/quick_start.html
  - https://docs.soda.io/soda-cl/anomaly-detection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Statistical anomaly detection on DQ metrics

**Goal:** alert when today's row count, null rate, distinct count or total looks abnormal for this table — without hand-setting thresholds for thousands of tables, and without crying wolf.

## 1. Collect metrics first
Per table (and key column) per load/day, store in `ops.dq_metrics(dataset, metric, ts, value)`: row count (or rows added), null % per column, distinct count of keys, sum of main measures, freshness lag, schema hash. One narrow table makes the detection generic.

## 2. Baseline with seasonality
Most data metrics have weekly patterns (weekends) and growth. Compare like with like:
- same weekday over the last N weeks (e.g. 8 Mondays), or
- residuals after removing trend + weekly seasonality (STL decomposition, Prophet).

## 3. Robust thresholds
Mean/stddev are distorted by past incidents; use median and MAD:
```sql
WITH hist AS (
  SELECT dataset, metric, value FROM ops.dq_metrics
  WHERE ts >= current_date - 56 AND ts < current_date
    AND dayofweek(ts) = dayofweek(current_date)),             -- same weekday, last 8 weeks
stats AS (
  SELECT dataset, metric, median(value) AS med,
         median(abs(value - med_inner)) * 1.4826 AS mad          -- scaled MAD ~ stddev for normal data
  FROM (SELECT *, median(value) OVER (PARTITION BY dataset, metric) AS med_inner FROM hist)
  GROUP BY dataset, metric)
SELECT t.dataset, t.metric, t.value, s.med, (t.value - s.med) / NULLIF(s.mad, 0) AS robust_z
FROM ops.dq_metrics t JOIN stats s USING (dataset, metric)
WHERE t.ts = current_date AND ABS((t.value - s.med) / NULLIF(s.mad, 0)) > 4;
```
(Run on DuckDB 1.5: returns robust_z 268.8 for 500 vs history 100-103. `median` may be `percentile_cont(0.5)` / `approx_percentile` and `dayofweek` may not exist on other engines; in DuckDB Sunday = 0.)
- |robust z| > 3.5-4 is a sensible starting threshold.
- MAD = 0 (constant metric) → any change is anomalous; handle as exact-match rule. The query above does NOT do this: `NULLIF(s.mad, 0)` makes robust_z NULL so a constant history never alerts (tested in DuckDB: 8 weeks of 100 then a different value returns no row). Add `OR (s.mad = 0 AND t.value <> s.med)` to the WHERE clause.

## 4. Practical rules
- **Minimum history** (e.g. 4 same-weekday points) before alerting; new tables use static rules.
- **Direction matters**: row count drops are usually worse than spikes; null-rate increases matter, decreases don't. Use one-sided tests where appropriate.
- **Combine with absolute floors**: "rows = 0" is always critical regardless of statistics.
- **Holidays/known events**: suppress or annotate via a calendar table.
- Exclude anomalous days from future baselines once confirmed as incidents (or the robust stats handle a few).

## 5. Tooling
Soda anomaly detection checks, dbt packages (elementary `volume_anomalies`, `column_anomalies`; both in the Elementary docs), Databricks Lakehouse Monitoring / anomaly detection, Monte Carlo/Bigeye/Metaplane (gated: unconfirmed, source is paywalled or blocked), or Prophet for strongly seasonal metrics. All of these still need the tuning rules above.

## 6. Tune with feedback
Log each alert's outcome (true issue / expected / noise). Precision below ~50% → raise thresholds or add seasonality; missed incidents → add metrics or lower thresholds for critical tables only.

## Verify
- [ ] Backtest: replaying the last 90 days flags known past incidents and few other days.
- [ ] Zero-row loads alert regardless of history.
- [ ] Alert precision is tracked monthly.
