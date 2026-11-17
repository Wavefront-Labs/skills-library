---
id: computing-software.cloud-infrastructure-engineering.google-cloud.memorystore-scaling-upgrades-maintenance-and-import-export
name: memorystore-scaling-upgrades-maintenance-and-import-export
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, memorystore, memorystore-scaling, resize-redis, redis-version-upgrade, memorystore-upgrade, memorystore-maintenance, redis-import-export, rdb-import]
level: practitioner
status: docs-checked
description: "Day-2 Memorystore for Redis: resize and add replicas, upgrade Redis versions, set maintenance windows and rescheduling, and move data with RDB import and export."
sources: ["https://docs.cloud.google.com/memorystore/docs/redis/scale-instances", "https://docs.cloud.google.com/memorystore/docs/redis/upgrade-redis-version", "https://docs.cloud.google.com/memorystore/docs/redis/about-maintenance", "https://docs.cloud.google.com/memorystore/docs/redis/about-importing-exporting", "https://redis.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memorystore for Redis: scaling, upgrades, maintenance and import/export

Tiers (API `Instance.tier`): `BASIC` is a standalone instance; `STANDARD_HA` has primary and replica nodes.

## 1. Scale
```bash
gcloud redis instances describe cache --region=<REGION> --format='value(tier,memorySizeGb,replicaCount,redisVersion)'
gcloud redis instances update cache --region=<REGION> --size=16              # GiB
gcloud redis instances update cache --region=<REGION> --replica-count=3 --read-replicas-mode=READ_REPLICAS_ENABLED
```
Export data before scaling, and scale Standard Tier at low traffic. When reducing a Standard Tier instance
you must choose a size greater than the data stored, or scaling fails (a 10 GB instance holding 5.5 GB can
go to 6 GB at minimum). Replica count can change only with read replicas enabled
(`READ_REPLICAS_DISABLED` is the default). Redis Cluster has its own scaling page (Scale instance capacity).

## 2. Upgrade Redis version
```bash
gcloud redis instances upgrade cache --region=<REGION> --redis-version=redis_7_2
```
You can upgrade to any newer version. Accepted values on the page: `redis_4_0`, `redis_5_0`, `redis_6_x`,
`redis_7_0`, `redis_7_2`. Check client compatibility and the Version upgrade behavior page first.

## 3. Maintenance
```bash
gcloud redis instances update cache --region=<REGION> --maintenance-window-day=SUNDAY --maintenance-window-hour=3
gcloud redis instances describe cache --region=<REGION> --format='yaml(maintenancePolicy,maintenanceSchedule)'
gcloud redis instances reschedule-maintenance cache --region=<REGION> --reschedule-type=NEXT_AVAILABLE_WINDOW
# other types: IMMEDIATE, or SPECIFIC_TIME with --schedule-time=<RFC3339_TIMESTAMP>
```
- A window is a day and start hour and lasts 1 hour. Without a window, maintenance can begin at any time
  without advance notice.
- Both tiers get a connection reset: clients need retries with exponential backoff. Standard Tier fails
  over (typically about 15 seconds); Basic Tier is unavailable (typically about 5 minutes).
- Notifications are off by default: set a window and opt in at least 7 days ahead; the email goes at
  least one week before maintenance to the Google account address only.
- Reschedule up to two times, each not more than one week after the original time.
- Scheduling for low traffic, or scaling up so System Memory Usage Ratio is 50% or lower, is recommended.

## 4. Import and export (RDB)
```bash
SA=$(gcloud redis instances describe cache --region=<REGION> --format='value(persistenceIamIdentity)')
gcloud redis instances export gs://<BUCKET>/cache.rdb cache --region=<REGION>
gcloud redis instances import gs://<BUCKET>/from-onprem.rdb cache-new --region=<REGION>
```
Grant `$SA` access to the bucket first (see "Granting restricted permissions for import and export").
- Import makes the instance unavailable and overwrites existing data on success; on failure data may be
  fully flushed. Cancelling an import leaves a fully flushed cache.
- An instance imports RDB files from the same or an older Redis version, never a newer one.
- During export you can read and write but cannot do admin operations. Under high write load memory can
  reach 2X and the export can fail; keep 50% free memory. Exports cannot run during a BGSAVE.
- Requester Pays buckets are not supported; use buckets in the instance's region.
- Monitor with `gcloud redis instances describe` (state `IMPORTING` or `READY`).

## Verify
- [ ] After changes, `describe` shows the expected size and version.
- [ ] A restore drill imports the latest export into a scratch instance and key counts match.

## Checked
2026-10-28. Confirmed against the Memorystore for Redis Scale, Upgrade, About maintenance and About
importing and exporting pages, plus the Redis API v1 discovery document (tiers, `readReplicasMode`,
`persistenceIamIdentity`, reschedule types). Commands were checked against the gcloud reference.
Removed: `usage_ratio` alert threshold, the Redis Cluster shard command, the Storage role name, the
`DBSIZE`/`connected_clients` checks and claims that Basic tier operations always flush the cache.
Method: documentation only; no commands were run.
