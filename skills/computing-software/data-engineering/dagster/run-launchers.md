---
id: computing-software.data-engineering.dagster.run-launchers
name: run-launchers
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, run-launcher, default-run-launcher, k8s-run-launcher, ecs-run-launcher, docker-run-launcher]
level: practitioner
status: docs-checked
description: "Pick a Dagster run launcher (Default, K8s, ECS, Docker, CeleryK8s) and distinguish launch from execute, and run worker from executor."
sources:
  - https://docs.dagster.io/deployment/execution/run-launchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run launchers (OSS)

A launch (from the UI, scheduler, or `dagster job launch`) allocates compute (process, container, Kubernetes pod) and starts execution. This differs from `execute_job` or the CLI `execute`. The run launcher is configured on the Dagster instance and receives the run ID plus a representation of what will execute.

## Built-ins
- `DefaultRunLauncher`: spawns a new process per run on the same node as the code location.
- `K8sRunLauncher` (dagster_k8s): one Kubernetes job per run.
- `EcsRunLauncher` (dagster_aws): one ECS task per run.
- `DockerRunLauncher` (dagster_docker): runs in a Docker container.
- `CeleryK8sRunLauncher` (dagster_celery_k8s): single Kubernetes jobs with extra config for `celery_k8s_job_executor`.

## Custom
Needed for custom infrastructure or APIs for allocating nodes, or custom logic to launch on different clusters or platforms.

The resource the launcher creates is the run worker. The launcher only determines the run worker behaviour; once execution starts, the executor (in-memory in the run worker) manages compute.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/deployment/execution/run-launchers

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
