---
id: computing-software.database-administration.influxdb.create-threshold-and-deadman-checks
name: create-threshold-and-deadman-checks
category: computing-software
field: database-administration
product: influxdb
tags: [checks, threshold, deadman, monitoring, alerting, level]
level: practitioner
status: docs-checked
description: "Create threshold and deadman checks, understand status levels stored in _level, and write a custom check with monitor.check."
sources:
  - https://docs.influxdata.com/influxdb/v2/monitor-alert/checks/create/
  - https://docs.influxdata.com/influxdb/v2/monitor-alert/custom-checks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A check is a query plus a configuration. It applies a status to each point and stores it in the `_level` column.

Check types:
- Threshold: assigns a status when a value is above, below, inside or outside defined thresholds. Needs an aggregate function and interval in the query step.
- Deadman: assigns a status when a series or group has not reported within the `for` duration (for example `90s`, `5m`). Choose the status to set on a dead series, and use `And stop checking after` to end monitoring of the series.

Statuses are `crit`, `warn`, `info` and `ok`.

Check options (UI, Alerts then Create): schedule `every` (matches the aggregate interval), `offset` to allow for late data (must be shorter than the interval), custom tags, and a status message template using Flux string interpolation, for example `${r._check_name}` and `${r._level}`. The message is stored in `_message`.

Custom check: create a Flux task whose script calls `monitor.check` (import `influxdata/influxdb/monitor`). The check object needs `_check_id` (16 characters, alphanumeric), `_check_name` and `_type: "custom"`. A custom check does not send a notification; set up a notification endpoint and rule separately. The API endpoint `/api/v2/checks/{checkID}/query` returns the Flux behind a check built in the UI, a useful starting point.

## Checked

Method: docs-checked 2026-11-09 against the Create a check page (from the check-parts section to Clone a check) and the full body of the Create a custom check page. Dropped the unconfirmed claim about the `statuses` measurement in the `_monitoring` bucket.
