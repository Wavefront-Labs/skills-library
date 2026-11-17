---
id: computing-software.data-engineering.apache-kafka.producer-batching-and-compression
name: producer-batching-and-compression
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-producer, linger-ms, batch-size, producer-compression, zstd, lz4, buffer-memory, max-request-size, producer-throughput, latency-tuning]
level: practitioner
status: docs-checked
description: "Tune Kafka producer throughput vs latency: linger.ms, batch.size, compression.type (lz4/zstd), buffer.memory and max.block.ms, max.request.size, and reading producer metrics."
sources:
  - https://kafka.apache.org/40/configuration/producer-configs/
  - https://kafka.apache.org/40/operations/monitoring/
  - https://kafka.apache.org/40/getting-started/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Producer batching and compression

**Goal:** push more MB/s with fewer requests and less broker CPU/disk, at an acceptable added latency.

## How batching works
The producer groups records per partition into batches up to `batch.size` bytes (default 16384). A batch is sent when full or after `linger.ms` (default 5 ms in Kafka 4.0 clients, 0 earlier). Compression applies per batch, so bigger batches compress better.

## Throughput profile
```properties
linger.ms=20
batch.size=131072            # 128 KB
compression.type=lz4         # or zstd for best ratio; snappy fine; gzip CPU-heavy
buffer.memory=67108864       # 64 MB total send buffer (default 32 MB)
acks=all
enable.idempotence=true
```
## Low-latency profile
```properties
linger.ms=0-5
batch.size=16384
compression.type=lz4
```

## Compression notes
- `compression.type` on the topic defaults to `producer` (keep what the producer sent). Setting a different codec on the topic makes brokers recompress: CPU cost.
- zstd needs brokers and clients 2.1.0 or later (KIP-110). Compare codecs on your own payloads: ratio and CPU cost vary.
- Consumers decompress; every client must support the codec.

## Back-pressure on the producer
- When `buffer.memory` fills (brokers slow or down), `send()` blocks up to `max.block.ms` (default 60 s), then throws `TimeoutException`. In a request thread this is a hidden latency spike: size buffer and handle the exception.
- `max.request.size` (default 1 MB) caps a request/record; also raise broker/topic `max.message.bytes` and consumer `max.partition.fetch.bytes` for large messages, or better, store blobs elsewhere and send references.

## Measure (producer metrics via JMX or client `metrics()`)
| Metric | Healthy |
|---|---|
| `batch-size-avg` | Close to `batch.size` under load (otherwise raise linger) |
| `records-per-request-avg` | Higher is better |
| `compression-rate-avg` | < 1 means compression is working (ratio) |
| `record-queue-time-avg` | Added latency from linger/buffering |
| `buffer-available-bytes` | Not near 0 |
| `request-latency-avg`, `record-error-rate` | Stable, ~0 errors |
`kafka-producer-perf-test.sh --topic t --num-records 1000000 --record-size 1024 --throughput -1 --producer-props bootstrap.servers=$B linger.ms=20 compression.type=lz4` to compare settings.

## Verify
- [ ] Perf test shows higher MB/s and lower broker request rate with the tuned profile.
- [ ] p99 end-to-end latency still within the SLA.
- [ ] No `TimeoutException` from `max.block.ms` under peak load.

## Checked
2026-10-28. Confirmed in the Apache Kafka 4.0 producer configuration page, 3.9 generated tables and 4.0 upgrade notes: `batch.size` 16384, `linger.ms` default changed from 0 to 5 in 4.0, `buffer.memory` 33554432 (32 MB), `max.block.ms` 60000, `max.request.size` 1048576, topic `compression.type` default `producer`; monitoring-page definitions of `compression-rate-avg` (compressed over uncompressed), `record-queue-time-avg`, `buffer-available-bytes`; zstd 2.1.0 requirement (3.9 upgrade notes, KIP-110). Removed the claimed 5-10x JSON compression figure.
Method: documentation only; no commands were run.
