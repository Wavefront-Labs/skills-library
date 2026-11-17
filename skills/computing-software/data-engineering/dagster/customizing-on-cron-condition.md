---
id: computing-software.data-engineering.dagster.customizing-on-cron-condition
name: customizing-on-cron-condition
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, on-cron, automation-condition, all-deps-updated-since-cron, job-schedule, partitions]
level: advanced
status: docs-checked
description: "Customize AutomationCondition.on_cron in Dagster: choose it over job schedules, ignore deps, start looking earlier than the run time, shift partitions."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/customizing-automation-conditions/customizing-on-cron-condition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customizing on_cron

## on_cron vs a job-based schedule
`AutomationCondition.on_cron()` is the recommended starting point for most asset orchestration on Dagster 1.7 and later. Use it for a schedule alongside a single asset or small group, asset-centric workflows that benefit from dependency tracking and freshness, and independent parallel materializations with no implicit ordering. Use a job-based schedule for complex orchestration across ops, multiple assets and external steps, conditional execution flows or shared state, and mixed asset/op workflows. With on_cron over multiple assets, each asset materializes independently in its own run, with no queue or ordering; use a job to coordinate them as a unit.

## Customizations
- Ignoring dependencies: by default on_cron waits for all upstream dependencies to be updated. Pass an `AssetSelection` to ignore, or one to allow.
- Blocking checks: `AutomationCondition.all_deps_blocking_checks_passed()` becomes true after all upstream blocking checks pass; combine with on_cron so the asset does not execute while upstream data fails checks.
- Execute later than upstream: modify the `AutomationCondition.all_deps_updated_since_cron()` sub-condition. Docs example: materialize at 9:00 AM daily but start looking for upstream data once the midnight boundary passes.
- Virtual assets (preview): the `.resolve_through_virtual()` modifier makes dependency sub-conditions look through virtual assets such as views to the nearest non-virtual ancestors.
- Older partitions: by default the latest time partition is targeted; replace the condition with one that targets a partition with a specific lag from the latest time window.

## Checked
2026-11-08. Confirmed against the Dagster docs page Customizing on_cron (raw markdown from the docs repo): all five customization sections and the on_cron versus job guidance. Code snippets referenced by file were not read. Nothing removed.
Method: documentation only; no commands were run.
