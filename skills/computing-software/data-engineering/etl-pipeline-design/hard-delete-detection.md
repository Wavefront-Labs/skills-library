---
id: computing-software.data-engineering.etl-pipeline-design.hard-delete-detection
name: hard-delete-detection
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, incremental-load, hard-delete-detection, soft-deletes, key-snapshot-diff, cdc, tombstones, anti-join, dbt-snapshots]
level: practitioner
status: docs-checked
description: "Detect rows physically deleted in a source when loading incrementally: CDC delete events, key-snapshot anti-joins, partition-scoped comparison, soft-delete handling."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-delete-events
  - https://docs.getdbt.com/docs/build/snapshots#hard-deletes
  - https://fivetran.com/docs/core-concepts/system-columns-and-tables
  - https://docs.databricks.com/aws/en/sql/language-manual/delta-merge-into
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hard delete detection

**Goal:** when a row disappears from the source, the warehouse knows — instead of keeping a ghost record forever because a high-water-mark extract never sees deletes.

## 1. Why incremental loads miss deletes
`WHERE updated_at > :last_watermark` returns changed rows; a deleted row has no `updated_at` any more. Unless something reports the deletion, the target keeps it.

## 2. Options, best first
| Method | How | Cost |
|---|---|---|
| Source soft deletes | app sets `deleted_at`; captured by the normal incremental extract | free, needs app cooperation |
| CDC | log-based CDC emits delete events (Debezium `op` = `d`, followed by a tombstone event by default) | best fidelity, needs CDC infrastructure |
| Audit/trigger table | DB trigger writes deleted keys to a table you extract | moderate; touches source |
| Key snapshot diff | periodically extract **all primary keys**, anti-join against target | simple, works with any source |
| Full reload + compare | reload whole table, diff | only for small tables |

## 3. Key snapshot diff
Extract keys only (narrow, cheap even for large tables), then mark missing ones:
```sql
-- staged_keys: full list of current source PKs extracted this run
MERGE INTO silver.customers t
USING (SELECT c.customer_id FROM silver.customers c
       LEFT ANTI JOIN staged_keys k ON c.customer_id = k.customer_id
       WHERE c.is_deleted = FALSE) d
ON t.customer_id = d.customer_id
WHEN MATCHED THEN UPDATE SET is_deleted = TRUE, deleted_detected_at = current_timestamp();
```
(`LEFT ANTI JOIN` is Spark/Databricks syntax; elsewhere use `NOT EXISTS`.)
- **Guard against partial key extracts**: if the key extract failed halfway, everything looks deleted. Check `count(staged_keys)` ≥ e.g. 95% of the active target count before applying; abort otherwise.
- Scope for huge tables: compare only partitions where deletes can happen (e.g. last 90 days of orders) or hash buckets (`mod(id, 16) = run_number % 16`) on a rotation.
- Rows reappearing (undelete) → set `is_deleted = FALSE` in the normal upsert path.

## 4. Represent deletes downstream
- Prefer **soft delete in silver** (`is_deleted`, `deleted_detected_at`) for audit; filter in marts.
- SCD2 tables: close the current version (`valid_to = detected_at`). dbt snapshots have a `hard_deletes` config with the options `ignore`, `invalidate` and `new_record`; `invalidate` closes the version and `new_record` adds a deletion row.
- Debezium: a delete event can be followed by a tombstone event (null value, same key) so Kafka log compaction can drop the key; `tombstones.on.delete` controls this (default `true`). Sinks must handle both.
- Physical deletion is required for privacy erasure requests — propagate those explicitly through every layer.
- Managed EL tools: Fivetran uses a boolean `_fivetran_deleted` column to mark rows deleted in the source (the column is dropped when history mode is activated for a table). For other tools, read the connector docs on delete handling.
- Delta Lake MERGE on Databricks has a `WHEN NOT MATCHED BY SOURCE` clause that can update or delete target rows with no match in the source, so a full-key or full-partition source can drive the delete flag directly. Add a `not_matched_by_source_condition` to limit the rows touched; Databricks warns an unrestricted clause can modify a large number of target rows.

## 5. Timing
`deleted_detected_at` is when you noticed, not when it was deleted. Document the detection lag (snapshot frequency) for consumers.

## Verify
- [ ] Deleting a test row in the source flags it in silver after the next detection run.
- [ ] A truncated/failed key extract aborts instead of mass-flagging deletes.
- [ ] Marts exclude soft-deleted rows; counts match the source.

## Checked
Date: 2026-11-09. Confirmed from the Debezium PostgreSQL connector page (op value d, tombstone events, tombstones.on.delete default true), the dbt snapshots page (hard_deletes options ignore, invalidate, new_record), the Fivetran system columns page (_fivetran_deleted boolean, dropped under history mode) and the Databricks MERGE INTO page (WHEN NOT MATCHED BY SOURCE and its warning). The SQL, the 95% guard, the hash-bucket rotation and the table of methods are illustrative design guidance, not vendor claims. Removed: the Airbyte statement about incremental modes. Not read: Debezium MySQL pages.
Method: documentation only; no commands were run.
