---
id: computing-software.data-engineering.apache-flink.materialized-tables
name: materialized-tables
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-sql, flink-materialized-table, freshness, sql-gateway, paimon, lakehouse]
level: advanced
status: docs-checked
description: "Define Flink materialized tables with a query and FRESHNESS so Flink schedules continuous or full-refresh pipelines, and manage suspend, resume and refresh."
sources:
  - https://cwiki.apache.org/confluence/display/FLINK/FLIP-435%3A+Introduce+a+New+Materialized+Table+for+Simplifying+Data+Pipelines
  - https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/table/materialized-table/statements/
  - https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/table/materialized-table/deployment/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Materialized tables

FLIP-435 lets you declare a table by its query plus a data freshness target. Flink derives the refresh mode and runs the pipeline for you, unifying streaming and batch.

```sql
CREATE MATERIALIZED TABLE dwd_orders
PARTITIONED BY (ds)
WITH ('format' = 'debezium-json', 'partition.fields.ds.date-formatter' = 'yyyy-MM-dd')
FRESHNESS = INTERVAL '3' MINUTE
REFRESH_MODE = CONTINUOUS              -- optional; otherwise derived from FRESHNESS
AS SELECT o.ds, o.id, o.order_number, o.user_id, p.pay_amt
   FROM orders o LEFT JOIN payments p ON o.id = p.order_id AND o.ds = p.ds;
```
- **CONTINUOUS** refresh: a streaming job keeps the table up to date; checkpoint interval derived from freshness. Chosen automatically when freshness is below `materialized-table.refresh-mode.freshness-threshold`; `REFRESH_MODE` overrides the inference.
- **FULL** refresh: a scheduled batch job recomputes (by partition when partitioned) at the freshness interval; the SQL Gateway acts as the embedded workflow scheduler (`workflow-scheduler: type: embedded` in `config.yaml`; only `embedded` is supported). FULL freshness is translated to a cron expression, so only some values are allowed (for example minutes: 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30; hours: 1, 2, 3, 4, 6, 8, 12; days: 1).

## Operations
```sql
ALTER MATERIALIZED TABLE dwd_orders SUSPEND;          -- stops the job (continuous: savepoint) or schedule
ALTER MATERIALIZED TABLE dwd_orders RESUME;
ALTER MATERIALIZED TABLE dwd_orders RESUME WITH ('sink.parallelism' = '10');
ALTER MATERIALIZED TABLE dwd_orders REFRESH PARTITION (ds = '2026-10-17');   -- backfill one partition
ALTER MATERIALIZED TABLE dwd_orders AS SELECT ...;                           -- change the query definition
DROP MATERIALIZED TABLE dwd_orders;
```

## Requirements and limits
- Must be created through the **SQL Gateway**, with a catalog store configured, and a catalog that supports materialized tables (the 2.1 docs say only Paimon Catalog currently does).
- Set `execution.checkpointing.savepoint-dir` before suspending a CONTINUOUS table (it is paused with STOP WITH SAVEPOINT).
- `ALTER ... AS <query>` only supports adding nullable columns to the end of the schema; in continuous mode the new job does not restore state, which may cause temporary duplication or loss.
- Limitations: no explicitly specified columns; no temporary tables, views or functions in the query. The partition column must appear in the query.
- Not a replacement for carefully tuned long-running streaming jobs with custom state; best for warehouse-style layered tables (ODS to DWD to DWS) on lake storage.

## Verify
- [ ] `DESCRIBE` / catalog shows the table with refresh status; the underlying job (continuous) or schedule (full) is visible in the Flink UI / scheduler.
- [ ] Data lag (max event time vs now) stays within the declared freshness (documented as best effort, not guaranteed).

## Checked
2026-11-09. Confirmed against the Flink 2.1 Materialized Table statements and deployment pages (syntax, FRESHNESS units, refresh modes, SUSPEND/RESUME/REFRESH/AS, savepoint dir, embedded scheduler, Paimon catalog note, limitations). Removed: the 1.20 version gate, the default threshold value, `SET FRESHNESS` (not in the 2.1 syntax) and the unconfirmed in-memory-catalog statement.
Method: documentation only; no commands were run.
