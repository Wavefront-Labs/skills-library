---
id: computing-software.database-administration.clickhouse.mergetree-order-by-primary-key
name: mergetree-order-by-primary-key
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, order-by, primary-key, sorting-key, explain-indexes]
level: practitioner
status: docs-checked
description: "Choose a ClickHouse MergeTree ORDER BY key from the columns most used in WHERE filters and confirm pruning with EXPLAIN indexes = 1."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/choosing_a_primary_key.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mergetree order by primary key
The page uses "ordering key" and "primary key" interchangeably (strictly they differ in ClickHouse; a ClickHouse primary key works very differently from OLTP databases such as Postgres). Each part has its own sparse primary index, and the key sets the physical order of data on disk, so it also affects compression. All columns are sorted by the ordering key, whether or not they are in it. Multiple key columns order with the same semantics as a SELECT's ORDER BY.

Selection guidance: prioritise columns frequently used in WHERE filters, especially those that exclude many rows, and columns highly correlated with other data (contiguous storage helps compression and memory use in GROUP BY and ORDER BY). The page says you can identify several candidate keys, with 4-5 typically sufficient. Ordering keys must be defined at table creation and can't be added later; extra orderings come only from projections, which duplicate data.

Docs example: `posts_unordered` has `ORDER BY tuple()` (no primary key), so counting questions created since 2024 scans the whole dataset (59.82 million rows, 361.34 MB). With the same data in `posts_ordered`:
```sql
ENGINE = MergeTree
ORDER BY (PostTypeId, toDate(CreationDate))
```
`PostTypeId` (cardinality 8) is the logical first column. Day granularity is enough for the date filters and still helps datetime filters, and a date fits in 16 bits so the index is smaller. The same query then processed 196.53 thousand rows (1.77 MB), about 4x faster. Confirm index use with:
```sql
EXPLAIN indexes = 1
SELECT count()
FROM stackoverflow.posts_ordered
WHERE (CreationDate >= '2024-01-01') AND (PostTypeId = 'Question')
```
The `PrimaryKey` section lists the keys, the condition, `Parts: 14/14` and `Granules: 39/7578`. Without a primary key, `EXPLAIN indexes = 1` shows no `Indexes` section, confirming a full scan.

## Checked
2026-11-03. Confirmed against the "Choosing a primary key" page. Removed: the invented three-column CREATE TABLE, the "equality first / lower cardinality earlier" rules, the later-column-filter gotcha, and the "confirm newer ALTER support" note, none of which are on the page.
Method: documentation only; no commands were run.
