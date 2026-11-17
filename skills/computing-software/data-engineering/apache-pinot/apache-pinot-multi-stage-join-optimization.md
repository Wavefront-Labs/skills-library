---
id: computing-software.data-engineering.apache-pinot.apache-pinot-multi-stage-join-optimization
name: apache-pinot-multi-stage-join-optimization
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, multi-stage-engine, joins, optimizing-joins, semi-join, predicate-pushdown, hash-join, table-statistics]
level: advanced
status: docs-checked
description: "Making Pinot multi-stage joins fast: smaller table on the right, predicate push-down, and rewriting joins to indexed semi-joins."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/querying-and-sql/multi-stage-query/optimizing-joins.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimizing multi-stage joins

Pinot does **not** rely on table statistics to order joins, so the order you write matters.

- The right input is fully consumed to build an in-memory hash table and may be broadcast to all workers. Joining a large table to a small one is cheaper than the reverse, so put the **smaller** relation on the right (second in SQL).
- With three or more tables left and right get confusing; check the explain plan to see which input is which.
- Predicates are pushed down to each table scan automatically when Pinot can prove the change keeps the semantics, which cuts shuffled data and can let indexes apply. Push-down stops short of the table scan when an input is a subquery with `LIMIT`; to filter before the limit, put the filter inside the subquery.
- A subquery in `WHERE` (`IN (SELECT ...)` or `EXISTS`) is executed first and its values are substituted into the main query as an `IN` list, so indexes can be used. This optimization does not appear in the explain plan.

An inner or left join is rewritten to a semi-join automatically when all three hold:
1. only columns from the left side are projected,
2. the join condition is an equality, and
3. the right side is unique.

Pinot columns cannot be marked unique, so the only way to tell Pinot the right side is unique is an expression that guarantees it, such as `DISTINCT` or `GROUP BY` on the join columns:
```
SELECT c.c_address FROM customer c
JOIN (SELECT DISTINCT o_custkey FROM orders) d ON c.c_custkey = d.o_custkey
```
Using the raw `orders` table would not be equivalent, because a join repeats left rows when the right side repeats and a semi-join never does. Often it is easier to write `WHERE c_custkey IN (SELECT o_custkey FROM orders)` directly.

Reduce shuffle: understand Pinot's join strategies, and use `stageStats` and the explain plan modes to see how data is shuffled.

## Checked

2026-11-09. Read the whole Pinot docs page `optimizing-joins.md`. Confirmed each statement above. Removed: the claim that dimension tables are replicated to all servers (the page does not say so), the advice to write filters in WHERE "so they apply before the join" (Pinot pushes them down itself), and the example that assumed `vip.userId` is unique without a guarantee. Not read: the linked join-strategies and hash-join operator pages.
Method: documentation only; no commands were run.
