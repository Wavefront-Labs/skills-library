---
id: computing-software.cybersecurity-defensive.splunk.smartstore-remote-storage
name: smartstore-remote-storage
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, smartstore, s2, remote-storage, s3, cachemanager, indexes-conf, cache-eviction, retention]
level: advanced
status: draft
description: "Move Splunk indexes to SmartStore object storage: remote volume config, cache sizing, migration steps and the operational limits that bite afterwards."
sources: ["Splunk Docs - Managing Indexers and Clusters (About SmartStore, Configure SmartStore)", "Splunk Docs - indexes.conf and server.conf cachemanager settings"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SmartStore (remote object storage for indexes)

**Goal:** decouple storage from indexers so retention scales on S3-compatible object
storage while recent, frequently searched buckets stay in a local cache.

## Configure (indexes.conf, pushed via the cluster bundle)
```
[volume:remote_store]
storageType = remote
path = s3://splunk-smartstore-prod/indexes
remote.s3.endpoint = https://s3.eu-west-1.amazonaws.com
remote.s3.encryption = sse-kms
remote.s3.kms.key_id = <kms key arn>

[default]
remotePath = volume:remote_store/$_index_name
repFactor = auto
maxDataSize = auto
```
Prefer instance roles (IAM) over access keys. All peers must point to the same remotePath.

## Cache sizing (server.conf on peers)
```
[cachemanager]
max_cache_size = 0
eviction_padding = 5120
hotlist_recency_secs = 86400
```
`max_cache_size = 0` lets the cache use the disk minus `minFreeSpace`. Size local disk to
hold the period most searches cover (typically 7-30 days of ingest after compression and
replication), otherwise searches keep re-downloading buckets and slow sharply.

## Migration
1. Validate on a test index first; check `| rest /services/admin/cacheman` for upload activity.
2. Enable on existing indexes via bundle push; existing warm buckets upload in the background.
3. Watch `index=_internal sourcetype=splunkd component=CacheManager` for upload/download errors.
Treat migration as one-way.

## Limits and gotchas
- Retention is enforced by `frozenTimePeriodInSecs` and `maxGlobalDataSizeMB`; `maxTotalDataSizeMB`
  does not govern total size on SmartStore indexes.
- Do not put object lifecycle expiry rules on the bucket: Splunk must manage deletion.
- Bucket versioning increases cost; add a short noncurrent-version expiry if you must keep it on.
- Accelerated data model summaries stay local and are rebuilt after cache eviction.
- Searches over long ranges (a year of firewall logs) pull everything back into cache: steer
  them to summary indexes.

## Verify
- [ ] `splunk cmd splunkd rfs -- ls --starts-with volume:remote_store` lists buckets.
- [ ] Cache hit ratio for typical searches stays high (SmartStore panels in the Monitoring Console).
- [ ] A search older than the cache window completes and its buckets show as downloaded.
