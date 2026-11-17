---
id: computing-software.database-administration.scylladb.admin-task-manager-and-tasks
name: admin-task-manager-and-tasks
category: computing-software
field: database-administration
product: scylladb
tags: [task-manager, nodetool-tasks, user-task-ttl, task-ttl, rest-api]
level: advanced
status: docs-checked
description: "ScyllaDB task manager: modules, cluster vs node tasks, internal tasks, task_ttl and user_task_ttl, task_status fields and the REST calls (list_module_tasks, abort_task)."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/admin-tools/task-manager.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Task manager

Task manager tracks long-running background operations (for example compaction, and node operations in the `node_ops` module: decommission, removenode, bootstrap, replace, rebuild). It is split into modules; operations are tasks arranged in trees (a root task for the operation, children for sub-operations).

Kinds:
- **Node tasks**: on a single node; ask that node for status.
- **Cluster tasks**: spread across nodes, visible from all nodes, cannot have parents or be internal. Their child status may be inaccessible even while the operation runs.
- **Internal** tasks have a parent or were started by an internal process. API calls skip them by default; they are unregistered when finished and folded into the parent status.

Retention: finished non-cluster tasks stay for `task_ttl` seconds, or `user_task_ttl` seconds if the user started them. Set with `task_ttl_in_seconds` / `user_task_ttl_in_seconds` or the `/task_manager/ttl` and `/task_manager/user_ttl` APIs (or `nodetool tasks user-ttl`).

Fields (`task_stats`): `task_id`, `type`, `kind`, `scope`, `state` (created, running, done, failed), `sequence_number`, `keyspace`, `table`, `entity`, `shard`, `start_time`, `end_time`. `task_status` adds `is_abortable`, `error`, `parent_id`, `progress_units`, `progress_total`, `progress_completed`, `children_ids`.

REST calls:
- `/task_manager/list_modules`
- `/task_manager/list_module_tasks/{module}` with `internal`, `keyspace`, `table` filters
- `/task_manager/task_status/{task_id}`
- `/task_manager/abort_task/{task_id}` (403 if not abortable)
- `/task_manager/wait_task/{task_id}`
Decommission and remove node tasks are abortable, but only before they finish tablet migration.

## Checked

2026-11-04: task kinds, internal tasks, TTL behaviour, task_stats and task_status fields and the REST calls confirmed against the ScyllaDB task manager documentation page. Removed the unsupported list of operations and monitoring advice.

Method: documentation only; no commands were run.
