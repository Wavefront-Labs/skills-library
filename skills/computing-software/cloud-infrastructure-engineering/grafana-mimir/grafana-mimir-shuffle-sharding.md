---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-shuffle-sharding
name: grafana-mimir-shuffle-sharding
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [shuffle-sharding, tenant-isolation, shard-size, blast-radius, multitenancy]
level: advanced
status: docs-checked
description: "Explains Mimir shuffle sharding to isolate tenants, the shard size settings per component and the properties of the algorithm. Use in multi-tenant clusters."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-shuffle-sharding/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shuffle sharding

By default (shard size `0`) each tenant uses all instances or partitions. In a multi-tenant cluster, an outage then affects all tenants and a misbehaving tenant (for example one causing OOM) can hurt everyone. Shuffle sharding gives each tenant a subset, reducing blast radius without needing more resources, though instances can become unbalanced.

Example: 4 of 50 partitions per tenant gives about 230,000 combinations; two random tenants share no partition with 71% probability and fully overlap with 0.0004%.

## Guaranteed properties

Stability (same ring gives same selection), consistency (adding or removing an instance changes at most one instance per shard), shuffling, and zone awareness when zone-aware replication is on. A shard size at or above the instance count disables the effect.

## Supported components and settings

- Ingest storage partitions: `-ingest-storage.ingestion-partition-tenant-shard-size`. Enabling on write also enables on read.
- Classic ingesters: `-distributor.ingestion-tenant-shard-size` (distributor, ingester, ruler, querier); per tenant `ingestion_tenant_shard_size`. Read path toggle `-querier.shuffle-sharding-ingesters-enabled` defaults true.
- Query-frontend and query-scheduler: `-query-frontend.max-queriers-per-tenant` above 0 and below the querier count.
- Store-gateway, ruler, compactor, Alertmanager have their own shard sizes.

## Enabling safely

1. Set `-querier.shuffle-sharding-ingesters-enabled=false`.
2. Enable on the write path.
3. Wait at least `-blocks-storage.tsdb.retention-period`.
4. Re-enable the read path.

## Decreasing shard size

Never lower it abruptly; queriers cannot know the previous size and could miss data. Use the same procedure above, or on ingest storage the `-ingest-storage.ingestion-partition-tenant-write-shard-size` override: set smaller write size, wait the retention period, set the main size to match, then remove the override.

## Checked

Confirmed against the page: default shard size 0, downsides, the 50-partition probabilities, guaranteed properties, per-component settings, the safe enabling sequence and the decrease procedures. Nothing removed.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir configure-shuffle-sharding page (grafana/mimir main), read in full.
