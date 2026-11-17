---
id: computing-software.data-engineering.apache-spark.window-functions
name: window-functions
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, dataframe-api, spark-window-functions, window, row-number, rank, lag, lead, rowsbetween, rangebetween, running-total, latest-record, spark-sql]
level: practitioner
status: docs-checked
description: "Use Spark window functions: latest-row-per-key with row_number, lag/lead deltas, running totals, rowsBetween vs rangeBetween frames, and the default frame trap."
sources:
  - https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-window.html
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/window.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Window functions in Spark

**Goal:** compute per-row values over related rows (dedupe to latest, deltas, running sums, moving averages) correctly and without a giant single partition.

## Latest record per key (dedupe)
```python
from pyspark.sql import functions as F, Window as W
w = W.partitionBy("customer_id").orderBy(F.col("updated_at").desc(), F.col("ingest_id").desc())
latest = (cdc.withColumn("rn", F.row_number().over(w))
             .filter("rn = 1").drop("rn"))
```
Add a tiebreaker column to `orderBy`: with ties, `row_number` picks arbitrarily and results differ between runs.
`rank` (gaps on ties) and `dense_rank` (no gaps) keep all tied rows; use them only when you want ties.

## Deltas and sessions
```python
w = W.partitionBy("device_id").orderBy("ts")
df = (df.withColumn("prev_ts", F.lag("ts").over(w))
        .withColumn("gap_s", F.col("ts").cast("long") - F.col("prev_ts").cast("long"))
        .withColumn("new_session", (F.col("gap_s") > 1800) | F.col("prev_ts").isNull())
        .withColumn("session_no", F.sum(F.col("new_session").cast("int")).over(w)))
```

## Frames: the default trap
With `orderBy` and no explicit frame, the default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. Two consequences:
- `F.last("x").over(w)` returns the current row (or its peers), not the partition's last row. Use `.rowsBetween(W.unboundedPreceding, W.unboundedFollowing)`.
- Running sum with duplicate order keys includes all peers of the current row (RANGE), so tied rows show the same total. Use `rowsBetween(W.unboundedPreceding, W.currentRow)` for a strict row-by-row running total.

Moving 7-day average on time (range in seconds over a numeric order key):
```python
w7 = (W.partitionBy("store").orderBy(F.col("day").cast("timestamp").cast("long"))
       .rangeBetween(-6 * 86400, 0))
df = df.withColumn("avg_7d", F.avg("sales").over(w7))
```
`rowsBetween(-6, 0)` would be "last 7 rows", wrong if days are missing.

## Performance
- Every distinct `partitionBy` spec is a shuffle + sort. Reuse the same window spec for several columns.
- `W.orderBy(...)` with **no partitionBy** moves all data to one partition (Spark logs a warning). Fine for small data only.
- Skewed partition keys -> one massive task holding the whole partition sorted in memory/spill.

## Verify
- [ ] Every `row_number` window has a deterministic, unique ordering.
- [ ] Any `last`/`first`/running aggregate has an explicit frame.
- [ ] `explain()` shows one `Window` + `Exchange` per distinct partition spec, none without partitioning on large data.

## Checked

2026-10-28. Confirmed: the default RANGE frame wording on the window-syntax page. Removed: a plan-node and version claim and a quoted warning that the pages do not show.

Method: documentation only; no commands were run.
