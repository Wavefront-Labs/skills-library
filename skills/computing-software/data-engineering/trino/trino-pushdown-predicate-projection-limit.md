---
id: computing-software.data-engineering.trino.trino-pushdown-predicate-projection-limit
name: trino-pushdown-predicate-projection-limit
category: computing-software
field: data-engineering
product: trino
tags: [pushdown, predicate-pushdown, projection-pushdown, dereference-pushdown, topn-pushdown]
level: advanced
status: docs-checked
description: "Recognise predicate, projection, dereference, limit and Top-N pushdown in Trino EXPLAIN plans and what each saves."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/optimizer/pushdown.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino pushdown predicate projection limit

Pushdown passes part of a query to the underlying database or storage system. Benefits: faster queries, less network traffic, less load on the source, often lower cost. Support is connector-specific.

How to tell it worked:
- Predicate pushdown (row filtering from `WHERE`): the `EXPLAIN` plan has no `ScanFilterProject` for that clause.
- Projection pushdown (column pruning from `SELECT` and other clauses): the `TableScan` `Layout` lists only the needed columns.
- Dereference pushdown: like projection, but selects only the used fields inside a top-level or nested `ROW` column. With Hive, the file reader reads just that field, which can save a lot of IO.
- Limit pushdown: `LIMIT N` or `FETCH FIRST N ROWS` on unsorted data is delegated, cutting transferred data.
- Top-N pushdown: `ORDER BY ... LIMIT N`. A PostgreSQL scan shows `sortOrder=[id ASC NULLS LAST] limit=5` and the plan has no `TopN` operator in the coordinator fragment. A connector without support, such as `tpch`, shows `TopN[5 by (custkey ASC NULLS LAST)]` in Fragment 0 and a `TopNPartial` on the source fragment.

Limit and Top-N support is connector-specific because data sources differ in capabilities and SQL syntax. The page's explicit three-part condition (connector support, function support, query shape) is stated only for aggregation pushdown.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. Replaced an unsupported generic troubleshooting line with what the page states.
