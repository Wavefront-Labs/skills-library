---
id: computing-software.database-administration.mongodb.force-reconfig-with-unavailable-members
name: force-reconfig-with-unavailable-members
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, force-reconfig, replica-set-recovery, mongodb-replication, rs-reconfig]
level: practitioner
status: docs-checked
description: "Recover a MongoDB replica set that lost its majority by force-reconfiguring from a surviving member, with the risks, steps and clean-up afterward."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/reconfigure-replica-set-with-unavailable-members/
  - https://www.mongodb.com/docs/manual/reference/method/rs.reconfig/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Force reconfig with unavailable members

**Goal:** bring a replica set back to writable when most members are permanently lost (e.g. a data centre with 2 of 3 members burned down) and only a secondary survives.

## When it is legitimate
Only to recover from catastrophic interruptions, when a majority of members are down or unreachable. Never use `force` when there is still a primary, in automatic scripts, or as your routine way to reconfigure. If the failure or partition was only temporary, shut down or decommission the removed members as soon as possible.

## Steps
1. Back up a surviving member, then connect to a surviving member.
2. Build a config with only reachable members:
```javascript
cfg = rs.conf()
printjson(cfg.members.map(m => m.host))
cfg.members = [cfg.members[2]]            // keep survivors only
rs.reconfig(cfg, { force: true })
```
3. The forced configuration is propagated to the surviving members listed in `members`, and the set then elects a new primary.
4. Immediately shut down and wipe (or keep isolated) the lost members' data if they could reappear; re-add them as fresh members so they initial-sync:
```javascript
rs.add({ host: "db2.example.net:27017", priority: 0, votes: 0 })   // add as non-voting first
// after it reaches SECONDARY:
cfg = rs.conf(); cfg.members[1].priority = 1; cfg.members[1].votes = 1; rs.reconfig(cfg)
```

## Risks
- Forcing a configuration is dangerous (see the manual's force warning); the manual warns it can cause unexpected behaviour including rollback of `majority`-committed writes.
- `force: true` raises the configuration version by tens or hundreds of thousands; this is normal and prevents version collisions if you accidentally force reconfigurations on both sides of a partition.
- Applications using the old seed list may still try lost hosts; update connection strings.

## Alternative for partial loss
If a majority still exists, never use force; use a normal `rs.reconfig()` to remove dead members.

## Verify
`rs.status()` shows one PRIMARY and the expected members; `rs.conf().version` increased sharply; a test write with `w: "majority"` succeeds.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: force reconfiguration is for catastrophic loss of a majority, never when a primary exists or in scripts, procedure (back up a surviving member, save rs.conf(), set cfg.members to survivors, rs.reconfig(cfg, {force: true})), config version rises by tens or hundreds of thousands, the force warning (unexpected behaviour including rollback of majority-committed writes), removed members should be shut down or decommissioned and resynced, normal rs.reconfig() when a majority is available. Removed unconfirmed optime-selection and rollback-file claims.

Method: documentation only; no commands were run.
