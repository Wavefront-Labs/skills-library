---
id: computing-software.devops-ci-cd.gitlab-runner.runner-docker-volumes-network
name: runner-docker-volumes-network
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [docker-volumes, volume-keep, network-mode, network-per-build]
level: practitioner
status: docs-checked
description: "Volumes, network modes and per-build networks for the Docker executor."
sources: ["https://docs.gitlab.com/runner/executors/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Volumes and networking

`volumes` lists paths and bind mounts for job containers (for example `["/cache"]`). `volume_keep` (default `false`), when true, stops Docker volumes being deleted after a job, so they accumulate on disk.

`network_mode` adds the container to a custom network.

Set `FF_NETWORK_PER_BUILD` to create a dedicated Docker network per job, with the docker executor.

`wait_for_services_timeout` (default `30`; `-1` disables) sets how long to wait for Docker services. `services_limit` caps services per job; `-1` (default) means no limit.

## Checked

2026-11-03. Confirmed against volumes, volume_keep, network_mode, wait_for_services_timeout, services_limit on Advanced configuration and FF_NETWORK_PER_BUILD on the Docker executor page. Removed the unsourced network_mode value list.

Method: documentation only; no commands were run.
