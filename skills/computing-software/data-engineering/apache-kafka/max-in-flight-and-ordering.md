---
id: computing-software.data-engineering.apache-kafka.max-in-flight-and-ordering
name: max-in-flight-and-ordering
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-producer, max-in-flight-requests, message-ordering, idempotent-producer, retries, out-of-order, throughput]
level: practitioner
status: docs-checked
description: "Tune max.in.flight.requests.per.connection for throughput without reordering: how retries reorder batches, why idempotence allows up to 5, and legacy client settings."
sources:
  - https://kafka.apache.org/40/configuration/producer-configs/
  - https://kafka.apache.org/40/getting-started/upgrade/
  - https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# max.in.flight.requests and ordering

**Goal:** keep per-partition order under retries while still pipelining requests for throughput.

## The reordering mechanism
With several in-flight requests per broker connection, batch 1 can fail (e.g. `NOT_LEADER_OR_FOLLOWER`) while batch 2 succeeds; the retry of batch 1 is then written after batch 2. Same partition, wrong order.

## Settings
| Client setup | Ordering-safe value |
|---|---|
| `enable.idempotence=true` (default since Kafka 3.0 clients) | `max.in.flight.requests.per.connection` <= 5; ordering is preserved for any allowed value. |
| Idempotence disabled, `retries > 0` | must be `1` for strict order (big throughput cost on high-latency links) |
| `retries=0` | any value, but you lose records on transient errors |

Idempotence requires `acks=all`, `retries > 0`, in-flight <= 5. From Kafka 4.0 the producer no longer silently falls back (disables idempotence) when in-flight exceeds 5; on older clients, conflicting settings could leave idempotence off if you had not enabled it explicitly. Check startup logs for the effective `enable.idempotence`.

## Recommended producer baseline
```properties
enable.idempotence=true
acks=all
max.in.flight.requests.per.connection=5
retries=2147483647
delivery.timeout.ms=120000
```

## Broker requirement
When producing to brokers older than 2.8.0, idempotent writes need the `IDEMPOTENT_WRITE` permission (see the 3.x upgrade notes and KIP-679).

## Non-Java clients
librdkafka: `enable.idempotence=true` sets `max.in.flight.requests.per.connection<=5`, `retries`, `acks=all` automatically. With idempotence off, set `max.in.flight=1` to preserve ordering. librdkafka also has an experimental `enable.gapless.guarantee` (default false).

## Gotchas
- Ordering is only per partition. Different keys -> different partitions -> no global order.
- `delivery.timeout.ms` expiry drops a batch after retries; later batches may already be written. Treat delivery failures as fatal for ordered streams (stop producing, alert).
- Async `send()` callbacks fire in order per partition; do not resend failed records from the callback (that reorders). Let the client retry.

## Verify
- [ ] Producer config dump in logs shows idempotence enabled and in-flight <= 5.
- [ ] Chaos test (restart partition leader under load) produces no out-of-sequence records per key.

## Checked
2026-10-28. Confirmed in the Kafka 4.0 producer config page, 3.9 and 4.0 upgrade notes, KafkaProducer javadoc (3.9) and librdkafka CONFIGURATION.md/INTRODUCTION.md: reordering with `max.in.flight.requests.per.connection` > 1 and idempotence off, ordering preserved when idempotence is on, the <= 5 limit, `enable.idempotence` default true since 3.0, no silent fallback from 4.0, `IDEMPOTENT_WRITE` for brokers older than 2.8.0, librdkafka automatic adjustments, in-order callbacks per partition. Removed: the version-by-version fallback behaviour, the `ClusterAuthorizationException` claim, the `ConfigException` claim and the librdkafka fatal-error text.
Method: documentation only; no commands were run.
