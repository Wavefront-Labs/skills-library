---
id: computing-software.devops-ci-cd.gitlab-runner.runner-docker-privileged-dind
name: runner-docker-privileged-dind
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [privileged, docker-in-docker, services-privileged, allowed-privileged-services, rootless]
level: advanced
status: docs-checked
description: "Privileged mode, service-only privileges and when jobs need Docker-in-Docker."
sources: ["https://docs.gitlab.com/runner/executors/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Privileged containers and Docker-in-Docker

`privileged = true` gives job containers all root capabilities of the host VM. Docker-in-Docker (`docker:dind` as a service) typically needs it.

Narrower controls:
- `services_privileged`: allows services to run in privileged mode; if unset, `privileged` is used.
- `allowed_privileged_services`: wildcard subset of `allowed_services` allowed to run privileged; if absent, all images are allowed.

The security guide says privileged mode effectively disables all container security mechanisms and exposes the host to privilege escalation and container breakout. If you must use it:
- run only on isolated, ephemeral virtual machines;
- use dedicated runners limited to protected branches;
- with Docker Machine, set `MaxBuilds = 1` so each VM serves one job.

Do not run containers with `--pid=host`; it breaks container isolation.

## Checked

2026-11-03. Confirmed against privileged settings on Advanced configuration and risks on the Security page. Removed the unsourced rootless-dind claim.

Method: documentation only; no commands were run.
