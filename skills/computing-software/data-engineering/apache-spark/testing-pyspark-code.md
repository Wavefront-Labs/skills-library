---
id: computing-software.data-engineering.apache-spark.testing-pyspark-code
name: testing-pyspark-code
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, pyspark-testing, assertdataframeequal, assertschemaequal, pytest, local-sparksession, unit-tests, transformation-unit-tests]
level: practitioner
status: docs-checked
description: "Unit test PySpark transformations: pure functions over DataFrames, a session-scoped local SparkSession fixture, assertDataFrameEqual/assertSchemaEqual, and fast-test settings."
sources:
  - https://spark.apache.org/docs/latest/api/python/getting_started/testing_pyspark.html
  - https://github.com/apache/spark/blob/master/python/pyspark/testing/utils.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing PySpark code

**Goal:** fast, deterministic unit tests for transformation logic that run in CI without a cluster.

## Structure code for testing
Keep I/O at the edges; make transformations pure functions `DataFrame -> DataFrame`:
```python
# pipeline/transforms.py
from pyspark.sql import DataFrame, functions as F
def add_net_amount(df: DataFrame) -> DataFrame:
    return df.withColumn("net", F.col("gross") - F.coalesce("discount", F.lit(0)))
```

## Session fixture (conftest.py)
```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    s = (SparkSession.builder.master("local[2]").appName("tests")
         .config("spark.sql.shuffle.partitions", "2")          # default 200 makes tiny tests slow
         .config("spark.ui.enabled", "false")
         .config("spark.sql.session.timeZone", "UTC")
         .getOrCreate())
    yield s
    s.stop()
```
One session per test run: starting a JVM per test costs seconds each.

## Assertions (Spark 3.5+, pyspark.testing.utils)
```python
from pyspark.testing.utils import assertDataFrameEqual, assertSchemaEqual
from pipeline.transforms import add_net_amount

def test_add_net_amount_handles_null_discount(spark):
    src = spark.createDataFrame([(100.0, None), (50.0, 5.0)], "gross double, discount double")
    expected = spark.createDataFrame([(100.0, None, 100.0), (50.0, 5.0, 45.0)],
                                     "gross double, discount double, net double")
    assertDataFrameEqual(add_net_amount(src), expected)          # order-insensitive by default
    assertSchemaEqual(add_net_amount(src).schema, expected.schema)
```
- `assertDataFrameEqual(actual, expected, checkRowOrder=False, rtol=1e-5, atol=1e-8, ...)`: row order is not checked by default, `rtol`/`atol` give float tolerance, and it also accepts lists of Rows. `maxErrors` and `showOnlyDiff` limit the failure report.
- The built-in utility functions are standalone and work with any test framework (the docs show unittest and pytest).
- Always declare schemas with DDL strings in tests; inferred types (long vs int) cause false failures.

## What to test
- Null handling, empty input, duplicate keys, late/out-of-order timestamps, schema of the output.
- Join cardinality (no fan-out): assert row counts.
- Not Spark itself (do not test that `groupBy` sums correctly).

## Speed and CI
- Keep slow integration tests separate (for example a pytest marker) and run them against a real cluster.
- Pin the `pyspark` version and a compatible Java in CI.
- Parallel test runners start one JVM per worker, so size them to the CI machine.

## Verify
- [ ] `pytest` runs the suite locally in seconds-to-a-minute with `local[2]`.
- [ ] Tests fail when a transform's null handling is broken (mutation check).

## Checked
2026-11-09. Confirmed against the PySpark testing getting-started page (Spark 3.5+ utilities, unittest and pytest options, `assertDataFrameEqual` with `rtol`, `assertSchemaEqual`, import from `pyspark.testing.utils`) and the `pyspark/testing/utils.py` source (signature and defaults of `assertDataFrameEqual`). Removed: the chispa recommendation, the Java 17 pin, and the xdist claim. Session-builder settings and the transform example are illustrative code, not documented claims.
Method: documentation only; no commands were run.
