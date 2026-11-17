---
id: computing-software.database-administration.mongodb.rollbacks-during-failover
name: rollbacks-during-failover
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-rollback, rollback-files, write-concern-majority, mongodb-replication]
level: practitioner
status: docs-checked
description: "Understand, prevent and recover MongoDB replica set rollbacks after failover: why writes roll back, where rollback files go, and how w:majority avoids them."
sources:
  - https://www.mongodb.com/docs/manual/core/replica-set-rollbacks/
  - https://www.mongodb.com/docs/manual/reference/write-concern/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rollbacks during failover

**Goal:** know when acknowledged writes can disappear and how to stop that.

## Why rollback happens
A primary accepts writes, steps down before secondaries replicate them, and a secondary is elected. When the old primary rejoins as a secondary it reverts ("rolls back") those operations to match the new primary. Rollbacks should be rare and are often the result of a network partition; secondaries that cannot keep up make the rollback larger.

## Prevention
- Run all voting members with journaling and use `w: "majority"` for writes that matter. `{ w: 1 }` only acknowledges on the primary, so data can roll back if the primary steps down before any secondary has it (this includes multi-document transactions committed with `w: 1`).
- Starting in 5.0 `{ w: "majority" }` is the implicit default write concern for most deployments. Exception: if the number of data-bearing voting members is not greater than the voting majority (for example a primary-secondary-arbiter set), the implicit default is `{ w: 1 }`.
- Keep `writeConcernMajorityJournalDefault` at its default `true`. If false, majority writes are acknowledged without waiting for the journal and could roll back after a transient loss (crash and restart) of a majority of nodes.
- Reads at `local` or `available` read concern can see data that is later rolled back.

## Where rolled-back data goes
By default MongoDB writes the rolled-back data to BSON files. For each affected collection:
```
<dbpath>/rollback/<collectionUUID>/removed.<timestamp>.bson
```
The `createRollbackDataFiles` parameter controls whether these files are created. Not written to the rollback directory: a rolled-back collection drop or document deletion. With `w: 1`, writes submitted after an oplog hole may also be missing if the primary restarts first.

To find the collection name for a UUID, search the log for `rollback file` (`grep "rollback file" <mongod log>`) or loop over databases with `db.getCollectionInfos({ "info.uuid": UUID("...") })`.

## Recover the data
Read the files with `bsondump` and, knowing your application, decide whether to re-apply or discard each document:
```bash
bsondump <dbPath>/rollback/<collectionUUID>/removed.<timestamp>.bson > rolled_back.json
```
Do not blindly restore into the live collection; later writes may conflict.

## Limits
- Default algorithm (recover to a timestamp): no limit on the amount of data rolled back.
- Rollback via refetch applies only when `enableMajorityReadConcern` is false (not changeable from 5.0) and can roll back up to 300 MB.
- Time limit: defaults to 24 hours, set by `rollbackTimeLimitSecs`; measured from the first common oplog operation to the last entry of the member being rolled back.
- From 4.2, MongoDB kills in-progress user operations when a member enters `ROLLBACK`.

## Verify
Search the log for `rollback file` after any unplanned failover and alert if files appear under `rollback/`. In tests, kill the primary while writing with `w:1` vs `w:"majority"` to demonstrate the difference.

## Checked
2026-10-31. Against the MongoDB manual pages "Rollbacks During Replica Set Failover" and "Write Concern": rollback cause, `<dbpath>/rollback/<collectionUUID>/removed.<timestamp>.bson` layout, exclusions, `w: 1` risk, 5.0 majority default and the arbiter exception, `writeConcernMajorityJournalDefault`, 300 MB refetch limit, 24 hour `rollbackTimeLimitSecs` default and the 4.2 operation kill. Removed unconfirmed details: the older `<db>.<collection>` directory layout, `mongorestore` command, "member shuts down and must be resynced" and the `getDefaultRWConcern` command.
Method: documentation only; no commands were run.
