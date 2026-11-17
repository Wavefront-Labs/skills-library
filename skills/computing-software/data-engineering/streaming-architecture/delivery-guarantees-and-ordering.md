---
id: computing-software.data-engineering.streaming-architecture.delivery-guarantees-and-ordering
name: delivery-guarantees-and-ordering
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, stream-processing, delivery-semantics, at-most-once, at-least-once, exactly-once, effectively-once, end-to-end-exactly-once, idempotent-sink, deduplication, transactional-outbox, message-ordering, partition-key, backpressure, stream-table-duality, changelog, lambda-architecture, kappa-architecture, kafka, flink, kafka-streams, spark-structured-streaming, event-driven]
level: advanced
status: draft
description: "Choose and achieve delivery guarantees end to end: at-most/at-least/exactly-once, idempotent sinks, key-based ordering, backpressure, stream-table duality and lambda vs kappa."
sources:
  - https://kafka.apache.org/documentation/#semantics
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
  - https://kafka.apache.org/documentation/streams/core-concepts
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Delivery guarantees and ordering — what "exactly-once" really costs

**Goal:** state precisely which guarantee each hop of a streaming system provides, and design the system so the end-to-end result is correct even when components fail and retry.

## 1. The three semantics
- **At-most-once:** commit position, then process. A crash loses messages. Acceptable for metrics sampling, never for money.
- **At-least-once:** process, then commit. A crash replays messages → duplicates. The default for almost every system.
- **Exactly-once (effectively-once):** each input affects the result once. In practice this is at-least-once delivery **plus** deduplication or atomic commit of output together with input position. Messages may be *processed* more than once; their *effects* are not duplicated.

## 2. Engine guarantees are not end-to-end guarantees
A framework's "exactly-once" usually means its internal state:
- **Flink:** checkpoints snapshot state + source offsets consistently. Output is exactly-once only with a two-phase-commit sink (Kafka transactional sink) or an idempotent sink.
- **Kafka Streams:** `processing.guarantee=exactly_once_v2` atomically commits outputs, state changelogs and input offsets in one Kafka transaction — exactly-once only for Kafka-to-Kafka.
- **Spark Structured Streaming:** checkpointed offsets + replayable sources + idempotent or transactional sinks (e.g. Delta) give exactly-once; `foreachBatch` is at-least-once unless you dedupe by `batchId`.
The chain is only as strong as its weakest hop. An HTTP call to a third-party API inside the job is at-least-once no matter what the engine says.

## 3. Make sinks idempotent (the cheapest exactly-once)
- **Upsert by deterministic key:** write with a key derived from the event (`event_id`, or `source_partition + offset`). Replays overwrite the same row.
- **Dedupe table / state:** store processed IDs with a TTL bounded by the maximum replay window.
- **Transactional write of output + offset:** store the consumer offset in the same database transaction as the result; on restart, resume from the stored offset.
- **Transactional outbox** on the producing service: write the business change and the outgoing event in the same DB transaction, and relay the outbox via CDC — avoids the "DB committed but event lost" dual-write bug.
**Gotcha:** generating IDs at processing time (`uuid()` in the job) defeats dedupe — the replay gets a new ID. IDs must come from the source event.

## 4. Ordering
- Global ordering doesn't scale; design for **per-key ordering**. Partition by the entity key so all its events go through one partition and one task (see computing-software.data-engineering.apache-kafka.topic-partition-and-consumer-design).
- Things that break ordering: retries with multiple in-flight requests on non-idempotent producers; repartitioning by a different key; async I/O in unordered mode; parallel consumers within one partition; changing partition counts.
- When order can't be guaranteed in transport, carry a version or sequence number and apply "last writer by version wins" at the sink.
- Event time vs processing time: ordering by arrival is not ordering by occurrence; use watermarks for event-time logic (computing-software.data-engineering.apache-flink.event-time-watermarks-and-checkpoints).

## 5. Backpressure
When a sink is slower than the source, a pull-based system (Kafka consumers, Flink credit-based flow control) slows reading and lag grows; push-based systems buffer and then drop or OOM.
- Monitor consumer lag (time, not just count) and Flink backpressure/busy ratios.
- Fix the bottleneck operator (batch sink writes, raise parallelism up to partition count, async I/O) before adding buffers.
- Decide in advance: under sustained overload, do you lag, shed load, or sample? Write it down.

## 6. Stream–table duality
A table is the latest value per key of a changelog stream; a stream is the sequence of changes to a table. Compacted Kafka topics, CDC streams and KTables are the same idea. Use it to: rebuild a table by replaying the changelog; emit updates (retractions/upserts) rather than appends for aggregations that change.

## 7. Lambda vs Kappa
- **Lambda:** batch layer recomputes truth, speed layer gives low-latency approximations; two codebases that drift apart.
- **Kappa:** one streaming codebase; reprocess by replaying the log from the start into a new version of the output, then switch readers. Requires long log retention (or tiered storage) and replayable, deterministic logic.
Most modern stacks are Kappa-like with a lakehouse table as the sink; keep a batch backfill path for history beyond log retention.

## Verify
- [ ] Each hop (source → engine → sink) has its guarantee written in the design doc.
- [ ] Killing the processing job mid-stream and restarting produces no duplicate or missing rows in the sink (checked by key counts).
- [ ] Event IDs used for dedupe originate at the source, not in the processing job.
- [ ] Per-key ordering is tested by replaying a shuffled sequence with version numbers.
- [ ] Consumer lag alert exists, expressed in seconds/minutes behind.
