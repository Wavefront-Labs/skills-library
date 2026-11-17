---
id: computing-software.devops-ci-cd.gitlab-runner.runner-docker-service-aliases
name: runner-docker-service-aliases
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [services, service-alias, healthcheck, healthcheck-tcp-port]
level: practitioner
status: docs-checked
description: "Service hostnames, alias derivation and health checks."
sources: ["https://docs.gitlab.com/runner/executors/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker service aliases and health checks

The runner derives a hostname for each service from its image name when you do not set an alias; characters such as `/` are replaced with `__` (and a `-` variant is also created). Set an explicit `alias` in `.gitlab-ci.yml` for predictable names.

Before the job starts, the runner health-checks each service by testing the exposed ports (the first 20 are considered). Use `HEALTHCHECK_TCP_PORT` as a service variable to choose the port when the default pick is wrong.

`wait_for_services_timeout` sets how long to wait for Docker services (default `30`; `-1` disables).

## Checked

2026-11-03. Confirmed against alias rules (slash replaced by `__`, plus a `-` variant), the 20-port limit and HEALTHCHECK_TCP_PORT on the Docker executor page; wait_for_services_timeout on Advanced configuration. Removed the unsourced failure statement.

Method: documentation only; no commands were run.
