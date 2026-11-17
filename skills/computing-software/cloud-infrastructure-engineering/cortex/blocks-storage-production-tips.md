---
id: computing-software.cloud-infrastructure-engineering.cortex.blocks-storage-production-tips
name: blocks-storage-production-tips
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [production, file-descriptors, disk-sizing, ingester, querier]
level: advanced
status: docs-checked
description: "Apply Cortex blocks storage production tips: ulimits, ingester disk sizing, querier caching and the bucket index."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/blocks-storage/production-tips.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ingester open files: the ingester holds file descriptors for TSDB WAL segments, chunk files and compacted blocks that have not hit retention, loaded via mmap. With many tenants or a long `-blocks-storage.tsdb.retention-period`, it can hit the `file-max` ulimit. Raise the limit or enable shuffle sharding. Rule of thumb: never below 65536, with higher values such as 1048576 recommended.

Ingester disk: ingesters cut a block every 2 hours (configurable) and are typically configured to keep blocks longer, to recover if uploading to long-term storage fails and to reduce querier work. With `-blocks-storage.tsdb.retention-period=24h`, estimate disk as the number of series after replication times 30KB. For example 20M active series replicated three ways comes to about 1.7TB; across 20 ingesters allow 100GB each, or 150GB to be comfortable.

Querier: make sure caching is configured and the cache (memcached) is scaled properly, because the querier relies on it to cut object-store API calls. Also ensure the bucket index is enabled, so the querier is ready immediately and makes fewer calls.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Production tips (blocks storage) (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
