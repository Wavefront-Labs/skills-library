---
id: computing-software.qa-testing-engineering.performance-testing.peak-load-forecasting
name: peak-load-forecasting
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [peak-load-forecast, growth-forecast, peak-to-average-ratio, seasonal-peaks]
level: practitioner
status: draft
description: "Forecast peak load targets for performance tests: busy-hour and peak-minute extraction, peak-to-average ratios, seasonal events, growth projections and safety margins."
sources:
  - https://sre.google/sre-book/software-engineering-in-sre/
  - https://sre.google/workbook/implementing-slos/
  - https://otexts.com/fpp3/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Peak and growth forecasting

**Goal:** test targets justified by data, not "10x for safety".

## Extract peaks from history
- Use at least 12 months of request metrics (or business events) to capture seasonality.
- Compute per-minute (or per-second) rates; the test target is based on the **peak minute** of the busiest day, not the daily average.
- Peak-to-average ratio = peak-minute rate / daily average rate. Typical web values are 2-5x, event-driven businesses far higher.

```sql
-- example on request logs
SELECT date_trunc('minute', ts) AS m, count(*) / 60.0 AS rps
FROM requests WHERE ts > now() - interval '365 days'
GROUP BY 1 ORDER BY rps DESC LIMIT 20;
```

## Project forward
target = historical peak x growth factor x event factor x safety margin
- Growth: trend from monthly peaks (linear or seasonal model; fpp3 methods), or business forecast (marketing plans, new markets).
- Event factor: known campaigns, Black Friday, sports events, product launches; use last year's event peak relative to its baseline.
- Safety margin: 20-50% depending on cost of failure and forecast confidence.

Example: last peak 400 rps x 1.3 growth x 1.0 (no extra event) x 1.25 margin = 650 rps target.

## Per-endpoint peaks
Peaks are not uniform: checkout may spike 8x during a sale while browse spikes 3x. Forecast per journey for the transaction mix.

## Document
Target table with the data source, date range, assumptions and owner sign-off. Review after each major event against actuals.

## Gotchas
- Bot traffic and retries inflate history; filter or account for them consciously.
- Averaging over 5-minute buckets hides sharp spikes; check finer granularity where available.

## Verify
Last year's event, replayed through the formula from the prior year's data, would have predicted within the margin.
