---
id: computing-software.data-engineering.etl-pipeline-design.checkpoint-restart-for-batch-jobs
name: checkpoint-restart-for-batch-jobs
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, error-handling, checkpoint-restart, resumable-jobs, chunked-processing, control-table, backfills, idempotency, long-running-jobs]
level: practitioner
status: docs-checked
description: "Make long batch jobs and backfills resumable: work units, a control table, idempotent per-unit writes, restart from the first incomplete unit, safe concurrency."
sources:
  - https://docs.spring.io/spring-batch/reference/step/chunk-oriented-processing.html
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#backfill
  - https://docs.databricks.com/aws/en/delta/selective-overwrite
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkpoint/restart for long batch jobs

**Goal:** a 6-hour job or a 3-year backfill that fails at hour 5 resumes from where it stopped, without duplicating or skipping data.

## 1. Split work into units
Pick a unit that is independently processable and writable: a date partition, a tenant, a key range (`id BETWEEN 1e6 AND 2e6`), a source file. Aim for minutes per unit — small enough to retry cheaply, big enough to avoid overhead.

## 2. Control table
```sql
CREATE TABLE ops.job_units (
  job_name STRING, run_id STRING, unit_key STRING,           -- e.g. '2024-03-17'
  status STRING,                                             -- PENDING / RUNNING / DONE / FAILED
  attempts INT, rows_written BIGINT, started_at TIMESTAMP, finished_at TIMESTAMP, error STRING,
  PRIMARY KEY (job_name, run_id, unit_key));
```
- On first start, insert all units as PENDING for the run.
- Worker loop: claim next PENDING/FAILED unit (set RUNNING + started_at), process, write output, set DONE with row count.
- On restart with the same `run_id`, DONE units are skipped. RUNNING units older than a timeout are treated as failed (worker died).

## 3. Idempotent per-unit writes
The unit's write must be safe to repeat, because a crash can happen after writing but before marking DONE:
```sql
-- Delta (Databricks): REPLACE WHERE atomically overwrites the rows matching the predicate
INSERT INTO silver.events REPLACE WHERE event_date = '2024-03-17' SELECT ... ;
-- Generic: delete + insert in one transaction
BEGIN; DELETE FROM silver.events WHERE event_date = '2024-03-17'; INSERT INTO silver.events SELECT ...; COMMIT;
-- Keyed: MERGE on business key
```
Never `append` without dedup in a resumable job.

## 4. Within-unit checkpoints (only if units can't be small)
For streaming-through-a-big-file style work, persist a cursor (last processed key/offset) after each committed chunk. Spring Batch's chunk-oriented processing is the model: items are read one at a time, and once the number read equals the commit interval the whole chunk is written by the `ItemWriter` and the transaction is committed. In custom code store `last_key` in the control table in the same transaction as the chunk write when the target supports it.

## 5. Orchestrator features to reuse first
- Airflow: a backfill re-runs a Dag for every data interval in a date range, from the Dag Details page (Trigger, then Backfill: date range, reprocess behavior, max active runs, optional backwards order) or `airflow backfill create` with `--from-date`, `--to-date`, `--reprocess-behavior`, `--max-active-runs` and `--run-backwards`. The scheduler's own `catchup=True` creates a run for each missed interval and runs them sequentially.
- Airflow re-run of failures: clearing a failed task instance (UI Clear with the Failed, Upstream, Downstream options, or `airflow tasks clear`) re-runs it; task instance history and logs of each try are kept.
Use a hand-rolled control table only when units don't map onto orchestrator runs or tasks (e.g. tens of thousands of units).

## 6. Concurrency
Multiple workers claiming units need an atomic claim (`UPDATE ... SET status='RUNNING' WHERE unit_key = ? AND status IN ('PENDING','FAILED')` and check rows affected = 1). Cap parallelism to what source and target tolerate.

Note: on an empty source query REPLACE WHERE might delete data (per the Databricks page), so guard against an empty extract before writing.

## Verify
- [ ] Killing the job mid-run and restarting completes with identical output to an uninterrupted run (row counts and checksums per unit).
- [ ] DONE units are not reprocessed on restart.
- [ ] A unit that fails repeatedly stops after N attempts and is reported, while other units complete.

## Checked
Checked 2026-11-08: Spring Batch chunk-oriented processing page (commit interval and transactional chunk write; read in full, short). Airflow Dag Runs page (catchup, backfill UI and CLI flags, clearing tasks, task instance history; read in full). Databricks selective overwrite page (REPLACE WHERE is atomic, empty-source behaviour; first part read, option table and REPLACE WHERE section). The Spring Batch restartability page cited earlier only lists section titles, so no restart claims are made from it. Removed: Spring JobRepository cursor claim, Airflow dynamic task mapping, Databricks for-each and repair run, Spark availableNow (no read page supports them). The SQL control table and claim logic are original design advice, not documentation claims.
Method: documentation only; no commands were run.
