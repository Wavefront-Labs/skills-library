---
id: computing-software.database-administration.clickhouse.partitioning-keys-low-cardinality
name: partitioning-keys-low-cardinality
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, partition-by, partitioning, parts, drop-partition]
level: practitioner
status: docs-checked
description: "Use ClickHouse PARTITION BY as a data lifecycle tool with a low-cardinality key, not as a query speed-up, to avoid too many parts."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/partitioning_keys.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# partitioning keys low cardinality
Partitioning is defined with `PARTITION BY` at table creation. ClickHouse creates one new data part per unique partition value among the inserted rows, and only merges parts within a partition, never across. Example:
```sql
CREATE TABLE uk.uk_price_paid_simple_partitioned
(
  date Date, town LowCardinality(String), street LowCardinality(String), price UInt32
)
ENGINE = MergeTree
ORDER BY (town, street)
PARTITION BY toStartOfMonth(date)
```
The docs call partitioning primarily a data management technique, not a query optimisation tool. Whole partitions can be dropped, moved or archived in one metadata operation, far cheaper than row-level deletes, and it works with TTL and tiered storage (recent data on SSD, older partitions moved to object storage). It can improve queries if the partition key is not in the primary key and you filter by it (ClickHouse builds MinMax indexes on partition columns, so filtering by month on a `toStartOfMonth(date)` key skips other partitions). Queries across partitions can be slower than on an unpartitioned table because there are more parts.

Cardinality rule: a low-cardinality key with fewer than 100-1,000 distinct values is usually optimal. A high-cardinality key creates many unmerged parts and eventually the "Too many parts" error, because merges do not cross partitions and inserts are rejected when part counts exceed limits in total or per partition.

If you are unsure whether partitioning is needed, the docs suggest starting without it and optimising later from observed access patterns; align the key with data life cycle policies such as retention via TTL.

## Checked
2026-11-03. Confirmed against the "Choosing a partitioning key" page. Removed: the monthly/daily period advice, the "changing the key requires a new table" gotcha, and the system.parts Verify query, none of which are on the page.
Method: documentation only; no commands were run.
