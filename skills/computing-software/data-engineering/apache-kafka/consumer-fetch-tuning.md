---
id: computing-software.data-engineering.apache-kafka.consumer-fetch-tuning
name: consumer-fetch-tuning
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-consumer, fetch-min-bytes, fetch-max-wait-ms, max-partition-fetch-bytes, fetch-max-bytes, max-poll-records, consumer-throughput]
level: practitioner
status: docs-checked
description: "Tune Kafka consumer fetching (fetch.min.bytes, fetch.max.wait.ms, max.partition.fetch.bytes, fetch.max.bytes, max.poll.records) for throughput vs latency and memory."
sources:
  - https://kafka.apache.org/40/configuration/consumer-configs/
  - https://kafka.apache.org/40/operations/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer fetch tuning

**Goal:** pull data in large enough chunks to keep up with lag, without blowing consumer memory or adding needless latency.

## The knobs
| Config | Default | Effect |
|---|---|---|
| `fetch.min.bytes` | 1 | broker waits until this much data is available... |
| `fetch.max.wait.ms` | 500 | ...or this long, whichever first |
| `max.partition.fetch.bytes` | 1 MiB | per partition per fetch |
| `fetch.max.bytes` | 50 MiB | per fetch response (across partitions) |
| `max.poll.records` | 500 | records returned per `poll()` from the already-fetched buffer |
| `receive.buffer.bytes` | 64 KiB | TCP receive buffer; raise it for high-latency links (-1 uses the OS default) |

`max.poll.records` does not change network fetching; it bounds how much work you take per loop, which matters for `max.poll.interval.ms`.

## Profiles
**Throughput / catch-up (batch-like consumers, sinks to warehouses):**
```properties
fetch.min.bytes=1048576
fetch.max.wait.ms=500
max.partition.fetch.bytes=8388608
fetch.max.bytes=104857600
max.poll.records=5000
receive.buffer.bytes=4194304   # example value, size to your bandwidth-delay product
```
**Low latency (alerting, user-facing):**
```properties
fetch.min.bytes=1
fetch.max.wait.ms=100
max.poll.records=100
```

## Memory estimate
Worst case buffered data ~ `min(fetch.max.bytes, partitions_assigned x max.partition.fetch.bytes)` per consumer, plus deserialized objects. 200 partitions x 8 MiB = 1.6 GiB raw before `fetch.max.bytes` caps it: size heaps accordingly.

## Diagnose with metrics (consumer JMX `consumer-fetch-manager-metrics`)
- `fetch-size-avg` far below `fetch.min.bytes` and `fetch-latency-avg` ~ `fetch.max.wait.ms`: topic is quiet, latency is the wait. Lower the wait if latency matters.
- `records-lag-max` growing while `fetch-rate` is high and `records-per-request-avg` small: increase fetch sizes.
- Lag growing while fetch is fine: processing is the bottleneck. Profile the handler, add partitions/consumers, or process asynchronously.

## Gotchas
- Cross-region consumers: bandwidth-delay product means small fetches are dominated by RTT. Use large fetches + large receive buffers, or consume from a local replica (follower fetching).
- Very large `max.poll.records` with slow processing breaches `max.poll.interval.ms` -> rebalance storm.
- Compressed batches are returned whole; a batch can exceed `max.partition.fetch.bytes` (still delivered) and spike memory.

## Verify
- [ ] Under backlog, lag drains at the target rate; under steady state p99 end-to-end latency meets SLO.
- [ ] Consumer heap stable (no GC thrash) at peak partition assignment.

## Checked
2026-10-28. Confirmed in the Apache Kafka 4.0 consumer configuration page and 3.9 generated config tables: defaults `fetch.min.bytes` 1, `fetch.max.wait.ms` 500, `max.partition.fetch.bytes` 1048576, `fetch.max.bytes` 52428800, `max.poll.records` 500, `receive.buffer.bytes` 65536; oversized first batch still returned; consumer fetch-manager metric names in the monitoring page. Removed the fixed 1-4 MiB recommendation for the receive buffer (marked the profile values as examples).
Method: documentation only; no commands were run.
