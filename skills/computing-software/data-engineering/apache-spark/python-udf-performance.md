---
id: computing-software.data-engineering.apache-spark.python-udf-performance
name: python-udf-performance
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, pyspark-udf, python-udf-performance, builtin-functions, arrow-optimized-udf, udf-serialization, catalyst-optimizer, udf-determinism]
level: practitioner
status: docs-checked
description: "Avoid slow PySpark UDFs: why row-at-a-time Python UDFs are costly, replacing them with built-in functions or SQL expressions, Arrow-optimized UDFs, and nondeterminism flags."
sources:
  - https://spark.apache.org/docs/latest/api/python/user_guide/udfandudtf.html
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.udf.html
  - https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html
  - https://spark.apache.org/docs/latest/api/python/tutorial/sql/arrow_pandas.html
  - https://spark.apache.org/docs/latest/api/python/tutorial/sql/arrow_python_udf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python UDF performance in PySpark

**Goal:** keep transformations in the JVM where possible and make unavoidable Python code cheap.

## Why plain UDFs are slow
A plain Python `@udf` runs Python code outside the JVM, so data is moved between the JVM and Python, and Spark cannot optimise inside your function the way it does for built-in expressions. Built-in functions stay in the JVM; measure before assuming a UDF is needed.

## Step 1: replace with built-ins (almost always possible)
| UDF doing | Built-in |
|---|---|
| String cleanup / regex | `F.regexp_replace`, `F.regexp_extract`, `F.split`, `F.trim`, `F.translate` |
| If/else mapping | `F.when(...).otherwise(...)`, or a join to a small mapping table |
| JSON parsing | `F.from_json`, `F.get_json_object` |
| Date math | `F.date_add`, `F.months_between`, `F.date_trunc` |
| Array processing | `F.transform`, `F.filter`, `F.aggregate` (higher-order functions) |
| Hashing | `F.sha2`, `F.xxhash64` |
| Anything SQL can say | `F.expr("...")` |

## Step 2: if Python is truly needed, vectorise
- **pandas UDF** (`@pandas_udf`) takes and returns `pandas.Series` (type hints select the variant).
- **Arrow-optimized Python UDF**: `@udf(returnType=..., useArrow=True)` or `spark.sql.execution.pythonUDF.arrow.enabled=true`. The Spark config takes effect only when `useArrow` is unset. The PySpark migration guide says regular Python UDFs are Arrow-optimized by default from Spark 4.2; check your version's docs.

## Step 3: make UDFs correct
```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def normalise_phone(s):
    if s is None:                       # UDFs receive None for nulls; handle it
        return None
    ...
normalise_phone = normalise_phone.asNondeterministic()   # only if output can vary (random, time, external calls)
```
- Declare the exact return type your function actually returns.
- SQL boolean expressions do not short-circuit: in `WHERE cond AND udf(x)` the UDF may be called on all rows regardless of `cond` (PySpark docs). Handle nulls and bad input inside the function.
- Heavy setup (loading a model, compiling a regex) inside the function repeats per call; the iterator pandas UDF form (`Iterator[pd.Series] -> Iterator[pd.Series]`) lets you set up state before iterating.
- Calling external APIs from UDFs: rate-limit and batch (`mapInPandas` is available for map operations), and expect retries to repeat calls.

## Verify
- [ ] `explain()` shows `ArrowEvalPython` (or a Python eval node) only where unavoidable.
- [ ] Benchmark built-in vs UDF on a representative sample; keep the faster.
- [ ] Null-input unit test for every UDF.

## Checked
2026-11-01. Confirmed in the Apache Spark repo (docs and PySpark source): `useArrow` parameter and `spark.sql.execution.pythonUDF.arrow.enabled` precedence, Arrow default from 4.2 (migration guide), `asNondeterministic`, `ArrowEvalPython` plan node, no short-circuit note, Iterator-of-Series pandas UDF, `mapInPandas`, and existence of every built-in function in the table. Removed: speed-up multipliers, the per-executor-core/pickle description, "3.5+" version gate, `BatchEvalPython`, the silent-null return type claim, and the Catalyst reordering claim.
Method: documentation only; no commands were run.
