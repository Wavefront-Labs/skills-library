---
id: computing-software.cloud-infrastructure-engineering.datadog.docker-agent
name: docker-agent
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, docker, container-agent, docker-socket, docker-run]
level: practitioner
status: docs-checked
description: "Run the Datadog Agent as a container with the Docker socket, proc and cgroup mounts, log-collection mounts and DD_ environment variables."
sources: ["https://docs.datadoghq.com/containers/docker/", "https://docs.datadoghq.com/containers/docker/log/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Datadog Agent on Docker
Goal: monitor a Docker host with the containerised Agent (supports Docker, containerd and Podman runtimes).

The docs recommend the in-app installation flow, which builds the `docker run` command with your key. Manual Linux command:

```
docker run -d --cgroupns host --pid host --name dd-agent \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -e DD_SITE=<DATADOG_SITE> \
  -e DD_API_KEY=<DATADOG_API_KEY> \
  registry.datadoghq.com/agent:7
```

For log collection the docs add `-e DD_LOGS_ENABLED=true`, `-e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true`, `-e DD_CONTAINER_EXCLUDE="name:datadog-agent"` (keeps the Agent's own logs out), and the mounts `-v /var/lib/docker/containers:/var/lib/docker/containers:ro` and `-v /opt/datadog-agent/run:/opt/datadog-agent/run:rw`. On Docker Desktop add `/opt/datadog-agent/run` under Settings, Resources, File sharing.

- On Windows the command mounts `\\.\pipe\docker_engine:\\.\pipe\docker_engine` instead of the Linux paths; supported on Windows Server 2019 (LTSC) and 2022 (LTSC).
- `DD_API_KEY` is required; `DD_SITE` defaults to `datadoghq.com`; `DD_TAGS` is space separated; `DD_ENV` sets the global env tag.
- `DD_DOGSTATSD_NON_LOCAL_TRAFFIC` makes the Agent accept DogStatsD packets from other containers (required for custom metrics from them).
- Images are published to the Datadog Container Registry (`registry.datadoghq.com`), Google Artifact Registry, Amazon ECR, Azure ACR and Docker Hub for x86-64 and Arm v8. Docker Hub applies pull rate limits; the docs recommend another registry. If you use `registry.datadoghq.com`, allow `us-docker.pkg.dev/datadog-prod/public-images`, to which it may redirect.
- For Docker Compose see the Compose and the Datadog Agent guide; for Podman see the Docker-integration-with-Podman guide.
- The docker socket mount is read-only (`:ro`), but the socket is still sensitive access.

## Verify
- `docker exec -it dd-agent agent status` runs and shows the Agent healthy.

## Checked
2026-11-03. Confirmed against the Docker Agent and Docker log collection pages. Changed: the image to `registry.datadoghq.com/agent:7` as in the docs, and added the `/opt/datadog-agent/run` mount the docs require for logs. Removed: the Live Containers verification, rootless/containerd mount advice marked "confirm", and image pinning advice.
Method: documentation only; no commands were run.
