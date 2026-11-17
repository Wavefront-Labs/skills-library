---
id: computing-software.data-engineering.apache-spark.streaming-watermarks-and-windowed-aggregation
name: streaming-watermarks-and-windowed-aggregation
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, structured-streaming, spark-streaming-watermark, windowed-aggregation, withwatermark, tumbling-window, sliding-window, session-window, output-modes, append-mode, state-cleanup]
level: advanced
status: docs-checked
description: "Event-time windowed aggregation in Spark Structured Streaming: withWatermark, tumbling/sliding/session windows, append vs update output, and why state grows without a watermark."
sources:
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html#window-operations-on-event-time
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html#handling-late-data-and-watermarking
  - https://github.com/apache/spark/blob/master/sql/api/src/main/scala/org/apache/spark/sql/streaming/progress.scala
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Watermarks and windowed aggregation in Structured Streaming

**Goal:** aggregate events by event time with bounded state and a known policy for late data.

## Pattern
```python
from pyspark.sql import functions as F
events = (spark.readStream.format("kafka")...load()
          .select(F.from_json(F.col("value").cast("string"), schema).alias("e")).select("e.*"))

agg = (events
       .withWatermark("event_ts", "10 minutes")                 # tolerate 10 min lateness
       .groupBy(F.window("event_ts", "5 minutes"), "page")      # tumbling 5-min windows
       .agg(F.count("*").alias("views")))

q = (agg.writeStream.outputMode("append")                       # emit each window once, when final
     .format("parquet").option("path", "s3://out/page_views_5m/")
     .option("checkpointLocation", "s3://ckpt/page_views/")
     .start())
```

## How the watermark works
- The watermark is the maximum event time seen minus the delay, set at the beginning of every trigger. With several input streams the global watermark is the minimum by default; `spark.sql.streaming.multipleWatermarkPolicy=max` follows the fastest stream but drops data from slower streams aggressively.
- Guarantee: data less than the delay behind the latest processed event time is aggregated; data delayed more than that may or may not be aggregated (the guarantee is strict in one direction only).
- Dropped late rows are counted by `numRowsDroppedByWatermark` in the stateOperators progress.
- Without a watermark the engine must keep intermediate state for every window; watermarking cleans state only when output mode is Append or Update, the aggregation is on the event-time column or a window over it, and `withWatermark` is called on the same column as the aggregate.

## Window types
```python
F.window("event_ts", "10 minutes", "5 minutes")    # sliding: 10-min windows every 5 min (each event in 2 windows)
F.session_window("event_ts", "30 minutes")         # gap-based session windows
F.window("event_ts", "1 day", startTime="-10 hours")  # shift daily windows to a local-day boundary
```

## Output modes with aggregation
| Mode | Behaviour | Needs |
|---|---|---|
| `append` | Only final counts are written, after the watermark passes the window | Watermark; output is delayed by the late threshold |
| `update` | Changed windows each batch | A sink that handles updates |
| `complete` | Whole result table each batch | Cannot use watermarking to drop state |
For `update` into a store that needs upserts, use `foreachBatch` and merge keyed on window plus key in your store.

## Choosing the delay
Look at actual lateness (arrival time minus `event_ts`) in a sample. A longer delay keeps more state and delays append-mode results.

## Gotchas
- Append-mode results appear only after the window end plus the delay, because the watermark advances per trigger from observed event times.
- Changing the number or type of grouping keys or aggregates of a streaming aggregation between restarts is not allowed with the same checkpoint.
- `withWatermark` on a non-streaming Dataset is a no-op.

## Verify
- [ ] `query.lastProgress["stateOperators"][0]["numRowsTotal"]` plateaus rather than growing forever.
- [ ] `numRowsDroppedByWatermark` is near zero or matches the expected late-data rate.
- [ ] A replayed day reproduces the window counts of a batch recomputation, allowing for data later than the delay.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in the streaming guide (docs/streaming/apis-on-dataframes-and-datasets.md): watermark = max event time minus delay set at each trigger, the one-direction late-data guarantee, conditions for state cleanup, output-mode semantics (complete cannot drop state), session_window, multipleWatermarkPolicy (default min), restrictions on changing aggregation keys across restarts; numRowsDroppedByWatermark exists in progress.scala. Removed the Delta sink, the 3.2+ and idle-source claims, and unsourced lateness-percentile advice. The example sink now uses the built-in file sink.

Method: documentation only; no commands were run.
