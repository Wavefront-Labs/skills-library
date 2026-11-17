---
id: computing-software.data-engineering.etl-pipeline-design.testing-streaming-jobs
name: testing-streaming-jobs
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, streaming-tests, structured-streaming, testing, event-time]
level: advanced
status: draft
description: "Test streaming pipelines: unit-testing transformations as batch, memory sources and sinks, controlled triggers, event-time and late data cases, and replay tests."
sources:
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/testing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing streaming jobs

**Goal:** confidence that streaming logic handles ordering, late data, duplicates and restarts before it runs in production.

## Layer 1: pure transformation tests
Factor logic into functions on DataFrames/streams and test them with **batch** inputs:
```python
def enrich(df):
    return df.withColumn("amount_eur", F.col("amount") * F.col("fx"))

def test_enrich(spark):
    out = enrich(spark.createDataFrame([(10.0, 0.5)], ["amount", "fx"])).collect()
    assert out[0].amount_eur == 5.0
```

## Layer 2: streaming semantics with controlled input
Spark Structured Streaming:
```python
from pyspark.sql.streaming import StreamingQuery
src = spark.readStream.format("rate").load()  # or files written by the test to a temp dir
q = (agg(src).writeStream.format("memory").queryName("out").outputMode("update")
     .option("checkpointLocation", tmp_chk).trigger(availableNow=True).start())
q.awaitTermination()
rows = spark.table("out").collect()
```
- Write test input files in steps (batch 1, run, batch 2, run) to simulate arrival order.
- Include events older than the watermark: assert they are dropped (or routed) as designed.
- Duplicates within/between batches with `dropDuplicatesWithinWatermark`.

Flink: `MiniClusterWithClientResource` for integration tests; operator test harnesses (`KeyedOneInputStreamOperatorTestHarness`) to push elements and watermarks and inspect state/timers.

## Layer 3: restart and replay
- Stop the query mid-stream, restart from the same checkpoint: output has no duplicates or gaps (exactly-once sink or idempotent MERGE).
- Change code compatibly and restart from the old checkpoint (state schema compatibility).
- Replay a recorded production sample (from Kafka topic or files) and compare with expected outputs.

## Kafka integration
Testcontainers Kafka (or Redpanda) in CI: produce known messages, run the job with `availableNow`, assert sink contents.

## Verify
CI runs all three layers; a change to watermark handling breaks the late-data test.
