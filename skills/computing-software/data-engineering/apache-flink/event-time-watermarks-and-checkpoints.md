---
id: computing-software.data-engineering.apache-flink.event-time-watermarks-and-checkpoints
name: event-time-watermarks-and-checkpoints
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, event-time, watermarks, watermarkstrategy, bounded-out-of-orderness, idleness, allowed-lateness, side-outputs, late-data, windows, checkpoints, savepoints, rocksdb, state-backend, exactly-once, two-phase-commit, kafka-sink, state-ttl, stream-processing, flink-sql, datastream-api]
level: advanced
status: docs-checked
description: "Make Flink jobs correct and recoverable: event-time watermarks with idleness, allowed lateness and side outputs, RocksDB state with TTL, checkpoint tuning, exactly-once sinks and savepoints."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/concepts/time/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/event-time/generating_watermarks/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/fault-tolerance/checkpointing/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/savepoints/
  - https://github.com/apache/flink-connector-kafka/blob/main/docs/content/docs/connectors/datastream/kafka.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink event time, watermarks and checkpoints — correct results that survive failure

**Goal:** windowed results that reflect when events happened (not when they arrived), with late data handled deliberately, and state that recovers exactly-once after a crash or upgrade.

## 1. Assign timestamps and watermarks at the source
```java
WatermarkStrategy<Order> wm = WatermarkStrategy
    .<Order>forBoundedOutOfOrderness(Duration.ofSeconds(30))
    .withTimestampAssigner((o, ts) -> o.getEventTimeMillis())
    .withIdleness(Duration.ofMinutes(1));

DataStream<Order> orders = env.fromSource(kafkaSource, wm, "orders");
```
- A watermark `W` asserts "no more events with timestamp ≤ W expected". Bounded out-of-orderness sets `W = max_seen − bound − 1 ms`.
- Choose the bound from measured disorder. Too small → many events are late and ignored for their window by default; too large → results are delayed by that much.
- Apply the strategy **in the source** (`fromSource`) so watermarks are generated per Kafka partition; assigning later merges partitions and loses that precision.
- **Gotcha — idle partitions stall everything:** an operator's watermark is the minimum of its inputs. One empty Kafka partition holds the whole job's event time back and windows never fire. `withIdleness` marks such inputs idle after the timeout.
- Also set source parallelism ≤ partition count; extra subtasks with no partitions are idle too.

## 2. Late data: allowed lateness and side outputs
```java
OutputTag<Order> late = new OutputTag<Order>("late") {};
SingleOutputStreamOperator<Agg> result = orders
    .keyBy(Order::getCustomerId)
    .window(TumblingEventTimeWindows.of(Duration.ofMinutes(5)))
    .allowedLateness(Duration.ofMinutes(10))
    .sideOutputLateData(late)
    .aggregate(new SumAgg());
result.getSideOutput(late).sinkTo(lateSink);
```
- Within allowed lateness, a late event re-fires the window with an **updated** result — downstream must upsert, not append.
- Beyond it, the event goes to the side output (or is silently dropped if you didn't add one). Always add one and count it.
- In Flink SQL, the equivalent is `WATERMARK FOR ts AS ts - INTERVAL '30' SECOND` in the DDL; late rows past the watermark are dropped by window TVFs.

## 3. State backend and TTL
- Use RocksDB (`state.backend.type: rocksdb`; the default is `hashmap`) for state larger than heap; enable incremental checkpoints with `execution.checkpointing.incremental: true` (default false).
- Unbounded keyed state (per-user maps, dedupe sets) grows forever. Add TTL:
```java
StateTtlConfig ttl = StateTtlConfig.newBuilder(Duration.ofDays(7))
    .setUpdateType(StateTtlConfig.UpdateType.OnCreateAndWrite)
    .cleanupInRocksdbCompactFilter(1000).build();
descriptor.enableTimeToLive(ttl);
```
For SQL jobs: `table.exec.state.ttl`.

## 4. Checkpoints
```java
env.enableCheckpointing(60_000, CheckpointingMode.EXACTLY_ONCE);
CheckpointConfig c = env.getCheckpointConfig();
c.setMinPauseBetweenCheckpoints(30_000);
c.setCheckpointTimeout(600_000);
c.setTolerableCheckpointFailureNumber(3);
c.setExternalizedCheckpointRetention(ExternalizedCheckpointRetention.RETAIN_ON_CANCELLATION);
```
- Interval trade-off: shorter = less replay after failure and lower end-to-end latency for transactional sinks; longer = less overhead.
- Checkpoints stall under backpressure because barriers queue behind data; unaligned checkpoints (`enableUnalignedCheckpoints()`) help but increase checkpoint size.
- Durable storage only: `execution.checkpointing.dir: s3://<BUCKET>/checkpoints`.

## 5. End-to-end exactly-once
Flink's checkpoints make *state* exactly-once. The output is exactly-once only with a transactional or idempotent sink:
- `KafkaSink` with `DeliveryGuarantee.EXACTLY_ONCE` and a `setTransactionalIdPrefix(...)` — two-phase commit tied to checkpoints. Output becomes visible only at checkpoint completion, so latency ≥ checkpoint interval.
- **Gotcha:** set the producer's Kafka `transaction.timeout.ms` above the maximum checkpoint duration plus the maximum restart duration, or pending transactions time out and data is lost.
- Downstream consumers must read only committed data (`isolation.level=read_committed`) to avoid duplicates.
See computing-software.data-engineering.streaming-architecture.delivery-guarantees-and-ordering.

## 6. Savepoints for upgrades
- Set stable `uid("...")` on every stateful operator; without uids, changing the job graph makes state unrestorable.
- `flink stop --savepointPath s3://<BUCKET>/savepoints <JOB_ID>` then `flink run -s <SAVEPOINT_PATH> job.jar`. Use `--allowNonRestoredState` (short `-n`) only when you deliberately removed an operator.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the event-time, windows, state (TTL), checkpointing, savepoints and CLI pages, the `BoundedOutOfOrdernessWatermarks` source (`W = maxTimestamp - bound - 1`), the generated configuration tables (`state.backend.type` default `hashmap`, `execution.checkpointing.dir|incremental`) and the Kafka connector page (`DeliveryGuarantee.EXACTLY_ONCE`, `setTransactionalIdPrefix`, `transaction.timeout.ms`, `isolation.level`). Replaced removed 1.x key names and the broker `transaction.max.timeout.ms` claim; removed unconfirmed typical intervals.

Method: documentation only; no commands were run.

## Verify
- [ ] Watermark per source subtask is advancing (Web UI or `currentInputWatermark`); none stuck.
- [ ] Late-event side output exists and its count is monitored.
- [ ] Checkpoints complete consistently; failures alerted.
- [ ] Killing a TaskManager mid-run yields no duplicate rows in the read_committed sink output.
- [ ] Every stateful operator has a `uid`, and a stop-with-savepoint → restore cycle succeeds.
- [ ] Keyed state size plateaus over days instead of growing linearly.
