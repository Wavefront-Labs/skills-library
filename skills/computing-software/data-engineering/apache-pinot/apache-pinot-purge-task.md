---
id: computing-software.data-engineering.apache-pinot.apache-pinot-purge-task
name: apache-pinot-purge-task
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, purge-task, purgetask, recordpurger, recordmodifier, lastpurgetimethresholdperiod, tablemaxnumtasks, gdpr, data-deletion]
level: advanced
status: docs-checked
description: "Row-level deletion with PurgeTask: RecordPurger and RecordModifier plugins, lastPurgeTimeThresholdPeriod, tableMaxNumTasks, scheduling."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/purge-task.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minion purge task

PurgeTask is a Minion task that removes or modifies records in segments by custom logic (for example GDPR deletion requests), then builds new segments and uploads them with updated metadata.

Enable in the table config:
```
"task": { "taskTypeConfigsMap": { "PurgeTask": { "lastPurgeTimeThresholdPeriod": "14d", "tableMaxNumTasks": "5" } } }
```
- `lastPurgeTimeThresholdPeriod` (default **14d**): minimum time between purge operations on the same segment; examples `7d`, `1h`, `30d`.
- `tableMaxNumTasks` (default `Integer.MAX_VALUE`): maximum number of concurrent purge tasks per table.

You must supply custom logic by implementing one or both interfaces as plugins, packaged and deployed with the Pinot cluster (see the Pinot plugin architecture docs):
- `RecordPurger`: `boolean shouldPurge(GenericRow record)`, true to remove the record.
- `RecordModifier`: `boolean modifyRecord(GenericRow record)`, modifies in place and returns true if changed.

How it runs: the task generator selects segments whose time since last purge exceeds the threshold (and which are available within the task limits). The executor downloads the segment, applies purge and/or modify logic to each record, creates a new segment if changes were made, and uploads it. A segment left with **no records** is deleted automatically. Original segment creation time and time intervals are preserved.

Schedule manually through the controller:
```
POST /tasks/schedule?taskType=PurgeTask
POST /tasks/schedule?taskType=PurgeTask&tableName=myTable_OFFLINE
```
The first form schedules every enabled table. For automatic scheduling, add a cron `"schedule": "0 0 2 * * ?"` to the PurgeTask config.

It is resource intensive on Minions for large segments; monitor with Minion metrics and the Task Manager in the Pinot UI.

## Checked

2026-11-08. Read the whole pinot-docs PurgeTask page. Confirmed the config location, both parameters with defaults, the two interfaces, task flow, zero-record cleanup, scheduling endpoints and cron option. Corrected tableMaxNumTasks (concurrent tasks per table, default Integer.MAX_VALUE, not a "per run" cap), removed the "register with the minion" wording in favour of the page's plugin packaging statement, and removed the claim that every selected segment is rebuilt (only when changes occur).

Method: documentation only; no commands were run.
