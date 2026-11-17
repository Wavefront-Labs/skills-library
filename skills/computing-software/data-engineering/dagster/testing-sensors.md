---
id: computing-software.data-engineering.dagster.testing-sensors
name: testing-sensors
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, test-sensor, sensor-preview, build-sensor-context, validate-run-config, cursor]
level: practitioner
status: docs-checked
description: "Test Dagster sensors with the UI Preview tick result, dagster sensor preview CLI, or direct Python invocation with build_sensor_context."
sources:
  - https://docs.dagster.io/guides/automate/sensors/testing-sensors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing sensors

Warning: test evaluations run the sensor's underlying Python function, so side effects it contains may execute.

## UI
**Overview > Sensors**, open the sensor, **Preview tick result** (top right). Optionally supply a cursor (the existing one is prefilled; leave blank if not using cursors). **Continue** shows the result: run requests, a skip reason or a Python error. For each run request the **{}** button in the Actions column shows run config and tags. **Launch all & commit tick result** launches all run requests.

## CLI
`dagster sensor preview my_sensor_name`

## Python
Invoke the sensor function directly; it returns the run requests it yields. Validate the config of returned run requests with `validate_run_config`. If the sensor does not use `context`, none is needed; otherwise build one with `build_sensor_context` (the docs use the cursor-based `my_directory_sensor_cursor` example). For sensors that use resources, provide the resources when invoking the function (the docs test `process_new_users_sensor` with a `users_api` resource).

## Checked
2026-11-08. Confirmed against the Dagster docs page Testing sensors (raw markdown from the docs repo): side-effect warning, UI steps, CLI command, direct invocation, validate_run_config, build_sensor_context, resource example. Code snippets are included by reference in the page and were not read. Minor rewording only; nothing removed.
Method: documentation only; no commands were run.
