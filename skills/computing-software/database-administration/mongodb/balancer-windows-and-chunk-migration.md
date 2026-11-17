---
id: computing-software.database-administration.mongodb.balancer-windows-and-chunk-migration
name: balancer-windows-and-chunk-migration
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, sharding, balancer-window, balancer, chunk-migration, range-deleter, sh-stopbalancer, active-window, data-size-balancing]
level: practitioner
status: docs-checked
description: "Control MongoDB's sharded cluster balancer: activeWindow scheduling, stopping it for backups and maintenance, migration throttling and range deletion."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/manage-sharded-cluster-balancer/
  - https://www.mongodb.com/docs/manual/core/sharding-balancer-administration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Balancer windows

**Goal:** chunk migrations happen when the cluster has spare capacity, never during backups or peak traffic.

## Status
```javascript
sh.getBalancerState()        // enabled?
sh.isBalancerRunning()       // a round in progress?
sh.status()                  // balancer state and chunk distribution
```

## Schedule a window (local time of the config server primary)
```javascript
use config
db.settings.updateOne({ _id: "balancer" },
  { $set: { activeWindow: { start: "01:00", stop: "05:00" } } }, { upsert: true })
// remove: db.settings.updateOne({ _id: "balancer" }, { $unset: { activeWindow: true } })
```
Ensure the window is long enough for the data growth per day; otherwise imbalance accumulates.

## Stop for maintenance / backups
```javascript
sh.stopBalancer()            // disables the balancer and waits for a running round to finish
// ... backup, rolling maintenance ...
sh.startBalancer()
sh.disableBalancing("app.events")   // per collection
sh.enableBalancing("app.events")
```
Backup tools that take inconsistent per-shard snapshots require the balancer off for the duration.

## How balancing works
- The balancer monitors the amount of data per shard for each sharded collection and migrates ranges when the difference between two shards reaches 3 x the configured `chunkSize` (default 128 MB, so 384 MB), while respecting zones.
- The balancer sends `moveRange` to the donor shard; after a move, the donor deletes the migrated range. Range deletion can be throttled with the `rangeDeleterBatchSize` and `rangeDeleterBatchDelayMS` parameters.
- `_secondaryThrottle` and `_waitForDelete` settings in `config.settings` trade migration speed for replica safety.

## Gotchas
- Window times are relative to the local time zone of the primary of the config server replica set.
- The balancer enforces zones (`sh.addShardToZone`, `sh.updateZoneKeyRange`), so data placement for zone changes follows the balancer's schedule.
- `activeWindowDOW` can also be set; if both `activeWindow` and `activeWindowDOW` exist, unset both to remove the schedule.

## Verify
`sh.status()` shows the balancer enabled with the expected window in `config.settings`; `db.coll.getShardDistribution()` stays within tolerance.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: activeWindow set on config.settings _id balancer and removal with $unset (plus activeWindowDOW), window relative to the config server primary's local time zone, sh.stopBalancer/sh.disableBalancing, migration threshold of 3 x chunkSize (384 MB at the 128 MB default), moveRange sent by the balancer, rangeDeleterBatchSize and rangeDeleterBatchDelayMS, _secondaryThrottle and _waitForDelete. Removed unconfirmed version attributions, actionlog/changelog queries, daylight-saving and queued-deletion claims.

Method: documentation only; no commands were run.
