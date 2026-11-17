---
id: computing-software.data-engineering.apache-spark.cogrouped-applyinpandas
name: cogrouped-applyinpandas
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, cogrouped-map, applyinpandas, pandas-udf, cogroup, pyspark-udfs]
level: advanced
status: docs-checked
description: "Process two DataFrames group-by-group in pandas with PySpark cogroup().applyInPandas: asof joins, per-key diffs, memory limits and schema rules."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.PandasCogroupedOps.applyInPandas.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cogrouped map: cogroup().applyInPandas

**Use when:** for each key you need the matching rows from **two** DataFrames together in pandas, e.g. `pd.merge_asof` per instrument, comparing a customer's old and new records, or custom per-key reconciliation that SQL joins express badly.

```python
import pandas as pd
def asof(trades: pd.DataFrame, quotes: pd.DataFrame) -> pd.DataFrame:
    trades = trades.sort_values("ts"); quotes = quotes.sort_values("ts")
    return pd.merge_asof(trades, quotes[["ts", "bid", "ask"]], on="ts", direction="backward")

out = (trades_df.groupby("symbol")
       .cogroup(quotes_df.groupby("symbol"))
       .applyInPandas(asof, schema="symbol string, ts timestamp, qty long, bid double, ask double"))
```
- The function receives two pandas DataFrames (one per side) for each key; either can be empty when a key exists on only one side. Handle empties explicitly.
- Optional 3-argument form `f(key, left, right)` passes the key tuple.
- `schema` must match the returned columns by name (and types). A mismatch fails at runtime.
- Both sides are shuffled by key. Each group (both sides) is loaded fully into the Python worker's memory: a hot key with millions of rows OOMs the worker. Check group sizes first and salt or pre-aggregate skewed keys.
- Timestamp conversion between Spark and pandas depends on the session time zone and the Spark release: test with real timestamps.

## Alternatives
- Plain equi-join or `ASOF`-style window logic in SQL is faster when expressible.
- One DataFrame per group: `groupBy().applyInPandas`.

## Verify
- [ ] Test the function locally on two small pandas frames including the empty-side cases.
- [ ] Max group size (`groupBy(key).count().orderBy(desc)`) fits comfortably in executor Python memory.

## Checked

2026-10-28. Confirmed: the applyInPandas reference for the cogroup API. Removed: a timezone-naive claim (contradicted the pandas-udfs skill), an unconfirmed config key and a quoted error.

Method: documentation only; no commands were run.
