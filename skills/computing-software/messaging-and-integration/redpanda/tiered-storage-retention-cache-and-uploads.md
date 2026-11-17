---
id: computing-software.messaging-and-integration.redpanda.tiered-storage-retention-cache-and-uploads
name: tiered-storage-retention-cache-and-uploads
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [tiered-storage, retention, local-retention, cache, pause-uploads, logdirs, remote-write]
level: advanced
status: docs-checked
description: "Size Tiered Storage retention and local capacity, inspect usage with rpk cluster logdirs describe, tune the cache, and pause uploads with cloud_storage_enable_segment_uploads."
sources:
  - https://docs.redpanda.com/streaming/current/manage/tiered-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Retention.** Since 22.3, retention properties work the same for tiered and local topics. `retention.ms` and `retention.bytes` apply to object storage per partition, and both limits apply together. A `compact` cleanup policy deletes nothing from object storage by retention; `compact,delete` deletes by `retention.ms` and `retention.bytes`.

**Local capacity.** Local data expires after `retention.local.target.ms` or `retention.local.target.bytes` (cluster defaults `retention_local_target_ms_default` and `retention_local_target_bytes_default`). New topics default to one day locally and seven days overall (`log_retention_ms`); upgraded topics keep infinite retention. Disabling Tiered Storage does not remove data already uploaded.

**Usage.** `rpk cluster logdirs describe` lists local directories and `remote://<bucket_name>` entries. Object storage is shared by brokers, so third-party tools may over-count.

**Remote write** uploads segments per partition from the leader. See state with `rpk topic describe-storage <topic_name> --print-all`. For idle topics, `cloud_storage_segment_max_upload_interval_sec` forces uploads; if null, metadata uploads but segments wait for `segment.bytes`.

**Pause uploads** (25.1+), with in-flight uploads completing:

```bash
rpk cluster config set cloud_storage_enable_segment_uploads false
rpk cluster config set cloud_storage_enable_segment_uploads true
```
Watch `redpanda_cloud_storage_paused_archivers`. Do not use `redpanda.remote.write` or `redpanda.remote.read` to pause; it can leave a gap between local and uploaded data.

**Cache.** Set the location with `cloud_storage_cache_directory`; the size is the minimum of `cloud_storage_cache_size` and `cloud_storage_cache_size_percent` (raise the percentage with a dedicated disk). `cloud_storage_cache_trim_threshold_percent_size` of 70% is suggested for most cases. Chunk eviction strategies: `eager` (default), `capped`, `predictive`.

## Checked

2026-11-04. Retention, usage, pause and cache details were confirmed on the Tiered Storage page.

Method: documentation only; no commands were run.
