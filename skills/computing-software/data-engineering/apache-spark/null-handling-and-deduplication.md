---
id: computing-software.data-engineering.apache-spark.null-handling-and-deduplication
name: null-handling-and-deduplication
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, dataframe-api, spark-null-handling, dropduplicates, fillna, dropna, coalesce, eqnullsafe, data-cleansing, deduplication, three-valued-logic]
level: practitioner
status: docs-checked
description: "Handle nulls and duplicates in Spark: three-valued logic in filters and joins, eqNullSafe, fillna/dropna scoping, dropDuplicates vs window dedupe, and trimming dirty strings."
sources:
  - https://spark.apache.org/docs/latest/sql-ref-null-semantics.html
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.dropDuplicates.html
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameNaFunctions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Null handling and deduplication in Spark

**Goal:** clean data without silently dropping or duplicating rows because of null semantics.

## Three-valued logic bites
- `filter(col("status") != "cancelled")` drops rows where status is null (null != x is null -> treated as false). Write `filter((F.col("status") != "cancelled") | F.col("status").isNull())` or `~F.col("status").eqNullSafe("cancelled")`.
- `NOT IN (subquery)` returns no rows if the subquery contains a null. Use `NOT EXISTS` / left anti join.
- Joins on nullable keys: `a.k == b.k` never matches null to null. If nulls should match, use `a.k.eqNullSafe(b.k)` (SQL `<=>`); usually better to treat null keys as unknown and keep them out of the join.
- `col("x") == None` in Python is always null; use `isNull()`.

## Fill and drop, scoped
```python
df = df.fillna({"discount": 0, "channel": "unknown"})   # per-column, never a blanket fillna(0)
df = df.dropna(subset=["order_id", "order_ts"])          # only on required columns
df = df.withColumn("email", F.nullif(F.lower(F.trim("email")), F.lit("")))   # '' -> null
```
`fillna` silently ignores columns whose type does not match the fill value (int fill on a string column does nothing).
Count what you drop: `before - after` logged per run.

## Deduplication
| Need | Use |
|---|---|
| Exact duplicate rows | `df.dropDuplicates()` |
| One row per key, any row | `df.dropDuplicates(["order_id"])` (non-deterministic which row) |
| One row per key, latest | `row_number()` over `partitionBy(key).orderBy(ts desc, tiebreak desc)` = 1 |
| Streaming | `dropDuplicatesWithinWatermark` or `dropDuplicates` with a watermark |

`dropDuplicates(subset)` keeps an arbitrary row: never use it where "which row" matters (latest status, CDC).

## Dirty strings
```python
F.trim, F.regexp_replace("phone", r"[^0-9+]", ""), F.initcap, F.translate
F.try_to_number, F.try_to_timestamp  # null instead of an ANSI error on bad input
```
With `spark.sql.ansi.enabled=true`, a bad `cast("int")` raises instead of returning null (check the default for your Spark version); use `try_to_number`/`try_to_timestamp` where bad input is expected and count the nulls they produce.

## Verify
- [ ] Each filter on a nullable column states its null intent explicitly.
- [ ] Rows dropped by `dropna`/filters are counted and logged.
- [ ] Dedupe on a key is deterministic (rerun twice -> identical output hash).

## Checked

2026-10-28. Confirmed: nullif, try_to_number and try_to_timestamp in the PySpark functions list; dropDuplicatesWithinWatermark on the DataFrame API pages. Removed: `F.try_cast` (not in the PySpark function list), the nullif version gate and an unconfirmed ANSI-default claim.

Method: documentation only; no commands were run.
