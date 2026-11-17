---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-privileged-and-dind
name: woodpecker-privileged-and-dind
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [privileged, docker-in-docker, dind]
level: sme
status: docs-checked
description: "Run a TLS-secured docker:dind service for Woodpecker steps on a trusted repository."
sources: ["https://woodpecker-ci.org/docs/usage/advanced-usage", "https://woodpecker-ci.org/docs/administration/configuration/backends/kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker Docker-in-Docker setup

This works only on trusted repositories. An instance admin must open the repository settings, enable `Security` under Trusted for the privileged service and `Volumes` for the certificate mount.

The daemon runs as a privileged service that generates TLS certificates into a shared host mount; the client step mounts the same path.

```yaml
steps:
  - name: test
    image: docker:cli
    environment:
      DOCKER_HOST: 'tcp://docker:2376'
      DOCKER_CERT_PATH: '/dind-certs/client'
      DOCKER_TLS_VERIFY: '1'
    volumes:
      - /opt/woodpeckerci/dind-certs:/dind-certs
    commands:
      - docker version

services:
  - name: docker
    image: docker:dind
    privileged: true
    environment:
      DOCKER_TLS_CERTDIR: /dind-certs
    volumes:
      - /opt/woodpeckerci/dind-certs:/dind-certs
    ports:
      - 2376
```

Notes:

- Unauthenticated TCP connections are deprecated as of Docker v27 and error in v28, so use TLS.
- In production pin versions like `docker:<major-version>-dind`.
- The `DOCKER_*` variables are generic, so frameworks such as TestContainers respect them.
- To build and publish images, consider the Docker Buildx plugin instead.
- On Kubernetes use a `detach: true` step with `privileged: true` and `DOCKER_TLS_CERTDIR: /woodpecker/dind-certs`.

## Checked

2026-11-03. Confirmed against: advanced-usage (dind, TLS, trusted settings, DOCKER_* variables, Docker v27/v28 note) and Kubernetes backend (headless services dind example). Removed: nothing.

Method: documentation only; no commands were run.
