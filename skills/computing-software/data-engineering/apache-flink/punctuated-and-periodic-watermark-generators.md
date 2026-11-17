---
id: computing-software.data-engineering.apache-flink.punctuated-and-periodic-watermark-generators
name: punctuated-and-periodic-watermark-generators
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, punctuated-watermarks, periodic-watermarks, watermarkgenerator, watermarkstrategy, event-time]
level: advanced
status: docs-checked
description: "Write custom Flink WatermarkGenerators: periodic (autoWatermarkInterval) vs punctuated (per-event markers), heuristics beyond bounded out-of-orderness, and their pitfalls."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Periodic vs punctuated watermark generators

Built-ins (`forMonotonousTimestamps`, `forBoundedOutOfOrderness`) are periodic generators. Write your own when the stream itself tells you when time has advanced, or when a fixed bound is wrong.

## Interface
```java
public interface WatermarkGenerator<T> {
  void onEvent(T event, long eventTimestamp, WatermarkOutput output);  // every record
  void onPeriodicEmit(WatermarkOutput output);                         // every auto-watermark interval
}
```

## Periodic (track state in onEvent, emit on timer)
```java
public class LagAwareGenerator implements WatermarkGenerator<Event> {
  private long maxTs = Long.MIN_VALUE + 1; private final long bound = 5_000;
  public void onEvent(Event e, long ts, WatermarkOutput o) { maxTs = Math.max(maxTs, ts); }
  public void onPeriodicEmit(WatermarkOutput o) { o.emitWatermark(new Watermark(maxTs - bound - 1)); }
}
```
Tune `env.getConfig().setAutoWatermarkInterval(ms)`: it sets how often `onPeriodicEmit()` is called (a new watermark is emitted only if it is non-null and larger than the previous one).

## Punctuated (emit when a marker event arrives)
```java
public class MarkerGenerator implements WatermarkGenerator<Event> {
  public void onEvent(Event e, long ts, WatermarkOutput o) {
    if (e.isEndOfBatchMarker()) o.emitWatermark(new Watermark(e.batchCloseTime()));
  }
  public void onPeriodicEmit(WatermarkOutput o) {}
}
```
Use when upstream sends explicit "all data up to T delivered" markers (end-of-file records, heartbeat events from a CDC source, per-device clock ticks).
- Do not emit a watermark on every event; emit only when it advances meaningfully.

## Wiring
```java
WatermarkStrategy<Event> ws = WatermarkStrategy.<Event>forGenerator(ctx -> new MarkerGenerator())
    .withTimestampAssigner((e, ts) -> e.ts())
    .withIdleness(Duration.ofMinutes(1));
env.fromSource(source, ws, "src");
```
Pass the strategy to `fromSource` so it is applied in the source.

## Rules
- Watermarks must be monotonic: only a watermark larger than the previous one is emitted.
- A generator that only advances with data stalls when data stops: use idleness, or a periodic generator that falls back to processing time when no events for N seconds (accepting possible late data).

## Verify
- [ ] Flink UI > operator > Watermarks shows the watermark advancing per subtask.
- [ ] Late-record drops in window operators stay near zero.

## Checked
2026-10-31. Confirmed against the Flink stable Generating Watermarks page: `onPeriodicEmit` semantics and `ExecutionConfig.setAutoWatermarkInterval`, `withIdleness(Duration)`, the generator examples. Removed: the 200 ms default, the 0-disables claim, the per-split and Long.MAX_VALUE remarks, and the metric name (not confirmed on the fetched pages).
Method: documentation only; no commands were run.
