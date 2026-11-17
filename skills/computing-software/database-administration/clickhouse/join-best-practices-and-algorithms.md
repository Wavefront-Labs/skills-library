---
id: computing-software.database-administration.clickhouse.join-best-practices-and-algorithms
name: join-best-practices-and-algorithms
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, join, join-algorithm, parallel-hash, any-join]
level: practitioner
status: docs-checked
description: "Make ClickHouse JOINs cheaper: denormalize, use ANY joins, filter early, pick a join_algorithm and avoid Cartesian products and disk spills."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/minimize_optimize_joins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# join best practices and algorithms
JOINs are inherently more expensive than querying a denormalized table; denormalization moves work to insert or pre-processing time. The page recommends it for latency-sensitive queries when tables change infrequently, relationships are not many-to-many or very high cardinality, and only a subset of columns is queried. Denormalize only frequently queried attributes, and consider materialized views to compute aggregates incrementally.

When JOINs are required use at least version 24.12: the planner then automatically puts the smaller table on the right side.
- Avoid Cartesian products: if you need only any single match, use `ANY` joins (e.g. `LEFT ANY JOIN`); they are faster and use less memory.
- Reduce table sizes with filters in `WHERE` or `JOIN ON`. ClickHouse pushes filters down; if that does not happen, rewrite one side as a sub-query.
- Use direct joins: if the right side is a dictionary or a key-value engine (EmbeddedRocksDB, Join table engine), the `direct` algorithm skips the hash-table build. Works for INNER and LEFT OUTER joins.
- Use sort-merge algorithms `full_sorting_merge` and `partial_merge` to exploit table sorting; when joining on primary key columns the sort step is omitted.
- Avoid disk-spilling joins: by default an oversized hash table gives an out-of-memory error. `grace_hash`, `partial_merge` and `full_sorting_merge` can spill to disk but disk access can slow joins considerably; the page prefers shrinking intermediate states.
- In outer joins, `join_use_nulls = 0` uses the column type's default value as the no-match marker instead of Nullable, avoiding overhead.

Algorithms: parallel hash (default; small-to-medium right tables that fit memory), direct, full sorting merge (both tables sorted on the join key), partial merge (minimal memory, slower), grace hash (memory-tunable). Set `join_algorithm`; `'auto'` lets ClickHouse choose, and the default value is `direct,parallel_hash,hash`. The page also advises keeping joins to a minimum, avoiding more than 3-4 per query, and benchmarking algorithms on real data.

Dictionaries silently deduplicate keys (the last loaded value is kept), so use them for one-to-one or many-to-one lookups, not one-to-many or many-to-many.

## Checked
2026-11-03. Confirmed against the "Minimize and optimize JOINs" page. Removed: the invented `a.id`/`b.id` example query and the `system.query_log` Verify step, which are not on the page.
Method: documentation only; no commands were run.
