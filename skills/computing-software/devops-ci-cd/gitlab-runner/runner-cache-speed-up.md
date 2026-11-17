---
id: computing-software.devops-ci-cd.gitlab-runner.runner-cache-speed-up
name: runner-cache-speed-up
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [speed-up, registry-mirror, dependency-proxy, docker-hub, pull-through-cache]
level: practitioner
status: docs-checked
description: "Reduce image pull time with the Dependency Proxy or a Docker Hub registry mirror."
sources: ["https://docs.gitlab.com/runner/configuration/speed_up_job_execution/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Speeding up job execution

Two proxies reduce image downloads:
- The GitLab Dependency Proxy.
- A Docker Hub registry mirror, which also helps with Docker Hub outages and rate limits.

Create a mirror on a dedicated machine:
```
docker run -d -p 6000:5000 \
  -e REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io \
  --restart always --name registry registry:2
```
This starts the server with HTTP; to enable TLS follow the official registry documentation. Use the private network IP of the server, which is usually the fastest and often does not count against bandwidth limits. The mirror is then reachable at `MY_REGISTRY_IP:6000` and referenced in `config.toml`.

`rpardini/docker-registry-proxy` can proxy most registries including the GitLab Container Registry.

For language dependencies, set up a distributed cache.

## Checked

2026-11-03. Confirmed against Dependency Proxy, Docker Hub mirror command, TLS note, private-network advice, rpardini proxy and distributed-cache pointer on Speed up job execution.

Method: documentation only; no commands were run.
