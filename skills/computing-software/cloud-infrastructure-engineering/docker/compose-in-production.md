---
id: computing-software.cloud-infrastructure-engineering.docker.compose-in-production
name: compose-in-production
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, docker-compose, compose-production, production-compose, restart-policy, deploy-resources, logging-options, pinned-images, compose-up-pull, compose-pull-update, single-host-deploy, live-restore]
level: advanced
status: docs-checked
description: "Compose on a single production host: pinned images, restart policies, resource limits, log rotation, secrets, hardening keys, a production override file, deploy via a remote context, and live-restore."
sources: ["https://docs.docker.com/compose/how-tos/production/", "https://docs.docker.com/reference/compose-file/deploy/", "https://docs.docker.com/reference/compose-file/services/", "https://docs.docker.com/reference/cli/docker/compose/up/", "https://docs.docker.com/engine/logging/drivers/json-file/", "https://docs.docker.com/engine/daemon/live-restore/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Compose in production

**Goal:** a single-host stack that comes back after a reboot, cannot fill the disk with logs,
is upgraded with one command from a laptop or CI, and has no dev-only conveniences. The Docker
guide's own advice is short: the easiest way to deploy is to run on a single server, and if you
need to scale up you can run Compose apps on a Swarm cluster.

## A production-grade service block
```yaml
services:
  api:
    image: ghcr.io/org/api:1.8.2@sha256:<digest>   # pinned tag + digest, not build:
    restart: unless-stopped
    read_only: true
    tmpfs: [/tmp]
    security_opt: [no-new-privileges:true]
    cap_drop: [ALL]
    user: "10001:10001"
    init: true
    stop_grace_period: 30s
    environment:
      LOG_LEVEL: info
    secrets: [api_db_url]
    ports: ["127.0.0.1:8080:8080"]                  # behind a reverse proxy; bind to localhost
    healthcheck:
      test: ["CMD", "/app/healthcheck"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 20s
    deploy:
      resources:
        limits: {cpus: "1.5", memory: 1g}
        reservations: {memory: 256m}
    logging:
      driver: json-file
      options: {max-size: "10m", max-file: "5", compress: "true"}
secrets:
  api_db_url: {file: ./secrets/db_url}
```
- `restart` values: `no` (default), `always`, `on-failure[:max-retries]`, `unless-stopped`
  (restarts irrespective of exit code, but not once the service is stopped or removed).
- `image` may carry a digest (`name@sha256:...`) as in the Compose reference examples.
- `init: true` runs an init process as PID 1 that forwards signals and reaps processes.
- The Compose reference says `ports` entries without a host IP bind to all interfaces
  (`0.0.0.0`), bypassing host firewall rules; give a host IP such as `127.0.0.1`.
- json-file options: `max-size` defaults to unlimited (-1); `max-file` (default 1) is only
  effective when `max-size` is also set; `compress` defaults to false.
- Secrets are mounted as files at `/run/secrets/<name>` (Linux containers only). The Docker
  secrets page recommends them over environment variables, which are broadly visible and can
  leak into logs.
- `cpus` and `mem_limit` also exist as service-level attributes and must be consistent with
  the Deploy specification values when both are set.

## Separate the dev conveniences
Keep `compose.yaml` production-shaped and put dev-only settings in `compose.override.yaml`;
Compose loads it automatically next to `compose.yaml` when you do not pass `-f`. The Docker
production guide recommends a second file such as `compose.production.yaml` holding only the
changes, applied with:
```bash
docker compose -f compose.yaml -f compose.production.yaml up -d
```
Production changes the guide lists: remove bind mounts of application code, bind different
host ports, change environment variables (less verbose logging, external services), set a
restart policy, and add services such as a log aggregator. `COMPOSE_FILE` (also settable in
`.env`) selects the files so operators cannot forget a `-f`.

## Deploy and update
```bash
docker --context prod compose pull            # fetch first so the swap is fast
docker --context prod compose up -d --remove-orphans --wait --wait-timeout 120
```
- The guide also describes pointing at a remote host with `DOCKER_HOST` (plus
  `DOCKER_TLS_VERIFY` and `DOCKER_CERT_PATH`), after which the normal commands work.
- `up -d` recreates only services whose configuration or image changed; `--no-recreate`
  prevents that, `--force-recreate` forces it.
- `--wait` waits for services to be running or healthy and implies detached mode;
  `--wait-timeout` bounds it. `--pull always|missing|never` sets the pull policy and
  `--no-build` skips building.
- Redeploy one service after a code change: `docker compose build web` then
  `docker compose up --no-deps -d web` (`--no-deps` leaves its dependencies alone).
- Roll back by changing the tag back and running `up -d` again.

## Boot persistence and engine upgrades
A `restart` policy (`always` or `unless-stopped`) brings containers back when the Docker
daemon starts, provided the daemon itself starts at boot. To keep containers running while
the daemon is down, set `"live-restore": true` in `daemon.json`; the Docker docs say live
restore is only supported across patch releases (`YY.MM.x`), not major (`YY.MM`) upgrades,
and that `systemctl reload docker` applies the setting without a restart.

## Checks before calling it production
- `docker compose config` shows no `build:` for deployed services, no unpinned images, and
  no published port bound to all interfaces except the proxy.
- Every service has `restart`, `logging` limits and resource limits.
- Backups scheduled for every named volume (`volume-backup-restore-and-migration`).
- Know the ceiling: Compose on one host has no multi-host scheduling. The Docker guide points
  to Swarm for scaling up (`compose-to-kubernetes-handoff` covers Kubernetes).

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main) with Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed: the production how-to (override file, `-f` merge, `up --no-deps -d web`, `DOCKER_HOST`
variables, Swarm remark); Compose file reference for `restart`, `init`, `healthcheck`,
`logging`, `ports` host-IP warning, image digest syntax, `cpus`/`mem_limit` consistency,
`security_opt`; Deploy reference for `resources.limits`/`reservations`; `up` options and
description (Compose CLI reference); json-file driver options and defaults; live-restore
page. Removed as unconfirmed: the claim that `deploy.replicas` or `deploy.resources` are
honoured differently by Compose than by Swarm, the scale-out zero-downtime recipe,
image-updater tools, the systemd unit, prune timers and host log-file paths.
