---
id: computing-software.data-engineering.databricks.query-profile-and-query-history
name: query-profile-and-query-history
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-query-profile, query-history, system-query-history, sql-warehouse, query-tuning, spill, file-pruning, photon]
level: practitioner
status: docs-checked
description: "Find slow and heavy Databricks SQL queries in system.query.history and the Query History UI, then read the query profile operators for time, rows, memory and shuffles."
sources:
  - https://docs.databricks.com/aws/en/sql/user/queries/query-profile
  - https://docs.databricks.com/aws/en/sql/user/queries/query-history
  - https://docs.databricks.com/aws/en/admin/system-tables/query-history
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query profile and query history

**Goal:** find the queries worth fixing, then read their profile to know why they're slow.

## 1. Find candidates in `system.query.history`
```sql
SELECT statement_id, executed_by, total_duration_ms/1000 AS secs,
       read_bytes, read_files, pruned_files, spilled_local_bytes,
       waiting_at_capacity_duration_ms, left(statement_text, 120) AS sql
FROM system.query.history
WHERE start_time >= current_date() - 7 AND execution_status = 'FINISHED'
ORDER BY total_duration_ms DESC LIMIT 50;
```
- All of these columns are in the documented table schema. `read_files` is the number of files read after pruning and `pruned_files` the number pruned.
- A large `waiting_at_capacity_duration_ms` means time spent queued before execution: analyse it separately from execution time.
- The `query_source` struct carries the origin of a statement (such as a job or dashboard), which lets you group queries by source.
- UI: the Query History page lists queries; open one and click **See query profile** to open the detailed DAG.

## 2. Read the profile
The detailed profile has summary metrics on the left and a graph view of operators on the right. Click a metric (Time spent, Memory peak, Rows) to change what the graph reports per operator. Some non-Photon operations run as a group and share the parent operator's metric values. A Shuffle operator means data was redistributed or repartitioned, which is expensive because it moves data between executors.

## 3. Keep a feedback loop
A recurring top-N report from `system.query.history` by total duration and by bytes read, with an owner per item.

## Verify
- [ ] Before/after profile for each fix shows reduced time, rows or memory on the slow operator.
- [ ] Queueing time is separated from execution time in the analysis.

## Checked
2026-11-01. Confirmed against the Databricks pages Query profile, Query history and the system.query.history reference (column names, See query profile, operator metrics, shuffle, non-Photon grouping). Removed: the compute.warehouse_id column, the signal and fix table (spill, skew, pruning, Photon fallback, Cloud Fetch) and the tuning commands (DESCRIBE DETAIL, ANALYZE TABLE).
Method: documentation only; no commands were run.
