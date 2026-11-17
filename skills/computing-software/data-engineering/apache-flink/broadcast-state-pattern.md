---
id: computing-software.data-engineering.apache-flink.broadcast-state-pattern
name: broadcast-state-pattern
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, datastream-api, broadcast-state, keyedbroadcastprocessfunction, dynamic-rules, reference-data, mapstatedescriptor, connected-streams]
level: practitioner
status: docs-checked
description: "Use Flink broadcast state to push rules or reference data to every parallel task: KeyedBroadcastProcessFunction, deterministic updates, ordering caveats, state size and bootstrapping."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/fault-tolerance/broadcast_state/
  - https://flink.apache.org/2019/06/26/a-practical-guide-to-broadcast-state-in-apache-flink/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broadcast state pattern

**Goal:** apply dynamically changing rules, thresholds or small reference data to a high-volume keyed stream without restarting the job or calling an external service per event.

## 1. Wire it up
```java
MapStateDescriptor<String, Rule> RULES = new MapStateDescriptor<>("rules", Types.STRING, TypeInformation.of(Rule.class));

BroadcastStream<Rule> rules = env.fromSource(ruleSource, WatermarkStrategy.noWatermarks(), "rules")
                                 .broadcast(RULES);

DataStream<Alert> alerts = transactions
    .keyBy(t -> t.accountId)
    .connect(rules)
    .process(new RuleEvaluator());
```

## 2. The function
```java
class RuleEvaluator extends KeyedBroadcastProcessFunction<String, Txn, Rule, Alert> {
  @Override public void processBroadcastElement(Rule r, Context ctx, Collector<Alert> out) throws Exception {
    BroadcastState<String, Rule> s = ctx.getBroadcastState(RULES);
    if (r.deleted) s.remove(r.id); else s.put(r.id, r);
  }
  @Override public void processElement(Txn t, ReadOnlyContext ctx, Collector<Alert> out) throws Exception {
    for (Map.Entry<String, Rule> e : ctx.getBroadcastState(RULES).immutableEntries())
      if (e.getValue().matches(t)) out.collect(new Alert(t, e.getKey()));
  }
}
```
- Keyed side gets **read-only** access to broadcast state; only the broadcast side may modify it.
- `ctx.applyToKeyedState(desc, fn)` in `processBroadcastElement` applies a `KeyedStateFunction` to the state of all keys (e.g. reset counters); it is not supported in PyFlink. Timers can only be registered in `processElement`, not in `processBroadcastElement`.
- Non-keyed variant: `BroadcastProcessFunction` when the main stream isn't keyed.

## 3. Rules that keep it correct
- **Deterministic updates only.** Every parallel instance receives the same broadcast elements and must end in the same state — no randomness, wall-clock time, or instance-specific logic in `processBroadcastElement`.
- **No cross-stream ordering.** A transaction may be processed before or after a concurrent rule update, and order differs per instance. If events must wait for rules, buffer them in keyed state until the rule version they need has arrived.
- Broadcast state is kept in memory at runtime (the RocksDB state backend is not used for it), and every task checkpoints its own copy, so checkpointed size grows by the parallelism. Keep it small. Large reference data → keyed state partitioned by the join key (e.g. a CDC stream joined with `connect` on the same key).

## 4. Bootstrapping
On first start the rule stream may lag the main stream; events processed before rules arrive see an empty state. Options:
- Read the rule topic from earliest (compacted Kafka topic keyed by rule id) so all rules replay on start.
- Buffer main events in keyed state until a "rules loaded" marker arrives.
- Use the State Processor API to pre-load a savepoint with rules.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the broadcast state page: `KeyedBroadcastProcessFunction` and `BroadcastProcessFunction`, read-only versus read-write context, `immutableEntries()`, `applyToKeyedState`, deterministic-update rule, per-task ordering differences, in-memory broadcast state and per-task checkpointing. Removed unconfirmed size figures.

Method: documentation only; no commands were run.

## Verify
- [ ] Adding/removing a rule takes effect on all subtasks (test with parallelism > 1).
- [ ] Broadcast state size per task is small enough for task memory (checkpoint metrics).
- [ ] Job restart restores rules without waiting for new rule messages.
