---
id: computing-software.data-engineering.streaming-architecture.reprocessing-and-replaying-streams
name: reprocessing-and-replaying-streams
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, stream-reprocessing, replay, kappa-architecture, blue-green-streaming, retention, backfill, idempotent-sink]
level: advanced
status: draft
description: "Reprocess history in a streaming system after a bug fix or logic change: retention and tiered storage prerequisites, parallel (blue/green) jobs, output versioning and switchover."
sources:
  - https://www.oreilly.com/radar/questioning-the-lambda-architecture/
  - https://kafka.apache.org/documentation/#tiered_storage
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reprocessing and replaying streams

**Goal:** recompute outputs from historical events (bug fix, new metric, new model) without stopping the live pipeline or corrupting what consumers read.

## Prerequisites
- **Source retention covers the history you need.** Kafka with long retention, tiered storage, or an archive of raw events in object storage (Iceberg/Delta bronze) that can be read as a bounded source.
- **Deterministic logic:** event-time semantics, not processing time or wall-clock lookups; external enrichment versioned or snapshotted.
- **Idempotent or versioned sinks.**

## Kappa-style reprocessing (blue/green)
1. Deploy the new job version as a **separate job** (new consumer group / new checkpoint, new name) reading from the beginning (or the needed offset/timestamp).
2. Write to a **new output** (`orders_agg_v2` table/topic).
3. Let it catch up (rate-limit to protect brokers and sinks; scale out temporarily).
4. Validate v2 vs v1 on overlapping periods (counts, key metrics, sample diffs).
5. Switch consumers (view repoint, alias, config) to v2.
6. Stop v1 and delete its output after a safety period.

## Replay from lake instead of Kafka
For long histories, run the same logic as a **batch/bounded job** over the bronze table for the historical range, then hand over to the streaming job at a boundary offset/time. Flink and Spark Structured Streaming can read bounded sources with the same code; ensure the boundary is clean (e.g. events with event_time < T from batch, >= T from stream, idempotent upserts at the edge).

## In-place replay (smaller fixes)
Reset the existing job's offsets (stop with savepoint, start from timestamp, or reset consumer group) only if the sink is **upsert/idempotent by key**; append sinks will duplicate. Stateful jobs: state must be reset too (start without savepoint) or the replay double-counts.

## Capacity planning
- Replay throughput vs broker egress: rereading 30 days can saturate brokers; use follower fetching, quotas for the replay consumer, or read from tiered storage/lake.
- Sinks (OLAP, DB) get a burst of writes: throttle or bulk-load.

## Gotchas
- Joins with dimension/enrichment data: replaying with today's dimension values changes historical results; use temporal joins against versioned dimensions.
- Compacted topics only hold the latest value per key: not a full event history.
- Schema evolution across history: the job must read all historical schema versions (registry-aware deserializers).

## Verify
- [ ] Runbook documents how far back each pipeline can replay and from which source.
- [ ] Last replay: v2 validation report attached and consumers switched without downtime.
