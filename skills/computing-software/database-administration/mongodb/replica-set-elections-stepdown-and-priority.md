---
id: computing-software.database-administration.mongodb.replica-set-elections-stepdown-and-priority
name: replica-set-elections-stepdown-and-priority
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, replica-set-elections, rs-stepdown, priority-takeover, mongodb-replication, electiontimeoutmillis]
level: practitioner
status: docs-checked
description: "Control MongoDB replica set elections: priorities, rs.stepDown for planned switchover, electionTimeoutMillis, catchUpTimeoutMillis and what writes do during a stepdown."
sources:
  - https://www.mongodb.com/docs/manual/core/replica-set-elections/
  - https://www.mongodb.com/docs/manual/reference/method/rs.stepDown/
  - https://www.mongodb.com/docs/manual/reference/replica-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elections, stepDown and priority

**Goal:** make primary changes predictable: the right member wins, planned switchovers are short, and unplanned elections are understood.

## How an election happens
- Members send heartbeats to each other every two seconds. A heartbeat that does not return within 10 seconds marks the member inaccessible (`settings.heartbeatTimeoutSecs`, default 10 seconds).
- `settings.electionTimeoutMillis` (default 10000) is the time limit for detecting that the primary is unreachable; it controls failover sensitivity with `protocolVersion: 1`, and failover detection is not expected to exceed it.
- A replica set can have up to 50 members but only 7 voting members; set `members[n].votes` to 0 for extra members. Do not change votes to control who becomes primary: change `members[n].priority` instead.

## Priorities
```javascript
cfg = rs.conf()
cfg.members[0].priority = 2     // preferred primary (DC1)
cfg.members[1].priority = 1
cfg.members[2].priority = 0     // never primary (DR site or backup node)
rs.reconfig(cfg)
```

## Planned switchover
```javascript
// on the current primary
rs.stepDown(60, 10)   // stepDownSecs=60 (cannot be primary again for 60 s), secondaryCatchUpPeriodSecs=10
```
`stepDownSecs` must be greater than `secondaryCatchUpPeriodSecs`; a non-numeric `stepDownSecs` means 60 seconds. If no electable secondary is up to date, the primary waits up to `secondaryCatchUpPeriodSecs` (default 10 seconds); if none catches up, it does not step down and the method errors. The method is valid only on the primary.

During a stepdown all writes to the primary fail, and writes in progress are killed; in-progress transactions fail with `TransientTransactionError` and can be retried as a whole. The write outage is at most `secondaryCatchUpPeriodSecs` (10 s default) plus `electionTimeoutMillis` (10 s default). Without `force`, the stepped-down primary nominates an eligible secondary to call an election immediately. Client connections are not closed.

## Tuning
- Lowering `electionTimeoutMillis` makes failover detection faster; set it deliberately for your network.
- `settings.catchUpTimeoutMillis` (default -1, infinite) is how long a new primary may catch up before accepting writes: it trades faster failovers against preserving `w:1` writes. 0 disables primary catchup and catchup takeover.

## Verify
After a planned `rs.stepDown()` check `rs.status()` shows the expected new primary and application error rate returned to baseline within the drill window.

## Checked
2026-10-31. Confirmed in the MongoDB manual pages for Replica Set Elections, the replica set
configuration reference and `rs.stepDown()`: heartbeat interval and timeout, `electionTimeoutMillis`
default, 50 members / 7 voters, votes versus priority advice, `stepDownSecs` / `secondaryCatchUpPeriodSecs`
defaults and constraints, write failure window, election handoff, `catchUpTimeoutMillis` default.
Removed (not confirmed in the fetched pages): the Raft-like terms and up-to-date voter rule, median
failover of 10-12 s, `retryWrites` and `NotWritablePrimary` remarks, the priority takeover 10 s rule,
`rs.freeze`, arbiter / PSA write concern advice, the `electionMetrics` field list and log message strings.
Method: documentation only; no commands were run.
