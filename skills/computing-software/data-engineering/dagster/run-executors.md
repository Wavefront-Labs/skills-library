---
id: computing-software.data-engineering.dagster.run-executors
name: run-executors
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, executor, multiprocess-executor, in-process-executor, k8s-job-executor, executor-def]
level: practitioner
status: docs-checked
description: "Pick and set a Dagster executor on a job or for a whole code location: in-process, multiprocess, Dask, Celery, Docker, K8s, ECS."
sources:
  - https://docs.dagster.io/guides/operate/run-executors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run executors

After the run worker starts, the executor runs the steps.

## Set
- On a job: pass an `ExecutorDefinition` as `executor_def` to `@job` or `GraphDefinition.to_job`. Every job has an executor; default is `multi_or_in_process_executor`, one process per step (configurable to a single process).
- For a code location: in a file under `/defs`, a function decorated with `@definitions` returns `Definitions` with the executor. A job explicit executor wins; others use the default.
- Gotcha: the docs note that executing a job via `JobDefinition` overrides the job executor and uses `in_process_executor` instead.

## Examples
`in_process_executor` (serial in run worker), `multiprocess_executor` (process per step, configurable parallelism), `dask_executor`, `celery_executor`, `docker_executor`, `k8s_job_executor` (ephemeral pod per step), `celery_k8s_job_executor` (Celery as control plane), `ecs.ecs_executor`, `celery_docker_executor`.

Custom executors are possible but poorly documented and internal APIs change.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/operate/run-executors

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: the explicit `execute_in_process` method name (the page text is truncated at `JobDefinition`).

Method: documentation only; no commands were run.
