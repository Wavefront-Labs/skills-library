---
id: computing-software.data-engineering.apache-kafka.exactly-once-and-transactions
name: exactly-once-and-transactions
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, exactly-once, idempotent-producer, transactional-id, kafka-transactions, read-committed, isolation-level, kafka-streams-eos, transaction-coordinator, zombie-fencing, enable-idempotence]
level: practitioner
status: docs-checked
description: "Configure idempotent producers and Kafka transactions for exactly-once semantics, and know their real limits."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://kafka.apache.org/39/configuration/producer-configs/
  - https://kafka.apache.org/39/configuration/consumer-configs/
  - https://www.confluent.io/blog/transactions-apache-kafka/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka exactly-once semantics — what it covers and what it doesn't

**Goal:** know exactly where Kafka's EOS guarantee starts and stops, so you don't ship a pipeline that's "exactly once" on paper and duplicates/loses data at its actual boundaries.

## 1. Idempotent producer — dedupes retries, nothing more
`enable.idempotence=true` (on by default if no conflicting configuration is set; explicitly enabling it with conflicting settings throws a `ConfigException`) assigns each producer a PID and sequence number per partition; the broker drops a retry with a sequence number it already committed. This eliminates **producer-retry duplicates within a single producer session** — it does not dedupe application-level reprocessing (re-running a job that re-reads the same source and re-produces) or duplicates across producer restarts without a stable `transactional.id`.
- Idempotence requires `max.in.flight.requests.per.connection` of 5 or less, `retries` greater than 0 and `acks=all`. If you override any of them and idempotence is not explicitly enabled, idempotence is silently disabled.

## 2. Transactions — atomic writes across partitions, and read-process-write
`transactional.id` (stable across restarts — same id, same producer identity) enables `initTransactions()`/`beginTransaction()`/`commitTransaction()`, making a batch of writes across multiple partitions/topics atomic: either all records become visible to `read_committed` consumers or none do. This is what powers **Kafka Streams' exactly-once processing (EOS)** — consume-transform-produce as one atomic unit, with the consumer's offset commit *included in the same transaction* as the output writes (`sendOffsetsToTransaction`), so a crash mid-processing can't commit the output without the input offset, or vice versa.
- **Gotcha:** consumers must set `isolation.level=read_committed` to actually get the benefit — with the default `read_uncommitted`, a consumer sees uncommitted/aborted transactional writes too, defeating the point.
- **Zombie fencing**: a new producer instance with the same `transactional.id` increments an internal epoch, fencing off any older "zombie" instance of itself (e.g. after a hung JVM that didn't crash cleanly) from committing further — this is why a stable, unique `transactional.id` per logical producer instance matters; reusing one across genuinely concurrent producers causes spurious fencing errors, and never setting one at all forfeits the guarantee.

## 3. Where exactly-once actually ends
- **Kafka-to-Kafka** (Streams, or your own read-process-write loop): true exactly-once, well-supported.
- **Kafka-to-external-system** (sink connector, a consumer writing to a DB/S3/API): Kafka's transaction guarantee stops at the Kafka boundary. The external write needs its own idempotency (upsert on a natural/dedup key, or a two-phase commit pattern). Don't advertise "exactly-once" to a downstream team unless the sink side was actually verified idempotent.
- Transactions add overhead (transaction markers are one extra write to each partition in the transaction, independent of how many messages it holds) — don't reach for them on a single-partition, no-external-side-effect pipeline where idempotence alone already suffices.

## Checked
2026-10-28. Confirmed against the Kafka 3.9 producer and consumer configuration pages: `enable.idempotence` requirements and default behaviour, `transactional.id` (unset by default, implies idempotence), `isolation.level` default `read_uncommitted`; against the Confluent transactions blog: epoch bump and zombie fencing, atomic read-process-write cycles, marker overhead. Removed: the claim that idempotence became default in 3.0, the infinite-retries and Kafka Connect exactly-once statements.
Method: documentation only; no commands were run.

## Verify
- [ ] `transactional.id` is stable across restarts for any producer relying on transactions, and unique per logical producer instance (no two concurrent producers share one).
- [ ] Downstream consumers of transactional topics are explicitly set to `isolation.level=read_committed`.
- [ ] The actual external sink (DB/S3/API) has its own dedup/upsert key — "Kafka is exactly-once" was not assumed to extend past the Kafka boundary.
- [ ] A forced producer crash mid-transaction leaves no partial/uncommitted records visible to `read_committed` consumers.
