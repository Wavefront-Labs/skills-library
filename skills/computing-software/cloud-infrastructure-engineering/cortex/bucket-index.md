---
id: computing-software.cloud-infrastructure-engineering.cortex.bucket-index
name: bucket-index
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [bucket-index, object-storage, store-gateway, querier, compactor]
level: advanced
status: docs-checked
description: "Use the per-tenant bucket index so queriers and store-gateways stop listing the object store, and know how the compactor maintains it."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/blocks-storage/bucket-index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The bucket index is a per-tenant file, `bucket-index.json.gz`, stored in the object store. It lists the tenant's complete blocks (including those marked for deletion; partial blocks are excluded), the block deletion marks, and an `updated_at` Unix timestamp.

It is enabled by default; disabling it with `-blocks-storage.bucket-store.bucket-index.enabled=false` is not recommended in production.

Why: queriers, store-gateways and rulers need a nearly current view of every block. Without the index they scan the bucket with list-objects calls. With it they read one file per tenant, which means fewer object-store API calls, no list calls from queriers and store-gateways, and a querier that is ready immediately after start without an initial bucket scan.

The compactor builds and updates the index periodically; frequency is set with `-compactor.cleanup-interval`. It builds the index even when the feature is not enabled for readers. That is intentional: enabling it later on a live cluster finds indexes already present, so query results stay consistent through the switch.

Querier and ruler behaviour: the index is downloaded lazily on a tenant's first query and cached in memory, refreshed in the background at `-blocks-storage.bucket-store.sync-interval`; a failed download is retried after `-blocks-storage.bucket-store.bucket-index.update-on-error-interval`; an index unused for `-blocks-storage.bucket-store.bucket-index.idle-timeout` is offloaded. If the index's `updated_at` is older than `-blocks-storage.bucket-store.bucket-index.max-stale-period`, the query fails rather than return partial results. The store-gateway fetches the index for each tenant in its shard at startup and periodically, as the source of truth for blocks.

## Checked

Method: docs-checked 2026-11-09 against the Cortex bucket index page (raw markdown, read in full).
