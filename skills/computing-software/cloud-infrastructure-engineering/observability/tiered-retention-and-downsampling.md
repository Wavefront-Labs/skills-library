---
id: computing-software.cloud-infrastructure-engineering.observability.tiered-retention-and-downsampling
name: tiered-retention-and-downsampling
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [retention-tiering, tiered-retention, observability-cost, downsampling, retention-policy]
level: practitioner
status: draft
description: "Design retention per signal and tier: hot vs object storage, Prometheus/Mimir/Thanos/Loki/Tempo retention settings, downsampling, and per-tenant or per-stream overrides."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/", "https://thanos.io/tip/components/compact.md/", "https://grafana.com/docs/loki/latest/operations/storage/retention/", "https://grafana.com/docs/mimir/latest/configure/configure-metrics-storage-retention/", "https://grafana.com/docs/tempo/latest/configuration/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tiered retention and downsampling

## Typical policy (start here, adjust to compliance)
| Signal | Full resolution | Downsampled / archive |
|---|---|---|
| Metrics | 15-30 d local Prometheus; 13 months in Mimir/Thanos | Thanos 5m res 90 d-1 y, 1h res 1-2 y |
| Logs | 7-14 d app/debug, 30 d prod, 1 y+ audit/security | archive to cold bucket for compliance |
| Traces | 7-14 d | none (keep span metrics long) |
| Profiles | 7-30 d | none |

## Settings
- Prometheus: `--storage.tsdb.retention.time=15d` and/or `--storage.tsdb.retention.size=200GB` (size includes WAL).
- Thanos compactor: `--retention.resolution-raw=30d --retention.resolution-5m=180d --retention.resolution-1h=2y`.
  Downsampling only helps queries over long ranges; it does not reduce raw storage until raw retention expires.
- Mimir: `compactor_blocks_retention_period: 1y` globally or per tenant in runtime overrides. No downsampling - use
  recording rules for long-range aggregates.
- Loki: `limits_config.retention_period: 30d`, compactor `retention_enabled: true`, plus per-stream:
  ```yaml
  retention_stream:
    - {selector: '{namespace="dev"}', priority: 1, period: 7d}
    - {selector: '{stream="audit"}', priority: 2, period: 8760h}
  ```
- Tempo: `compactor.compaction.block_retention: 336h`, per-tenant `block_retention` override.
- Object storage lifecycle rules (S3 transitions to IA/Glacier) only for data the backend no longer reads;
  never transition live Mimir/Loki/Tempo blocks to Glacier (reads fail).

## Long-range metrics without raw data
Recording rules for SLO and capacity series (`job:http_requests:rate5m`) cost a fraction of raw series; keep
those longer (separate tenant with longer retention in Mimir).

## Gotchas
- Bucket lifecycle deletion must be longer than backend retention, or the index references missing chunks.
- Loki retention requires the compactor to run with `delete_request_store` set (3.x).
- Changing retention down deletes data at next compaction - irreversible.
