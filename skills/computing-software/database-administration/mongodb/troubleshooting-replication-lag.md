---
id: computing-software.database-administration.mongodb.troubleshooting-replication-lag
name: troubleshooting-replication-lag
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, replica-set, replication-lag-mongodb, flow-control-mongodb, oplog-window, majority-write-concern]
level: practitioner
status: docs-checked
description: "Measure MongoDB secondary lag with rs.printSecondaryReplicationInfo and rs.printReplicationInfo, understand flow control throttling, and work through likely causes."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/troubleshoot-replica-sets/
  - https://www.mongodb.com/docs/manual/replication/#flow-control
  - https://www.mongodb.com/docs/manual/reference/method/rs.printSecondaryReplicationInfo/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting replication lag

## Measure
```js
rs.printSecondaryReplicationInfo()       // "x secs (y hrs) behind the primary" per secondary
rs.printReplicationInfo()                // oplog size of the member you are connected to
rs.status()                              // per-member state and optimes
```
A delayed member (`members[n].secondaryDelaySecs`) may show 0 seconds behind when the primary has
been idle for longer than the delay, so read lag together with write activity. Lag that approaches
the oplog window means a secondary can fall off the oplog and need a full resync: keep the window
comfortably above your longest expected outage or maintenance.

## Likely causes (check each, none is certain)
- Secondary hardware or storage weaker than the primary.
- Network bandwidth or latency (cross-region secondaries): lag that follows write bursts.
- Heavy reads on the secondary: move analytics to a dedicated member.
- Huge multi-document or bulk operations: batch large updates.
- Index builds that run during peak writes.
- Chained replication through a member that is itself lagging.

## Flow control
Administrators can limit the rate at which the primary applies writes to keep the majority
committed lag under `flowControlTargetLagSeconds`. As lag nears that target, writes on the primary
must obtain tickets before taking locks, and limiting the tickets issued per second throttles
writers. It is a symptom of slow secondaries, not the cause: fix the lag instead of disabling it.

## Verify
After the fix, `rs.printSecondaryReplicationInfo()` shows seconds of lag at peak and write latency on
the primary has returned to normal.

## Checked
2026-10-31. Confirmed in the MongoDB manual pages Troubleshoot Replica Sets, Replication
(flow control) and `rs.printSecondaryReplicationInfo()`: the helper names and output format,
delayed-member behaviour, `rs.printReplicationInfo()` for oplog size, flow control mechanism and
`flowControlTargetLagSeconds`. Removed (not confirmed in the fetched pages): the `replSetResizeOplog`
example, the 24-72 h window and 30-60 s alert thresholds, `flowControl` serverStatus fields, the 10 s
and 4.2+ flow control details, zstd compression and `chainingAllowed` fixes, the PSA / `votes: 0`
advice, and the exporter metric name.
Method: documentation only; no commands were run.
