---
id: computing-software.devops-ci-cd.argo-workflows.synchronization-database-locks
name: synchronization-database-locks
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [database-lock, sync-limit, sync-state, inactive-controller-seconds, multiple-controllers]
level: advanced
status: docs-checked
description: "Share mutexes and semaphores across controllers or clusters through PostgreSQL, MySQL or MariaDB tables, with heartbeat behaviour and manual release of stale locks."
sources: ["https://argo-workflows.readthedocs.io/en/latest/synchronization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-controller database locks
Database locks let several controllers share locks, normally across clusters. Configure the database in the workflow-controller-configmap `SyncConfig` section; without it, using a database lock is an error. All participating controllers must share the same tables, and cluster clocks must be synchronized because timestamps decide controller liveness and queue order.

Use in a Workflow: `mutexes: [{database: true, name: bar}]` or `semaphores: [{database: {key: bar}}]`. Lock keys in the state and lock tables are `mtx/<namespace>/<key>` or `sem/<namespace>/<key>`, but the limit table uses plain `<namespace>/<key>`.

Tables (names configurable: `limitTableName` default `sync_limit`, `stateTableName` `sync_state`, `controllerTableName` `sync_controller`, `lockTableName` `sync_lock`; all auto-created):
- limit: `name`, `sizelimit`. You insert semaphore sizes yourself: `INSERT INTO sync_limit (name, sizelimit) VALUES ('foo/bar', 3);`
- controller heartbeat: written every `heartbeatSeconds` (60); a controller is inactive after `inactiveControllerSeconds` (300).
- state: name, workflowkey, controller, held, priority, time; polled every `pollSeconds`.
- lock: coordination only.

Overriding `namespace` to `global` shares one lock across all controllers.

Held locks are never taken over, even from an inactive controller. A held lock from an inactive controller needs manual intervention (edits to the state and lock tables are otherwise not recommended). To remove a deleted controller permanently: `DELETE FROM sync_controller WHERE controller = 'inactive-controller';` and `DELETE FROM sync_state WHERE controller = 'inactive-controller';`. List waiters with `SELECT ... FROM sync_state WHERE held = false ORDER BY priority DESC, time ASC`.

## Checked

2026-11-08. Read the Argo Workflows synchronization page in full (raw markdown) and confirmed database lock syntax, lock key formats, tables and their configurable names, heartbeat defaults, polling, global namespace, and controller removal SQL. Reworded the manual release guidance to match the page (held locks from inactive controllers need manual intervention; the DELETE statements are for permanent controller removal).

Method: documentation only; no commands were run.
