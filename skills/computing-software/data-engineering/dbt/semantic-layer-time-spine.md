---
id: computing-software.data-engineering.dbt.semantic-layer-time-spine
name: semantic-layer-time-spine
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-semantic-layer, metricflow, time-spine, metricflow-time-spine, cumulative-metrics, time-granularity, custom-calendar, fiscal-calendar]
level: advanced
status: gated
description: "Configure the MetricFlow time spine: a date spine model, time_spine YAML (1.9+), granularities, custom calendar columns, and why cumulative/offset metrics need it."
sources:
  - https://docs.getdbt.com/docs/build/metricflow-time-spine
  - https://docs.getdbt.com/docs/build/cumulative
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semantic Layer time spine

**Goal:** MetricFlow can produce complete time series (no missing days), cumulative/rolling metrics, period-over-period offsets, and fiscal-calendar groupings.

## Build the spine model
```sql
-- models/marts/utilities/time_spine_daily.sql
{{ config(materialized='table') }}
with days as (
    {{ dbt.date_spine('day', "to_date('2015-01-01')", "to_date('2035-12-31')") }}
)
select
    cast(date_day as date) as date_day,
    {{ fiscal_quarter('date_day') }} as fiscal_quarter,      -- your macro, e.g. FY starting July
    {{ fiscal_year('date_day') }}    as fiscal_year
from days
```
Cover the full range of your data plus future dates used in forecasts; queries outside the spine range lose rows.

## Register it (dbt 1.9+ YAML)
```yaml
models:
  - name: time_spine_daily
    time_spine:
      standard_granularity_column: date_day
      custom_granularities:
        - name: fiscal_quarter
          column_name: fiscal_quarter
        - name: fiscal_year
          column_name: fiscal_year
    columns:
      - name: date_day
        granularity: day
```
Older setups used a model literally named `metricflow_time_spine` with a `date_day` column; it still works but the YAML config is preferred. Add an hourly spine (`granularity: hour`) if any metric needs sub-daily grain.

## What uses it
- `cumulative` metrics (running totals, trailing windows `window: 7 days`, `grain_to_date: month`).
- `offset_window` in derived metrics (e.g. revenue vs same period last year). (gated: unconfirmed, source is paywalled or blocked)
- `fill_nulls_with: 0` / `join_to_timespine: true` on measures so days with no events appear as zero.
- Custom granularity queries: `mf query --metrics revenue --group-by metric_time__fiscal_quarter`.

## Gotchas
- Spine at a coarser grain than the metric's time dimension -> errors or wrong joins.
- Time zone: spine dates are naive; agg_time_dimension columns should be in the same zone convention.

## Verify
- [ ] `mf validate-configs` (or `dbt sl validate`) passes.
- [ ] A cumulative metric query returns a row for every day, including zero-activity days.

## Checked

2026-11-02

- Confirmed: The MetricFlow time spine page (time_spine key, standard_granularity_column, custom_granularities with column_name, column-level granularity, dbt 1.9+) and the cumulative metrics page (window, grain_to_date, join_to_timespine) were fetched.
- Removed or gated: Added the column_name that the docs example shows for custom granularities. Gated: offset_window, fill_nulls_with, the mf/dbt sl validate commands and the custom-granularity query syntax were not stated on the fetched pages.

Method: documentation only; no commands were run.
