---
id: computing-software.data-engineering.dagster.schedule-execution-timezone-and-dst
name: schedule-execution-timezone-and-dst
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, execution-timezone, dst, daylight-savings, partitions-definition, schedule]
level: practitioner
status: docs-checked
description: "Set execution_timezone on Dagster schedules and timezone on partitions, and predict daily and hourly schedule behaviour across DST changes."
sources:
  - https://docs.dagster.io/guides/automate/schedules/customizing-execution-timezone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Schedule timezone and DST

Goal: run at a local time and understand DST edge cases.

- Schedules with no set timezone execute in UTC.
- Set `execution_timezone` on `@schedule`, `ScheduleDefinition`, or `build_schedule_from_dbt_selection`. It accepts any tz database timezone, for example `America/Los_Angeles` for every day at 9:00 AM US Pacific.
- Schedules constructed from partitioned jobs execute in the timezone defined on the partitions definition, which has a `timezone` parameter accepting any tz timezone.

## DST behaviour
- Daily at a time that does not exist (2:30 AM when time jumps from 2:00 to 3:00): Dagster runs at the next time that exists, 3:00 AM.
- Daily at a time that exists twice (1:30 AM when the 1:00-2:00 hour repeats): Dagster runs at the second occurrence.
- Hourly schedules are unaffected: at 30 past the hour on the DST-end day it runs at 12:30 AM, both 1:30 AMs, then 2:30 AM.

## Checked
2026-11-08. Confirmed against the Dagster docs page Customizing a schedule's execution timezone (raw markdown from the docs repo): UTC default, supported objects, partition timezone, all three DST examples. Nothing removed.
Method: documentation only; no commands were run.
