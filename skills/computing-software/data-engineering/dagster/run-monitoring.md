---
id: computing-software.data-engineering.dagster.run-monitoring
name: run-monitoring
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, run-monitoring, start-timeout-seconds, max-runtime-seconds, free-slots-after-run-end-seconds, max-resume-run-attempts]
level: advanced
status: docs-checked
description: "Enable Dagster run monitoring: start and cancel timeouts, max_runtime_seconds, freeing stale concurrency slots, detecting and resuming crashed run workers."
sources:
  - https://docs.dagster.io/deployment/execution/run-monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run monitoring

Requires the Dagster daemon and `run_monitoring` enabled in the instance. In Dagster+ it is always enabled and set via deployment settings.

- `start_timeout_seconds`: a run stuck in STARTING (worker never spun up) is failed after this time.
- `cancel_timeout_seconds`: a run stuck in CANCELING is marked canceled after this time.
- `run_monitoring.max_runtime_seconds`: failing runs that exceed it after STARTED; per run use the `dagster/max_runtime` tag.

```yaml
run_monitoring:
  enabled: true
  max_runtime_seconds: 7200
```

## Concurrency slots
Op concurrency limits with `dagster/concurrency_key` claim slots; cancelled or failed runs can leave stale slots, deadlocking the pool (limit 1, for example DuckDB, blocks all future runs until freed in the UI or database). Set:

```yaml
run_monitoring:
  enabled: true
  free_slots_after_run_end_seconds: 300
```
Default is unset (no cleanup).

## Crashed workers
Crash detection only works with a run launcher other than `DefaultRunLauncher`. The daemon health-checks run workers (for example a K8s Job with non-zero exit) and marks the run failed or resumes it. Resuming works only with `K8sRunLauncher` plus `k8s_job_executor`, or `DockerRunLauncher` plus `docker_executor`; enable by setting `max_resume_run_attempts` above 0. After that many failed attempts the run is marked failed.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/deployment/execution/run-monitoring

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
