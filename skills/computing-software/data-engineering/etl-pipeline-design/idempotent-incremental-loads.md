---
id: computing-software.data-engineering.etl-pipeline-design.idempotent-incremental-loads
name: idempotent-incremental-loads
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, etl, elt, incremental-load, idempotency, high-water-mark, watermark-column, overlap-window, merge, upsert, partition-overwrite, change-data-capture, cdc, debezium, replay, backfill, dead-letter-queue, deduplication, late-arriving-data, data-pipelines, batch-processing]
level: practitioner
status: gated
description: "Design incremental loads that can be re-run safely: high-water-mark extraction with overlap, MERGE or partition overwrite, CDC handling, deletes, replay/backfill and dead-letter rows."
sources:
  - https://debezium.io/documentation/reference/stable/index.html
  - https://docs.getdbt.com/docs/build/incremental-models
  - https://docs.databricks.com/en/delta/merge.html
  - https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotent incremental loads — move only what changed, safely

**Goal:** a pipeline that loads only new/changed data, produces the same target state no matter how many times a run is repeated, and can replay any past window on demand.

## 1. The two invariants
1. **Idempotent:** running load(window) twice equals running it once.
2. **Complete:** every source change eventually lands, including late and out-of-order ones.
Everything below serves these. If you can't guarantee both cheaply, a full reload of a small table is a legitimate design.

## 2. Extract: high-water mark with overlap
Track the last processed value of a monotonically increasing column (`updated_at`, an auto-increment id, a log sequence number) in a state table, not in memory:
```sql
-- state: etl_watermarks(pipeline, last_value)
SELECT * FROM src.orders
WHERE updated_at >  :last_value - INTERVAL '2 hours'   -- overlap
  AND updated_at <= :run_upper_bound;                   -- fixed upper bound
```
- **Fixed upper bound:** capture `run_upper_bound = now() - small safety lag` at run start and use it everywhere; advance the watermark to it only after the load commits. Using open-ended `> last_value` lets rows committed mid-extract slip between runs.
- **Overlap:** long transactions commit rows whose `updated_at` is earlier than rows you already saw. Re-reading a window (minutes to hours, sized from observed lateness) catches them; the idempotent write absorbs the duplicates.
- **Gotcha:** `updated_at` maintained by application code is often not updated on every change (bulk updates, triggers missing). Verify with source-vs-target counts, or use CDC.
- Timezones: store and compare in UTC; DST shifts create gaps or overlaps with local timestamps.

## 3. Load: make the write idempotent
Pick per target:
- **MERGE/upsert on the business key** — deduplicate the batch first (latest by `updated_at` or source sequence) and only update when the incoming version is newer, so replaying old data doesn't regress rows.
- **Partition overwrite** — for event data partitioned by date: recompute and atomically replace the affected partitions (`INSERT OVERWRITE ... PARTITION`, Delta `replaceWhere`, BigQuery partition decorators, dbt `insert_overwrite`).
- **Delete-then-insert in one transaction** for the window when MERGE isn't available.
- Never plain append without a dedupe key.
Checked on DuckDB 1.5.6: a MERGE from a staging table deduplicated with `qualify row_number() ... = 1` and guarded by `when matched and s.updated_at > t.updated_at` did not regress a newer target row, and a second run changed nothing. Engine-specific syntax (`INSERT OVERWRITE ... PARTITION`, Delta `replaceWhere`, BigQuery partition decorators) was not run (gated: unconfirmed, source is paywalled or blocked); dbt does list `insert_overwrite` as a built-in incremental strategy that replaces whole partitions.
Load to a staging table first, validate, then swap/merge in one transaction so readers never see half a load.

## 4. Change data capture
When the source can't provide a reliable timestamp, or deletes matter, use log-based CDC (e.g. Debezium reading the Postgres WAL / MySQL binlog into Kafka, or a managed equivalent).
- Each event carries an operation (Debezium `c`/`u`/`d`; `r` for snapshot reads, because a snapshot is a READ operation per the Debezium docs) and a source position (LSN/binlog offset). Order and dedupe by that position, not by arrival time.
- Apply deletes explicitly (hard delete or `is_deleted` soft-delete flag) — timestamp-based extraction never sees deletes.
- Initial snapshot plus streaming must be stitched consistently; follow the tool's snapshot mode rather than doing your own bulk copy.
- **Gotcha:** PostgreSQL docs: replication slots persist across crashes and "prevent removal of required resources even when there is no connection using them", which consumes storage and in extreme cases can shut the database down; drop slots no longer needed and monitor slot lag.

## 5. Replay and backfill
- Parameterize every run by `[start, end)` window; the scheduler supplies it (see computing-software.data-engineering.apache-airflow.idempotent-dag-design).
- Keep immutable raw/landing data (bronze) so you can replay transformations without re-extracting from the source.
- Backfill in bounded chunks with a concurrency limit to protect the source.

## 6. Bad records: dead letters, not dead pipelines
- Validate rows (schema, required fields, parse errors). Route failures to a dead-letter table/topic with the raw payload, error reason, pipeline, run id, and timestamp.
- Decide thresholds: fail the run if rejects exceed e.g. 1% (a sign of an upstream schema change); otherwise warn.
- Make reprocessing dead letters a supported command, and make it idempotent too.
See computing-software.data-engineering.data-quality.data-tests-and-freshness-slas.

## Verify
- [ ] Running the same window twice leaves target row count and checksums unchanged.
- [ ] Watermark advances only after a successful commit (kill the job mid-load and rerun to prove it).
- [ ] A row updated at the source with a back-dated timestamp inside the overlap appears in the target.
- [ ] Source deletes are reflected (hard or soft) when CDC is used.
- [ ] A one-week backfill can be launched by date range without code changes.
- [ ] Dead-letter volume is visible on a dashboard with an alert threshold.
