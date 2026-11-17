---
id: computing-software.data-engineering.dagster.customizing-eager-condition
name: customizing-eager-condition
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, eager, automation-condition, blocking-checks, data-version-changed, any-new-update-has-run-tags]
level: advanced
status: docs-checked
description: "Tune AutomationCondition.eager in Dagster: allow missing deps, include older partitions, gate on blocking checks, ignore manual runs or deps."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/customizing-automation-conditions/customizing-eager-condition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customizing eager

Starting point: `AutomationCondition.eager()`. Modify by removing or adding sub-conditions.

- Missing upstream data: eager skips a target with any missing upstream data. If that is expected, remove `~AutomationCondition.any_deps_missing()`.
- Older time partitions: eager updates only the latest time partition; remove that sub-condition if updates to historical partitions should propagate.
- Blocking checks: combine with `AutomationCondition.all_deps_blocking_checks_passed()` so the asset does not run while upstream data fails quality checks.
- Ignore manual runs: `AutomationCondition.any_new_update_has_run_tags()` filters updates to runs whose tags match given keys.
- Ignore or allow dependencies: pass an `AssetSelection` to ignore, or one to allow.
- Virtual assets (preview): `.resolve_through_virtual()` makes dependency sub-conditions (`any_deps_updated()`, `any_deps_missing()`, `any_deps_in_progress()`) look through views to non-virtual ancestors.
- Data versions: by default any materialization is an update. Use `AutomationCondition.data_version_changed()` to count only changed data versions.
- Combined scheduled plus dependency-driven: a custom condition can run on a cron (docs: every 5 minutes) and also when deps update, but only if the asset updated since the last scheduled run and no deps are missing or in progress.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/declarative-automation/customizing-automation-conditions/customizing-eager-condition

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
