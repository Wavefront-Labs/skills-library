---
id: computing-software.database-administration.vitess.external-reparenting-and-replication-repair
name: external-reparenting-and-replication-repair
category: computing-software
field: database-administration
product: vitess
tags: [reparenting, external-reparenting, tabletexternallyreparented, disable-active-reparents, reparenttablet, replication-repair]
level: advanced
status: docs-checked
description: "Handle reparents done by an outside tool: what TabletExternallyReparented updates, when to disable active reparents, and how to repair an orphaned tablet."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-advanced/reparenting/
  - https://vitess.io/docs/25.0/user-guides/configuration-basic/initialize-shard-primary/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In external reparenting another tool changes the shard primary and Vitess only updates its topology service, replication graph and serving graph. After the change the tool must call `vtctl TabletExternallyReparented`, which:
1. Reads the tablet from the local topology.
2. Reads the Shard object from the global topology.
3. Sets the tablet type to PRIMARY if it is not already.
4. Updates the Shard record asynchronously with the new primary alias if needed.
5. Makes any other tablet still marked PRIMARY demote itself to REPLICA.

It fails completely if the global topology service cannot be locked and modified. If you depend on external reparents, active reparents are dangerous; start `vtctld` with `--disable-active-reparents` set to true (it cannot be set after startup). GTIDs are required for operations; with external reparenting Vitess assumes the outside tool manages replication.

A tablet that was unavailable during a reparent can be orphaned; VTOrc fixes its replication automatically. Manually, run `vtctl ReparentTablet` to point it at the current shard primary, then `vtctl StartReplication` if replication had stopped.

For first-time setup, a new primary is normally elected automatically by VTOrc. `InitShardPrimary` (for example `vtctldclient InitShardPrimary --force commerce/0 cell1-100`) is deprecated and destructive: it resets servers by deleting binlog metadata and copies `executed_gtid_set`, can hang or deadlock with semi-sync and fewer than two replicas, and should only initialize a brand new cluster. Use PlannedReparentShard if manual action is needed. Until a primary exists vttablet logs may show `Cannot start query service: Unknown database`.

## Checked

2026-11-08. Read in full: Reparenting (advanced) and Initializing the Shard Primary pages (vitess.io docs 25.0, via the website repo markdown). Confirmed: TabletExternallyReparented steps and failure case, `--disable-active-reparents`, GTID requirement, ReparentTablet and StartReplication repair, InitShardPrimary example, warnings and deprecation, and the log message. Nothing removed.

Method: documentation only; no commands were run.
