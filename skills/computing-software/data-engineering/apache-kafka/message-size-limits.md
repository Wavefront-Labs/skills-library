---
id: computing-software.data-engineering.apache-kafka.message-size-limits
name: message-size-limits
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, max-message-bytes, message-max-bytes, max-request-size, recordtoolargeexception, large-messages, claim-check]
level: practitioner
status: docs-checked
description: "Raise or work around Kafka's message size limits consistently across broker, topic, producer, consumer and replication, or use the claim-check pattern instead."
sources:
  - https://kafka.apache.org/40/configuration/broker-configs/
  - https://kafka.apache.org/40/configuration/producer-configs/
  - https://kafka.apache.org/40/configuration/consumer-configs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka message size limits

**Goal:** send records bigger than the ~1 MB default without breaking replication or consumers, or decide not to.

## The chain of limits (all must agree)
| Setting | Scope | Default | Meaning |
|---|---|---|---|
| `message.max.bytes` | broker | 1048588 | max record batch size the broker accepts (after compression) |
| `max.message.bytes` | topic | inherits broker | per-topic override, the usual knob |
| `max.request.size` | producer | 1048576 | max request; effectively a cap on the **uncompressed** record batch size |
| `replica.fetch.max.bytes` | broker | 1048576 | follower fetch size per partition; not an absolute maximum, a larger first batch is still returned so replication progresses |
| `max.partition.fetch.bytes` | consumer | 1048576 | per-partition fetch; not an absolute maximum, an oversized first batch is still returned |
| `fetch.max.bytes` | consumer | 52428800 | per-fetch total |
| `buffer.memory` / `batch.size` | producer | 32 MB / 16 KB | buffer must exceed record size |

The broker limits (`message.max.bytes`, `max.message.bytes`) apply to the batch **after compression**, so compression can let a larger payload fit under them. The producer's `max.request.size` is checked against the **uncompressed** size, so raise it for large payloads regardless of compression.

## Raise for one topic (e.g. 5 MB)
```bash
kafka-configs.sh --bootstrap-server $BS --alter --entity-type topics --entity-name docs \
  --add-config max.message.bytes=5242880
```
Producer: `max.request.size=5242880`, `buffer.memory` >= several records, `compression.type=zstd`.
Consumer: `max.partition.fetch.bytes=5242880` (avoid slow progress and memory spikes).
Broker: if the broker-level `message.max.bytes` is raised as well, also raise `replica.fetch.max.bytes` to match (a larger first batch is still returned, but the fetch size is a per-partition target).

## Errors
- Producer: `RecordTooLargeException` when a record or batch exceeds `max.request.size` (client side) or the broker/topic limit (server side).

## Prefer the claim-check pattern
For payloads in the MB-GB range (documents, images): write the blob to object storage, send a small event with the URI, checksum and size. Keeps brokers fast, page cache effective, and consumers' memory bounded.
```json
{"doc_id":"d-91","uri":"s3://blobs/docs/d-91.pdf","sha256":"...","bytes":7340032}
```

## Gotchas
- Large records hurt tail latency for every other producer on the partition and blow up consumer memory (`max.poll.records` x record size).
- Managed services and proxies may impose their own caps: check the provider's limits page.

## Verify
- [ ] Produce a test record at the target size and consume it end to end, including through mirroring/Connect.
- [ ] Follower replicas stay in ISR while large records flow.

## Checked
2026-10-28. Confirmed in the Apache Kafka 4.0 broker, producer and consumer configuration pages (and the 3.9 generated config tables): defaults `message.max.bytes` 1048588, `max.request.size` 1048576 (cap on uncompressed batch size), `replica.fetch.max.bytes` 1048576, `max.partition.fetch.bytes` 1048576, `fetch.max.bytes` 52428800, `buffer.memory` 33554432, `batch.size` 16384; broker limit applies after compression; oversized first batch still returned. Removed: the exact exception message strings, the MirrorMaker/Connect and Schema Registry claims, the Confluent Cloud size figure, and the wrong claim that producer limits apply to the compressed batch.
Method: documentation only; no commands were run.
