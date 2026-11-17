---
id: computing-software.data-engineering.dagster.asset-sensors
name: asset-sensors
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-sensor, multi-asset-sensor, success-hook, cross-code-location, runrequest]
level: practitioner
status: docs-checked
description: "Use @asset_sensor to trigger jobs after an asset materializes, pass config, or skip; know when to prefer declarative automation or hooks."
sources:
  - https://docs.dagster.io/guides/automate/asset-sensors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asset sensors

Goal: monitor asset materializations and trigger downstream computations or notifications (launch a job, send a Slack message), including across jobs and code locations.

- If you are automating execution of assets only, the docs recommend declarative automation instead (it also supports cross-code-location dependencies).
- `success_hook`: for lightweight side effects (notifications, metrics emission) tied to the producing op or asset; it fires automatically once the materialization succeeds. Asset sensor: for conditional logic, multi-asset coordination, cross-job triggering, or behavior depending on run/materialization metadata.

## Usage
Create one with the `@asset_sensor` decorator; the decorated function is the evaluation function. It monitors an asset for new materialization events and targets a job. Typically return a `RunRequest` to trigger the job, or a `SkipReason` if the materialization should not trigger one (docs example: a daily asset where you do not want to trigger jobs on holidays). The custom evaluation function can return a `RunRequest` only when certain metadata is present, else skip.

Provide a config to the `RunRequest` to trigger the job with specific configuration, for example passing metadata about the materialization to the job.

## Multiple assets
`@multi_asset_sensor` monitors several assets with one sensor (docs example: trigger an asset job once both of two assets have materialized; op jobs also work). It is deprecated but will not be removed until Dagster 2.0; its functionality is largely superseded by the `AutomationCondition` system.

## Checked
2026-11-08. Confirmed against the Dagster docs page Asset sensors (raw markdown from the docs repo): recommendation box, hook versus sensor table, RunRequest/SkipReason, cross-code-location pattern, config, multi-asset deprecation note. Removed an unverified `asset_key=` argument from the usage line; snippets referenced by file were not read.
Method: documentation only; no commands were run.
