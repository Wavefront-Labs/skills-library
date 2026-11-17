---
id: computing-software.data-engineering.apache-spark.unionbyname-and-set-operations
name: unionbyname-and-set-operations
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, spark-sql, unionbyname, union, intersect, except, set-operations, schema-drift]
level: practitioner
status: docs-checked
description: "Combine DataFrames correctly in Spark: union vs unionByName with allowMissingColumns, intersect/exceptAll, and distinct-vs-all semantics that silently change row counts."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.unionByName.html
  - https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-setops.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unionByName and set operations

## union matches by POSITION
`df1.union(df2)` (and SQL `UNION ALL`) aligns columns by position, not name. Two files with the same columns in a different order union "successfully" with values in the wrong columns.
```python
out = df1.unionByName(df2)                              # by name, error if a column is missing
out = df1.unionByName(df2, allowMissingColumns=True)    # missing columns become null (3.1+)
from functools import reduce
out = reduce(lambda a, b: a.unionByName(b, allowMissingColumns=True), dfs)
```
- SQL `UNION ALL` keeps duplicates and SQL `UNION` removes them (add `.distinct()` after a DataFrame union to match).
- Cast columns explicitly on both sides before a union so types do not change unexpectedly.

## intersect / except
| SQL | duplicates |
|---|---|
| `INTERSECT` / `INTERSECT DISTINCT` | removed |
| `INTERSECT ALL` | kept |
| `EXCEPT` / `EXCEPT DISTINCT` | removed |
| `EXCEPT ALL` | kept |
- `MINUS` is an alias for `EXCEPT`. The DataFrame methods for these are in the PySpark DataFrame API docs.
- Good for "rows in prod not in staging" diff checks:
```sql
SELECT * FROM expected EXCEPT ALL SELECT * FROM actual;
SELECT * FROM actual EXCEPT ALL SELECT * FROM expected;
```

## Verify
- [ ] Column order of inputs printed (`df.columns`) or unionByName used.
- [ ] Row count after union equals the sum of inputs (or the expected distinct count).

## Checked

2026-10-28. Confirmed against: PySpark DataFrame.unionByName page (resolves by name, allowMissingColumns fills nulls, new in 3.1.0), Spark SQL set operators page (INTERSECT/EXCEPT with ALL and DISTINCT, MINUS alias). Removed (not confirmable in the fetched pages): type-widening claim, DataFrame method names in the table, null-equality and min-count claims, deep-plan claim, shuffle/anti-join advice.

Method: documentation only; no commands were run.
