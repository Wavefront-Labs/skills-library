---
id: computing-software.data-engineering.apache-spark.pandas-udfs-and-applyinpandas
name: pandas-udfs-and-applyinpandas
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, pyspark-udf, pandas-udf, applyinpandas, mapinpandas, cogroup, grouped-map, iterator-udf, vectorized-udf, maxrecordsperbatch]
level: advanced
status: docs-checked
description: "Use pandas UDFs in PySpark: Series-to-Series, iterator UDFs with per-partition setup, grouped applyInPandas, mapInPandas, cogroup, and memory limits per group."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.pandas_udf.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# pandas UDFs, applyInPandas and mapInPandas

**Goal:** run vectorised Python (pandas/numpy/scikit-learn) at scale with Arrow transfer and bounded memory.

## Series -> Series (scalar)
```python
import pandas as pd
from pyspark.sql.functions import pandas_udf

@pandas_udf("double")
def fahrenheit(c: pd.Series) -> pd.Series:
    return c * 9 / 5 + 32

df.withColumn("temp_f", fahrenheit("temp_c"))
```
Type hints decide the UDF kind. Output length must equal input length.

## Iterator UDF: expensive setup once per partition
```python
from typing import Iterator
@pandas_udf("double")
def score(batches: Iterator[pd.DataFrame]) -> Iterator[pd.Series]:
    model = load_model("s3://models/churn/7")      # once per task, not per batch
    for pdf in batches:
        yield pd.Series(model.predict_proba(pdf)[:, 1])

df.withColumn("p_churn", score(F.struct("tenure", "spend", "tickets")))
```

## Grouped map: applyInPandas
```python
def fit_trend(pdf: pd.DataFrame) -> pd.DataFrame:
    import numpy as np
    slope = np.polyfit(pdf.day_num, pdf.sales, 1)[0]
    return pd.DataFrame({"store": [pdf.store.iloc[0]], "slope": [slope]})

trends = sales.groupBy("store").applyInPandas(fit_trend, schema="store string, slope double")
```
- **Each group is loaded fully into one Python worker's memory.** A skewed group (one giant store) OOMs the worker. Check max group size first; salt or pre-aggregate big groups.
- Output schema must match exactly (names and types); the function must return a DataFrame even for empty results.

## mapInPandas: arbitrary row-count transforms per partition
```python
def explode_json(it):
    for pdf in it:
        yield pd.json_normalize(pdf["payload"].map(json.loads))
df.mapInPandas(explode_json, schema=out_schema)
```

## cogroup: two DataFrames by key
`df1.groupBy("id").cogroup(df2.groupBy("id")).applyInPandas(func, schema)`: func gets both pandas groups (e.g. as-of joins).

## Tuning
- `spark.sql.execution.arrow.maxRecordsPerBatch` (default 10,000): lower for wide rows/large objects.
- Python worker memory is outside the JVM heap: raise `spark.executor.memoryOverhead` or set `spark.executor.pyspark.memory`.
- Arrow type support is version-dependent (Map, nested struct arrays, some timestamp types): check the PySpark user guide's supported-types table for your release.
- `pyarrow` and `pandas` versions must be compatible with the Spark release on every executor.

## Verify
- [ ] Unit test the pure pandas function locally on a small pandas DataFrame before wrapping.
- [ ] Max group size (`groupBy(key).count().agg(max)`) is far below executor Python memory.
- [ ] `explain()` shows the Arrow-based Python evaluation nodes.

## Checked

2026-10-28. Confirmed: spark.sql.execution.arrow.maxRecordsPerBatch default 10000 and spark.executor.pyspark.memory on the configuration page. Removed: a timestamp-timezone claim that contradicted the cogrouped skill, a version gate and plan-node names.

Method: documentation only; no commands were run.
