---
id: computing-software.data-engineering.data-warehouse-architecture.clickhouse-order-by-and-partition-keys
name: clickhouse-order-by-and-partition-keys
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, clickhouse-order-by, clickhouse, mergetree, primary-key]
level: advanced
status: docs-checked
description: "Design ClickHouse MergeTree tables: ORDER BY (primary key) for sparse index skipping, PARTITION BY for lifecycle, low-cardinality types, projections and skip indexes."
sources:
  - https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree
  - https://clickhouse.com/docs/best-practices/choosing-a-primary-key
  - https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ClickHouse ORDER BY and partition keys

**Goal:** queries read few granules because the sort key matches filters, and partitions serve data lifecycle, not query speed.

## Table design
```sql
CREATE TABLE events
(
  tenant_id   UInt32,
  event_type  LowCardinality(String),
  event_time  DateTime64(3, 'UTC'),
  user_id     UInt64,
  properties  String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (tenant_id, event_type, toDate(event_time), user_id)
TTL toDateTime(event_time) + INTERVAL 13 MONTH DELETE
SETTINGS index_granularity = 8192;
```

## ORDER BY = sparse primary index
- Data is sorted by the ORDER BY tuple; the primary index stores one entry per granule (8192 rows). Filters on a **prefix** of the key skip granules efficiently.
- Put columns most often filtered with equality first, lower cardinality before higher (`tenant_id`, `event_type`, then date, then `user_id`).
- `PRIMARY KEY` can be a prefix of `ORDER BY` to keep the index small.
- Treat ORDER BY as a design decision made at table creation; projections can add alternative sort orders after the fact.

## PARTITION BY = lifecycle
- Partition by time (for example monthly) so whole partitions can be dropped, moved or archived in a single metadata operation, and to support TTL.
- Too many partitions (high-cardinality keys like user_id) creates many small parts and slows inserts/merges. ClickHouse answers inserts with a "too many parts" error when part counts exceed its limits.

## Secondary access paths
- **Projections**: alternative sort orders/pre-aggregations stored with the table, chosen automatically.
- **Data skipping indexes** (`minmax`, `set`, `bloom_filter`) on non-key columns with clustered values.
- Materialized views into aggregate tables (`AggregatingMergeTree`).

## Insert hygiene
Send fewer, larger inserts or use asynchronous inserts (`async_insert`); many tiny inserts create too many parts ("too many parts" errors).

## Verify
`EXPLAIN indexes = 1 SELECT ...` shows granules selected vs total; `system.parts` shows a healthy part count per partition.

## Checked

2026-10-28. Confirmed in the ClickHouse MergeTree and best-practice pages: the primary index stores one entry per granule of 8192 rows, partitioning for lifecycle operations, "too many parts" error with too many partitions, projections for alternative ordering (with data duplication), skip index types `minmax`, `set`, `bloom_filter`, asynchronous inserts. Removed: the ORDER BY immutability claim, the DROP PARTITION example, the partition count range and the insert batch size range (not in the pages).

Method: documentation only; no commands were run.
