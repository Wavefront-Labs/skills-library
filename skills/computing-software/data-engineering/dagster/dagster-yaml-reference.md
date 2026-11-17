---
id: computing-software.data-engineering.dagster.dagster-yaml-reference
name: dagster-yaml-reference
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, dagster-yaml, dagster-home, instance-config, storage, retention]
level: advanced
status: docs-checked
description: "Reference for dagster.yaml keys: storage, run_launcher, run_coordinator, compute_logs, run_monitoring, run_retries, retention, sensors, concurrency and env overrides."
sources:
  - https://docs.dagster.io/deployment/oss/dagster-yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# dagster.yaml reference

Location: the directory in `DAGSTER_HOME`. It configures the OSS instance and the Dagster+ agent.

Override any value from the environment:
```yaml
instance:
  module: dagster.core.instance
  class: DagsterInstance
  config:
    some_key:
      env: ME_ENV_VAR
```

## Key sections
- `storage`: `sqlite`, `postgres` (needs `dagster-postgres`), `mysql` (needs `dagster-mysql`).
- `run_launcher`: `DefaultRunLauncher`, `DockerRunLauncher`, `K8sRunLauncher`.
- `run_coordinator`: `DefaultRunCoordinator` or `QueuedRunCoordinator` with `max_concurrent_runs` and `tag_concurrency_limits`.
- `compute_logs`: local by default; S3, GCS, Azure options (S3 example uses `dagster_aws.s3.compute_log_manager.S3ComputeLogManager` with `bucket` and `prefix`).
- `run_monitoring`: `enabled`, `poll_interval_seconds: 60`.
- `run_retries`: `enabled`, `max_retries`, `retry_on_asset_or_op_failure`.
- `code_servers.local_startup_timeout: 360`; `secrets` mapping names to `env`.
- `retention`: `schedule.purge_after_days: 90`; `sensor.purge_after_days` per `skipped`, `failure`, `success` (the page example uses skipped 7, failure 30, success -1).
- `sensors`, `schedules`, `backfills`: `use_threads`, `num_workers`.
- `auto_materialize`: `enabled`, `minimum_interval_seconds`, `run_tags`, `respect_materialization_data_versions`, `max_tick_retries` (default 3), `use_sensors`, `use_threads` (default false), `num_workers`.
- `concurrency.default_op_concurrency_limit`: default for unconfigured concurrency keys.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/deployment/oss/dagster-yaml

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: the claim that -1 means keep forever (the page shows -1 only in an example).

Method: documentation only; no commands were run.
