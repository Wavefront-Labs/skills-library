---
id: computing-software.data-engineering.etl-pipeline-design.batch-ids-and-audit-columns
name: batch-ids-and-audit-columns
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, audit-columns, batch-id, load-metadata, lineage, idempotency, run-log, record-source]
level: practitioner
status: docs-checked
description: "Add standard audit columns (batch id, loaded_at, source file, row hash) and a run log table so rows are traceable, reruns surgical and loads reconcile."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/etl-architecture-34-subsystems/
  - https://docs.getdbt.com/reference/dbt-jinja-functions/invocation_id
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch IDs and audit columns

**Goal:** answer "which run loaded this row, from which file, and when" for any row, and delete/reload exactly one bad batch.

## Standard columns
| Column | Content | Purpose |
|---|---|---|
| `_batch_id` | orchestrator run id (Airflow `run_id`, dbt `invocation_id`, job run id) | surgical rollback, lineage |
| `_loaded_at` | timestamp of load (UTC) | freshness, incremental watermarks downstream |
| `_source_file` / `_record_source` | file path, source system, API endpoint | debugging, multi-source dedup |
| `_source_row` | file row number / source offset | exact dedup and tracing |
| `_row_hash` | hash of business columns | change detection, dedup |
| `_extracted_at` | when pulled from source (vs loaded) | latency measurement |
| `_is_deleted` | soft-delete flag from CDC/hard-delete detection | history without loss |

Prefix with `_` (or a consistent convention) so they are clearly technical and easy to exclude from marts.

## Populate
```sql
insert into raw.orders
select s.*, '{{ run_id }}' as _batch_id, current_timestamp as _loaded_at,
       s.source_file_path as _source_file, md5(to_json(s.*)) as _row_hash   -- illustrative; function names vary by engine
from staged s;
```
dbt: `invocation_id` outputs a UUID generated for each dbt command, so `'{{ invocation_id }}' as _dbt_invocation_id` and `current_timestamp as _dbt_loaded_at` in a macro applied to incremental models stamp every row. dbt also puts `invocation_id` in the query-comment context, event and log info, artifact metadata, and as a label on all BigQuery jobs it originates, so rows can be tied back to logs.

## Run log table
```sql
create table ops.load_runs (
  batch_id varchar primary key, pipeline varchar, source varchar,
  started_at timestamp, finished_at timestamp, status varchar,
  rows_read bigint, rows_written bigint, rows_rejected bigint,
  watermark_from varchar, watermark_to varchar, error text);
```
Write a row at start (`running`) and update at end. Watermarks per run make incremental windows auditable and replayable.

## Using them
- **Rollback a bad batch:** `delete from raw.orders where _batch_id = 'scheduled__2026-10-17T03:00'` then rerun.
- **Reconcile:** `select _batch_id, count(*) from raw.orders group by 1` vs `rows_written` in run log vs source counts.
- **Freshness:** `max(_loaded_at)` per table feeds observability.

## Gotchas
- Using `current_timestamp` as the incremental watermark for downstream models is fine, but use the **source** change timestamp for business logic (late loads would otherwise look new).
- Batch ids must be stable across retries of the same logical run so reruns replace rather than add. In Airflow, clearing a task increments that task instance's `try_number` within the same Dag run, so key on the Dag run id, not the try. A dbt `invocation_id` is new for every command, so a rerun gets a different id: record which invocation replaced which.
- Do not propagate all audit columns into marts; keep `_loaded_at` and lineage keys where useful.

## Verify
- [ ] Every raw/bronze table has the standard columns (schema test).
- [ ] Deleting and rerunning one batch restores identical row counts.

## Checked
Checked 2026-11-08: dbt "About invocation_id" page (read in full: UUID per command, where it appears, example usage) and the Kimball Group "ETL Architecture's 34 Subsystems" overview (read in full; it only describes the subsystem categories, 13 of which manage the production ETL environment, and contains no audit-column specifics). The Airflow try_number remark comes from the Airflow Dag Runs page (Re-run Tasks section). The column list, run log DDL and SQL are design advice and illustrative SQL, not documentation claims, and were not run.
Method: documentation only; no commands were run.
