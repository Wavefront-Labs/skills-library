---
id: computing-software.data-engineering.apache-pinot.apache-pinot-minion-task-metrics-and-plugins
name: apache-pinot-minion-task-metrics-and-plugins
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, minion, metrics, numminiontasksinprogress, numminionsubtasksrunning, maxsubtaskwaittimems, taskgenerator, taskexecutorfactory, eventobserverfactory, task-metrics-emitter]
level: advanced
status: docs-checked
description: "Monitoring and extending minion tasks: task metric names, the emitter period, task timeout and concurrency cluster configs, and the plugin annotations for custom task types."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/cluster/minion.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minion task metrics and plugins

A controller job runs every 5 minutes by default (`controller.minion.task.metrics.emitter.frequencyPeriod`) and emits per-task-type metrics:
- `NumMinionTasksInProgress`, `NumMinionSubtasksRunning`, `NumMinionSubtasksWaiting` (not yet assigned to a minion), `NumMinionSubtasksError`
- `PercentMinionSubtasksInQueue` (waiting or running), `PercentMinionSubtasksInError`
- `MaxSubtaskWaitTimeMs` and `MaxSubtaskRunningTimeMs`: per-table, per-task-type controller gauges for the longest current wait or run time; 0 when nothing is waiting or running, so alerts can self-resolve.

Cron-scheduled tasks: `cronSchedulerJobScheduled` (gauge), `cronSchedulerJobTrigger` (meter), `cronSchedulerJobSkipped` (meter, late schedules skipped), `cronSchedulerJobExecutionTimeMs` (timer).

Each minion emits `TASK_QUEUEING` (dequeue time minus in-queue time; can be negative if Helix controller and minion clocks drift), `TASK_EXECUTION`, `NUMBER_OF_TASKS` (in progress on that minion), and meters `NUMBER_TASKS_EXECUTED`, `NUMBER_TASKS_COMPLETED`, `NUMBER_TASKS_CANCELLED`, `NUMBER_TASKS_FAILED` (may succeed on retry) and `NUMBER_TASKS_FATAL_FAILED` (not recoverable by retrying).

Two task settings go in cluster configs, via the controller's `POST /cluster/configs` API: `<TaskType>.timeoutMs` (overall task timeout, 1 hour by default) and `<TaskType>.numConcurrentTasksPerInstance` (tasks per minion worker, 1 by default), e.g. `RealtimeToOfflineSegmentsTask.numConcurrentTasksPerInstance`.

Custom task types: implement `PinotTaskGenerator`, `PinotTaskExecutorFactory` and optionally `MinionEventObserverFactory`, all returning the same string from `getTaskType()`. Annotate them with `@TaskGenerator`, `@TaskExecutorFactory` and `@EventObserverFactory` respectively, and put them in a package matching `org.apache.pinot.*.plugin.minion.tasks.*`; the controller and minion auto-register them.

Starting from Pinot 1.3.0, duplicate keys in the minion configuration file throw a `ConfigurationException` at startup (previously merged into a list).

## Checked

Confirmed against the Pinot docs page "Minion": the emitter period, every metric name listed, the cluster config keys and defaults, the plugin interfaces, annotations and package pattern, and the 1.3.0 duplicate-key behaviour. Corrected `cronSchedulerJobTriggered` to the page's `cronSchedulerJobTrigger`. Removed the unsourced diagnostic advice about waiting subtasks and wait time.

Method: docs-only read of cited pages, 2026-11-08
