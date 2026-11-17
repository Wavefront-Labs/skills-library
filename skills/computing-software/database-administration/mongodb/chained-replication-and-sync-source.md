---
id: computing-software.database-administration.mongodb.chained-replication-and-sync-source
name: chained-replication-and-sync-source
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, chained-replication, sync-source, mongodb-replication, replsetsyncfrom]
level: practitioner
status: docs-checked
description: "Understand MongoDB chained replication and sync source selection, when to disable chaining, and how to pin a member's sync source with replSetSyncFrom."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/manage-chained-replication/
  - https://www.mongodb.com/docs/manual/core/replica-set-sync/
  - https://www.mongodb.com/docs/manual/reference/command/replSetSyncFrom/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chained replication and sync source selection

**Goal:** know which member each secondary pulls the oplog from, and control it when cross-region lag or load matters.

## Defaults
- `settings.chainingAllowed: true`: a secondary may sync from another secondary that is closer (lowest ping) and ahead of it.
- A candidate whose newest oplog entry is more than `maxSyncSourceLagSecs` (default 30) behind the primary is rejected as a sync source.
- `initialSyncSourceReadPreference` (read preference mode; default `primaryPreferred` for voting members, `nearest` for newly added or non-voting members, `primary` when chaining is disabled) selects the source for initial sync and takes precedence over `chainingAllowed` for that sync.

## See current sources
```javascript
rs.status().members.map(m => [m.name, m.stateStr, m.syncSourceHost])
```

## Disable chaining
Useful when chained hops add lag in cross-region sets or `w:majority` latency suffers:
```javascript
cfg = rs.conf(); cfg.settings.chainingAllowed = false; rs.reconfig(cfg)
```
With chaining off, secondaries sync from the primary (chained replication can reduce primary load, so expect more load on it).

## Pin a source temporarily
```javascript
db.adminCommand({ replSetSyncFrom: "db3.eu.example.net:27017" })   // run on the secondary
```
`replSetSyncFrom` (or `rs.syncFrom()`) only overrides the sync target when `settings.chainingAllowed` is `true`: with chaining disabled it returns `ok: 1` but does not set the target, unless the server parameter `enableOverrideClusterChainingSetting` is `true` (5.0.2+). The target must have data, be reachable, be in the same set and build indexes. The override reverts when the mongod restarts, the connection to the target closes, or the target falls more than `maxSyncSourceLagSecs` behind another member. Running it during an initial sync restarts that sync with the new target. Use it to keep a DR member syncing from a local peer instead of crossing the WAN.

## Gotchas
- A chain makes lag cumulative; monitor lag of the last hop, not just the first.
- `enableOverrideClusterChainingSetting` (5.0.2+, startup parameter, default false) lets secondaries replicate from other secondaries even when the set disables chaining.

## Verify
After the change, `syncSourceHost` shows the expected host and `rs.printSecondaryReplicationInfo()` shows lag stable or better.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: settings.chainingAllowed behaviour and ping-based selection, maxSyncSourceLagSecs default 30, initialSyncSourceReadPreference modes and defaults, enableOverrideClusterChainingSetting (5.0.2, default false), replSetSyncFrom limitations (needs chainingAllowed true else ok:1 with no effect; reverts on restart, closed connection or lagging target), syncSourceHost in replSetGetStatus. Corrected: the previous text implied replSetSyncFrom works with chaining disabled.

Method: documentation only; no commands were run.
