---
id: computing-software.data-engineering.apache-kafka.producer-metrics-and-throughput-tuning
name: producer-metrics-and-throughput-tuning
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-producer, producer-metrics, throughput-tuning, record-queue-time, batch-size, jmx]
level: advanced
status: docs-checked
description: "Read Kafka producer metrics (batch size, queue time, request latency, retries, buffer exhaustion) and tune throughput systematically with kafka-producer-perf-test."
sources:
  - https://kafka.apache.org/40/operations/monitoring/
  - https://kafka.apache.org/40/configuration/producer-configs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Producer metrics and throughput tuning

## Metrics that matter (JMX `kafka.producer:type=producer-metrics,client-id=*`)
| Metric | Healthy reading / what it says |
|---|---|
| `record-send-rate`, `byte-rate` | throughput achieved |
| `batch-size-avg` vs `batch.size` | well below batch.size = batches sent before full (linger too low or low traffic) |
| `records-per-request-avg` | how much batching you get per request |
| `record-queue-time-avg/max` | time records wait in the accumulator; high = sender cannot keep up (network, broker, in-flight limit) |
| `request-latency-avg/max` | broker round-trip; rises with broker load or acks=all with slow followers |
| `record-retry-rate`, `record-error-rate` | non-zero = broker trouble, leader moves, timeouts |
| `buffer-available-bytes`, `bufferpool-wait-ratio`, `buffer-exhausted-rate` | producer blocked on full buffer (`max.block.ms` then TimeoutException) |
| `compression-rate-avg` | compressed/uncompressed ratio; ~1.0 means compression ineffective |
| `requests-in-flight` | at the `max.in.flight.requests.per.connection` cap = pipeline saturated |
Per-topic: `producer-topic-metrics` (`record-send-rate`, `compression-rate`). Per-broker node: `producer-node-metrics` (`request-latency-avg` shows one slow broker).
In code: `producer.metrics()`; librdkafka: `statistics.interval.ms` JSON.

## Tuning loop
Baseline with the perf tool against a test topic shaped like production:
```bash
kafka-producer-perf-test.sh --topic perf --num-records 5000000 --record-size 1024 --throughput -1 \
  --producer-props bootstrap.servers=$BS acks=all linger.ms=5 batch.size=65536 compression.type=lz4
```
Change one setting at a time:
1. Raise `linger.ms` and `batch.size` step by step: bigger batches, better compression, fewer requests (the `kafka-producer-perf-test.sh` values above are examples).
2. `compression.type=lz4` or `zstd`: less network/disk; check `compression-rate-avg`.
3. `buffer.memory` up if `bufferpool-wait-ratio` > 0 with spare network.
4. More partitions or more producer instances if a single partition leader is the bottleneck.
5. `acks=all` latency is bounded by the slowest ISR follower: check broker `RemoteTimeMs` for Produce requests before blaming the producer.
Keep `enable.idempotence=true` (default 3.0+); it allows up to 5 in-flight requests with ordering preserved.

## Verify
- [ ] Throughput target met at p99 `request-latency` within SLO.
- [ ] `record-error-rate` = 0 and `buffer-exhausted-rate` = 0 under peak load.

## Checked
2026-10-28. Confirmed in the Kafka 3.9 and 4.0 monitoring pages: `producer-metrics`, `producer-topic-metrics` and `producer-node-metrics` mbeans and the metrics named above (`batch-size-avg`, `records-per-request-avg`, `record-queue-time-avg`, `request-latency-avg`, `record-retry-rate`, `record-error-rate`, `buffer-available-bytes`, `bufferpool-wait-ratio`, `buffer-exhausted-rate`, `compression-rate-avg`, `requests-in-flight`), broker `RemoteTimeMs` for produce with acks=-1; producer-performance flags (`--num-records`, `--record-size`, `--throughput`, `--producer-props`, ProducerPerformance source 3.9); idempotence default and the 5 in-flight limit (producer config pages); librdkafka `statistics.interval.ms`. Removed: the suggested ranges for `linger.ms` and `batch.size`.
Method: documentation only; no commands were run.
