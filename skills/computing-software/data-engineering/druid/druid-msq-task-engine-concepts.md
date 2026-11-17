---
id: computing-software.data-engineering.druid.druid-msq-task-engine-concepts
name: druid-msq-task-engine-concepts
category: computing-software
field: data-engineering
product: druid
tags: [msq, multi-stage-query, sql-ingestion, extern, partitioned-by, clustered-by, rollup]
level: practitioner
status: docs-checked
description: "How Druid SQL-based ingestion (MSQ) works: INSERT vs REPLACE, PARTITIONED BY, CLUSTERED BY, rollup, task flow, memory and disk."
sources:
  - https://github.com/apache/druid/blob/master/docs/multi-stage-query/concepts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The MSQ task engine runs SQL statements as batch tasks in the indexing service, on Middle Managers. INSERT and REPLACE publish segments like other batch ingestion. Each query uses at least two task slots: one controller and at least one worker. SELECT also runs as a batch task, but its behaviour and result format are subject to change. Run statements from the console Query view or the `/druid/v2/sql/task` API.

## SQL extensions

- `EXTERN` reads external data with any native batch input source and input format. It reads many files in parallel across workers but does not split one file, so split a few very large files to raise parallelism. With `INTO` (`INSERT INTO EXTERN(...)`) it writes to an external destination; format via an `AS` clause.
- `INSERT` creates or appends; Druid has no `CREATE TABLE`. It takes a shared lock on the datasource, so several INSERTs can run together given free slots. Each publishes at the end, so use it for larger batches, not microbatches (use streaming ingestion).
- `REPLACE` creates or overwrites with an `OVERWRITE` clause (whole table or a time range aligned to the `PARTITIONED BY` granularity). It takes an exclusive write lock on the target time range; other time ranges stay open.
- Segments from `REPLACE` can use dimension-based pruning; those from `INSERT` cannot.
- Primary timestamp is always `__time`, often set with a function such as `TIME_FORMAT`. With `PARTITIONED BY ALL` (or `ALL TIME`) you need no `__time` column, but Druid still creates one with every value 1970-01-01 00:00:00.

## Partitioning and clustering

- `PARTITIONED BY` is required for INSERT and REPLACE and sets the time chunk. It matters for time pruning, lock granularity, and segment count (too fine makes many small segments). `HOUR` and `DAY` are most common; `ALL` suits data without a primary timestamp.
- `CLUSTERED BY` optionally splits within a time chunk. It improves compression and enables dimension-based pruning for filters like `x = 'foo'` or `x IN (...)`. Pruning needs both: segments written by `REPLACE`, and `CLUSTERED BY` starting with single-valued string columns. Otherwise data is still clustered but not pruned. Check `shard_spec` in `sys.segments` (or the console Partitioning column): `range` or `single` means pruning is possible. The page's example gives roughly 3 million rows per segment, the default `rowsPerSegment`.

## Rollup

1. Use `GROUP BY`: grouped columns become dimensions, aggregates become metrics.
2. Set context `finalizeAggregations: false` so intermediate aggregate state is written and can be aggregated further at query time.
3. See the ARRAY and multi-value dimension pages for those column types.

With these, rollup metadata is written to segments (readable via `segmentMetadata` queries). Supported ingest-time aggregates: `COUNT` (use `SUM` at query time), `SUM`, `MIN`, `MAX`, `EARLIEST`, `EARLIEST_BY`, `LATEST`, `LATEST_BY`, `APPROX_COUNT_DISTINCT`, `APPROX_COUNT_DISTINCT_BUILTIN`, `APPROX_COUNT_DISTINCT_DS_HLL`, `APPROX_COUNT_DISTINCT_DS_THETA`, `DS_QUANTILES_SKETCH` (use `APPROX_QUANTILE_DS` at query time). Do not use `AVG`; ingest `SUM` and `COUNT` and divide at query time.

## Execution flow

1. The Broker plans the SQL into a native query and wraps it in a `query_controller` task submitted to the indexing service, then returns the task id and exits.
2. The controller launches workers (`query_worker`) based on the `maxNumTasks` and `taskAssignment` context parameters, settable per query.
3. SELECT: workers send results to the controller, which writes them to its task report. INSERT/REPLACE: workers generate and publish segments.

## Parallelism, memory, disk

- `maxNumTasks` counts the controller too; minimum 2. Do not exceed free slots or the query fails with `TaskStartTimeout`. `druid.worker.capacity` on each Middle Manager caps workers per server; workers are single-threaded.
- Heap on Peons: 75% of JVM heap (less lookups) split equally into a processor bundle and a worker bundle (37.5% each). Sketches for partition boundaries are capped at 10% of memory or 300 MB, whichever is lower. Each downstream stage needs 1 MB of buffer per upstream worker (100 upstream workers need 100 MB). The worker bundle sorts stage output and spills to disk when needed.
- Direct memory: set `-XX:MaxDirectMemorySize` to at least `(druid.processing.numThreads + 1) * druid.processing.buffer.sizeBytes`; more does not speed things up.
- Disk (under `druid.indexer.task.baseDir`): one input file at a time, one segment's worth of generation data (generally under 2 GB per task), plus space for a compressed copy of the task's whole output for the external sort and again for shuffle storage.

## Checked

2026-11-08. Read the cited concepts page in full. Expanded the draft with INSERT/REPLACE locking, pruning requirements, rollup steps, execution flow, and the memory and disk sizing rules.

Method: documentation only; no commands were run.
