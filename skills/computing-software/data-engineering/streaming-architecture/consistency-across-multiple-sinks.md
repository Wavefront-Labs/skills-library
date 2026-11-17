---
id: computing-software.data-engineering.streaming-architecture.consistency-across-multiple-sinks
name: consistency-across-multiple-sinks
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, multi-sink-consistency, exactly-once, outbox, idempotent-sink, stream-processing, cdc]
level: advanced
status: draft
description: "Keep several sinks (database, search index, cache, topic) consistent from one stream: single source of truth plus derived sinks, idempotent writes, ordering and repair."
sources:
  - https://www.confluent.io/blog/turning-the-database-inside-out-with-apache-samza/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/#exactly-once-end-to-end
  - https://martin.kleppmann.com/2015/05/27/logs-for-data-infrastructure.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Consistency across multiple sinks

**Problem:** one event must update a database, a search index and a cache (or several topics). Writing to each from one process means partial failure leaves them disagreeing, and there is no distributed transaction across Postgres, Elasticsearch and Redis.

## Principle: one log, many derived views
1. Write the event to **one** durable, ordered log first (a Kafka topic, or the database with CDC/outbox so DB and log are atomically the same).
2. Each sink is a separate consumer (or connector) that derives its view from the log at its own pace, with its own offsets.
3. Each sink write is **idempotent** (upsert by key, with a version) so replays converge.
Sinks are then *eventually* consistent with each other and always consistent with the log; any sink can be rebuilt by replaying.

## Making each derived sink correct
- Key by entity, keep per-key order (partition by entity id), and carry a monotonically increasing version (source LSN, `updated_at`, sequence number). Sinks reject writes with a lower version than stored (conditional update, Elasticsearch external versioning).
- Commit offsets only after the sink write succeeds (at-least-once) and let idempotency absorb duplicates.
- Deletes: emit tombstones and handle them in every sink.

## When sinks must agree atomically
- Same database: write all tables in one transaction (one sink, many tables).
- Several Kafka topics: a single Kafka transaction can span topics (Kafka Streams/Flink EOS).
- Flink: multiple two-phase-commit sinks in one job commit on the **same checkpoint**, but commits are not atomic across them; a failure between commits is repaired by re-committing on recovery (eventual, not atomic).
- Otherwise, expose a "consistent as of" watermark: each sink records the log offset/version it has applied; readers that need cross-sink consistency read at the minimum applied offset, or the UI tolerates lag.

## Anti-patterns
- Service writes DB then publishes event (dual write): event lost on crash, or published for a rolled-back write. Use outbox/CDC.
- Fan-out sink in one consumer that writes A then B and commits offset: if B fails forever, A races ahead; route B failures to a retry topic per sink instead of blocking A.

## Repair
- Reconciliation job: periodically compare counts/checksums per key range between source of truth and each sink; replay the log or re-snapshot differences.
- Keep log retention (or a compacted topic, or the lakehouse table) long enough to rebuild any sink.

## Verify
- [ ] Chaos test: kill each sink writer mid-stream; after recovery all sinks match the source for sampled keys.
- [ ] Reconciliation job runs and alerts on drift.
