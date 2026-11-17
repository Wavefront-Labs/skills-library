---
id: computing-software.data-engineering.databricks.delta-change-data-feed
name: delta-change-data-feed
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-lake, change-data-feed, cdf, table-changes, readchangefeed, incremental-processing, silver-to-gold]
level: practitioner
status: docs-checked
description: "Enable and consume Delta change data feed: table_changes and readChangeFeed streams, change types, propagating updates and deletes downstream, and retention limits."
sources:
  - https://docs.databricks.com/aws/en/delta/delta-change-data-feed
  - https://docs.delta.io/latest/delta-change-data-feed.html
  - https://docs.databricks.com/aws/en/sql/language-manual/functions/table_changes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta change data feed (CDF)

**Goal:** downstream tables process only rows that changed in a Delta table — including updates and deletes — instead of rescanning it.

## 1. Enable
```sql
ALTER TABLE prod.silver.customers SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
-- new tables
CREATE TABLE prod.silver.orders (...) TBLPROPERTIES (delta.enableChangeDataFeed = true);
```
Changes are recorded only from the version where CDF was enabled; earlier history is not available as a feed.

## 2. Read in batch
```sql
SELECT * FROM table_changes('prod.silver.customers', 120, 130);          -- versions inclusive
SELECT * FROM table_changes('prod.silver.customers', '2026-10-15 00:00:00');
```
Extra columns:
| Column | Values |
|---|---|
| `_change_type` | `insert`, `update_preimage`, `update_postimage`, `delete` |
| `_commit_version` | Delta version |
| `_commit_timestamp` | commit time |

## 3. Read as a stream
```python
changes = (spark.readStream
    .option("readChangeFeed", "true")
    .option("startingVersion", 120)        # omit to start from the current snapshot
    .table("prod.silver.customers"))
```
Use `trigger(availableNow=True)` for incremental batch jobs; the checkpoint remembers the last processed version.

## 4. Apply changes downstream
A version range can contain several changes per key — keep the last one, drop pre-images:
Apply the batch with a MERGE keyed on the business key, keeping the last change per key by `_commit_version`, ignoring `update_preimage` rows and applying `delete` rows as deletes (select explicit columns rather than `*`, since the feed adds metadata columns).
In Lakeflow declarative pipelines, `AUTO CDC` / `APPLY CHANGES` does this ordering and delete handling for you.

## 5. Gotchas
- **Retention:** change files are removed by VACUUM like data files. A consumer offline longer than the retention window cannot resume — reading an expired version errors. Keep VACUUM retention > maximum consumer lag.
- Non-additive schema changes (rename/drop with column mapping) can block streaming CDF reads across the change; plan a restart from a new starting version.

## Verify
- [ ] `DESCRIBE HISTORY` shows CDF enabled before the version consumers start from.
- [ ] Downstream row count equals source after replaying a range with updates and deletes.
- [ ] VACUUM retention exceeds the slowest consumer's worst-case lag.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the Databricks change data feed page, the Delta Lake CDF page and the table_changes reference: delta.enableChangeDataFeed, table_changes by version or timestamp, _change_type values including update_preimage, _commit_version, readChangeFeed with startingVersion, availableNow with checkpoint, VACUUM retention limiting readable history, column-mapping schema-change limits, AUTO CDC / APPLY CHANGES in pipelines.

Removed: the session-default property, write-overhead and _change_data detail, OPTIMIZE and overwrite remarks, and the foreachBatch MERGE code sample (not on the pages read).

Method: documentation only; no commands were run.
