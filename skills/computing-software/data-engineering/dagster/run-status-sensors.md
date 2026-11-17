---
id: computing-software.data-engineering.dagster.run-status-sensors
name: run-status-sensors
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, run-status-sensor, dagsterrunstatus, alerts, slack, cursor]
level: practitioner
status: docs-checked
description: "React to run success or failure with run_status_sensor and DagsterRunStatus, avoid infinite run loops, and coordinate multiple jobs with a cursor."
sources:
  - https://docs.dagster.io/guides/automate/sensors/run-status-sensors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run status sensors

Goal: act when a run reaches a status.

Decorate a function with `run_status_sensor` and a `DagsterRunStatus`. Uses: launch other runs, alert a monitoring service on failure, report success (docs: Slack message on job success).

## Avoid infinite loops
In the docs `report_status_sensor` launches `status_reporting_job` after a success. It returns a `RunRequest` conditionally, otherwise the success of `status_reporting_job` would trigger itself endlessly.

When the sensor is triggered but returns nothing, Dagster reports an event back to the run to indicate the sensor ran.

## Coordinating independent jobs
To trigger `downstream_job` only after `upstream_job_1` and `upstream_job_2` both succeed (they may run on different schedules), use a run status sensor that tracks processed runs in a cursor, so downstream triggers exactly once per batch of upstream completions.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/sensors/run-status-sensors

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
