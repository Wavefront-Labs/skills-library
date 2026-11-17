---
id: computing-software.cybersecurity-defensive.splunk.indexes-conf-bucket-lifecycle
name: indexes-conf-bucket-lifecycle
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, bucket-lifecycle, indexes-conf, frozentimeperiodinsecs, retention, coldtofrozendir, volumes, data-retention]
level: advanced
status: draft
description: "Design Splunk indexes.conf for security retention: hot/warm/cold/frozen buckets, frozenTimePeriodInSecs vs size limits, volumes, frozen archiving, and checking real retention."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Indexer/HowSplunkstoresindexes", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Indexesconf", "https://docs.splunk.com/Documentation/Splunk/latest/Indexer/Setaretirementandarchivingpolicy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# indexes.conf and the bucket lifecycle

Retention is a security requirement (investigations reach back months; regulations set minimums).
Splunk deletes data when **either** the age **or** the size limit is hit, whichever comes first.

## Bucket stages
hot (being written) -> warm (read-only, same volume) -> cold (cheaper volume) -> frozen
(deleted, or archived if configured) -> thawed (manually restored).

## Example
```
[volume:hotwarm]
path = /splunk/hot
maxVolumeDataSizeMB = 1800000

[volume:cold]
path = /splunk/cold
maxVolumeDataSizeMB = 6000000

[wineventlog]
homePath   = volume:hotwarm/wineventlog/db
coldPath   = volume:cold/wineventlog/colddb
thawedPath = $SPLUNK_DB/wineventlog/thaweddb
frozenTimePeriodInSecs = 31536000     # 365 days
maxTotalDataSizeMB = 2000000
maxDataSize = auto_high_volume         # 10 GB buckets for >10 GB/day indexes
coldToFrozenDir = /archive/splunk/wineventlog
repFactor = auto                       # replicate in an indexer cluster
```
- `thawedPath` cannot use a volume reference.
- `maxHotSpanSecs` (default 90 days) and `maxHotIdleSecs` control when hot buckets roll.
- A bucket freezes only when its **newest** event is older than frozenTimePeriodInSecs,
  so long-spanning buckets (events with bad timestamps) keep old data and block deletion.

## Sizing
daily ingest x compression (raw ~15% + tsidx ~35% of raw, so ~50%) x retention days x
replication factor / number of peers. Leave 20% headroom; volume caps freeze the oldest
buckets across **all** indexes on that volume when full.

## Archiving frozen data
`coldToFrozenDir` copies the raw journal (rawdata only) before delete; restoring means copying
to thaweddb and `splunk rebuild <bucket>`. Alternatively `coldToFrozenScript`. On SmartStore,
freezing behaves differently (remote store is the master copy).

## Check real retention
```
| dbinspect index=wineventlog
| stats min(startEpoch) as oldest by splunk_server
| eval days=round((now()-oldest)/86400)
```
If `days` is below policy, size limits are freezing early: check
`index=_internal sourcetype=splunkd component=BucketMover "freeze"` for the reason.

## Gotchas
- Changing paths on existing indexes does not move data; plan migrations.
- Index names are lowercase, no leading underscore (reserved for internal).
- In clusters, indexes.conf must be identical on all peers (deploy via manager bundle).

## Verify
dbinspect oldest-event age matches policy for each security index, and volumes are below 80%.
