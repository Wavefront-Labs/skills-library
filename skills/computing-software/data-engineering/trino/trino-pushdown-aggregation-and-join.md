---
id: computing-software.data-engineering.trino.trino-pushdown-aggregation-and-join
name: trino-pushdown-aggregation-and-join
category: computing-software
field: data-engineering
product: trino
tags: [aggregation-pushdown, join-pushdown, explain, pushdown-limitations, connector-pushdown]
level: advanced
status: docs-checked
description: "When Trino pushes aggregations and joins down to connectors such as PostgreSQL, how to verify it in EXPLAIN, and what blocks it."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/optimizer/pushdown.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino pushdown aggregation and join

Aggregation pushdown needs three things: the connector supports aggregation pushdown, supports the specific function, and the query structure allows it. Verify with `EXPLAIN`: if pushed down, no `Aggregate` operator appears for that function and the function shows inside the connector's `TableScan`. In the docs example, `SELECT regionkey, count(*) FROM nation GROUP BY regionkey` on PostgreSQL shows `count(*)` in the `TableScan` with `groupingSets`. A pushdown can be defeated by adding a condition, using a function the connector cannot push, or using a connector without support; then Trino shows `Aggregate(PARTIAL)` and `Aggregate(FINAL)`.

Unsupported shapes:
- `ROLLUP`, `CUBE`, `GROUPING SETS`
- expressions inside the call, such as `sum(a * b)`
- coercions, such as `sum(integer_column)`
- aggregations with ordering
- aggregations with a filter

Join pushdown delegates the join to the source, so Trino processes less data afterwards. Generic conditions: every predicate in the join can be pushed down, and the joined tables come from the same catalog. Details vary per connector. A pushed-down join shows no `Join` operator; the PostgreSQL `TableScan` instead contains the whole `INNER JOIN` query text. The docs warn that a pushed-down join can output more rows than its inputs contained, which may hurt performance.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
