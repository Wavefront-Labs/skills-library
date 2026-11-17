---
id: computing-software.data-engineering.etl-pipeline-design.partitioned-runs-and-backfill-design
name: partitioned-runs-and-backfill-design
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, partitioned-runs, backfill, idempotency, data-intervals]
level: advanced
status: docs-checked
description: "Design pipelines around partitioned runs (one run per date or key range): deterministic inputs, idempotent writes, safe backfills, concurrency and dependency handling."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#backfill
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partitioned runs and backfill design

**Goal:** any time slice can be (re)computed independently, identically and safely, so backfills are routine instead of scary.

## Principles (functional data engineering)
1. **A run = a partition**: run for `2026-10-17` reads only inputs for that interval and writes only that output partition.
2. **Deterministic**: no `now()` inside logic; use the run's interval (`data_interval_start` / `data_interval_end` in Airflow, the partition key in Dagster, a date variable passed to dbt). Airflow warns that for manually triggered runs the data interval may differ from the supplied `logical_date`, so use `logical_date` explicitly if you need the user-specified date.
3. **Idempotent overwrite**: write by replacing the partition (your engine's partition overwrite, or delete+insert in one transaction). Running twice = same result.
4. **Immutable inputs** where possible: read from raw/append-only layers with explicit partition filters.

```python
@task
def build(ds=None):   # Airflow injects the logical date string
    run_sql("""delete from mart.daily_sales where sale_date = %(d)s;
               insert into mart.daily_sales select ... from core.orders where order_date = %(d)s""", {"d": ds})
```

## Backfills
- Airflow: a backfill runs the Dag for a historical period, from the UI (Trigger > Backfill form: date range, reprocess behaviour, max active runs, optional backwards ordering) or the CLI: `airflow backfill create --dag-id DAG_ID --from-date START_DATE --to-date END_DATE --reprocess-behavior failed --max-active-runs 3 --run-backwards`. It re-runs all intervals within the dates.
- Catchup is separate: with `catchup=True` the scheduler creates a run for every interval not yet run; the default (`scheduler.catchup_by_default=False`) creates a run only for the latest interval. Leave catchup off if the Dag is not written to be limited to its interval.
- Dagster and dbt: use partition-aware backfills (Dagster) or date variables in incremental filters (dbt); check their current docs for the exact commands.
- Throttle with max active runs so the warehouse and sources are not overwhelmed; prioritise recent partitions.

## Dependencies
- Downstream partitions depend on upstream partitions of the same (or mapped) interval: sensors/assets per partition, not "latest".
- Partition mapping for different grains: daily -> weekly aggregates depend on 7 daily partitions.

## Gotchas
- Logic using "current" dimension attributes gives different results for old partitions; decide if backfills should use historical (SCD2 as-of) attributes.
- Changing code then backfilling mixes old and new logic across history unless you backfill everything affected.
- Partitions that span time zones: define the interval's time zone explicitly.

## Verify
Rerun a past partition twice: output identical (checksum) and no other partitions changed.

## Checked
Date: 2026-11-09. Confirmed from the Airflow Dag runs page (Catchup and Backfill sections: catchup default, backfill UI fields, CLI flags, logical_date caution). The Dagster page returned only a stub and the Medium article was blocked, so Dagster and functional-data-engineering points are design guidance, not confirmed claims. Removed: INSERT OVERWRITE and replaceWhere names, dbt --vars and --full-refresh specifics, the Airflow 3 and REST API backfill wording, and Dagster launch details. The Python snippet is an illustration.
Method: documentation only; no commands were run.
