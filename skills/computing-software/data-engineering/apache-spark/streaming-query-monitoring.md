---
id: computing-software.data-engineering.apache-spark.streaming-query-monitoring
name: streaming-query-monitoring
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, structured-streaming, streaming-query-listener, streaming-progress-metrics, lastprogress, input-rate, processing-rate, batch-duration, kafka-offset-lag, streaming-ui, observability]
level: advanced
status: docs-checked
description: "Monitor Structured Streaming queries: lastProgress fields, StreamingQueryListener to push metrics, falling-behind signals (input vs processed rate, batch duration), and alerting."
sources:
  - https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.StreamingQueryListener.html
  - https://spark.apache.org/docs/latest/web-ui.html#structured-streaming-tab
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring Structured Streaming queries

**Goal:** know within minutes when a streaming query is falling behind, stuck, or growing state.

## The progress object
```python
p = query.lastProgress            # dict for the last trigger; query.recentProgress = last few progresses
p["batchId"], p["numInputRows"]
p["inputRowsPerSecond"], p["processedRowsPerSecond"]
p["durationMs"]["triggerExecution"]
p["eventTime"]["watermark"]
p["stateOperators"]   # list; empty for stateless queries
p["sources"][0]["startOffset"], ["endOffset"]
query.status          # what the query is doing right now (isTriggerActive, isDataAvailable)
```

## Falling-behind signals
- `processedRowsPerSecond < inputRowsPerSecond` for many consecutive batches.
- `triggerExecution` duration > trigger interval (batches queue up).
- Source offsets (`endOffset`) falling behind the topic's latest offsets.
- State growing without bound -> missing watermark/timeout.
- No progress events at all for N intervals -> query hung or dead (`query.isActive`, `query.exception()`).

## Push metrics with a listener
```python
from pyspark.sql.streaming import StreamingQueryListener

class Metrics(StreamingQueryListener):
    def onQueryStarted(self, e): log.info("started %s %s", e.name, e.id)
    def onQueryProgress(self, e):
        p = e.progress
        statsd.gauge(f"stream.{p.name}.input_rps", p.inputRowsPerSecond)
        statsd.gauge(f"stream.{p.name}.processed_rps", p.processedRowsPerSecond)
        statsd.gauge(f"stream.{p.name}.batch_ms", p.durationMs.get("triggerExecution", 0))
    def onQueryIdle(self, e): pass
    def onQueryTerminated(self, e):
        if e.exception: alert(f"stream {e.id} died: {e.exception[:500]}")

spark.streams.addListener(Metrics())
```
Alternatively set `spark.sql.streaming.metricsEnabled=true` (it must be set explicitly): queries started afterwards report Dropwizard metrics to the configured sinks (e.g. Ganglia, Graphite, JMX).

Name every query (`.queryName("orders_silver")`) so metrics and UI rows are identifiable.

## Keep the driver alive
`query.awaitTermination()` in jobs; on termination with exception, exit non-zero so the scheduler (Databricks job, K8s) restarts it. Use `spark.streams.awaitAnyTermination()` when several queries share a driver.

## Verify
- [ ] Dashboard shows input vs processed rate and batch duration per named query.
- [ ] Alert fires when the query falls behind or makes no progress (test by pausing the sink).
- [ ] Killing the query produces a termination alert with the exception text.

## Checked

2026-11-01. Confirmed against the Spark Structured Streaming monitoring section (`lastProgress`, `recentProgress`, `status`, sample fields `inputRowsPerSecond`, `processedRowsPerSecond`, `durationMs.triggerExecution`, `eventTime.watermark`, `stateOperators`, `sources` offsets, `spark.sql.streaming.metricsEnabled` and Dropwizard sinks, `awaitAnyTermination`) and the StreamingQueryListener API page (`onQueryIdle`). Removed: Kafka lag metric names, state metric names, version gates, UI tab description, alert thresholds.

Method: documentation only; no commands were run.
