---
id: computing-software.data-engineering.dagster.blocking-partitioned-and-scheduled-asset-checks
name: blocking-partitioned-and-scheduled-asset-checks
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-check, blocking, partitions-def, schedule, sensor]
level: advanced
status: docs-checked
description: "Block downstream materialization on failed Dagster asset checks, partition checks (preview), and run them on their own schedule with an alert sensor."
sources:
  - https://docs.dagster.io/guides/test/asset-checks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Blocking, partitioned and scheduled checks

## Blocking
By default, if a parent's asset check fails during a run, the run continues and downstream assets are still materialized. Set the `blocking` argument to `True` in the `@asset_check` decorator to prevent this. Docs example: if the `orders_id_has_no_nulls` check fails, the downstream `augmented_orders` asset is not materialized.

## Partitioned (preview)
Provide a `partitions_def` to the `@asset_check` decorator or `AssetCheckSpec`; each execution of the check then targets a single partition of the asset, and the UI shows check status per partition. The check's `partitions_def` must be the same as the associated asset's.

## Separate schedule and monitoring
To run checks apart from the job materializing the assets (for example, all quality checks once a day with an alert on failure), use schedules and sensors. Docs example: one job for the asset and one for the asset check, schedules that run them independently, and a sensor that sends an email alert when the asset check job fails.

## Checked
2026-11-08. Confirmed against the Dagster docs page Testing assets with asset checks (raw markdown from the docs repo, which marks the partitioned section as Preview): blocking, partitioned checks, scheduling and monitoring. Snippets referenced by file were not read. Nothing removed.
Method: documentation only; no commands were run.
