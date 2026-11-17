---
id: computing-software.database-administration.clickhouse.query-performance-find-slow-queries
name: query-performance-find-slow-queries
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, query-log, normalized-query-hash, slow-queries, clusterallreplicas]
level: practitioner
status: docs-checked
description: "Find slow and memory-heavy ClickHouse queries in system.query_log across replicas and group by normalized_query_hash."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/best-practices/query-optimization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# query performance find slow queries
ClickHouse logs every query to `system.query_log`. Query it on all replicas with `clusterAllReplicas`:
```sql
SELECT type, event_time, query_duration_ms, query, read_rows, tables
FROM clusterAllReplicas(default, system.query_log)
WHERE has(databases, 'mydb')
  AND event_time >= now() - toIntervalMinute(60)
  AND type = 'QueryFinish'
ORDER BY query_duration_ms DESC
LIMIT 5 FORMAT VERTICAL;
```
Rank by memory with `formatReadableSize(memory_usage)` and read CPU from `ProfileEvents['UserTimeMicroseconds']`; cache behaviour from `CachedReadBufferReadFromCacheMicroseconds` vs `...FromSourceMicroseconds`. Exclude internal users with `user NOT ILIKE '%internal%'`.

Method from the guide: narrow by `user`, `tables` or `databases`, then `GROUP BY normalized_query_hash` to find query shapes that are expensive in aggregate, since one-off slow runs are often outliers from ad-hoc work or system stress.

Gotcha: `type = 'QueryFinish'` excludes queries that did not finish, so drop that filter when hunting failures.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "Query optimization": `system.query_log`, `clusterAllReplicas`, `has(databases, ...)`, the `ProfileEvents` reads (`UserTimeMicroseconds`, `CachedReadBufferReadFromSourceMicroseconds`), the `user NOT ILIKE '%internal%'` filter, grouping by `normalized_query_hash` and the outlier warning. Removed: the query_log TTL claim, the exception type names and the Verify step.
Method: documentation only; no commands were run.
