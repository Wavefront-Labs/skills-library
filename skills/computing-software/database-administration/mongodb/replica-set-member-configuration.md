---
id: computing-software.database-administration.mongodb.replica-set-member-configuration
name: replica-set-member-configuration
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, replica-set, hidden-member, delayed-member, priority, votes, arbiter, rs-reconfig, secondary-delay-secs]
level: practitioner
status: docs-checked
description: "Configure MongoDB replica set members with rs.reconfig: priority, votes, hidden and delayed members, and why arbiters are risky with majority write concern."
sources:
  - https://www.mongodb.com/docs/manual/reference/replica-configuration/
  - https://www.mongodb.com/docs/manual/core/replica-set-hidden-member/
  - https://www.mongodb.com/docs/manual/core/replica-set-delayed-member/
  - https://www.mongodb.com/docs/manual/core/replica-set-arbiter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replica set member configuration

**Goal:** design members for failover, backups and analytics without breaking elections or majority writes.

## Edit config
```javascript
cfg = rs.conf()
cfg.members[1].priority = 2            // preferred primary (0..1000, default 1, 0 = never primary)
cfg.members[3].priority = 0
cfg.members[3].hidden = true           // invisible to client applications
cfg.members[4].priority = 0
cfg.members[4].hidden = true
cfg.members[4].secondaryDelaySecs = 3600
cfg.members[4].votes = 0
rs.reconfig(cfg)
```
Changing a member's priority triggers one or more elections, and the election is best-effort: a lower-priority member can still become primary, after which the server keeps calling elections until the highest-priority member is primary.

## Member types
| Type | Settings | Use |
|---|---|---|
| Normal | priority >= 1 | Electable |
| Priority 0 | `priority: 0` | DR site member that must never be primary |
| Hidden | `priority: 0, hidden: true` | Backups, reporting via direct connection; no app traffic |
| Delayed | hidden + `secondaryDelaySecs` | Protection from human error (drop/delete) |
| Non-voting | `votes: 0, priority: 0` | More than 7 members (a set has up to 50 members but only 7 voting) |
| Arbiter | `rs.addArb()` | Exactly 1 vote, no data, priority 0 by default |

Rules: members with `priority` above 0 cannot have `votes: 0`, and non-voting members must have priority 0.

## Arbiters: avoid
- In a primary-secondary-arbiter (PSA) set, `w: "majority"` can cause performance issues if the secondary is unavailable or lagging, because the majority commit point lags and puts pressure on the cache. The implicit default write concern drops to `{ w: 1 }` when data-bearing voting members are not more than the voting majority.
- In a sharded cluster, a PSA shard can lose availability when its data-bearing secondary is down, since shards run `w: "majority"` operations.
- Transactions spanning shards abort if they touch a shard that contains an arbiter, and you cannot change a shard key with a transaction when the set has an arbiter.
- Use at most one arbiter. From 5.3 multiple arbiters are refused unless every node starts with `--setParameter allowMultipleArbiters=true`.
- Never run an arbiter on a host that also runs the primary or a secondary. Prefer three data-bearing members.

## Delayed members
- Must be priority 0 and hidden. Make them non-voting (`votes: 0`) so they do not count toward `w: "majority"`; a voting delayed member can make majority writes wait for the delay when another secondary is down.
- The delay must be at least your maintenance window and smaller than the oplog capacity.
- A delayed member can acknowledge `w: <number>` writes (no earlier than `secondaryDelaySecs`) but needs `votes > 0` to acknowledge `w: "majority"`.
- Of limited use in sharded clusters with the balancer enabled, because chunk migrations replicate with the delay.

## Gotchas
- Aim for an odd number of votes (that is what an arbiter provides when there are two data-bearing members).
- Hidden members can still vote and can acknowledge majority writes if `votes > 0`.
- `buildIndexes: false` can only be set when adding a member and needs `priority: 0`.

## Verify
`rs.status()` shows members; `rs.conf()` shows priorities, votes and `hidden`; `db.hello()` does not display hidden members.

## Checked
2026-10-31. Against the MongoDB manual pages Replica Set Configuration, Hidden Members, Delayed Members and Arbiter: priority range, default and election behaviour, 50 members / 7 voting, votes and priority rules, `secondaryDelaySecs` and delayed-member requirements, `db.hello()` and hidden members, arbiter vote, PSA and sharding warnings, single arbiter and the 5.3 `allowMultipleArbiters` parameter. Removed unconfirmed details: `rs.reconfigForPSASet()`, the "5.0+ name; slaveDelay before" note, the `votes: 0` rescue for a failed PSA secondary, the force-reconfig advice, and the WiredTiger cache wording.
Method: documentation only; no commands were run.
