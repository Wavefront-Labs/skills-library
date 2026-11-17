---
id: computing-software.devops-ci-cd.gitlab-runner.runner-gpus
name: runner-gpus
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [gpus, docker-executor, nvidia, service-gpus]
level: practitioner
status: docs-checked
description: "Give Docker executor jobs access to GPUs."
sources: ["https://docs.gitlab.com/runner/configuration/gpus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GPU support

Introduced in GitLab Runner 13.9. The shell executor needs no runner configuration.

For the Docker executor, install the NVIDIA driver and the NVIDIA Container Toolkit, then set `gpus` or `service_gpus` in `[runners.docker]`:
```
[runners.docker]
    gpus = "all"
    service_gpus = "all"
```
If Podman is your container runtime, GPUs are not detected.

For Docker Machine, the docs point to the GitLab fork of Docker Machine; the Kubernetes executor has its own prerequisites on the same page.

## Checked

2026-11-03. Confirmed against GPU support on the GPUs page.

Method: documentation only; no commands were run.
