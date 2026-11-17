---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-ingester-wal-and-replication
name: loki-ingester-wal-and-replication
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [ingester-wal-loki, loki-replication-factor, loki-architecture, ingester, data-durability]
level: advanced
status: gated
description: "Configure Loki ingester WAL, replication factor and flush settings for durability, and handle WAL replay memory, ring health and zone-aware replication."
sources: ["https://grafana.com/docs/loki/latest/operations/storage/wal/", "https://grafana.com/docs/loki/latest/configure/#ingester", "https://grafana.com/docs/loki/latest/operations/zone-ingesters/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ingester WAL and replication

Ingesters hold recent log data in memory as chunks until flushed to object storage. Two mechanisms protect it: replication (copies on several ingesters) and the WAL (local disk log replayed after restart).

## Config
```yaml
common:
  replication_factor: 3
ingester:
  wal:
    enabled: true
    dir: /var/loki/wal
    flush_on_shutdown: true
    replay_memory_ceiling: 4GB      # flush during replay when memory exceeds this
  chunk_idle_period: 30m
  max_chunk_age: 2h
  chunk_target_size: 1572864
```
Ingesters need a PersistentVolume for the WAL (StatefulSet) (gated: unconfirmed, source is paywalled or blocked): no Kubernetes here. Writes succeed when a quorum (2 of 3) acknowledges (gated: unconfirmed, source is paywalled or blocked): a single-ingester node was run, not a replicated ring.

## Zone awareness
Spread replicas across zones so a zone loss keeps a copy: `ingester.lifecycler.ring.zone_awareness_enabled: true` (key accepted by `-verify-config`) with per-zone StatefulSets (Helm `zoneAwareReplication` (gated: unconfirmed, source is paywalled or blocked): chart not run).

## Operations
- Rolling restarts one ingester at a time; wait for `/ready` (WAL replay complete) before the next (`/ready` answers 503 with `Ingester not ready: waiting for 15s after being ready` while the node starts).
- Ring status page `/ring` (HTTP 200 on the test node; per-component pages such as `/distributor/ring` and `/ruler/ring` also exist): unhealthy entries block writes if quorum is lost; "Forget" stale members (gated: unconfirmed, source is paywalled or blocked).
- Metrics: `loki_ingester_wal_replay_duration_seconds`, `loki_ingester_memory_chunks`, `loki_ingester_chunks_flushed_total{reason}`, `loki_ingester_wal_disk_full_failures_total`.

## Gotchas
- WAL disk full stops WAL writes (data then only in memory); alert on it.
- Replication factor 3 triples ingester memory for the same data.
- `max_chunk_age` too high delays data in object storage and enlarges replay (default 2h).

## Verify
- [ ] Killing one ingester under load loses no lines (compare counts before/after); replay completes within the startup probe window (gated: unconfirmed, source is paywalled or blocked): the kill test needs a replicated ring.

## Checked
Ran Loki 3.7.9 on one node with the page's `ingester` block (`wal.enabled`, `dir`, `flush_on_shutdown`, `replay_memory_ceiling: 4GB`, `chunk_idle_period: 30m`, `max_chunk_age: 2h`, `chunk_target_size: 1572864`) and `common.replication_factor`: it loaded with `-verify-config`, matched the defaults in `-print-config-stderr`, and `lifecycler.ring.zone_awareness_enabled` was accepted. The metrics `loki_ingester_wal_replay_duration_seconds`, `loki_ingester_memory_chunks`, `loki_ingester_wal_disk_full_failures_total` exist on `/metrics`; `loki_ingester_chunks_flushed_total` is a counter vector with a `reason` label (read from `pkg/ingester/metrics.go` at v3.7.9). Replication quorum, zone-aware rollout, Helm values and the kill test were not run and are marked.
