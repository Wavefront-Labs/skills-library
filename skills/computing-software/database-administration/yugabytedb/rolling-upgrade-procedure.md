---
id: computing-software.database-administration.yugabytedb.rolling-upgrade-procedure
name: rolling-upgrade-procedure
category: computing-software
field: database-administration
product: yugabytedb
tags: [upgrade, rolling-upgrade, pre-checks, rollback, yb-master, yb-tserver, finalize]
level: advanced
status: docs-checked
description: "Plan an in-place rolling upgrade: pre-checks, install side by side, upgrade masters then tservers, monitor, then finalize or roll back, with xCluster ordering."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/upgrade-deployment.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/upgrade-deployment-kubernetes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rolling upgrade procedure

Phases: Upgrade, Monitor, then Finalize or Rollback.

Pre-checks:
- All masters are running and there are no leaderless or under-replicated tablets (`/tablet-replication`).
- Tserver load is balanced (`/tablet-servers`).
- Delete snapshot schedules before upgrading and recreate them after finalizing or rolling back.
- Upgrade to the latest minor release of your series first.

Upgrade:
1. Install the new version into a new directory beside the current one.
2. Restart masters one at a time on the new binaries, then tservers one at a time, pausing at least 60 seconds before the next one.

Monitor for up to about 2 days.

Rollback is supported from v2.20.2: roll back tservers first, then masters. It is impossible after finalize.

Finalize (see the AutoFlags skill): `promote_auto_flags`, then `upgrade_ysql` if the upgrade changed the YSQL catalog.

xCluster: upgrade the target universe first, then the source; the target version must be the same or later. For bidirectional setups upgrade both, then finalize both close together.

## Checked

2026-11-04. Confirmed against the upgrade deployment page: pre-check URLs, latest minor version advice, new install directory, 60 second pauses, the two-day Monitor limit, rollback from v2.20.2 with tservers before masters, no rollback after finalize, promote_auto_flags and upgrade_ysql, and the xCluster ordering and version rule. Removed unsupported rationale clauses.

Method: documentation only; no commands were run.
