---
id: computing-software.cloud-infrastructure-engineering.cortex.shuffle-sharding
name: shuffle-sharding
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [shuffle-sharding, tenant-isolation, ingesters, store-gateway, rollout]
level: advanced
status: docs-checked
description: "Enable shuffle sharding to isolate tenants on ingesters, store-gateways, rulers, compactors and the query path, with the safe rollout order."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/shuffle-sharding.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default sharding spreads every tenant across all instances, so an outage or one misbehaving tenant can affect everyone. Shuffle sharding gives each tenant a subset of instances, minimising overlap between tenants. For 50 ingesters and 4 per tenant there are about 230K combinations, and two random tenants share no instance 71% of the time. It needs no more resources than default sharding but instances may be less evenly balanced. It is disabled by default.

Guarantees: stability (same instances for a tenant given the same ring), consistency (adding or removing one instance changes at most one instance per tenant shard), shuffling, and zone-awareness when zone-aware replication is on.

Supported in: ingesters, query-frontend and query-scheduler, store-gateway, ruler and compactor.

Ingester write path (distributor, ingester, ruler): `-distributor.sharding-strategy=shuffle-sharding` and `-distributor.ingestion-tenant-shard-size=<size>`; a size larger than the ingester count means all ingesters. Read path (querier, ruler): the same two flags plus `-querier.shuffle-sharding-ingesters-lookback-period`, which should be at least `-querier.query-store-after` and `-querier.query-ingesters-within`.

Rollout: enable on the write path, wait at least the lookback period, then enable on the read path. Decreasing a tenant's shard size while read-path sharding is on is unsafe; disable read-path sharding, decrease, wait the lookback, re-enable.

Query path: setting `-frontend.max-queriers-per-tenant` above 0 and below the number of queriers limits a tenant to that many queriers (set it on the query-scheduler when one is used). A tenant sending a "query of death" would otherwise get a replacement querier immediately, so set `-query-frontend.querier-forget-delay=1m` (or `-query-scheduler.querier-forget-delay=1m`) to delay the replacement.

Store-gateway: `-store-gateway.sharding-strategy=shuffle-sharding` and `-store-gateway.tenant-shard-size`, set on store-gateway, querier and ruler; per-tenant override `store_gateway_tenant_shard_size`.

Ruler: `-ruler.enable-sharding=true` with `-ruler.sharding-strategy=shuffle-sharding` and `-ruler.tenant-shard-size` (override `ruler_tenant_shard_size`); each rule group is still evaluated by a single ruler.

Compactor: `-compactor.sharding-enabled=true` with `-compactor.sharding-strategy=shuffle-sharding` and `-compactor.tenant-shard-size` (override `compactor_tenant_shard_size`).

Subrings are computed client-side and not stored in the ring, so the KV store sees no extra load; only a small memory increase, mostly in the distributor.

## Checked

Method: docs-checked 2026-11-09 against the Cortex shuffle sharding guide (raw markdown, read in full).
