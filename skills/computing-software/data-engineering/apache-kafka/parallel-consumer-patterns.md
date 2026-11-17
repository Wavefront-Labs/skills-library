---
id: computing-software.data-engineering.apache-kafka.parallel-consumer-patterns
name: parallel-consumer-patterns
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-consumer, parallel-consumer, multi-threaded-consumer, key-ordering, confluent-parallel-consumer]
level: advanced
status: docs-checked
description: "Process Kafka records concurrently beyond one thread per partition: thread-per-consumer, worker pools with per-key ordering, and Confluent Parallel Consumer, with safe commits."
sources:
  - https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html
  - https://github.com/confluentinc/parallel-consumer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-threaded and parallel consumer patterns

`KafkaConsumer` is **not thread-safe** (only `wakeup()` may be called from another thread). Parallelism is capped by partition count unless you process records concurrently yourself.

## Pattern 1: one consumer per thread
N threads, each with its own `KafkaConsumer` in the same group. Simple, ordering per partition kept, scales up to the partition count. Default choice.

## Pattern 2: one poller, worker pool
Poll in one thread, hand records to workers. Needed when per-record work is slow (HTTP calls) and partitions are few.
Rules:
- **Ordering**: route by key hash to a fixed worker (`workers[hash(key) % n]`) to keep per-key order; a plain pool reorders.
- **Commits**: only commit offset X+1 for a partition when **all** records <= X on that partition are done. Track per-partition completed offsets (a sorted set) and commit the highest contiguous one.
- **Backpressure**: when worker queues fill, `consumer.pause(partitions)` and keep calling `poll()` (heartbeats and `max.poll.interval.ms` are satisfied), then `resume()`.
- **Rebalance**: in `onPartitionsRevoked`, wait for in-flight work on those partitions (or discard it), commit, then return; otherwise the new owner reprocesses or you commit offsets you no longer own.

## Pattern 3: Confluent Parallel Consumer (library)
```java
var options = ParallelConsumerOptions.<String, String>builder()
    .ordering(ParallelConsumerOptions.ProcessingOrder.KEY)   // KEY, PARTITION or UNORDERED
    .maxConcurrency(200)
    .consumer(kafkaConsumer)
    .commitMode(ParallelConsumerOptions.CommitMode.PERIODIC_CONSUMER_ASYNCHRONOUS)
    .build();
var pc = ParallelStreamProcessor.createEosStreamProcessor(options);
pc.subscribe(List.of("orders"));
pc.poll(ctx -> callApi(ctx.getSingleConsumerRecord()));
```
It tracks per-record completion and encodes incomplete offsets in commit metadata, so a restart does not reprocess completed records beyond the gap. Concurrency can far exceed partition count with `KEY` ordering.

## Choosing
- CPU-bound, enough partitions: Pattern 1.
- I/O-bound, few partitions, per-key order needed: Parallel Consumer (Java) or Pattern 2 with key routing.
- Increasing partitions is often simpler than any of this, if consumers of that topic can tolerate the key remap.

## Verify
- [ ] Kill a worker mid-batch: no record skipped (offset not committed past unfinished work).
- [ ] Per-key ordering test: sequence numbers per key arrive in order at the sink.

## Checked
2026-11-09. Confirmed in the KafkaConsumer 3.9 javadoc (not thread-safe, `wakeup()` the only exception, one consumer per thread, decoupling consumption and processing, `pause`/`resume`) and the Parallel Consumer README (`createEosStreamProcessor`, `ProcessingOrder.KEY`, `maxConcurrency`, `PERIODIC_CONSUMER_ASYNCHRONOUS`, `getSingleConsumerRecord`, offset map stored in commit metadata). `callApi` and the worker-routing expression are illustrative code, not API claims.
Method: documentation only; no commands were run.
