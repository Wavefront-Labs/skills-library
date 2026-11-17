---
id: computing-software.database-administration.duckdb.duckdb-schema-and-indexing-performance
name: duckdb-schema-and-indexing-performance
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, performance, schema, types, primary-key, art-index, zonemaps]
level: advanced
status: docs-checked
description: "Schema and index rules for DuckDB speed: strict column types, avoiding constraints on bulk load, zonemap ordering, ART index scan eligibility and memory costs."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/guides/performance/schema.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/guides/performance/indexing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: design tables so scans, joins and loads are fast.

Types: use the most restrictive type; never store numbers or dates as strings. Docs benchmarks: 554M timestamps as `DATETIME` took 3.3 GB and 0.9 s versus `VARCHAR` 5.2 GB and 3.9 s; joining on `BIGINT` ids (1.2 s) beat `VARCHAR` ids (2.1 s), about 1.8x. In memory-constrained environments, smaller types (TINYINT) cut memory and disk needed for a query; bitpacking means small values in big types do not enlarge disk but do enlarge memory.

Constraints (`UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`) build indexes and checks, slow loading, and rarely speed queries since joins and aggregations do not use them. Define them only for integrity. Load of 554M rows: with primary key 461.6 s, without 121.0 s, load then add key 242.0 s. For bulk loads, add keys afterward.

Zonemaps (min-max per row group) exist automatically for general-purpose types and power predicate pushdown and some aggregates. Row groups whose range excludes the filter are skipped, so ordered data is far more skippable. Pre-sort on the columns you filter by when inserting (even imperfect order helps). Ordered timestamp column: 1.3 GB and 0.6 s versus 3.3 GB and 0.9 s unordered. Prefer auto-increment `INTEGER` over random `UUID` for selectively filtered keys.

ART indexes come from `PRIMARY KEY`/`FOREIGN KEY`/`UNIQUE` or `CREATE INDEX`. Tradeoffs: enable constraint checks; slow inserts, updates and deletes; may speed highly selective single-column lookups; no effect on join, aggregation or sort. Index scans trigger for equality and `IN (...)` (and dynamic filters pushed from hash joins) only on single-column indexes without expressions:

```sql
CREATE INDEX idx ON tbl (col1);              -- eligible
CREATE INDEX idx_multi ON tbl (col1, col2);  -- not eligible
CREATE INDEX idx_expr ON tbl (col1 + 1);     -- not eligible
```
Threshold: `MAX(2048, 0.001 * table_cardinality)` rows, tuned via `index_scan_max_count` and `index_scan_percentage` (zero disables). Confirm with `EXPLAIN ANALYZE`.

Memory: index buffers are registered but not yet buffer-managed, so they are never evicted and can crowd out queries. `DETACH` then `ATTACH` reloads them lazily; disabling index scans and re-attaching after changes reduces the impact further. Indexes are serialized and lazily loaded, so they do not slow database opening.

Guidelines: constraints only for integrity; explicit indexes only for highly selective queries with spare memory; create them after bulk loading.

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages guides/performance/schema.md and guides/performance/indexing.md in full. Confirmed: every benchmark figure (timestamps, join, primary key load, ordering), constraint and zonemap guidance, ART tradeoffs, index scan eligibility examples, the scan threshold and the two settings (zero disables), `EXPLAIN ANALYZE` advice, memory and DETACH/ATTACH behaviour, lazy index loading, guidelines. Changed: tied the smaller-types advice to memory-constrained environments and completed the disable-scans plus re-attach advice per the page; removed the invented Verify step.

Method: documentation only; no commands were run.
