---
id: computing-software.data-engineering.dagster.preventing-runs-on-sensor-reactivation
name: preventing-runs-on-sensor-reactivation
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, automation-condition-sensor, reactivation, eager, backlog, time-aware-condition]
level: advanced
status: docs-checked
description: "Stop a flood of catch-up runs when re-enabling a Dagster automation condition sensor using a cron-gated or date-range condition."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/customizing-automation-conditions/preventing-runs-on-reactivation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Preventing runs when reactivating a sensor

Problem: after an automation condition sensor has been off for an extended period, the default `AutomationCondition.eager` triggers every partition that became eligible meanwhile, which can mean thousands of unwanted runs for high-cardinality or expensive workloads (GPU jobs, large batch transforms).

## Steps
1. Before reactivating, click into the **target** section of the sensor in the UI to preview which assets and partitions would trigger.
2. Replace the default with a time-aware condition that gates execution on a cron tick, so it triggers only when a dependency was updated since the most recent cron tick rather than at any point during the downtime.
3. Roll out incrementally: apply to a small subset of assets, observe for a day or two for unexpected materializations or skips, then apply to the remaining downstream assets.
4. If the cron-tick approach is too coarse, define a custom `AutomationCondition` subclass that filters partitions by a fixed date range.

Warning: `AutomationCondition.any_deps_updated() & ~AutomationCondition.initial_evaluation()` does not account for time gaps and still triggers for partitions added during the inactive period.

Prevention: when you know a sensor will be deactivated for an extended period, design the condition with a time-aware bound from the start.

## Checked
2026-11-08. Confirmed against the Dagster docs page Preventing runs when reactivating a sensor (raw markdown from the docs repo): problem statement, preview step, cron-gated condition, staged rollout, warning, date-range subclass, prevention. Code snippets referenced by file were not read. Nothing removed.
Method: documentation only; no commands were run.
