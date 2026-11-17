---
id: computing-software.database-administration.clickhouse.sparse-primary-index-granules
name: sparse-primary-index-granules
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, granules, sparse-index, mergetreeindex, index-granularity]
level: practitioner
status: docs-checked
description: "Understand the ClickHouse sparse primary index (one entry per 8,192-row granule) and inspect it with mergeTreeIndex and EXPLAIN indexes = 1."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/managing-data/core-concepts/primary-indexes.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sparse primary index granules
Each column's data is logically divided into granules of 8,192 rows by default, the smallest unit ClickHouse's processing works with. The primary index is sparse: it stores the primary key values of only the first row of every granule, one entry per granule, so it is small enough to fit entirely in memory. Each data part has its own primary index, used independently at query time.

Query flow from the docs: for `WHERE town = 'LONDON' AND street = 'OXFORD STREET'` on a table with primary key `(town, street)`, ClickHouse loads the primary index into memory, scans its entries to find granules that might contain matching rows, then loads and processes only those granules along with the corresponding granules of any other needed columns.

Inspect the index per part with the `mergeTreeIndex` table function:
```sql
SELECT part_name, max(mark_number) AS entries
FROM mergeTreeIndex('uk', 'uk_price_paid_simple')
GROUP BY part_name;
```
See how the index is used with `EXPLAIN`:
```sql
EXPLAIN indexes = 1
SELECT max(price)
FROM uk.uk_price_paid_simple
WHERE town = 'LONDON' AND street = 'OXFORD STREET';
```
In the docs output the `PrimaryKey` section reports `Granules: 3/3609`: only 3 of 3,609 granules were selected, and the query processed about 25,000 of roughly 30 million rows.

## Checked
2026-11-03. Confirmed against the "Primary indexes" page: granule size, one-entry-per-granule sparsity, in-memory size, per-part indexes, query flow, `mergeTreeIndex` and `EXPLAIN indexes = 1` examples. Removed: the `index_granularity` setting name, the "Consequences" list (point lookups read 8192 rows, key width and memory, smaller granularity tradeoff), and the entries-to-row-counts claim, none of which are on the page.
Method: documentation only; no commands were run.
