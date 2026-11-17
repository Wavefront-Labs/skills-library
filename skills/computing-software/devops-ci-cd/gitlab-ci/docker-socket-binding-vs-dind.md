---
id: computing-software.devops-ci-cd.gitlab-ci.docker-socket-binding-vs-dind
name: docker-socket-binding-vs-dind
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, docker-socket-binding, docker-in-docker-tradeoffs, dind-tls, sibling-containers, docker-tls-certdir]
level: practitioner
status: docs-checked
description: "Choose between binding the host Docker socket and Docker-in-Docker for GitLab jobs: setup for each, security impact, volume path surprises, caching and cleanup."
sources: ["https://docs.gitlab.com/ci/docker/using_docker_build/#use-the-docker-executor-with-docker-socket-binding", "https://docs.gitlab.com/ci/docker/using_docker_build/#use-docker-in-docker"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Docker socket binding vs Docker-in-Docker

## 1. Socket binding
```toml
[runners.docker]
  volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
  privileged = false
```
```yaml
build:
  image: docker:27
  script: docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" .
```
+ Fast: host layer cache persists across jobs. No privileged flag.
− Sharing the host Docker daemon effectively disables the container's security mechanisms and exposes the host to privilege escalation (GitLab docs).
− Containers you start are **siblings** of the runner, not children, so volume paths refer to the host, not the job container.

## 2. Docker-in-Docker
```yaml
build:
  image: docker:27
  services: [docker:27-dind]
  # set the DOCKER_HOST / TLS variables as shown in GitLab's Docker-in-Docker section
  script: docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" .
```
Some approaches, including this one, require privileged mode on the runner. A socket-bound daemon cannot be combined with the dind service. Layer cache is not shared between jobs; GitLab documents caching Docker layers in Docker-in-Docker builds.

## 3. Decision
| Situation | Pick |
|---|---|
| Single-team dedicated runner, speed matters | socket binding |
| Shared/multi-tenant runners | neither - if privileged mode is not allowed, use a Docker alternative (see GitLab docs) |
| Need `docker compose` integration tests on shared runners | dind on isolated privileged runners |

## Verify
- [ ] Security review signed off the chosen mode for the runner's audience.
- [ ] Build job works and leaves no containers behind (`docker ps -a` on host for socket mode).

## Checked

2026-11-02. Confirmed: socket-binding runner config (`volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]`); containers are siblings of the runner; socket binding cannot be combined with the dind service; shared daemon exposes the host to privilege escalation; some approaches need privileged mode and a Docker alternative exists otherwise; layer caching in DinD (GitLab 'Use Docker to build Docker images'). Removed: TLS variable block and port troubleshooting, prune/name-collision claim, specific alternative tools, docker run demo.

Method: documentation only; no commands were run.
