---
id: computing-software.data-engineering.apache-pinot.apache-pinot-minion-task-scheduling
name: apache-pinot-minion-task-scheduling
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, minion, task-scheduling, taskconfig, tasktypeconfigsmap, controller-task-frequencyperiod, controller-task-scheduler-enabled, minioninstancetag, concurrentschedulingenabled, allowdownloadfromserver, task-schedule]
level: practitioner
status: docs-checked
description: "Scheduling Pinot minion tasks: per-table enablement, frequencyPeriod vs cron, distributed locking, manual schedule API and minionInstanceTag."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/cluster/minion.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minion task scheduling

Tasks are enabled per table in its config, with optional custom properties per task type:
```
"task": { "taskTypeConfigsMap": { "MergeRollupTask": { "schedule": "0 0 * * * ?" } } }
```
Built-in tasks: SegmentGenerationAndPushTask, RealtimeToOfflineSegmentsTask, MergeRollupTask, PurgeTask, RefreshSegmentTask, UpsertCompactionTask, UpsertCompactMergeTask.

Scheduling (two ways):
- Controller level, all task types on all enabled tables: set `controller.task.frequencyPeriod` in the controller config to a period string such as `2h`, `30m` or `1d`.
- Per table and task type, cron: a Quartz-syntax `schedule` entry in the task config, plus `controller.task.scheduler.enabled=true` in the controller config.
- To generate tasks for different tables in parallel, set `controller.task.enableDistributedLocking=true` first, then `controller.task.concurrentSchedulingEnabled=true`. A table can override with `task.concurrentSchedulingEnabled` (`true`/`false`; omitted inherits the cluster default). The concurrent path is used only when every table in a scheduling request resolves to concurrent.

Manual run through the controller:
```
POST /tasks/schedule?taskType=PurgeTask&tableName=myTable_OFFLINE&minionInstanceTag=tag1_MINION
```
Without `taskType` all types are scheduled; without `tableName` all enabled tables. `minionInstanceTag` can also be set in the task config; its default is `minion_untagged`, and tagging minions lets you isolate tasks per table or task type.

`allowDownloadFromServer`: when deep store is unreachable a minion may download the segment from a server. Task-config key, default `false`; the instance-level default is the minion config `pinot.minion.task.allow.download.from.server` (default `false`), and the task-level value overrides it.

Cluster configs (set with `POST /cluster/configs`): `<TaskType>.timeoutMs` (default 1 hour) and `<TaskType>.numConcurrentTasksPerInstance` (default 1).

## Checked

2026-11-09. Read the Pinot docs page `minion.md` (built-in tasks table, enable tasks, schedule tasks, task-level advanced configs sections). Confirmed everything above. Corrected: `pinot.minion.task.allow.download.from.server` is a minion instance config rather than a cluster key. Not read: the task-metrics section and the plug-in custom task code.
Method: documentation only; no commands were run.
