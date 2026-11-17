---
id: computing-software.data-engineering.dagster.freshness-checks
name: freshness-checks
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, freshness-checks, build-last-update-freshness-checks, build-sensor-for-freshness-checks, last-updated-timestamp, anomaly-detection]
level: advanced
status: docs-checked
description: "Detect overdue Dagster assets with build_last_update_freshness_checks plus a schedule or sensor; external assets need dagster/last_updated_timestamp."
sources:
  - https://docs.dagster.io/guides/test/data-freshness-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data freshness checks

Note: the page is marked unlisted and carries a warning that freshness checks have been superseded by asset freshness policies; they are still available but are no longer considered best practice.

Freshness checks identify assets overdue for an update, for example because the pipeline errored, runs were not scheduled, the run queue backed up, or runs took longer than expected. They can also communicate SLAs for data freshness.

## Steps
1. Define with `build_last_update_freshness_checks` (uses the asset's last updated time). Dagster+ Pro also offers `build_anomaly_detection_freshness_checks` (a time series anomaly detection model; if the asset has not been updated enough times, the check passes with a message that more data is needed).
2. Define a schedule or sensor (`build_sensor_for_freshness_checks`). Required so the check executes: if it only ran after materialization it could not detect failed materializations.
3. Pass the freshness checks and the schedule/sensor to the `Definitions` object.
4. View results in the UI.

## Asset types
- Materializable assets use the last materialization timestamp (docs example: fail if the latest materialization is more than one hour before now).
- External assets need update timestamps emitted as values of the `dagster/last_updated_timestamp` observation metadata key.

Alerts on overdue assets are a Dagster+ feature.

## Checked
2026-11-08. Confirmed against the Dagster docs page Data freshness checks (raw markdown from the docs repo, plus the superseded-feature partial it imports): steps, anomaly detection, asset types, alerting. Replaced the vague "legacy" wording with the page's superseded warning. Snippets referenced by file were not read.
Method: documentation only; no commands were run.
