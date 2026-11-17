---
id: computing-software.data-engineering.dagster.automating-asset-jobs
name: automating-asset-jobs
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-job, automation-condition, any-job-root-assets-match, define-asset-job, partitioned-job]
level: advanced
status: docs-checked
description: "Attach an automation_condition to define_asset_job using any_job_root_assets_match or all_job_root_assets_match; partitioned job restrictions (preview)."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/automating-jobs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Automating jobs (preview)

Goal: run a fixed set of assets together as one run when a condition fires.

Pass `automation_condition` to `define_asset_job`, wrapping an asset-level condition (`eager()`, `missing()`, `on_cron()`) in:
- `AutomationCondition.any_job_root_assets_match(A)`: A true for at least one root asset.
- `AutomationCondition.all_job_root_assets_match(A)`: A true for all root assets.

Root assets are those in the job selection with no parents inside the job. Only roots are evaluated; downstream assets run as part of the same single run. Docs example: when `raw_data` updates, `eager()` is true for `processed_data` and one run of `analytics_job` runs `processed_data` and `report`.

Jobs are always evaluated by `default_automation_condition_sensor`, which must be enabled; custom sensors cannot target jobs.

## Partitioned jobs
Evaluated per partition, one run per true partition, tagged with the partition key. Restrictions: all assets share the same partitions definition; no `PartitionedConfig` (or `config`) together with an `automation_condition`, which raises an error when the job resolves; runs are individual, not grouped into backfills.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/declarative-automation/automating-jobs

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
