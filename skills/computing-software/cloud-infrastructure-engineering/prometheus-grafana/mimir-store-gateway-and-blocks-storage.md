---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.mimir-store-gateway-and-blocks-storage
name: mimir-store-gateway-and-blocks-storage
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [mimir, mimir-store-gateway, mimir-blocks-storage, index-header, bucket-index, sharding-ring]
level: advanced
status: docs-checked
description: "Operate the Mimir store-gateway over blocks storage: sharding and replication, index-header lazy loading, bucket index, caches, and troubleshooting slow long-range queries."
sources: ["https://grafana.com/docs/mimir/latest/references/architecture/components/store-gateway/", "https://grafana.com/docs/mimir/latest/references/architecture/bucket-index/", "https://grafana.com/docs/mimir/latest/manage/run-production-environment/production-tips/", "https://grafana.com/docs/mimir/latest/references/architecture/binary-index-header/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mimir store-gateway and blocks storage

**Goal:** long-range queries served efficiently from object storage.

## How it works
- Ingesters write 2 h TSDB blocks to object storage; the compactor merges them (up to 24 h+ blocks) and maintains the **bucket index** (`bucket-index.json.gz` per tenant) listing blocks and deletion marks.
- **Store-gateways** shard blocks among themselves via a hash ring, with `replication_factor` (default 3) so each block is loaded by several gateways for availability.
- For each owned block, a gateway keeps an **index-header** (symbols and postings offsets) on local disk; full index and chunks are read from the bucket on demand through caches.
- Queriers ask the gateways for series in blocks older than `query_store_after` (default 12h); newer data comes from ingesters.

## Config essentials
```yaml
blocks_storage:
  backend: s3
  s3: { bucket_name: mimir-blocks, endpoint: s3.eu-west-1.amazonaws.com }
  bucket_store:
    sync_dir: /data/tsdb-sync
    index_cache:    { backend: memcached, memcached: { addresses: dns+memcached-index.mimir.svc:11211 } }
    chunks_cache:   { backend: memcached, memcached: { addresses: dns+memcached-chunks.mimir.svc:11211 } }
    metadata_cache: { backend: memcached, memcached: { addresses: dns+memcached-metadata.mimir.svc:11211 } }
    index_header:
      lazy_loading_enabled: true
      lazy_loading_idle_timeout: 1h
store_gateway:
  sharding_ring: { replication_factor: 3, zone_awareness_enabled: true }
```
- `sync_dir` (default `./tsdb-sync/`) holds the downloaded index-headers; `zone_awareness_enabled` defaults to false.
- Index-headers load lazily by default and are released after `lazy_loading_idle_timeout` (default 1h) of inactivity.

## Troubleshooting
| Symptom | Check |
|---|---|
| Slow queries over weeks | Cache hit ratios and memcached evictions, compactor lagging (many small blocks) |
| "Failed to sync blocks" | Bucket permissions, bucket index missing (compactor not running for tenant) |
| OOM on startup | Too many blocks per gateway: add replicas, enable lazy loading |
| Queries miss recent data | `query_store_after` vs ingester `query_ingesters_within` overlap misconfigured |

## Verify
- [ ] `cortex_bucket_store_blocks_loaded` balanced across gateways; store-gateway latency within target; the compactor is running (see the runbooks for `MimirCompactorNotRunningCompaction`).

## Checked
- 2026-10-28. Confirmed against the Mimir store-gateway page (index-header lazy loading, `bucket-index.json.gz`, memcached caches) and the configuration reference (`sync_dir`, `lazy_loading_idle_timeout` 1h, `replication_factor` 3, `zone_awareness_enabled` false, `query_store_after` 12h, `query_ingesters_within` 13h, compactor `block_ranges` 2h, 12h, 24h) and the runbooks page.
- Removed: `thanos_store_index_cache_hits_total` (a Thanos metric), `cortex_compactor_last_successful_run_timestamp_seconds`, the "Queries" dashboard reference and the zone-roll claim.
Method: documentation only; no commands were run.
