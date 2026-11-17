---
id: computing-software.data-engineering.apache-pinot.apache-pinot-controller-periodic-tasks
name: apache-pinot-controller-periodic-tasks
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, controller, periodic-tasks, retentionmanager, segmentstatuschecker, segmentrelocator, frequencyperiod, cronexpression, startcontroller]
level: practitioner
status: docs-checked
description: "Controller periodic tasks (RetentionManager, SegmentStatusChecker and more), running one over REST, frequencyPeriod versus cronExpression."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/cluster/controller.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller periodic tasks

The controller runs housekeeping as periodic tasks in the background (management and validation). The names returned by `GET /periodictask/names` on the documented cluster are: RetentionManager, OfflineSegmentIntervalChecker, RealtimeSegmentValidationManager, BrokerResourceValidationManager, SegmentStatusChecker, SegmentRelocator, StaleInstancesCleanupTask and TaskMetricsEmitter.

Each task has its own configuration (see the controller configuration reference, periodic task section): either a fixed `frequencyPeriod` or, for supported tasks, a Quartz `cronExpression`. If both are set for a task, Pinot uses the cron schedule.

Trigger one manually on the controller (port 9000 in the docs example):
```
GET /periodictask/names
GET /periodictask/run?taskname=SegmentStatusChecker&tableName=myTable&type=OFFLINE
```
- `type` is `OFFLINE` or `REALTIME`. If `tableName` and its type are omitted, the task runs against all tables.
- The task runs on the lead controller for each table.
- The response holds a `Log Request Id` (for example `api-09630c07`) that you can search for in the pinot-controller log to see the entries from that manual run, and `Controllers notified: true`.

Start a controller with the launcher script:
```
bin/pinot-admin.sh StartController -zkAddress localhost:2181 -clusterName PinotCluster -controllerPort 9000
```
(The Docker form is `StartController -zkAddress <zookeeper-host>:2181` on the Pinot image.) Multiple controllers can run for redundancy, all configured with the same back-end storage (for example NFS, HDFS or ADLS).

## Checked

2026-11-08. Read the whole pinot-docs controller page. Confirmed the task names, frequencyPeriod versus cronExpression (cron wins), the REST calls and parameters, omitted table meaning all tables, the Log Request Id, the StartController command and shared storage note. Removed the unsourced paragraph claiming which task repairs stuck realtime partitions and that running RealtimeSegmentValidationManager is the standard fix.

Method: documentation only; no commands were run.
