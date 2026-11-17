---
id: computing-software.data-engineering.dagster.declarative-automation-builtin-conditions
name: declarative-automation-builtin-conditions
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, declarative-automation, automation-condition, on-cron, eager, on-missing]
level: practitioner
status: docs-checked
description: "Choose between AutomationCondition.on_cron, eager and on_missing in Dagster, with their partition behaviour and the sensor that must be enabled."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Declarative Automation built-in conditions

Goal: launch asset runs from asset and dependency status instead of hand-written schedules.

Required: turn on the default **default_automation_condition_sensor** under **Automation** for the code location; it evaluates conditions and launches runs.

## on_cron
Runs an asset once per cron tick, after all upstream deps updated. Waits from the tick start; requested as soon as all deps updated since the tick. If upstreams do not all update in the tick, no request. Time-partitioned assets: only the latest time partition. Static and dynamic partitions: all partitions.

## eager
Updates an asset whenever any dependency updates. Not requested if any upstream partition is unmaterialized; waits for in-progress upstream runs and for its own in-progress run. Time-partitioned: latest partition only; static/dynamic: all. An observed upstream counts as updated only if its data version changed; a materialization always counts.

## on_missing
Fills a missing partition once all its upstream partitions are available (for example hourly upstream partitions fully filled). Any unmaterialized upstream partition blocks it. Time-partitioned: latest only. Only partitions added after the condition was enabled are considered.

Test in isolation, without the daemon, using `evaluate_automation_conditions`.

## Checked

2026-11-09. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/declarative-automation/index

Confirmed: the default_automation_condition_sensor requirement, on_cron, eager and on_missing behaviours including partition handling, and evaluate_automation_conditions for testing.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
