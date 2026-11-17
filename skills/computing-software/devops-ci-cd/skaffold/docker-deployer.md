---
id: computing-software.devops-ci-cd.skaffold.docker-deployer
name: docker-deployer
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [docker, compose, deployer, container]
level: advanced
status: docs-checked
description: "The experimental docker deployer runs built images as local containers, optionally from a compose file."
sources:
  - "https://skaffold.dev/docs/deployers/docker/"
  - "https://skaffold.dev/docs/port-forwarding/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `docker` deployer runs containers on the local Docker daemon instead of Kubernetes, for simple container-based apps that do not rely on Kubernetes resource types. The docs mark it experimental and subject to change. It also skips pushing images to a remote registry.

```yaml
deploy:
  docker:
    useCompose: false
    images: [my-registry/app]
portForward:
- resourceType: container
  resourceName: app
  port: 8080
  localPort: 8080
```

Options (from the `DockerDeploy` schema):

- `images` (required): container images to run in Docker. Each listed image must also have a corresponding build artifact built by Skaffold.
- `useCompose` (default `false`): deploy using `docker-compose`.

Port forwarding: a user-defined `portForward` entry must set `resourceType: container`, otherwise Skaffold does not tell the Docker daemon to expose the port.

Use it for a lightweight inner loop when a full cluster is unnecessary, and test against the kubectl or helm deployers for production-like behaviour. A profile can switch between the docker deployer and a Kubernetes deployer so one `skaffold.yaml` serves both workflows.

## Checked

2026-11-04. Read the Skaffold Docker deployer page, the Port Forwarding page note on Docker deployments and the `DockerDeploy` definition in the v4beta14 schema. Confirmed experimental status, `images` required, `useCompose` default, the build-artifact requirement and the `container` resourceType. Removed: the claims that there is no status check, that no Kubernetes manifests are used, that log tailing follows the containers and that Ctrl+C cleanup stops the containers (none appear on these pages).
Method: documentation only; no commands were run.
