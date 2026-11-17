---
id: computing-software.database-administration.influxdb.system-buckets-monitoring-and-tasks
name: system-buckets-monitoring-and-tasks
category: computing-software
field: database-administration
product: influxdb
tags: [system-buckets, monitoring, tasks, rejected-points, statuses]
level: advanced
status: docs-checked
description: "Schema and retention of the _monitoring (7 days) and _tasks (3 days) system buckets, including statuses, notifications and task runs."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/internals/system-buckets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Each organization includes two system buckets, `_monitoring` and `_tasks`; they hold data used by and generated from the monitoring and alerting system and the task engine.

`_monitoring`, retention 7 days, stores data used to monitor data and send alerts. Measurements:
- `statuses`: tags `_check_id`, `_check_name`, `_level` (ok, info, warn or crit), `_source_measurement`, `_type` (threshold or deadman), plus tags inherited from the queried data or the check configuration; fields `_message`, `_source_timestamp`, plus inherited fields.
- `notifications`: tags `_check_id`, `_check_name`, `_level`, `_notification_endpoint_id`, `_notification_endpoint_name`, `_notification_rule_id`, `_notification_rule_name`, `_sent` (true or false), `_source_measurement`, `_type`; fields `_message`, `_source_timestamp` and `_status_timestamp` (when the status level was evaluated).

`_tasks`, retention 3 days, stores task execution data. Measurement `runs` (one task run is one execution) has tags `status` (success or failed) and `taskID`, and fields `finishedAt`, `logs`, `requestedAt`, `runID`, `scheduledFor` and `startedAt`.

Because retention is short, copy anything you want to keep to another bucket.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "InfluxDB system buckets" page, article body (lines 574-640) read in full from the downloaded text.

Removed: the `rejected_points` measurement and its tags (not on the page), the claim about why user buckets cannot start with an underscore, and the failed-task custom check remark.
