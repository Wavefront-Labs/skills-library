---
id: computing-software.devops-ci-cd.gitlab-runner.runner-executor-selection
name: runner-executor-selection
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [executors, executor-choice, maintenance-mode, fleeting]
level: intro
status: docs-checked
description: "Which executors are active and which are in maintenance mode."
sources: ["https://docs.gitlab.com/runner/executors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing an executor

The executor decides where a job's script runs.

Active development: Kubernetes, Docker, Docker Autoscaler and Instance. Docker Autoscaler and Instance use fleeting plugins to create cloud instances on demand.

Maintenance mode: SSH, Shell, VirtualBox, Parallels and Custom.

Points from the docs:
- Shell runs jobs directly on the host as the runner user and is the highest-risk option for shared hosts; use it only for trusted builds.
- Docker gives per-job container isolation when not run privileged.
- Kubernetes creates one pod per job.
- Instance is for jobs needing full access to the host OS and devices.

Set the choice with `executor = "..."` in the `[[runners]]` section or `--executor` at registration.

## Checked

2026-11-03. Confirmed against active and maintenance-mode executors on the Executors page.

Method: documentation only; no commands were run.
