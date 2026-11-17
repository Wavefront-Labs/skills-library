---
id: computing-software.data-engineering.dagster.automation-condition-operands-and-operators
name: automation-condition-operands-and-operators
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, automation-condition, newly-true, since, any-deps-match, operators]
level: advanced
status: docs-checked
description: "Compose custom Dagster AutomationConditions from operands (missing, newly_updated, cron_tick_passed), operators (~ | & since newly_true) and dep matchers."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/automation-condition-reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Automation condition reference

## Operands
`missing`, `in_progress`, `execution_failed`, `newly_updated` (since previous evaluation), `newly_requested`, `code_version_changed`, `cron_tick_passed`, `in_latest_time_window`, `will_be_requested`, `initial_evaluation` (all `AutomationCondition.<name>`).

## Operators
- `~A` not, `A | B` or, `A & B` and
- `A.newly_true()`: false last evaluation, true now
- `A.since(B)`: A became true more recently than B
- `AutomationCondition.any_deps_match(A)`, `all_deps_match(A)` with `.allow()` / `.ignore()` to target upstream assets
- `AutomationCondition.any_downstream_conditions()`

## Composites
`any_deps_updated`, `any_deps_missing`, `any_deps_in_progress`, `all_deps_updated_since_cron`.

## Statuses vs events
Statuses persist (`missing`); events are momentary (`newly_updated`). `A.since(B)` turns two events into a status. `.newly_true()` turns a status into an event. The default eager condition uses `AutomationCondition.missing().newly_true().since_last_handled()` so a missing partition is requested only once, not on every evaluation while its run spins up.

## Evaluation and grouping
The `default_automation_condition_sensor` evaluates every 30 seconds, so conditions are defined against evaluation ticks. `any_deps_updated` and `any_deps_missing` rely on `will_be_requested` so chained eager assets are grouped into a single run.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/declarative-automation/automation-condition-reference

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
