---
id: computing-software.database-administration.clickhouse.memory-debugging-queries-and-tables
name: memory-debugging-queries-and-tables
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, memory, systemprocesses, peak-memory-usage, asynchronous-metrics]
level: practitioner
status: docs-checked
description: "Find where ClickHouse memory goes: running queries, merges, dictionaries, Memory/Set/Join tables, caches and primary keys."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/developer/debugging-memory-issues.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# memory debugging queries and tables
The "Debugging memory issues" guide lists queries that show which queries, databases and tables use memory.
```sql
-- running queries by peak memory
SELECT initial_query_id, query, elapsed,
       formatReadableSize(memory_usage), formatReadableSize(peak_memory_usage)
FROM system.processes ORDER BY peak_memory_usage DESC LIMIT 100;

-- cache and memory metrics
SELECT metric, description, formatReadableSize(value) size
FROM system.asynchronous_metrics
WHERE metric LIKE '%Cach%' OR metric LIKE '%Mem%' ORDER BY value DESC;

-- tables by current memory usage
SELECT database, name, formatReadableSize(total_bytes)
FROM system.tables WHERE engine IN ('Memory','Set','Join');

-- totals
SELECT formatReadableSize(sum(memory_usage)) FROM system.merges;
SELECT formatReadableSize(sum(memory_usage)) FROM system.processes;
SELECT formatReadableSize(sum(bytes_allocated)) FROM system.dictionaries;
```
Primary keys and index granularity (from `system.parts`):
```sql
SELECT
    sumIf(data_uncompressed_bytes, part_type = 'InMemory') AS memory_parts,
    formatReadableSize(sum(primary_key_bytes_in_memory)) AS primary_key_bytes_in_memory,
    formatReadableSize(sum(primary_key_bytes_in_memory_allocated)) AS primary_key_bytes_in_memory_allocated,
    formatReadableSize(sum(index_granularity_bytes_in_memory)) AS index_granularity_bytes_in_memory,
    formatReadableSize(sum(index_granularity_bytes_in_memory_allocated)) AS index_granularity_bytes_in_memory_allocated
FROM system.parts;
```

## Checked
2026-11-03. Confirmed all queries above against the "Debugging memory issues" page. Removed: the claim that Memory/Set/Join tables and dictionaries stay in RAM permanently, the server-memory-limit comparison, and the `MemoryTracking` Verify step, none of which are on the page.
Method: documentation only; no commands were run.
