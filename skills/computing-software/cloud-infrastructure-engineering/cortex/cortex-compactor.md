---
id: computing-software.cloud-infrastructure-engineering.cortex.cortex-compactor
name: cortex-compactor
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [compactor, compaction, sharding, deduplication, bucket-index]
level: practitioner
status: docs-checked
description: "Understand vertical and horizontal compaction in the Cortex compactor, per-tenant sharding, and its role in keeping the bucket index current."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/blocks-storage/compactor.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The compactor is stateless and does two jobs: it merges multiple blocks of a tenant into larger optimized blocks (reducing storage cost through deduplication and index size reduction, and speeding queries by reducing block count), and it keeps each tenant's bucket index updated.

Compaction has two stages:

- Vertical compaction merges all blocks a tenant's ingesters uploaded for the same time range (2 hours by default) into one block, de-duplicating the samples that exist N times because of replication. This reduces blocks per 2-hour range from the number of ingesters to one.
- Horizontal compaction runs after that and combines blocks with adjacent 2-hour ranges into a larger one. Chunk size does not change, but the index and the index-header held in store-gateway memory shrink significantly.

Sharding is optional. When enabled, compactor instances split work by tenant using the hash ring: all blocks of one tenant are processed by a single instance at a time, while different tenants compact in parallel on different instances. When compactors are added or removed, tenants are resharded automatically without manual intervention.

## Checked

Method: docs-checked 2026-11-09 against the Cortex blocks-storage compactor.md (raw markdown, master; read the overview, how-compaction-works and sharding sections). Claims match the page.
