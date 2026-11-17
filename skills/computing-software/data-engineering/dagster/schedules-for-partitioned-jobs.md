---
id: computing-software.data-engineering.dagster.schedules-for-partitioned-jobs
name: schedules-for-partitioned-jobs
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, build-schedule-from-partitioned-job, end-offset, partition-key, static-partitions, schedule]
level: advanced
status: docs-checked
description: "Build Dagster schedules from time-partitioned jobs, shift timing and end_offset, target static partitions, and look up partition keys."
sources:
  - https://docs.dagster.io/guides/automate/schedules/constructing-schedules-for-partitioned-assets-and-jobs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Schedules from partitioned assets and jobs

Goal: run each tick against the right partition.

## Time partitions
`build_schedule_from_partitioned_job` makes a schedule whose interval matches the partition spacing. Works for asset jobs (`define_asset_job`) and op jobs. Control timing with `minute_of_hour`, `hour_of_day`, `day_of_week`, `day_of_month`. Docs: on 2024-05-20 a schedule evaluated at 1:30 AM UTC starts a run for partition `2024-05-19`.

## Which partition runs
A partition key is the start of its time window, and the partition joins the set only once the window completes. So a daily tick on 2024-05-20 targets `2024-05-19`. Shift with `end_offset` in the partitions definition: positive integers fill the current window, negative ones earlier ones. Formula: `current_date - 1 type_of_partition + end_offset`. With date 2024-05-20: -1 gives 05-18, 0 gives 05-19, 1 gives 05-20.

## Static partitions
Write the schedule with `@schedule` and yield `RunRequest`s per partition (docs example: continents, or only `Antarctica`).

## Different cadence than partitions
Do not use `build_schedule_from_partitioned_job` (it sets the cadence from the partitions). Use `context.scheduled_execution_time` from `ScheduleEvaluationContext` to compute the key.

## Last partition key as of a time
Wrap `get_last_partition_key` in `partition_loading_context` with `effective_dt`. `get_last_partition_key` takes no `current_time` argument. `get_partition_key_for_timestamp` can return keys for partitions that do not exist yet, so validate.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/schedules/constructing-schedules-for-partitioned-assets-and-jobs

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
