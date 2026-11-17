---
id: computing-software.data-engineering.dagster.testing-schedules
name: testing-schedules
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, test-schedule, preview-tick, build-schedule-context, validate-run-config, schedule]
level: practitioner
status: docs-checked
description: "Test Dagster schedules via the Preview tick result UI or by invoking the function with build_schedule_context and validate_run_config."
sources:
  - https://docs.dagster.io/guides/automate/schedules/testing-schedules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing schedules

## In the UI
1. **Overview > Schedules tab**, open the schedule.
2. Click **Preview tick result** (top right).
3. Pick a mock evaluation time (past and future times along the schedule's cadence), then **Continue**.
4. Review results; per run request click the **{}** button in the Actions column to see run config and tags.
5. **Launch all & commit tick result** launches the runs and links to the /runs page filtered to the launched run IDs.

## In Python
- Invoke a `@schedule`-decorated function like a regular Python function; it returns run config, which you can validate with `validate_run_config`.
- If it takes `context`, build one with `build_schedule_context` (a `ScheduleEvaluationContext`). If the function has no context parameter, you do not need to provide one.
- For schedules using resources, provide the resources when invoking the function (docs example: `process_data_schedule` with a `date_formatter` resource).

## Checked
2026-11-08. Confirmed against the Dagster docs page Testing schedules (raw markdown from the docs repo): UI steps, Python invocation, build_schedule_context, resources example. Code snippets are referenced by file and were not read. Nothing removed.
Method: documentation only; no commands were run.
