---
id: computing-software.database-administration.clickhouse.delete-update-mutations
name: delete-update-mutations
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, mutations, lightweight-delete, alter-delete, drop-partition]
level: practitioner
status: docs-checked
description: "Choose the right ClickHouse delete method: lightweight DELETE, ALTER DELETE mutation, TRUNCATE TABLE or DROP PARTITION."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/managing-data/deleting-data/overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# delete update mutations
Pick the method by data model and how much you delete (from the deleting-data overview):
- Lightweight delete, `DELETE FROM [table]`: for small amounts of data. Rows are immediately filtered out of later SELECTs but only marked deleted internally (a mutation adds a `_row_exists` column), and are removed from disk during natural merge cycles, after an unspecified period. Deleting large volumes this way can hurt SELECT performance, and it is not compatible with tables with projections. Prefer it over mutations when the data may remain on disk (non-compliance cases).
- Delete mutation, `ALTER TABLE [table] DELETE`: when data must leave disk immediately (e.g. compliance). It rewrites every part matching the WHERE expression, is extremely IO-heavy, is not atomic (a SELECT during a mutation sees both mutated and unmutated parts), and hurts SELECT performance, so use it sparingly. It runs synchronously by default if the table is non-replicated, otherwise as set by the `mutations_sync` setting. Track progress in `system.mutations`.
- `TRUNCATE TABLE [db.table]`: efficiently removes all data from a table; a lightweight operation.
- `DROP PARTITION`: efficiently removes a whole partition when you defined a custom partitioning key. Avoid high-cardinality partitioning.

```sql
-- delete all 2018 data with a lightweight delete (docs: not recommended)
DELETE FROM posts WHERE toYear(CreationDate) = 2018
-- same with a mutation (docs: not recommended)
ALTER TABLE posts DELETE WHERE toYear(CreationDate) = 2018
TRUNCATE TABLE posts
ALTER TABLE posts (DROP PARTITION '2008')
```
For deleting all data, avoid lightweight delete; use TRUNCATE or DROP PARTITION.

## Checked
2026-11-03. Confirmed against the "Delete overview" page: the four methods, their syntax and when to use each, mutation behaviour and `mutations_sync`, and the examples. Removed: update mutations and the ReplacingMergeTree/CollapsingMergeTree advice, `KILL MUTATION` and the `system.mutations` column list, the per-replica and block-merges gotchas, and the Verify step, none of which are on the page.
Method: documentation only; no commands were run.
