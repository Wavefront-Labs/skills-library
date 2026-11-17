---
id: computing-software.database-administration.postgresql.partitionwise-join-and-aggregate
name: partitionwise-join-and-aggregate
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, partitionwise-join, enable-partitionwise-aggregate, enable-partitionwise-join, partitioning, query-planning]
level: practitioner
status: verified
description: "Enable and verify PostgreSQL partition-wise joins and aggregates for identically partitioned tables, and weigh their planning-time and memory cost."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-ENABLE-PARTITIONWISE-JOIN
  - https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-DECLARATIVE-BEST-PRACTICES
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partition-wise join and aggregate

Both are **off by default** because they raise planning time and memory with many partitions.

## Partition-wise join
Two tables partitioned **identically** (same partition key type, same bounds) joined on the partition key can be joined partition by partition: smaller hash tables, parallelisable, prunable.
```sql
SET enable_partitionwise_join = on;
EXPLAIN SELECT ... FROM orders o JOIN order_lines l ON l.order_month = o.order_month AND l.order_id = o.order_id;
-- Append
--   -> Hash Join (orders_2026_09, order_lines_2026_09)
--   -> Hash Join (orders_2026_10, order_lines_2026_10)
```
Without it you see one Hash Join above two Appends. PG13 release notes: partitionwise joins can also happen when the partition bounds do not match exactly (docs still require one-to-one matching sets of partitions; a table split into finer ranges on one side gave no partitionwise join).

## Partition-wise aggregate
```sql
SET enable_partitionwise_aggregate = on;
EXPLAIN SELECT tenant_id, count(*) FROM events GROUP BY tenant_id;
```
- GROUP BY includes the partition key: full aggregation per partition, results simply appended.
- Otherwise: partial aggregate per partition + Finalize Aggregate on top (still helps parallelism and memory).

## Rolling it out
1. Test the specific queries with `SET` in a session; compare `Planning Time` and `Execution Time` in `EXPLAIN ANALYZE`.
2. Enable per role or database where the reporting workload runs: `ALTER ROLE reporting SET enable_partitionwise_join = on;`
3. Leave it off for OLTP roles that hit one partition per query (no benefit, only planning cost).

## Gotchas
- With hundreds of partitions per side, planning can take more time and memory than execution saves.
- Each per-partition hash join can use `work_mem` (times `hash_mem_multiplier`); total memory per query grows with the number of partitions joined.
- Partition sets that do not match one-to-one (for example one side split into finer ranges) prevent the optimisation; in 17.6 default partitions on both sides, or on one side only, still joined partition by partition.

## Checked
PostgreSQL 17.6: both settings default off; with `enable_partitionwise_join = on` two identically partitioned tables joined on the key gave `Append` of per-partition `Hash Join`s, a join on `order_id` alone gave one Hash Join over two Appends, and a finer-split second table gave none; with `enable_partitionwise_aggregate = on`, `GROUP BY` the list partition key gave `Append` of `HashAggregate`s, and `GROUP BY` another column gave `Finalize GroupAggregate` over `Partial HashAggregate`s. Docs (runtime-config-query) and the PG13 release notes for the bounds claim.
