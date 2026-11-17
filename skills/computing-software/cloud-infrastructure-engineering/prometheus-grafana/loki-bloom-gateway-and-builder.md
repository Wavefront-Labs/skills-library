---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-bloom-gateway-and-builder
name: loki-bloom-gateway-and-builder
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [bloom-gateway, bloom-builder, bloom-filters, loki-architecture, query-acceleration]
level: advanced
status: docs-checked
description: "Set up experimental Loki query acceleration with blooms: planner, builder and gateway components, per-tenant limits, retention, sizing guidance and the bounded sharding strategy."
sources: ["https://grafana.com/docs/loki/latest/operations/bloom-filters/", "https://grafana.com/docs/loki/latest/configure/#bloom_build", "https://grafana.com/docs/loki/latest/configure/#bloom_gateway"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki bloom gateway and bloom builder

Bloom filters let Loki skip chunks that cannot contain a structured metadata key/value pair, which speeds up "needle in a
haystack" queries such as `{cluster="prod"} | traceID="3c0e3dcd33e7"`. Status per the docs: **experimental** in Loki and
Grafana Enterprise Logs (no engineering or on-call support, no SLA), intended for users ingesting more than 75TB of logs
a month; a public preview for select large Grafana Cloud customers. Not supported in single binary deployments; usable
with Simple Scalable deployment, but the docs recommend fully distributed microservice mode because blooms are costly to
build and query and only pay off at scale.

## Components
- **Bloom Planner**: runs as a single instance (the docs warn never to run more than one). Finds gaps in fingerprint
  ranges per tenant, creates build tasks, dispatches them to builders and applies bloom retention.
- **Bloom Builder**: stateless, horizontally scalable; builds bloom blocks from chunks and uploads them. The docs estimate
  4MB of data processed per second per core.
- **Bloom Gateway**: handles chunk filtering requests from the index gateway; horizontally scalable, each instance owns a
  subset of the stream fingerprint range, with client-side sharding via DNS discovery and jumphash.

## Config (from the docs' enable section)
```yaml
bloom_build:
  enabled: true
  planner:
    planning_interval: 8h        # reference default 8h
  builder:
    planner_address: bloom-planner.<namespace>.svc.cluster.local:9095
bloom_gateway:
  enabled: true
  client:
    addresses: dnssrvnoa+_bloom-gateway-grpc._tcp.bloom-gateway-headless.<namespace>.svc.cluster.local
limits_config:
  bloom_creation_enabled: true
  bloom_split_series_keyspace_by: 1024
  bloom_gateway_enable_filtering: true
```
Deploy planner, builder and gateway as microservices or via the SSD backend target, enable them in their config blocks
and enable building and filtering per tenant or for all tenants by default. CLI equivalents in the reference:
`-bloom-build.enabled`, `-bloom-build.planner.interval`, `-bloom-build.builder.planner-address`, `-bloom-gateway.enabled`
(all default off or empty), `-bloom-gateway-client.addresses`.

## Per-tenant tuning (from the operations page)
- `bloom_planning_strategy`: `split_keyspace_by_factor` (default, uses `bloom_split_series_keyspace_by`) or
  `split_by_series_chunks_size` (uses `bloom_task_target_series_chunk_size`).
- `bloom_build_max_builders` (0 = unlimited), `bloom_build_builder_response_timeout` (0 disables),
  `bloom_build_task_max_retries`, `bloom_block_encoding`, `bloom_prefetch_blocks`.
- `-bloom-build.max-block-size` and `-bloom-build.max-bloom-size`: a stream whose bloom exceeds the latter is discarded.
- Builders needed depend on `-bloom-build.split-keyspace-by`, tenant count and log volume.

## Retention
Bloom retention is applied by the planner, disabled by default and, when enabled, applies to all tenants. A tenant's bloom
retention is the longest of its `retention_period` and stream retention (`retention_stream`).

## Gateway sizing
Gateways use the local file system as an LRU cache of downloaded blooms; with default settings blooms are under 1% of the
raw structured metadata size. Reading depends on disk IOPS, so use multiple locally attached NVMe SSDs, listed in
`-bloom.shipper.working-directory` (comma separated). Peak bloom data in memory is the product of
`-bloom-gateway.worker-concurrency`, `-bloom-gateway.block-query-concurrency` and `-bloom.max-query-page-size`; the
docs' 4-core example is 4 x 8 x 64MiB = 2048MiB, and the minimum requirement is double that.

## Query sharding
The per-tenant `tsdb_sharding_strategy` defaults to the power-of-two shard computation from index stats. The `bounded`
strategy uses blooms during planning in the query frontend to cut the chunks to process and spread them evenly across
shards.

## Verify
- [ ] The planner runs as one instance; builders pick up tasks within the planning interval.
- [ ] A structured-metadata filter query over a large range processes far fewer chunks than the same query before enabling
      blooms (compare query statistics).

## Checked

Checked 2026-11-08 against the Loki bloom filters operations page and the bloom build and gateway reference sections.
Corrected the planning interval to the documented 8h and the size estimate to "under 1%" of structured metadata, and
the DNS service name in the client address. Removed because the pages do not state them: the Loki 3.3 version claim, the
"queries that do not benefit" list, Helm values, the planner queue and gateway filtering metric names and the
`logcli --stats` verification.
Method: docs-only read of cited pages, 2026-11-08
