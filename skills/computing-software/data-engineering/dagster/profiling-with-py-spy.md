---
id: computing-software.data-engineering.dagster.profiling-with-py-spy
name: profiling-with-py-spy
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, py-spy, profiling, hanging-run, sys-ptrace, kubernetes]
level: practitioner
status: docs-checked
description: "Debug hanging or slow Dagster code with py-spy dump and record, including a SYS_PTRACE security context for Kubernetes run pods."
sources:
  - https://docs.dagster.io/deployment/troubleshooting/py-spy-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Profiling hanging or slow code with py-spy

- Hanging: `py-spy dump` shows each thread.
- Slow: `py-spy record -f speedscope --idle` (speedscope profile, includes idle time).
- py-spy usually needs elevated permissions. Example for slow definition import: `sudo py-spy record -f speedscope --idle -- dagster definitions validate`

## Hanging run in Kubernetes
1. Give run pods a security context with `SYS_PTRACE` (elevated permission, clear with cluster admins, temporary).
   - OSS Helm: `runLauncher.type: K8sRunLauncher` with `config.k8sRunLauncher.runK8sConfig.containerConfig.securityContext.capabilities.add: [SYS_PTRACE]`.
   - Dagster+ Hybrid K8s agent, in `container_context.yaml`: under `k8s`, set `server_k8s_config.container_config.securityContext.capabilities.add` and `run_k8s_config.container_config...` to `SYS_PTRACE`.
2. Launch a run and wait for the hang.
3. Find the run pod in the event logs and `kubectl exec -it <pod name here> /bin/bash`.
4. `pip install py-spy` then `py-spy dump --pid 1`.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/deployment/troubleshooting/py-spy-guide

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
