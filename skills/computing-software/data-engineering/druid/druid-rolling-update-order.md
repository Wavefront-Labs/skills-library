---
id: computing-software.data-engineering.druid.druid-rolling-update-order
name: druid-rolling-update-order
category: computing-software
field: data-engineering
product: druid
tags: [rolling-updates, upgrade, restore-tasks-on-restart, middle-manager, downgrade]
level: practitioner
status: docs-checked
description: "Follow the recommended service order for zero-downtime Druid upgrades."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/rolling-updates.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For a rolling update with no downtime, update services in this order:
1. Historical
2. Middle Manager and Indexer, if any
3. Broker
4. Router
5. Overlord (it may be upgraded before Middle Managers if you use autoscaling-based replacement)
6. Coordinator, or merged Coordinator plus Overlord

For a rolling downgrade reverse the order, starting with the Coordinators.

Historicals can be updated one at a time. Each one needs startup time to memory-map the segments it served before, from seconds to minutes depending on hardware, so wait longer than one startup between nodes. Overlords can be updated one at a time.

Middle Managers and Indexers run batch and real-time tasks, and you generally want to update them without failing real-time tasks. The restore-based strategy updates them one at a time when `druid.indexer.task.restoreTasksOnRestart=true`: tasks that support restoring recover their state on restart instead of failing. Only realtime tasks support restoring, so non-realtime indexing tasks fail and must be resubmitted.

The graceful-termination strategy works for every task type. POST to `<Middle_Manager_IP:PORT>/druid/worker/v1/disable` so the Overlord stops sending it tasks while started tasks run to completion; check state at `/druid/worker/v1/enabled` and list tasks with GET `/druid/worker/v1/tasks`. When the list is empty, update it. It is enabled again automatically on startup, or manually by POSTing to `/druid/worker/v1/enable`.

The autoscaling-based strategy applies when autoscaling is enabled on the Overlord: set `druid.indexer.runner.minWorkerVersion` and `druid.indexer.autoscale.workerVersion`, and raise the version each time you update the Overlord to trigger a mass launch of new Middle Managers while old ones terminate as their tasks finish.

Brokers can be updated one at a time with a delay between each, since a Broker must load the entire cluster state before it returns valid results. Coordinators and standalone real-time processes can also be updated one at a time.

## Checked

2026-11-08. Read operations/rolling-updates.md in full. Added the graceful-termination and autoscaling strategies with their endpoints and properties, and the Broker and Coordinator notes.

Method: documentation only; no commands were run.
