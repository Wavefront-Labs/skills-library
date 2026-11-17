---
id: computing-software.data-engineering.dagster.automation-condition-sensors
name: automation-condition-sensors
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, automation-condition-sensor, default-automation-condition-sensor, run-tags, auto-materialize-policy, use-sensors]
level: advanced
status: docs-checked
description: "Understand and extend default_automation_condition_sensor in Dagster: when it exists, extra sensors, default RUNNING status, run_tags, migration flag."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/automation-condition-sensors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Automation condition sensors

Every automation condition is evaluated by a sensor. `default_automation_condition_sensor` is created automatically when: the code location has at least one asset, asset check or asset job with an `AutomationCondition` (or legacy `AutoMaterializePolicy`); Dagster is 1.5+; and definitions load successfully. Toggle it on under **Automation**.

Migrating from `AutoMaterializePolicy`: you must set `use_sensors: true` in your `auto_materialize` configuration; toggling in the UI alone is not enough. If the default sensor is missing, check the three conditions first.

## Extra sensors
Create an `AutomationConditionSensorDefinition` and pass it in the `sensors` argument of `Definitions`. Benefits: faster evaluations, isolation of operational issues, targeted on/off. The default sensor then covers only conditions not claimed by the additional ones. Asset jobs with conditions are always evaluated by the default sensor.

## Options
- New sensors start `STOPPED`; set `default_status` to `RUNNING` to change.
- `run_tags` adds tags to the runs a sensor produces.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/declarative-automation/automation-condition-sensors

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
