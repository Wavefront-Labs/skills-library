---
id: computing-software.database-administration.vitess.emergency-reparent-shard
name: emergency-reparent-shard
category: computing-software
field: database-administration
product: vitess
tags: [reparenting, emergencyreparentshard, failover, primary-down, prevent-cross-cell-promotion, gtid]
level: advanced
status: docs-checked
description: "Use EmergencyReparentShard when a primary is dead: candidate selection, steps, the cross-cell promotion flag and how VTOrc triggers it."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-advanced/reparenting/
  - https://vitess.io/docs/25.0/user-guides/configuration-basic/vtorc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`EmergencyReparentShard` (ERS) forces a new primary when the current one is unavailable. It does not rely on the old primary at all. It finds the replica with the most advanced replication position and only promotes the primary-elect once that candidate is the most advanced, waiting for it to catch up if necessary. You can name the candidate; otherwise the keyspace durability policy chooses (with the MySQL version considered, though ERS always ranks by replication position first).

Steps:
1. Determine the replication position on all replicas and find the most advanced.
2. Choose the primary-elect from the durability policy if you did not.
3. Wait for it to catch up to the most advanced replica.
4. Promote it, changing its type to primary and applying other required changes.
5. Insert a row in `reparent_journal`, update `PrimaryAlias` on the global shard object, and in parallel repoint every replica except the old primary at the new primary, waiting for the row to replicate.

Like PRS it takes the shard lock in the global topology, cannot run in parallel with PRS or another ERS for the shard, and needs the global topology. Cross-cell promotion is allowed by default; set `--prevent-cross-cell-promotion` to forbid it.

VTOrc runs ERS automatically for `DeadPrimary`, and for `IncapacitatedPrimary` it runs PlannedReparentShard and falls back to ERS if that fails. Metrics: `emergency_reparent_counts` by keyspace, shard and result, and `reparent_shard_operation_timings`, on `/debug/vars` (and `/metrics`) of VTOrc and vtctld.

## Checked

2026-11-08. Read in full: Reparenting (advanced) and VTOrc user guide pages (vitess.io docs 25.0, via the website repo markdown). Confirmed: ERS behaviour, step list, locking, `--prevent-cross-cell-promotion` and metrics (Reparenting page); `DeadPrimary` and `IncapacitatedPrimary` recovery mapping (VTOrc page). Fixed: the IncapacitatedPrimary recovery runs PRS and falls back to ERS on failure.

Method: documentation only; no commands were run.
