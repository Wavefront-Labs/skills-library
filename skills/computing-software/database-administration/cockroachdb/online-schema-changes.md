---
id: computing-software.database-administration.cockroachdb.online-schema-changes
name: online-schema-changes
category: computing-software
field: database-administration
product: cockroachdb
tags: [online-schema-changes, schema-change-jobs, backfill, schema-locked, ddl-transactions]
level: practitioner
status: docs-checked
description: "Run CockroachDB schema changes without downtime: background jobs, bridging strategy, storage headroom up to 3x, schema_locked and the lack of transactional DDL."
sources:
  - https://www.cockroachlabs.com/docs/stable/online-schema-changes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change schemas on live tables safely.

How it works: a statement such as `ALTER TABLE`, `CREATE INDEX` or `TRUNCATE` starts a background job. The engine runs multiple schema versions concurrently, backfills or deletes data in steps, then all nodes switch to the new schema. No table locks are held. On acceptance you get a `NOTICE: waiting for job(s) to complete: <job id>`; track with `WITH x AS (SHOW JOBS) SELECT * FROM x WHERE job_type = 'SCHEMA CHANGE';`. If the statement is canceled, the job continues in the background.

Cautions:
- Schema changes consume resources; adding or dropping columns or adding indexes near peak capacity can cause latency spikes. Avoid running many at once.
- DDL is only fully atomic as individual implicit-transaction statements. Schema changes inside explicit multi-statement transactions lack full atomicity and rollback is limited; some tools work around this with a setting that automatically commits before schema changes.
- Jobs pause if the executing node is running out of disk space. This affects changes that trigger an index backfill, `ADD COLUMN` combined with `INDEX` or `UNIQUE`, and `SET LOCALITY` changes to or from `REGIONAL BY ROW` (the page lists more statements that this stripped copy does not show; read the page for the full list).
- Some operations (add or drop column, alter primary key) can temporarily need up to three times the storage of the affected data. Estimate with:
```sql
SHOW RANGES FROM TABLE {table name} WITH DETAILS, KEYS, INDEXES;
```
and read `range_size_mb`. This form may need `SET CLUSTER SETTING sql.show_ranges_deprecated_behavior.enabled TO 'false';`.

Changefeeds: set the `schema_locked` table storage parameter to `true` when no schema change is running to improve changefeed performance; CockroachDB unsets and reapplies it automatically around many schema changes. The `create_table_with_schema_locked` session variable applies it to new tables and is on by default from v26.1.

Verify: the schema change job completes in `SHOW JOBS` and the table definition shows the new schema.

## Checked
2026-11-03. Confirmed on the online schema changes page: background-job model, `NOTICE: waiting for job(s) to complete`, canceled statement leaves the job running, latency risk near peak capacity, atomicity limits in explicit transactions, disk-space pausing, up to three times storage with `range_size_mb` and `sql.show_ranges_deprecated_behavior.enabled`, `schema_locked` and its default from v26.1. Removed: the pause/resume claim, the Jobs page mention and the unconfirmed statement list.
Method: documentation only; no commands were run.
