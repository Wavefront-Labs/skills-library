---
id: computing-software.data-engineering.streaming-architecture.late-data-policies
name: late-data-policies
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, late-data-policy, allowed-lateness, side-outputs, watermarks, retractions, corrections, windowing]
level: advanced
status: draft
description: "Choose what a stream processor does with events behind the watermark: drop, side-output for batch correction, or update results, in Flink, Spark and Kafka Streams."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/#allowed-lateness
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#handling-late-data-and-watermarking
  - https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#windowing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Late data policies

**Goal:** a written decision for each streaming output about late events, balancing latency, completeness and state cost.

## The three options
| Policy | Behaviour | Cost | Fits |
|---|---|---|---|
| **Drop** | events behind watermark (+lateness) ignored | lowest state | monitoring, approximate dashboards |
| **Side output / dead-letter** | late events routed elsewhere; batch job corrects later | low state, extra batch path | finance, billing (must be complete) |
| **Update (allowed lateness)** | window state kept longer; late events re-fire windows, emitting corrected results | state for lateness horizon; downstream must handle updates | operational metrics, near-real-time with corrections |

Measure first: distribution of `processing_time - event_time` (p99, p99.9) tells you the watermark delay and lateness horizon.

## Flink
```java
OutputTag<Event> late = new OutputTag<>("late"){};
SingleOutputStreamOperator<Agg> agg = events
  .keyBy(e -> e.key)
  .window(TumblingEventTimeWindows.of(Duration.ofMinutes(5)))
  .allowedLateness(Duration.ofMinutes(30))     // re-fire on late events within 30 min
  .sideOutputLateData(late)                     // later than that -> side output
  .aggregate(new SumAgg());
agg.getSideOutput(late).sinkTo(lateSink);
```
Re-fired windows emit additional results for the same window: the sink must upsert by (key, window).

## Spark Structured Streaming
```python
(events.withWatermark("event_time", "30 minutes")
  .groupBy(F.window("event_time", "5 minutes"), "key").agg(F.sum("amount"))
  .writeStream.outputMode("update")      # emits changed windows; "append" emits only finalised windows
  ...)
```
Records older than the watermark are dropped (count in `numRowsDroppedByWatermark` in query progress). No built-in side output: to keep them, land raw events separately and correct in batch.

## Kafka Streams
```java
.windowedBy(TimeWindows.ofSizeAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(30)))
.count()
.suppress(Suppressed.untilWindowCloses(Suppressed.BufferConfig.unbounded()))   // emit once, after grace
```
Without suppress, each update is emitted (update policy); records after grace are dropped (`dropped-records` metric).

## Downstream implications
- Update policy: consumers must handle multiple versions per window (upsert sinks, compacted topics, or retractions).
- Drop policy: publish the expected completeness ("data for a window is final 10 min after window end; ~0.1% late events excluded").
- Side output: build the reconciliation job and a restatement process.

## Verify
- [ ] Lateness distribution measured and policy documented per output.
- [ ] Metrics for dropped/late records alert when above baseline.
