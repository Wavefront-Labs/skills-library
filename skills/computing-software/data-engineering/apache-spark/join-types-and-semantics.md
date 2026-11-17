---
id: computing-software.data-engineering.apache-spark.join-types-and-semantics
name: join-types-and-semantics
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, spark-join-types, null-safe-join, left-semi, left-anti, cross-join, eqnullsafe, ambiguous-columns, dataframe-api]
level: practitioner
status: docs-checked
description: "Choose and write the right Spark join: inner/outer/semi/anti/cross, null-safe equality, ambiguous column handling after joins, and row explosion checks."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.join.html
  - https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-join.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark join types and semantics

**Goal:** get the correct rows out of a join (not just a fast join), with no duplicate columns and no silent row multiplication.

## Join types
| how | Returns | Typical use |
|---|---|---|
| `inner` | matching rows | enrich facts with required dims |
| `left` / `left_outer` | all left, nulls for no match | optional enrichment |
| `full` / `outer` | all rows both sides | reconciliation |
| `left_semi` | left rows that have a match (left side values only) | "exists" filter |
| `left_anti` | left rows with no match | "not exists", new-record detection, orphan checks |
| `cross` | Cartesian | small calendar x entity grids only |

```python
new_customers = incoming.join(existing, "customer_id", "left_anti")
active_orders = orders.join(active_customers.select("customer_id"), "customer_id", "left_semi")
```
`left_semi` returns only left-side values, so it suits existence checks without multiplying left rows.

## Null-safe equality
`=` never matches null to null. For keys that may be null (composite natural keys):
```python
cond = a["k1"].eqNullSafe(b["k1"]) & a["k2"].eqNullSafe(b["k2"])
a.join(b, cond, "inner")
```
SQL: `ON a.k1 <=> b.k1`.

## Ambiguous columns
- Join on a column name list (`on="id"` or `["id","dt"]`) to get one copy of the key.
- With expression conditions, alias both sides:
```python
o = orders.alias("o"); c = customers.alias("c")
o.join(c, F.col("o.customer_id") == F.col("c.id"), "left").select("o.*", F.col("c.segment"))
```
- Self-joins: always alias, otherwise the condition can be ambiguous or trivially true.

## Row explosion check
Before trusting a join, check uniqueness of the right-side key:
```python
dupes = customers.groupBy("id").count().filter("count > 1")
assert dupes.limit(1).count() == 0
```
Compare `count()` before and after a left join; growth means duplicate keys on the right.

## Gotchas
- Joining on columns with different types (string vs bigint) casts implicitly; compare columns in the same type.
- Filters on the right table placed in `WHERE` after a left join turn it into an inner join; put them in the `ON` clause or filter the right DataFrame first.
- Outer joins with `coalesce(a.key, b.key)` are needed to get a single key column in full joins on expressions.

## Verify
- [ ] Right-side join keys proven unique (or duplication intended).
- [ ] Row counts before/after match expectations.

## Checked

2026-11-01. Confirmed against the PySpark `DataFrame.join` page (accepted `how` names: inner, cross, outer, full, left, right, semi/left_semi, anti/left_anti) and the Spark SQL JOIN page (cross = Cartesian product; semi returns left values with a match; anti returns left values without). Removed: hash-optimisation note, warning text, crossJoin default claim, "01" cast claim.

Method: documentation only; no commands were run.
