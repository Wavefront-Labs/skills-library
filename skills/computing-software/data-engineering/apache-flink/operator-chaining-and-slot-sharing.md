---
id: computing-software.data-engineering.apache-flink.operator-chaining-and-slot-sharing
name: operator-chaining-and-slot-sharing
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, datastream-api, operator-chaining, slot-sharing, task-slots, parallelism, disablechaining, slotsharinggroup]
level: advanced
status: docs-checked
description: "Control how Flink operators map to tasks and slots: operator chaining, startNewChain/disableChaining, slot sharing groups, and sizing TaskManager slots for a job."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/operators/overview/#task-chaining-and-resource-groups
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/concepts/flink-architecture/#task-slots-and-resources
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/finegrained_resource/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator chaining and slot sharing

**Goal:** understand why a job needs N slots, and isolate or split operators when one hot operator starves others.

## Chaining
Flink by default chains operators where possible (for example consecutive `map`s with a 1-to-1 connection) into one **task** that runs in one thread. `keyBy()` and `rebalance()` require a network shuffle and break the chain.
```java
stream.map(new Parse())               // chained with source
      .filter(new Valid())
      .keyBy(e -> e.userId)           // chain break: network shuffle
      .process(new Sessionize())
      .name("sessionize").uid("sessionize");
```
Controls:
- `env.disableOperatorChaining()`: disables chaining for the whole job.
- `.startNewChain()`: begin a new chain, starting with this operator (`filter(...).map(...).startNewChain().map(...)` chains the two maps but not the filter to the first map).
- `.disableChaining()`: do not chain this operator.
Reasons to break a chain: isolate a CPU-heavy operator to see its own backpressure/busy metrics, or let a slow sink run in a separate thread.

## Slots and slot sharing
- Each TaskManager offers `taskmanager.numberOfTaskSlots` slots (default 1); each slot is a fixed subset of the TM's resources: a TM with three slots dedicates 1/3 of its managed memory to each. There is no CPU isolation between slots.
- By default subtasks of the same job may share a slot (slot sharing), so one slot can hold a whole pipeline and a cluster needs exactly as many slots as the highest parallelism used in the job, not the sum.
```java
heavyStream.process(new MlScoring()).slotSharingGroup("scoring").setParallelism(8);
```
Operations without the slot sharing group go into other slots, which isolates them; the group is inherited from input operations if they are all in the same group. Required slots then add up across groups (max parallelism in `default` plus max in `scoring`).

## Fine-grained resources (optional)
Slot sharing groups can declare a resource profile via `SlotSharingGroup.newBuilder("scoring").setCpuCores(2).setTaskHeapMemoryMB(2048)`; CPU cores and task heap memory must be positive, task off-heap can be 0. See the fine-grained resource management page for prerequisites and limitations.

## Sizing guidance
- One slot per TaskManager isolates task groups in separate JVMs; more slots share a JVM, TCP connections and heartbeats, reducing per-task overhead.
- Managed memory is divided evenly among slots, so fewer slots per TM gives each slot more (relevant for heavy RocksDB state).

## Gotchas
- Chained operators share one thread: a blocking call in a `map` stalls the source too. Use async I/O.
- Set `.uid()` on stateful operators so savepoints survive job graph changes.
- Web UI shows chained operators as one vertex; use `.name()` to keep it readable.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the DataStream operators overview (task chaining, `startNewChain`, `disableChaining`, `slotSharingGroup`), the Flink architecture page (task slots, managed memory split, slot sharing, slots needed equal highest parallelism), the DataStream execution mode page (`keyBy`/`rebalance` shuffles), the fine-grained resource management page and the generated configuration table (`taskmanager.numberOfTaskSlots` default 1). Removed unconfirmed sizing rules and the fine-grained configuration key.

Method: documentation only; no commands were run.

## Verify
- [ ] Web UI job graph shows the intended vertices and parallelism; required slots match available slots.
- [ ] Busy/backpressure metrics of the isolated operator explain the bottleneck.
