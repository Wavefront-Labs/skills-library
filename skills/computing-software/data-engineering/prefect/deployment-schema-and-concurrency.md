---
id: computing-software.data-engineering.prefect.deployment-schema-and-concurrency
name: deployment-schema-and-concurrency
category: computing-software
field: data-engineering
product: prefect
tags: [deployments, collision-strategy, entrypoint, concurrency-limit, version]
level: practitioner
status: docs-checked
description: "Prefect deployment fields, deployment concurrency slots and collision strategies, default versioning and where deployed code can live."
sources:
  - https://docs.prefect.io/v3/concepts/deployments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand what a deployment stores and how its concurrency works.

Key fields: `name` (required, unique per flow, referenced `{FLOW_NAME}/{DEPLOYMENT_NAME}`), `entrypoint` (`path/to/file.py:function_name` or module path), `path`, `parameters`, `parameter_openapi_schema`, `schedules`, `paused` (default `False`), `trigger`, `concurrency_limit`, `concurrency_options`, `version`, `version_type` (`vcs:github`, `vcs:gitlab`, `vcs:bitbucket`, `vcs:azuredevops`, `vcs:git`, `prefect:simple`), `description`, `tags`, `work_pool_name`, `work_queue_name`, `job_variables`, `pull_steps`.

Concurrency:
- `collision_strategy`: `ENQUEUE` (default; new runs go to `AwaitingConcurrencySlot`) or `CANCEL_NEW`.
- `grace_period_seconds`: 60 to 86400, default 300; a run must reach `Running` in that time after taking a slot.
- A slot is taken on `Pending` and held through `Pending`, `Running`, `Cancelling`.

```bash
prefect deploy ... --concurrency-limit 3 --collision-strategy ENQUEUE
```
```python
my_flow.deploy(..., concurrency_limit=ConcurrencyLimitConfig(
    limit=3, collision_strategy=ConcurrencyLimitStrategy.CANCEL_NEW,
    grace_period_seconds=120))
my_flow.serve(..., global_limit=3)
```
Workers prefetch runs; `flow.serve()` runners prefetch up to 10 seconds.

Default `version`: first eight characters of the commit hash in a git directory or CI; otherwise the flow's `version` or a hash of its file.

Flows must be defined in Python files; REPL or notebook flows cannot be triggered. Hybrid pools need a worker; Push and Managed do not.

## Checked

2026-11-09. Confirmed: Deployments page (docs.prefect.io/v3/concepts/deployments): concurrency_limit, collision strategies, grace_period_seconds range 60 to 86400 and default 300, slot states, flow.serve() 10 second prefetch, default version rules, REPL and notebook limitation, hybrid versus push and managed pools. Nothing removed.

Method: documentation only; no commands were run.
