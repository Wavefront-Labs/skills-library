---
id: computing-software.database-administration.mongodb.initial-sync-resync-member
name: initial-sync-resync-member
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, replica-set, initial-sync, resync-member, too-stale, file-copy-based-initial-sync, logical-initial-sync, recovering-state]
level: practitioner
status: docs-checked
description: "Resync a stale or corrupted MongoDB replica set member via logical or file-copy initial sync, or by seeding from a snapshot, and monitor progress."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/resync-replica-set-member/
  - https://www.mongodb.com/docs/manual/core/replica-set-sync/
  - https://www.mongodb.com/docs/manual/reference/parameters/#mongodb-parameter-param.initialSyncMethod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resyncing a member (initial sync)

**Goal:** bring back a stale member (it fell so far behind that the primary overwrote the oplog entries it needs) or one with damaged data.

## Option A: automatic initial sync (empty dbPath)
1. `db.adminCommand({ shutdown: 1 })` on the member (or stop the service).
2. Move the data directory aside (keep it until done): `mv /var/lib/mongo /var/lib/mongo.old && mkdir /var/lib/mongo && chown mongod: /var/lib/mongo`.
3. Start mongod with the same config. It clones all databases from a sync source, then applies the oplog that accumulated meanwhile.

Sync source: set `initialSyncSourceReadPreference` (startup-only parameter; modes primary, primaryPreferred, secondary, secondaryPreferred, nearest) to choose the source, for example `secondary` to keep load off the primary. Defaults: `primaryPreferred` for voting members, `nearest` for newly added or non-voting members, `primary` if chaining is disabled.

## Logical vs file copy
| Method | Notes |
|---|---|
| `logical` (default) | Copies documents, rebuilds every index; slow for large data; source does reads |
| `fileCopyBased` (Enterprise, 5.2+) | Copies the source's WiredTiger files (replacing the target's `local` database); set `initialSyncMethod: "fileCopyBased"` at startup. No backups on source or target and no writes to the target's `local` database during the sync |

## Monitor
```javascript
db.adminCommand({ replSetGetStatus: 1, initialSync: 1 }).initialSyncStatus
// databases.databasesCloned, databasesToClone, collectionsCloned ...
```
When the initial sync finishes the member moves from STARTUP2 to SECONDARY.

## Option B: seed from a snapshot (huge datasets)
Take a snapshot backup of another member (a mongodump backup cannot be used; the copy must include the `local` database), put it in the target's dbPath and start mongod with a new `members[n]._id`. It only replays the oplog since the snapshot, so the data files must be recent enough to catch up from the oplog; otherwise it needs a full initial sync.

## Gotchas
- The oplog window must cover the time of the final steps of the sync (checking continuity and applying oplog); on a gap the initial sync restarts from the beginning, and the member retries up to 10 times before exiting. Grow the oplog first for big datasets.
- The target needs free disk space in its `local` database to hold oplog records pulled during the data copy.
- Do not delete the old dbPath until the member is SECONDARY and healthy.

## Verify
`rs.status()` shows the member as SECONDARY with `optimeDate` close to the primary's; `db.stats()` sizes are comparable across members.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: initialSyncSourceReadPreference modes, defaults and startup-only setting, logical vs fileCopyBased initial sync (Enterprise, 5.2, initialSyncMethod at startup, limitations), replSetGetStatus initialSync:1 and initialSyncStatus.databases fields, STARTUP2 to SECONDARY transition, restart on oplog gap and up to 10 attempts, local database space needed for pulled oplog, seeding from a snapshot copy including local with a new member _id (mongodump not usable). Removed unconfirmed status field names, the RECOVERING step and the Percona backup mention.

Method: documentation only; no commands were run.
