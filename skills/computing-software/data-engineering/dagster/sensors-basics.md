---
id: computing-software.data-engineering.dagster.sensors-basics
name: sensors-basics
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, sensor, run-request, skip-reason, minimum-interval-seconds, default-sensor-status]
level: practitioner
status: docs-checked
description: "Define a Dagster sensor with @sensor, enable it, set minimum_interval_seconds, and dedupe runs with run_key."
sources:
  - https://docs.dagster.io/guides/automate/sensors/index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sensors

Goal: poll for events and launch runs (or skip with a reason).

Events: a run completes or fails, a job materializes an asset, a file lands in S3, an external system is down. Actions: launch a run, send Slack, insert a row. Alternative to polling: push events with the Dagster GraphQL API.

## Basic
`@sensor` function checks something and either yields `RunRequest(run_key=filename)` for `my_job` or skips (docs log `No new files found`). Scaffold with `dg scaffold`.

## Enabling
A sensor is not enabled on first deploy unless `default_status` is `DefaultSensorStatus.RUNNING`. Find and enable it under **Automation > Sensors**. `DefaultSensorStatus.STOPPED` explicitly disables.

## Interval
`@dg.sensor(job=my_job, minimum_interval_seconds=30)`. This is a minimum, not an exact frequency; a slow evaluation delays the next one.

## Duplicates
Each unique `run_key` per sensor creates one run; repeated keys are skipped.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/sensors/index

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
