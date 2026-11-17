---
id: computing-software.data-engineering.kestra.docker-task-runner
name: docker-task-runner
category: computing-software
field: data-engineering
product: kestra
tags: [task-runner, docker, containerimage, dind, insecure-registries, working-dir]
level: practitioner
status: docs-checked
description: "Run Kestra script tasks in Docker containers with the Docker task runner: containerImage, working directory, failure behaviour, and insecure registries."
sources:
  - https://kestra.io/docs/task-runners/types/docker-task-runner
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Docker task runner runs script tasks as containers on any Docker-compatible engine, local or Docker-in-Docker.

```yaml
tasks:
  - id: shell
    type: io.kestra.plugin.scripts.shell.Commands
    containerImage: ubuntu
    taskRunner:
      type: io.kestra.plugin.scripts.runner.docker.Docker
      cpu:
        cpus: 1
    commands:
      - echo "Hello World!"
```

`containerImage` is required on the script task and can come from a public or private registry. Memory, volumes, env vars and more are in the Docker plugin docs.

The container does not start in the Kestra working directory. Reference files with `{{ workingDir }}` or `WORKING_DIR`, not relative paths.

Failure behaviour: containers keep running until the task completes even if the worker crashes. Kestra in Docker with DinD: stopping Kestra stops DinD and task containers. Same Kubernetes pod: a pod restart restarts both. Docker Compose with DinD: Kestra restart does not restart DinD.

Insecure registries are set on the host, not in the flow. In `/etc/docker/daemon.json` (omit the scheme), then restart Docker:

```json
{
  "insecure-registries": ["10.10.1.5:5000"]
}
```

## Checked

2026-11-04. Confirmed against the Kestra Docker task runner page: containerImage is the only required property, workingDir and WORKING_DIR guidance, failure behaviour for Docker, Kubernetes pod and Compose DinD deployments, insecure-registries in the daemon file without a scheme, restart of the daemon. Nothing removed.

Method: documentation only; no commands were run.
