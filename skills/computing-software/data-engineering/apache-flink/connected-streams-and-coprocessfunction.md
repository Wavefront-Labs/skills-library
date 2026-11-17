---
id: computing-software.data-engineering.apache-flink.connected-streams-and-coprocessfunction
name: connected-streams-and-coprocessfunction
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, coprocessfunction, connected-streams, keyedcoprocessfunction, datastream-api, control-stream]
level: advanced
status: docs-checked
description: "Combine two Flink streams with connect() and a (Keyed)CoProcessFunction: shared keyed state, timers, buffering until the other side arrives, and dynamic rules."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/overview/#connect
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/process_function/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/event-time/generating_watermarks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connected streams and CoProcessFunction

`a.connect(b)` gives one operator that sees two inputs of different types, with **shared state**. Use it for custom joins (wait for both sides, any timeout logic), control streams (per-key on/off switches), or enrichment where the reference side updates.

## Keyed example: match order with payment, timeout after 1 h
```java
orders.keyBy(Order::id).connect(payments.keyBy(Payment::orderId))
  .process(new KeyedCoProcessFunction<String, Order, Payment, Matched>() {
    ValueState<Order> order; ValueState<Payment> payment;
    public void open(OpenContext ctx) {
      order = getRuntimeContext().getState(new ValueStateDescriptor<>("order", Order.class));
      payment = getRuntimeContext().getState(new ValueStateDescriptor<>("payment", Payment.class));
    }
    public void processElement1(Order o, Context ctx, Collector<Matched> out) throws Exception {
      Payment p = payment.value();
      if (p != null) { out.collect(new Matched(o, p)); payment.clear(); }
      else { order.update(o); ctx.timerService().registerEventTimeTimer(o.ts() + 3_600_000); }
    }
    public void processElement2(Payment p, Context ctx, Collector<Matched> out) throws Exception {
      Order o = order.value();
      if (o != null) { out.collect(new Matched(o, p)); order.clear(); }
      else { payment.update(p); ctx.timerService().registerEventTimeTimer(p.ts() + 3_600_000); }
    }
    public void onTimer(long ts, OnTimerContext ctx, Collector<Matched> out) throws Exception {
      if (order.value() != null) ctx.output(UNPAID, order.value());   // side output
      order.clear(); payment.clear();
    }
  });
```

## Rules
- Both inputs must be keyed **by the same key type and value** to share keyed state (`keyBy` on both, or `connect(...).keyBy(k1, k2)`).
- No ordering guarantee between the two inputs: either side may arrive first. Always buffer both ways.
- The operator's watermark is the **minimum** of both inputs. A quiet input stalls event-time timers: use `withIdleness` on its source, or processing-time timers.
- Always clear state or set state TTL, or unmatched keys accumulate forever.
- If one side is a small, slowly changing, all-keys config stream (rules), use broadcast state instead; connect with a keyed stream only works for per-key control.
- Timers require keyed streams: use `KeyedCoProcessFunction` on `keyBy` on both inputs.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the operators overview and ProcessFunction pages (connect shares state between streams, timers and keyed state only on keyed streams), the generating-watermarks page (two-input watermark is the minimum), the testing page (`KeyedTwoInputStreamOperatorTestHarness`) and the ConnectedStreams source. Removed the unconfirmed version gate for `open(OpenContext)` and the operator-state claim for non-keyed CoProcessFunction.

Method: documentation only; no commands were run.

## Verify
- [ ] Test with `KeyedTwoInputStreamOperatorTestHarness`: both arrival orders, timeout path.
- [ ] State size metrics flat over time.
