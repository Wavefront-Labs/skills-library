---
id: computing-software.database-administration.clickhouse.drop-partition-and-truncate
name: drop-partition-and-truncate
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, drop-partition, truncate, partition-expression, data-management]
level: practitioner
status: docs-checked
description: "Remove old ClickHouse data cheaply with ALTER TABLE DROP PARTITION, and list partitions from system.parts first."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/managing-data/drop_partition.mdx
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/managing-data/deleting-data/overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# drop partition and truncate
Partitioning is declared with `PARTITION BY` and is principally a data-management feature, not a query optimisation: each partition can be operated on independently, e.g. deleted, or moved between storage tiers. The docs example partitions a table by year with `PARTITION BY toYear(CreationDate)`.
```sql
ALTER TABLE table_name [ON CLUSTER cluster] DROP PARTITION|PART partition_expr
```
This tags the partition as inactive and deletes the data completely, approximately in 10 minutes. The query is replicated: it deletes data on all replicas. List the partitions first, then drop one:
```sql
SELECT DISTINCT partition FROM system.parts WHERE `table` = 'posts'

ALTER TABLE posts
(DROP PARTITION '2008')
```
Avoid high-cardinality partitioning. To remove all data from a table use `TRUNCATE TABLE posts`, which the delete overview calls a lightweight operation.

## Checked
2026-11-03. Confirmed against the "Dropping partitions" page (partition background, DROP PARTITION|PART syntax, 10-minute deletion, replication, system.parts listing, the '2008' example) and, for TRUNCATE and high cardinality, the "Delete overview" page. Removed: the `DROP PART '2008_1_1_0'` example, "keeps the table / cannot be reversed" for TRUNCATE, the sum(rows) query, and the backup and retention-design advice, none of which are on those pages.
Method: documentation only; no commands were run.
