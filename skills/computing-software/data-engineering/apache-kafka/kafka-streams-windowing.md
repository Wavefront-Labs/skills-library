---
id: computing-software.data-engineering.apache-kafka.kafka-streams-windowing
name: kafka-streams-windowing
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-streams, kafka-streams-windowing, grace-period, timewindows, slidingwindows, sessionwindows, suppress, suppress-operator, emit-strategy, timestamp-extractor, stream-time]
level: advanced
status: docs-checked
description: "Window aggregations in Kafka Streams: tumbling/hopping/sliding/session windows, grace and stream time, suppress or EmitStrategy for final results, timestamp extractors."
sources:
  - https://kafka.apache.org/39/streams/developer-guide/dsl-api/
  - https://kafka.apache.org/39/streams/core-concepts/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Windowing in Kafka Streams

**Goal:** count/aggregate by event-time windows, accept a bounded amount of late data, and emit final results only once when needed.

## Windows
```java
Duration size = Duration.ofMinutes(5), grace = Duration.ofMinutes(2);
TimeWindows tumbling = TimeWindows.ofSizeAndGrace(size, grace);
TimeWindows hopping  = TimeWindows.ofSizeAndGrace(Duration.ofMinutes(10), grace).advanceBy(Duration.ofMinutes(5));
SlidingWindows sliding = SlidingWindows.ofTimeDifferenceAndGrace(Duration.ofMinutes(10), grace);
SessionWindows sessions = SessionWindows.ofInactivityGapWithNoGrace(Duration.ofMinutes(30));

KTable<Windowed<String>, Long> counts = clicks
    .groupByKey()
    .windowedBy(tumbling)
    .count(Materialized.as("clicks-5m"));
```
Use `ofSizeWithNoGrace` or `ofSizeAndGrace` to state the grace period explicitly.

## Time semantics
- Record time comes from the `TimestampExtractor` (default: record timestamp set by producer/broker). Use a custom extractor to read an event-time field from the payload.
- **Stream time** = max timestamp seen per task (partition group). It only advances when new records arrive.
- A window closes when stream time > window end + grace; later records for it are discarded.

## Getting final results
Default: every update emits a new result downstream (count goes 1, 2, 3... per window). For "one row per window":
```java
counts.suppress(Suppressed.untilWindowCloses(unbounded()))
```
`unbounded()` is `Suppressed.BufferConfig.unbounded()`; check the javadoc of your version for bounded buffers and for any newer way to emit on window close.
Because stream time advances only with new data, the last window of a quiet partition is not emitted until more records arrive on that partition. Low-traffic topics need heartbeat/punctuation records if timely closure matters.

## Downstream
To write windowed results to a topic with a plain key, map the `Windowed` key first:
```java
counts.toStream().map((wk, v) -> KeyValue.pair(wk.key() + "@" + wk.window().startTime(), v)).to("page-clicks-5m");
```

## Gotchas
- Grace too short -> many late drops; too long -> more state and later final results.
- A custom `TimestampExtractor` gives the stream time its meaning (event time from a payload field, or wall-clock for processing time).

## Checked
2026-10-28. Confirmed on the Kafka 3.9 Streams pages: `TimeWindows.ofSizeAndGrace`/`ofSizeWithNoGrace` with `advanceBy`, `SlidingWindows.ofTimeDifferenceAndGrace`, `SessionWindows.ofInactivityGapWithNoGrace`, `Suppressed.untilWindowCloses(unbounded())`, stream time advancing only when records arrive, records discarded after window end plus grace, `TimestampExtractor` semantics, `Materialized.as`. Removed: `ofInactivityGapAndGrace`, `EmitStrategy`, `Grouped.as`, the old 24-hour default grace, `dropped-records` for late data, retention and repartition-timestamp claims, which the fetched pages do not state.
Method: documentation only; no commands were run.

## Verify
- [ ] Topology test with out-of-order records: within-grace late record updates the window; beyond-grace record is dropped and counted.
- [ ] With suppression, exactly one output record per key per window.
