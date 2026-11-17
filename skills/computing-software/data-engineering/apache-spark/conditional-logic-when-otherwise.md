---
id: computing-software.data-engineering.apache-spark.conditional-logic-when-otherwise
name: conditional-logic-when-otherwise
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, spark-sql, when-otherwise, case-when, expr, coalesce, conditional-columns]
level: intro
status: docs-checked
description: "Write conditional column logic in Spark with when/otherwise, CASE WHEN via expr, coalesce and nullif, including evaluation order and null traps."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.when.html
  - https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-case.html
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.nullif.html
  - https://spark.apache.org/docs/latest/api/python/tutorial/sql/arrow_python_udf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional logic: when / otherwise / CASE

```python
from pyspark.sql import functions as F
df = df.withColumn("tier",
    F.when(F.col("spend") >= 10000, "gold")
     .when(F.col("spend") >= 1000, "silver")
     .otherwise("bronze"))
# same thing as SQL
df = df.withColumn("tier", F.expr("CASE WHEN spend >= 10000 THEN 'gold' WHEN spend >= 1000 THEN 'silver' ELSE 'bronze' END"))
```

## Rules that bite
- Order the branches deliberately and put the narrowest condition first.
- Without `.otherwise`, unmatched rows get **null** (`None`), not the original value. To change only some rows: `F.when(cond, new).otherwise(F.col("x"))`.
- A comparison with a null spend yields null, not true, so `spend >= 1000` does not select that row. Handle nulls with an explicit first branch `F.when(F.col("spend").isNull(), "unknown")`.
- Combine conditions with `&`, `|`, `~` and parentheses: `(F.col("a") > 1) & (F.col("b") == "x")`. Python `and`/`or` raise "Cannot convert column into bool".
- In SQL CASE, the then and else expressions must be the same type or coercible to a common type.
- SQL boolean expressions do not short-circuit (PySpark UDF docs): do not rely on a `when` or `WHERE` guard to protect a UDF from bad input. Make the UDF null/edge safe itself.

## Related helpers
- `F.coalesce(a, b, F.lit(0))` first non-null.
- `F.nullif(a, b)` (Python API added in 3.5.0) returns null when equal, e.g. turn "" into null.
- `F.greatest`/`F.least` skip null values.
- Many conditions mapping codes to labels: join to a small lookup DataFrame (broadcast) instead of a long `when` chain; easier to maintain and test.

## Verify
- [ ] Group by the new column and count, including nulls: no unexpected null bucket.

## Checked
2026-11-01. Confirmed in the Apache Spark repo: `when` returns None for unmatched rows without `otherwise`; CASE type coercion wording; `nullif` versionadded 3.5.0; `greatest` skips nulls; `coalesce` returns first non-null; the `Cannot convert column into bool` message; no-short-circuit note in the PySpark Arrow UDF tutorial. Removed: first-match-wins wording, "mixing int and string gives string", the SQL-earlier nullif claim and the `IF(...)` example (not found in the docs read).
Method: documentation only; no commands were run.
