---
id: computing-software.database-administration.mongodb.rolling-maintenance-on-replica-sets
name: rolling-maintenance-on-replica-sets
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, rolling-maintenance, mongodb-replication, rolling-restart, maintenance-mode]
level: practitioner
status: docs-checked
description: "Perform OS patching, config changes or hardware swaps on a MongoDB replica set one member at a time with no downtime: order, checks, stepDown, and verification."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/perform-maintence-on-replica-set-members/
  - https://www.mongodb.com/docs/manual/reference/method/rs.stepDown/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling maintenance on replica set members

**Goal:** patch or reconfigure every member while the set stays writable.

## Pre-checks
```javascript
rs.status().members.map(m => [m.name, m.stateStr, m.optimeDate])
```
Confirm every member is healthy and caught up before taking one down.

## Order
Secondaries first, primary last.

For each secondary:
1. `db.adminCommand({ shutdown: 1 })` (or `systemctl stop mongod`).
2. Do the work (patch, change `mongod.conf`, resize disk).
3. Start `mongod`; wait for `stateStr: "SECONDARY"` and lag near 0 before moving on.

For the primary:
1. `rs.stepDown(120)` and confirm another member is PRIMARY.
2. Repeat the secondary steps on the old primary.


## Gotchas
- Never take down two voting members of a 3-member set at once: majority is lost and writes stop.

## Verify
After the last member: all SECONDARY/PRIMARY, lag near 0, and application error logs show only the expected brief retry during stepDown.

## Checked

2026-10-28. Confirmed against MongoDB manual maintenance tutorial and rs.stepDown page: perform maintenance on the primary last, db.shutdownServer / shutdown command, rs.stepDown(stepDownSecs) with the primary becoming ineligible for that period and eligible secondaries holding an election, majority means a majority of voting members. Removed unconfirmed: oplog window helpers and resync rule, standalone isolation step, priority takeover, the shell wait loop, wtimeout and FCV and sharded-cluster notes.

Method: documentation only; no commands were run.
