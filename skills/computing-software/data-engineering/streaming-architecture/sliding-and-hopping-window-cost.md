---
id: computing-software.data-engineering.streaming-architecture.sliding-and-hopping-window-cost
name: sliding-and-hopping-window-cost
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, hopping-window, sliding-window, window-state, pane-aggregation, performance, windowing]
level: advanced
status: draft
description: "Control the cost of sliding/hopping windows: size/slide amplification, pane-based pre-aggregation, cumulate windows, and alternatives like per-event sliding aggregates."
sources:
  - https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#hopping-time-windows
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#window-operations-on-event-time
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sliding and hopping window cost

A hopping window of size S that advances by slide H puts every event into **S/H windows**. A 1-hour window sliding every 1 minute = 60 windows per event: 60x the state updates and output records of a tumbling window.

## Engine behaviour
- **Flink DataStream** `SlidingEventTimeWindows.of(1h, 1m)`: each element is assigned to 60 windows, each with its own state (with an incremental `AggregateFunction`, 60 accumulator updates per event). Costly on RocksDB.
- **Flink SQL** `HOP(TABLE t, DESCRIPTOR(ts), INTERVAL '1' MINUTE, INTERVAL '1' HOUR)` window TVF aggregation uses **slicing**: it aggregates into non-overlapping slices of size gcd(size, slide) and merges slices when a window fires. Much cheaper; prefer SQL/TVF for hopping aggregates.
- **Kafka Streams** `TimeWindows.ofSizeAndGrace(1h, ...).advanceBy(1m)` (hopping): updates 60 windows per record. `SlidingWindows.ofTimeDifferenceAndGrace(...)` (2.7+) creates windows only where records exist (output changes per event, not per slide), often cheaper for sparse keys.
- **Spark** `window(ts, "1 hour", "1 minute")`: expands each row into 60 rows (an `Expand` node) before aggregation; state store holds 60 windows per key.

## Reduce the cost
1. **Bigger slide**: does the business really need minute-level updates of an hourly metric? 1h/5m is 12x instead of 60x.
2. **Pane/slice pre-aggregation** by hand: tumbling 1-minute aggregates, then a second stage computes the trailing 60 panes (ring buffer per key in a process function, or Flink SQL OVER window on the pane stream). Cost: 1 update per event + 60 merges per minute per key (independent of event rate).
3. **CUMULATE** windows (Flink SQL) when the need is "today so far, updated every minute": windows grow from a fixed start, one slice per step, no overlap amplification.
4. **OVER aggregation** for per-event trailing values: `SUM(x) OVER (PARTITION BY k ORDER BY ts RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW)` produces a value per event, not per slide; state = events in the last hour.
5. Approximate structures: exponential decay counters (one number per key) when exact window bounds are not required.

## Output volume
With final-only emission, one window closes per key per slide, so output = keys x (1/H): 60x a tumbling 1-hour window for a 1-minute slide. Emitting updates before close (early firing, Kafka Streams without suppress) multiplies that by the event rate across all S/H open windows. Use suppress/final emission to keep sinks sane.

## Verify
- [ ] State size and busy time compared between the hopping implementation and the pane-based alternative under production rates.
- [ ] Results identical (or within tolerance for approximations).
