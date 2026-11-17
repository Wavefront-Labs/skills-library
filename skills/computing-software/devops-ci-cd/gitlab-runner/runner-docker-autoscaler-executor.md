---
id: computing-software.devops-ci-cd.gitlab-runner.runner-docker-autoscaler-executor
name: runner-docker-autoscaler-executor
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [docker-autoscaler, fleeting, taskscaler, autoscaling, executor]
level: advanced
status: docs-checked
description: "How the Docker Autoscaler executor wraps the Docker executor and uses fleeting plugins."
sources: ["https://docs.gitlab.com/runner/executors/docker_autoscaler/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker Autoscaler executor

Introduced as an experiment in 15.11, beta in 16.6 and generally available in 17.1. It wraps the Docker executor, so all Docker executor options work, and adds instances created on demand through fleeting plugins for cloud providers such as Google Cloud, AWS and Azure.

In `config.toml`:
- `executor = "docker-autoscaler"` in `[[runners]]`;
- `[runners.docker]` for Docker options;
- `[runners.autoscaler]` for scaling, with `plugin` naming the fleeting plugin.

Install the plugin for your platform on the runner manager.

Each runner configuration needs its own dedicated autoscaling resource: an AWS auto scaling group, GCP instance group or Azure scale set. Sharing one across runner managers or across `[[runners]]` entries lets several systems issue conflicting scaling commands, leading to unpredictable behavior, job failures and higher costs.

## Checked

2026-11-03. Confirmed against release history, fleeting plugins and dedicated autoscaling resource requirement on the Docker Autoscaler page.

Method: documentation only; no commands were run.
