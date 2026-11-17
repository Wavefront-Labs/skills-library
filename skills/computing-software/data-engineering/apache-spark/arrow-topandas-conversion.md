---
id: computing-software.data-engineering.apache-spark.arrow-topandas-conversion
name: arrow-topandas-conversion
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, apache-arrow, topandas, createdataframe, arrow-pyspark-enabled, driver-oom, fallback, pyarrow, toarrow]
level: practitioner
status: docs-checked
description: "Move data between Spark and pandas efficiently: Arrow-enabled toPandas/createDataFrame, fallback behaviour, driver memory limits, unsupported types, and safer alternatives."
sources:
  - https://spark.apache.org/docs/latest/configuration.html#runtime-sql-configuration
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Arrow and toPandas / createDataFrame

**Goal:** convert between Spark and pandas quickly when the data genuinely fits on the driver, and avoid it when it does not.

## Enable Arrow
```python
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")          # default true in current Spark
spark.conf.set("spark.sql.execution.arrow.pyspark.fallback.enabled", "true") # falls back to the non-Arrow path on error
pdf = df.toPandas()
sdf = spark.createDataFrame(pdf)            # with Arrow: fast; without: row-by-row pickle
```
With fallback enabled, an error before the actual computation reverts to the non-Arrow path; set fallback to `false` in tests to catch it. `ArrayType` of `TimestampType` is documented as unsupported.

## Size limits
- `toPandas()` collects everything to the driver. Rule: only for results you would happily hold in a laptop's memory (well under driver memory).
- Large results hit `spark.driver.maxResultSize` (default 1g; jobs abort above it, 0 is unlimited).
- Better options for large data: write Parquet and read with pandas/polars/duckdb in batches, or keep the work in Spark (pandas API on Spark).

## createDataFrame from pandas
- Pass an explicit schema to avoid type guesses.
- With Arrow, batches are capped by `spark.sql.execution.arrow.maxRecordsPerBatch` (default 10000) and still pass through the driver: fine for MBs, bad for GBs (write to storage instead).

## Type gotchas
- Timestamps are converted using the session time zone (`spark.sql.session.timeZone`); set it explicitly.
- Check the Arrow type-support table in the PySpark pandas/Arrow guide for Decimal, Map and nested types in your version.

## Verify
- [ ] Row count and dtypes of the pandas result match the Spark schema.
- [ ] With fallback disabled in CI, conversions pass (no unsupported types sneaking in).
- [ ] No `toPandas()` on unbounded production data (code review / grep).

## Checked
2026-10-31. Confirmed against the Spark configuration page and the PySpark pandas/Arrow guide: Arrow enabled by default, fallback behaviour, `maxResultSize` default 1g, `maxRecordsPerBatch` default 10000, ArrayType of TimestampType unsupported. Removed unconfirmed speed-up multiple, `toArrow` version, error message text, memory multiple, NaN, Decimal, Map and ns-range claims.
Method: documentation only; no commands were run.
