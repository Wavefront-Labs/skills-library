---
id: computing-software.cloud-infrastructure-engineering.docker.healthchecks-in-swarm-rolling-updates
name: healthchecks-in-swarm-rolling-updates
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, healthcheck, swarm-healthcheck, docker-swarm, rolling-update, update-monitor, task-state]
level: advanced
status: docs-checked
description: "Make Swarm act on container health: unhealthy tasks replaced, rolling updates wait for healthy, update-monitor and failure-action interplay, VIP routing to healthy tasks."
sources: ["https://docs.docker.com/reference/cli/docker/service/create/", "https://docs.docker.com/reference/cli/docker/service/update/", "https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/", "https://docs.docker.com/engine/swarm/services/", "https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/reference.md", "https://github.com/docker/cli/blob/master/cli/compose/schema/data/config_schema_v3.13.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Healthchecks in Swarm

Plain `docker run` only reports health. Swarm **acts** on it:
- If a container fails its health checks or terminates, its task terminates and the orchestrator
  creates a replacement task.
- During a rolling update each updated task is watched for failure for `update-monitor`.

## Stack file
```yaml
services:
  api:
    image: reg.example.com/api:1.8.0
    healthcheck:
      test: ["CMD", "/app/healthcheck"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 40s
      start_interval: 2s       # needs Engine 25.0+
    deploy:
      replicas: 4
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
        monitor: 60s
        failure_action: rollback
        max_failure_ratio: 0
      rollback_config:
        parallelism: 2
        order: stop-first
      restart_policy:
        condition: any
        delay: 5s
```
CLI equivalents: `--health-cmd`, `--health-interval`, `--health-start-period`,
`--update-monitor`, `--update-failure-action rollback`, `--update-order start-first`.

## How the pieces interact
- `start_period` must cover cold start (migrations, JIT warmup). Failures inside it do not
  count toward `retries`, but a success ends it early.
- `monitor` (default 5s) is how long after a task is updated Swarm watches it for failure.
  Consider setting it longer than `start_period + interval * retries` so a failing health check is seen before the update is accepted.
- `order: start-first` starts the new task before stopping the old one (default `stop-first`); it needs spare capacity on nodes.
- Without any health check, only exit or crash is detected. Define health in the image or stack.

## Diagnose
```bash
docker service ps api --no-trunc            # task history with errors
docker inspect --format '{{json .State.Health}}' <container>
docker service inspect api --format '{{json .UpdateStatus}}'   # e.g. state paused after a failed update
docker events --filter event=health_status
```

## Gotchas
- `--health-cmd` with `curl` in an image without curl fails health permanently, so tasks are replaced repeatedly.
- Health checks run inside the task's network namespace: `localhost` means the task, not the
  node, and published ports are not involved.
- `docker service update --force` re-runs the update path and is the quickest way to test
  your gating.

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master) plus the Dockerfile reference (moby/buildkit) and the docker/cli stack schema v3.13. Confirmed: unhealthy or terminated containers have their task terminated and replaced; `--health-cmd/-interval/-start-period/-start-interval` exist on `docker service create`; start period failures do not count toward retries and a success during it ends it; `start_interval` needs Engine 25.0+; `--update-monitor` default 5s, `--update-order` default `stop-first`, failure action default `pause`; stack keys `update_config` (parallelism, delay, order, monitor, failure_action, max_failure_ratio), `rollback_config`, `restart_policy`; `health_status` is a docker events type; a failed update shows state `paused`. Removed: VIP-traffic gating claim, health-gated update claim, exit-137 message, jq pipeline, rollback_completed state name.
Method: documentation only; no commands were run.
