---
id: computing-software.data-engineering.databricks.delta-table-properties-and-log-retention
name: delta-table-properties-and-log-retention
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-table-properties, delta-lake, log-retention, tblproperties]
level: advanced
status: docs-checked
description: "Set Delta table properties deliberately: log and deleted-file retention vs time travel, CDF, auto optimize, deletion vectors, data skipping columns and session defaults."
sources:
  - https://docs.databricks.com/aws/en/delta/table-properties
  - https://docs.databricks.com/aws/en/delta/history#configure-data-retention-for-time-travel-queries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta table properties and log retention

**Goal:** tables that keep the history you need, skip data efficiently and stay compact, configured once and consistently.

## Inspect and set
```sql
SHOW TBLPROPERTIES main.sales.orders;
ALTER TABLE main.sales.orders SET TBLPROPERTIES (
  'delta.logRetentionDuration' = 'interval 30 days',
  'delta.deletedFileRetentionDuration' = 'interval 7 days',
  'delta.enableChangeDataFeed' = 'true',
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'auto',
  'delta.enableDeletionVectors' = 'true',
  'delta.dataSkippingStatsColumns' = 'order_date,customer_id,status'
);
ALTER TABLE main.sales.orders UNSET TBLPROPERTIES ('delta.appendOnly');
```

## Retention and time travel
- `delta.logRetentionDuration` (default 30 days): how long commit history is kept (checkpoint cleanup).
- `delta.deletedFileRetentionDuration` (default 7 days): how old unreferenced files must be before VACUUM removes them.
- Time travel to version N needs **both** the log entry and the data files: effective window = min of the two. For 30-day time travel set both to 30 days and accept storage cost.

## Other useful properties
| Property | Use |
|---|---|
| `delta.appendOnly = true` | forbid updates/deletes (audit logs) |
| `delta.enableChangeDataFeed` | row-level changes for downstream incremental |
| `delta.dataSkippingNumIndexedCols` (default 32) or `delta.dataSkippingStatsColumns` | which columns get min/max stats; put filter columns first or list them |
| `delta.targetFileSize` | override file sizing for OPTIMIZE/writes |
| `delta.columnMapping.mode = 'name'` | renames/drops of columns |
| `delta.checkpointPolicy = 'v2'` | V2 checkpoints (`classic` is the other value) |

## Defaults for new tables
```python
spark.conf.set("spark.databricks.delta.properties.defaults.enableChangeDataFeed", "true")
```
Enforce the same properties through table creation templates.

## Gotchas
- Enabling deletion vectors updates the table protocol: older readers may lose access.
- Predictive optimization on UC managed tables handles OPTIMIZE/VACUUM; do not schedule duplicate jobs.

## Verify
`DESCRIBE DETAIL` shows properties; `DESCRIBE HISTORY` goes back the expected number of days after a VACUUM.

## Checked
2026-10-28. Confirmed against the Delta table properties page and the table history page (logRetentionDuration default 30 days, deletedFileRetentionDuration default 7 days, dataSkippingNumIndexedCols default 32, dataSkippingStatsColumns, targetFileSize, checkpointPolicy classic or v2, columnMapping.mode, appendOnly, autoOptimize.autoCompact auto, optimizeWrite, enableDeletionVectors, session defaults prefix spark.databricks.delta.properties.defaults). Removed: dbt tblproperties and schema or catalog default remarks, large-table checkpoint claim, column-mapping protocol claim.
Method: documentation only; no commands were run.
