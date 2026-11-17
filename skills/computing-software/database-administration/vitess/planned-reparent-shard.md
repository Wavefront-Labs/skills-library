---
id: computing-software.database-administration.vitess.planned-reparent-shard
name: planned-reparent-shard
category: computing-software
field: database-administration
product: vitess
tags: [reparenting, plannedreparentshard, failover, avoid-tablet, maintenance, reparent-journal]
level: practitioner
status: docs-checked
description: "Run PlannedReparentShard for maintenance: step sequence, the avoid_tablet flag, in-flight transaction handling and buffering."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-advanced/reparenting/
  - https://vitess.io/docs/25.0/user-guides/configuration-basic/reparenting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`PlannedReparentShard` (PRS) moves a healthy shard to a new primary; both the old and new primary must be up. Use `EmergencyReparentShard` if the primary is down. Do a trial PRS after bringing up a cluster. The `avoid_tablet` flag names the vttablet you will maintain: if it is the primary, PRS fails over to another eligible replica, otherwise it is a no-op. VTAdmin can also trigger a planned reparent.

Sequence when changing primary:
1. Put the current primary in read-only mode.
2. Shut down its query service.
3. Read its executed GTID position.
4. Wait for the primary-elect to catch up.
5. Promote the primary-elect.
6. Insert a row into an internal table on the new primary, update the shard's `PrimaryAlias` in the global topology, and in parallel repoint every replica (including the old primary) at the new primary, waiting for the row to replicate.

If no new primary is specified, the durability policy picks one, with MySQL version also considered. Both reparent commands lock the shard record in the global topology, cannot run concurrently for a shard, need the global topology available, and write to `reparent_journal`, which you can inspect for history. Tablets of type RESTORE are excluded so PRS can succeed during a restore.

Transactions cannot be buffered because their state is in MySQL: new `begin` statements are buffered, in-flight ones get a grace period and are then killed with an error that clients should treat as fatal. Enable VTGate buffering to handle non-transactional queries with zero errors. The Kubernetes operator performs PRS on graceful pod shutdown; abrupt crashes need VTOrc. If a reparent fails midway and two tablets claim primary, the newer timestamp wins and the older demotes itself.

## Checked

2026-11-08. Read in full: Reparenting (advanced) and Reparenting (basic) pages (vitess.io docs 25.0, via the website repo markdown). Confirmed: step list, `avoid_tablet`, buffering and transaction handling, `reparent_journal`, locking and RESTORE exclusion (advanced page); trial failover, VTAdmin, operator and two-primaries notes (basic page). Nothing removed.

Method: documentation only; no commands were run.
