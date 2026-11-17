---
id: computing-software.database-administration.postgresql.choosing-partition-key-and-count
name: choosing-partition-key-and-count
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, partition-count, partition-key, partitioning-strategy, partition-pruning, range-partitioning, hash-partitioning]
level: practitioner
status: verified
description: "Choose a PostgreSQL partition key, strategy and partition count/size: align with retention and query filters, keep pruning effective, avoid too many partitions."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-DECLARATIVE-BEST-PRACTICES
  - https://www.postgresql.org/docs/current/ddl-partition-pruning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing the partition key and partition count

Partitioning is a maintenance tool first (drop old data instantly, vacuum smaller pieces) and a query tool second. Decide with both in mind.

## The key
- Pick the column that is in the WHERE clause of the hot and the heavy queries; queries without it scan every partition.
- Pick the column that drives data removal (`created_at` for retention) so retention is `DETACH`/`DROP` instead of `DELETE`.
- Unique constraints and primary keys must include the partition key: `PRIMARY KEY (id, created_at)`. If the application needs global uniqueness on `id` alone, partitioning by time makes that unenforceable.

## Strategy
| Strategy | Use |
|---|---|
| RANGE (time) | retention, time-bounded queries, append-mostly |
| LIST (tenant/region) | few large tenants or regions, per-tenant moves |
| HASH (id, n partitions) | spread write/vacuum load when no natural range; equality prunes to one partition but a range on the key (`id BETWEEN 1 AND 5`) scans all, no easy retention |
| Sub-partitioning | e.g. range by month then hash by tenant; multiplies partition count fast |

## How many / how big
- Docs (ddl-partitioning, best practices): the planner handles hierarchies of up to a few thousand partitions fairly well if typical queries prune to a small number; planning time and memory grow with the partitions that remain after pruning, and each session loads metadata for every partition it touches. Too few partitions leave indexes large and cache hit ratios low. Think about future growth: one LIST partition per customer is fragile if customers multiply, and HASH with a fixed count is safer.
- Size partitions so the indexes of the hot (recent) ones fit in memory; the docs give no byte figure, so measure.
- Each partition is several files (heap, indexes, TOAST, FSM, VM) and queries touching many partitions take a lock on each, so very large counts also stress `max_locks_per_transaction` and `pg_dump`.
- Retention granularity sets the floor: daily retention needs daily partitions, monthly retention allows monthly.

## Validate pruning
```sql
EXPLAIN (ANALYZE) SELECT * FROM events WHERE created_at >= now() - interval '1 day';
-- look for "Subplans Removed: N" (execution-time pruning) or only the expected partitions listed
```
Pruning needs the predicate on the key in a sargable form; `date_trunc('day', created_at) = ...` or casting the key defeats it.

## Gotchas
- Adding partitions ahead of time: automate (pg_partman or a cron job); inserts without a matching partition fail unless a DEFAULT partition exists, and a large DEFAULT partition makes later ATTACH slow.
- Changing the key later means rebuilding the table; prototype with production-like queries first.

## Checked
PostgreSQL 17.6, 20 daily partitions: `PRIMARY KEY (id)` on a table partitioned by `created_at` fails (`unique constraint on partitioned table must include all partitioning columns`); `created_at >= now() - interval '1 day'` shows `Subplans Removed: 17` (execution-time pruning); a literal bound lists only the matching partitions; `date_trunc('day', created_at) = ...` lists every partition (no pruning); HASH partitioning prunes `id = 5` to one partition but not `id BETWEEN 1 AND 5`. The partition-count guidance is quoted from the PG docs best-practices section (ddl-partitioning), checked this session; default-partition behaviour is verified in default-partitions-and-partitioned-indexes.
