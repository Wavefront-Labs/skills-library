---
id: computing-software.data-engineering.apache-spark.pandas-api-on-spark
name: pandas-api-on-spark
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, pandas-api-on-spark, pyspark-pandas, koalas, ps-dataframe, default-index, compute-ops-on-diff-frames, pandas-migration]
level: practitioner
status: gated
description: "Scale pandas code with pyspark.pandas: import changes, default index types and their cost, ops on different frames, unsupported/slow APIs, and converting to Spark DataFrames."
sources:
  - https://spark.apache.org/docs/latest/api/python/user_guide/pandas_on_spark/index.html
  - https://spark.apache.org/docs/latest/api/python/user_guide/pandas_on_spark/options.html
  - https://spark.apache.org/docs/latest/api/python/user_guide/pandas_on_spark/best_practices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pandas API on Spark (pyspark.pandas)

**Goal:** run existing pandas-style code on data too big for one machine with minimal rewrites, knowing which pandas habits become expensive.

## Start
```python
import pyspark.pandas as ps
psdf = ps.read_parquet("s3://lake/orders/")
psdf["margin"] = psdf["revenue"] - psdf["cost"]
out = psdf.groupby("country")["margin"].sum().sort_values(ascending=False)
out.head(10)
sdf = psdf.to_spark()                      # to a Spark DataFrame (index dropped unless index_col given)
psdf2 = sdf.pandas_api(index_col="order_id")
```

## The index is the expensive part
pandas always has an index; Spark rows do not. Choose via `ps.set_option("compute.default_index_type", ...)`: (gated: unconfirmed, source is paywalled or blocked)
| Type | Cost | Behaviour |
|---|---|---|
| `sequence` (default) | Moves data to a single partition to number rows: slow on big data | 0..n-1 exactly |
| `distributed-sequence` | Extra job, distributed | 0..n-1, recommended general default |
| `distributed` | Cheapest | Monotonic increasing, non-consecutive ids |
Better: set a real key as index (`index_col="order_id"`) when reading.

## Things that behave differently
- **Operations between two different frames** (`psdf1["a"] + psdf2["b"]`) need a join on the index and are disabled by default: `ps.set_option("compute.ops_on_diff_frames", True)` enables them (expensive).
- Row order is not guaranteed unless you sort; `head()` without sorting returns arbitrary rows.
- `iterrows`, `apply` with Python functions per row, and `to_pandas()` on big frames are slow or collect to driver.
- Some APIs are unsupported or bounded: options `compute.max_rows` (default 1000) controls when shortcuts use a local pandas sample (e.g. for plotting, some `__repr__`).
- `psdf.spark.cache()` / `.spark.persist()` for reuse; `psdf.spark.explain()` to see the plan.

## Migration approach
1. Swap `import pandas as pd` to `import pyspark.pandas as ps` for the heavy steps only.
2. Read with an explicit index column.
3. Run tests comparing output against pandas on a small sample (`ps.testing` / compare `to_pandas()` results).
4. Rewrite hot spots that fall back to row-wise Python into Spark DataFrame code.

## Verify
- [ ] No `sequence` default index on large frames (check options at session start).
- [ ] Results on a sample equal the original pandas implementation.
- [ ] Spark UI shows no stage running with a single task caused by index creation.

## Checked

2026-11-02

- Confirmed: Only the pandas-on-Spark user-guide pages were requested.
- Removed or gated: The user-guide index, options and best-practices pages returned no readable text, so option names (compute.default_index_type, compute.ops_on_diff_frames, compute.max_rows) and API calls are gated, confirm in the PySpark pandas-on-Spark docs.

Method: documentation only; no commands were run.
