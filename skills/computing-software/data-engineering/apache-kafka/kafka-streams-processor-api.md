---
id: computing-software.data-engineering.apache-kafka.kafka-streams-processor-api
name: kafka-streams-processor-api
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-streams, processor-api, punctuator, state-store, process-operator, wall-clock-time, custom-processor]
level: advanced
status: docs-checked
description: "Use the Kafka Streams Processor API (process(), state stores, punctuators) for logic the DSL cannot express: timeouts, custom dedup, TTL eviction, and mixing with the DSL."
sources:
  - https://kafka.apache.org/39/streams/developer-guide/processor-api/
  - https://kafka.apache.org/39/streams/developer-guide/dsl-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Streams Processor API

**Goal:** implement stateful per-record logic with timers (e.g. "emit if no payment within 30 min") while keeping Streams' fault-tolerant state and exactly-once semantics.

## Processor with a store and a punctuator
```java
public class PaymentTimeout implements Processor<String, Order, String, Alert> {
  private KeyValueStore<String, Order> pending;
  private ProcessorContext<String, Alert> ctx;

  @Override public void init(ProcessorContext<String, Alert> ctx) {
    this.ctx = ctx;
    this.pending = ctx.getStateStore("pending-orders");
    ctx.schedule(Duration.ofMinutes(1), PunctuationType.WALL_CLOCK_TIME, now -> {
      try (KeyValueIterator<String, Order> it = pending.all()) {
        while (it.hasNext()) {
          KeyValue<String, Order> kv = it.next();
          if (now - kv.value.createdAt() > Duration.ofMinutes(30).toMillis()) {
            ctx.forward(new Record<>(kv.key, new Alert(kv.key, "unpaid"), now));
            pending.delete(kv.key);
          }
        }
      }
    });
  }
  @Override public void process(Record<String, Order> rec) {
    if (rec.value().paid()) pending.delete(rec.key()); else pending.put(rec.key(), rec.value());
  }
}
```

## Wiring into the DSL
```java
StoreBuilder<KeyValueStore<String, Order>> store = Stores.keyValueStoreBuilder(
    Stores.persistentKeyValueStore("pending-orders"), Serdes.String(), orderSerde);
builder.addStateStore(store);
builder.stream("orders", Consumed.with(Serdes.String(), orderSerde))
       .process(PaymentTimeout::new, "pending-orders");
```
The Kafka 3.9 DSL page documents `KStream#process()` as a terminal operation (`KStream -> void`) and says a store already added with `addStateStore()` is connected by passing its name to `process()`. Its `transform()` entry is `KStream -> KStream`. Check the javadoc of your Kafka version for a `process` variant that returns a `KStream` before chaining `.to(...)` after it, and for `processValues`.

## Punctuation types
- `STREAM_TIME`: advances only when records arrive (event-time based). No input -> no firing. Good for deterministic replay.
- `WALL_CLOCK_TIME`: fires on system time even with no input. Needed for timeouts, but replay gives different results.

## Practical rules
- A punctuator that iterates `pending.all()` scans the whole store on every run; for big stores keep a secondary index keyed by time and range-scan only expired entries.
- Fault-tolerant stores are backed by a compacted changelog topic; `withLoggingDisabled()` removes that fault tolerance.
- Never block in `process()` (no remote calls).

## Checked
2026-10-28. Confirmed on the Kafka 3.9 Processor API and DSL pages: `Processor`/`Record<K, V>`, `ProcessorContext#schedule()`, `forward()`, `getStateStore()`, `PunctuationType.STREAM_TIME` and `WALL_CLOCK_TIME` semantics, `addStateStore()`, `KStream#process()` taking a store name, compacted changelog and `withLoggingDisabled()`. Removed: the claim that `process()` returns a `KStream` since 3.3 (the 3.9 page says terminal), `processValues` advice, the partition-local and `advanceWallClockTime` and `estimate-num-keys` details.
Method: documentation only; no commands were run.

## Verify
- [ ] A topology test advances wall-clock time and asserts the alert.
- [ ] Store size stays bounded in production.
