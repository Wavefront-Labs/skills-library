---
id: computing-software.data-engineering.apache-flink.window-assigners-triggers-evictors
name: window-assigners-triggers-evictors
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, datastream-api, window-assigners, triggers, evictors, aggregatefunction, processwindowfunction, allowed-lateness, session-windows]
level: practitioner
status: docs-checked
description: "Build DataStream windows in Flink: tumbling, sliding, session and global assigners, incremental vs full window functions, custom triggers, evictors and their state cost."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink window assigners, triggers and evictors

**Goal:** windowed aggregations that emit at the right time and keep state small.

## 1. Assigners
```java
DataStream<Order> orders = env.fromSource(kafkaSource, watermarkStrategy, "orders");
orders.keyBy(o -> o.customerId)
      .window(TumblingEventTimeWindows.of(Duration.ofMinutes(5)))      // fixed, non-overlapping
//    .window(SlidingEventTimeWindows.of(Duration.ofHours(1), Duration.ofMinutes(5)))   // size, slide
//    .window(EventTimeSessionWindows.withGap(Duration.ofMinutes(30)))  // activity gaps
//    .window(GlobalWindows.create())                                  // needs a custom trigger
      .aggregate(new SumAmount(), new AddWindowInfo());
```
- Intervals are `java.time.Duration` values (`Duration.ofMinutes(x)` and so on) in the stable docs.
- Event-time assigners need a `WatermarkStrategy`; processing-time variants (`TumblingProcessingTimeWindows`) don't.
- Sliding windows duplicate each element into size/slide windows — a 1 h window sliding by 1 min keeps 60 copies of state.
- Offsets for time zones: `TumblingEventTimeWindows.of(Duration.ofDays(1), Duration.ofHours(-8))` for UTC-8 days.

## 2. Window functions: incremental first
| Function | State per window | Use |
|---|---|---|
| `reduce` / `aggregate` (`AggregateFunction`) | one accumulator | sums, counts, averages |
| `process` (`ProcessWindowFunction`) | **all elements** | needs all elements (median) or window metadata |
| `aggregate(agg, processWindowFn)` | one accumulator + metadata | the usual best of both |
```java
class SumAmount implements AggregateFunction<Order, Double, Double> {
  public Double createAccumulator() { return 0.0; }
  public Double add(Order o, Double acc) { return acc + o.amount; }
  public Double getResult(Double acc) { return acc; }
  public Double merge(Double a, Double b) { return a + b; }        // required for session windows
}
class AddWindowInfo extends ProcessWindowFunction<Double, Result, String, TimeWindow> {
  public void process(String key, Context ctx, Iterable<Double> sums, Collector<Result> out) {
    out.collect(new Result(key, ctx.window().getStart(), ctx.window().getEnd(), sums.iterator().next()));
  }
}
```

## 3. Lateness
```java
OutputTag<Order> late = new OutputTag<>("late") {};
SingleOutputStreamOperator<Result> res = orders.keyBy(...).window(...)
    .allowedLateness(Duration.ofMinutes(10))      // window state kept 10 min after watermark passes end
    .sideOutputLateData(late)
    .aggregate(...);
res.getSideOutput(late).sinkTo(lateSink);
```

## 4. Triggers
Each assigner comes with a default trigger; set `trigger(...)` to replace it.
- `CountTrigger.of(100)` — fire every 100 elements (replaces the default trigger, so combine logic if you still need end-of-window firing).
- `PurgingTrigger.of(t)` — clear window contents after firing.
- Custom `Trigger`: return `CONTINUE`, `FIRE`, `PURGE`, `FIRE_AND_PURGE` from `onElement`, `onEventTime`, `onProcessingTime`; clean timers in `clear()`.
`GlobalWindows` have no natural end, so they need a custom trigger.

## 5. Evictors
`CountEvictor.of(n)`, `TimeEvictor.of(d)`, `DeltaEvictor` remove elements before/after the window function. Using any evictor disables pre-aggregation: every element is buffered. Prefer a different window or a `KeyedProcessFunction` if state size matters.

## Verify
- [ ] Window results match a batch recomputation of the same input.
- [ ] Window state size (checkpoint size per operator) is stable, not growing.
- [ ] Late-data side output is monitored and its volume is small.

## Checked
2026-10-31. Confirmed against the Flink stable Windows page: assigner names and `Duration` intervals, day offset example, `allowedLateness` / `sideOutputLateData`, `merge` needed for session windows, `CountTrigger`, `PurgingTrigger`, `FIRE_AND_PURGE`, evictor classes, and that any evictor prevents pre-aggregation and adds state. Removed: `ContinuousEventTimeTrigger`, the Flink 1.x/2.x API split, replay non-determinism and late-firing upsert remarks (not confirmed on these pages).
Method: documentation only; no commands were run.
