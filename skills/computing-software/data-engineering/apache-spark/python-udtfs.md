---
id: computing-software.data-engineering.apache-spark.python-udtfs
name: python-udtfs
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, python-udtf, table-function, udtf, lateral-join, arrow-udtf, analyze-method]
level: advanced
status: docs-checked
description: "Write PySpark Python UDTFs (Spark 3.5+) that return multiple rows and columns per input, register them for SQL, use LATERAL joins, and know their cost vs builtins."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.udtf.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Python UDTFs

**Goal:** turn one input row (or a table partition) into zero or many output rows with a custom schema, callable from SQL and DataFrames.

## Basic UDTF
```python
from pyspark.sql.functions import udtf, lit

@udtf(returnType="token: string, pos: int")
class Tokenize:
    def eval(self, text: str):
        if text is None:
            return
        for i, tok in enumerate(text.split()):
            yield tok, i

Tokenize(lit("a quick fox")).show()
spark.udtf.register("tokenize", Tokenize)
```
```sql
SELECT d.id, t.token, t.pos
FROM docs d, LATERAL tokenize(d.body) t;
```

## Table arguments and partitioning
```python
@udtf(returnType="user_id: string, sessions: int")
class Sessionize:
    def __init__(self):
        self.user, self.n, self.last = None, 0, None
    def eval(self, row):
        self.user = row["user_id"]
        if self.last is None or (row["ts"] - self.last).total_seconds() > 1800:
            self.n += 1
        self.last = row["ts"]
    def terminate(self):
        yield self.user, self.n
```
```sql
SELECT * FROM Sessionize(TABLE(events) PARTITION BY user_id ORDER BY ts);
```
`terminate()` is called once per partition: put per-group aggregation there.

## Dynamic schema with analyze
A static method `analyze(*args)` can return `AnalyzeResult(schema=...)` so the output schema depends on literal arguments (e.g. a column list). Use only when a fixed schema really does not fit.

## Performance
- Each row crosses JVM <-> Python. For simple explode/split use builtins (`explode`, `posexplode`, `split`, `inline`): much faster.
- Arrow-optimized UDTFs batch the transfer: `useArrow` on the `udtf` decorator, or the session conf `spark.sql.execution.pythonUDTF.arrow.enabled` (documented default `true`, since 3.5.0).
- UDTFs are opaque to the optimizer: no predicate pushdown through them.

## Gotchas
- Yield tuples matching the schema order; yielding a scalar for a one-column schema needs `yield (value,)`.
- Exceptions in `eval` fail the whole task; catch and emit an error column instead for dirty data.
- Requires Spark 3.5+.

## Verify
- [ ] Unit test the class directly in Python (`list(Tokenize().eval("a b"))`) and through `spark.sql`.
- [ ] Compare runtime against a builtin-only version on a sample.

## Checked

2026-10-28. Confirmed: useArrow on the udtf page and pythonUDTF.arrow.enabled (default true, 3.5.0) on the configuration page. Removed: a wrong claim that Arrow UDTFs arrived in Spark 4.0 with the setting opt-in, a speedup range and a Databricks version.

Method: documentation only; no commands were run.
