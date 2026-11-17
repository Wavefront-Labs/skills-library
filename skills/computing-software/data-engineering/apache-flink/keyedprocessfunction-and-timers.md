---
id: computing-software.data-engineering.apache-flink.keyedprocessfunction-and-timers
name: keyedprocessfunction-and-timers
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, datastream-api, keyedprocessfunction, flink-timers, keyed-state, valuestate, event-time-timers, state-cleanup, timeouts]
level: practitioner
status: docs-checked
description: "Write Flink KeyedProcessFunctions with keyed state and event/processing-time timers: timeouts, custom sessionisation, timer coalescing, cleanup and testing with harnesses."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/process_function/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/fault-tolerance/state/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/testing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KeyedProcessFunction and timers

**Goal:** per-key logic windows can't express — "alert if no payment within 15 minutes of an order", custom sessions, dedup with expiry — with bounded state.

## 1. Skeleton: order without payment timeout
```java
public class PaymentTimeout extends KeyedProcessFunction<String, Event, Alert> {
  private transient ValueState<Long> orderTs;      // when the order arrived
  private transient ValueState<Long> timerTs;      // registered timer, to delete later

  @Override public void open(OpenContext ctx) {
    orderTs = getRuntimeContext().getState(new ValueStateDescriptor<>("orderTs", Long.class));
    timerTs = getRuntimeContext().getState(new ValueStateDescriptor<>("timerTs", Long.class));
  }

  @Override public void processElement(Event e, Context ctx, Collector<Alert> out) throws Exception {
    if (e.type == Type.ORDER) {
      long t = e.eventTime + Duration.ofMinutes(15).toMillis();
      ctx.timerService().registerEventTimeTimer(t);
      orderTs.update(e.eventTime); timerTs.update(t);
    } else if (e.type == Type.PAYMENT && timerTs.value() != null) {
      ctx.timerService().deleteEventTimeTimer(timerTs.value());
      orderTs.clear(); timerTs.clear();
    }
  }

  @Override public void onTimer(long ts, OnTimerContext ctx, Collector<Alert> out) throws Exception {
    out.collect(new Alert(ctx.getCurrentKey(), orderTs.value()));
    orderTs.clear(); timerTs.clear();             // always clean up state
  }
}
events.keyBy(e -> e.orderId).process(new PaymentTimeout());
```

## 2. Timer facts
- Timers are per key and timestamp; the `TimerService` deduplicates them, so there is at most one timer per key and timestamp. Flink synchronizes `onTimer()` and `processElement()`, so no concurrent state modification.
- Event-time timers fire when the **watermark** passes the timestamp; processing-time timers fire on wall clock. Event time = deterministic replays; if a partition is idle and watermarks stall, event-time timers never fire — configure `withIdleness` on the watermark strategy.
- Timers are checkpointed with keyed state and restored on recovery (processing-time timers that should have fired during downtime fire immediately on restore).
- Inside `onTimer`, `ctx.timeDomain()` tells event vs processing time; `ctx.getCurrentKey()` gives the key.
- Timers are part of the checkpointed state, so large numbers of timers increase checkpointing time (with RocksDB, the timer store is chosen by `state.backend.rocksdb.timer-service.factory`: `ROCKSDB` default, or `HEAP`). **Coalesce**: reduce timer resolution so many events share one timer, e.g. to the next minute `long t = (ts / 60000 + 1) * 60000;`.

## 3. State hygiene
- Every code path that creates state must eventually clear it (timer or explicit clear) — otherwise state grows without bound.
- Add `StateTtlConfig` as a safety net for keys that go silent:
```java
ValueStateDescriptor<Long> d = new ValueStateDescriptor<>("orderTs", Long.class);
d.enableTimeToLive(StateTtlConfig.newBuilder(Duration.ofDays(1)).cleanupInRocksdbCompactFilter(1000, Duration.ofHours(1)).build());
```
- Prefer `MapState` over a `ValueState<Map>` for large per-key collections so single entries can be accessed without handling the whole map.
- Emit side outputs (`ctx.output(tag, value)`) for anomalies instead of separate jobs.

## 4. Test with harnesses
```java
KeyedOneInputStreamOperatorTestHarness<String, Event, Alert> h = ProcessFunctionTestHarnesses
    .forKeyedProcessFunction(new PaymentTimeout(), e -> e.orderId, Types.STRING);
h.processElement(order("o1", 1000L), 1000L);
h.processWatermark(1000L + 15 * 60_000L);
assertEquals(1, h.extractOutputValues().size());
```
Harnesses control watermarks and processing time precisely — test timeouts without sleeping.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the ProcessFunction page (timer deduplication per key and timestamp, timers checkpointed and restored, processing-time timers that were due fire immediately on restore, timer coalescing, `getCurrentKey()`), the state page (`StateTtlConfig`, `cleanupInRocksdbCompactFilter(queryTimeAfterNumEntries, periodicCompactionTime)`), the generated configuration tables (`state.backend.rocksdb.timer-service.factory`: ROCKSDB or HEAP) and the `ProcessFunctionTestHarnesses.forKeyedProcessFunction` source. Removed the version note and the RocksDB read-cost claim.

Method: documentation only; no commands were run.

## Verify
- [ ] Harness tests cover: payment before timeout (no alert), no payment (alert), late payment.
- [ ] Checkpointed state size for the operator stabilises under steady load.
- [ ] Idle sources don't block event-time timers (idleness configured).
