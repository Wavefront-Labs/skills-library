---
id: computing-software.data-engineering.etl-pipeline-design.reprocessing-partitions-for-late-data
name: reprocessing-partitions-for-late-data
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, partition-reprocessing, late-arriving-data, backfill, idempotency]
level: advanced
status: draft
description: "Handle late-arriving facts by reprocessing affected partitions: detecting touched partitions, lookback windows, idempotent overwrite, downstream propagation and cost."
sources:
  - https://docs.getdbt.com/docs/build/incremental-strategy#about-incremental_predicates
  - https://cloud.google.com/bigquery/docs/managing-partitioned-tables
  - https://docs.databricks.com/aws/en/delta/selective-overwrite
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reprocessing partitions for late data

**Goal:** outputs for a day become correct when late records for that day arrive, without full rebuilds.

## Detect affected partitions
Drive from **load time**, act on **event time**:
```sql
select distinct event_date
from raw.events
where _loaded_at > :last_successful_run_loaded_at;
```
These are the partitions to recompute downstream.

## Recompute idempotently
- Delta: `INSERT INTO t REPLACE WHERE event_date IN (...) SELECT ...` or `replaceWhere` option.
- BigQuery/Spark dynamic partition overwrite: `insert overwrite` with `spark.sql.sources.partitionOverwriteMode=dynamic`.
- Snowflake: `delete ... where event_date in (...)` + insert in one transaction, or MERGE.
- dbt: `incremental_strategy: insert_overwrite` (BigQuery/Spark) or `delete+insert` with `unique_key: event_date`.
Recompute the whole partition from source data, never "add the late rows" to aggregates.

## Lookback window as a safety net
Always reprocess the last N days (N from observed lateness distribution, e.g. p99.9 lateness = 2 days -> N = 3) in addition to detected partitions. Very late data beyond N goes through the detected-partitions path or a manual backfill.

## Propagate downstream
Every dependent model must reprocess the same partitions: pass the partition list as a run parameter (Airflow params / dbt vars) or let each model detect from its upstream's load timestamps.

## Measure lateness
```sql
select datediff('hour', event_ts, _loaded_at) lateness_h, count(*)
from raw.events where _loaded_at > current_date - 30 group by 1 order by 1;
```

## Gotchas
- Partition by event date but cluster raw by load date for cheap detection queries.
- Reprocessing very old partitions can conflict with closed financial periods: route to a restatement process.

## Verify
Inject records for 5 days ago; after the next run, that day's outputs include them and other days are unchanged.
