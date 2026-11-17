---
id: computing-software.cloud-infrastructure-engineering.docker.container-lifecycle-create-start-kill-and-rm
name: container-lifecycle-create-start-kill-and-rm
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-run, container-lifecycle, docker-create, docker-start, docker-kill, auto-remove, rm-flag, container-naming, hostname-flag]
level: practitioner
description: "Drive the container lifecycle: create vs run vs start, stop vs kill and signals, --rm and rm -f/-v semantics, and naming with --name, --hostname and labels."
sources: ["https://docs.docker.com/reference/cli/docker/container/stop/", "https://docs.docker.com/reference/cli/docker/container/kill/", "https://docs.docker.com/reference/cli/docker/container/rm/", "https://docs.docker.com/reference/cli/docker/container/start/", "https://docs.docker.com/engine/containers/start-containers-automatically/", "https://docs.docker.com/reference/cli/docker/container/ls/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Container lifecycle: create, start, kill, rm

Container states (the `docker ps --filter status=` values): `created`, `restarting`, `running`, `removing`, `paused`, `exited`, `dead`.

## create / start / run
```sh
docker create --name job -v data:/data app:1 migrate     # config fixed, not started
docker cp seed.sql job:/data/                             # prepare files before first start
docker start -a job                                       # attach STDOUT/STDERR and forward signals
# docker run = create + start (+ attach unless -d)
```
`docker start` starts an existing container with its existing configuration.
`docker start -ai` for an interactive container created with `-it`.

## stop vs kill
```sh
docker stop -t 30 app          # STOPSIGNAL (default SIGTERM), wait 30 s, then SIGKILL
docker stop -s SIGQUIT app     # choose the first signal (default: STOPSIGNAL, else SIGTERM)
docker kill app                # SIGKILL immediately
docker kill -s HUP app         # send any signal
docker kill -s USR1 app        # app-specific signal
```
Exit codes: 143 = 128+15 (SIGTERM), 137 = 128+9 (SIGKILL), 0 = clean.
Restart policy `always` does not restart a manually stopped container until the daemon restarts or you restart it; `unless-stopped` does not restart it even after a daemon restart.

## Removal
```sh
docker run --rm alpine true                 # removed (and its anonymous volumes) on exit
docker rm job                               # must be stopped
docker rm -f app                            # SIGKILL then remove - no graceful stop
docker rm -v job                            # also remove its anonymous volumes
docker container prune -f
```
- `rm -v` and `--rm` remove anonymous volumes associated with the container; named volumes stay.
- Use `docker stop && docker rm` in deploy scripts, not `rm -f`, to get graceful shutdown.

## Identity
```sh
docker run -d --name api-blue --hostname api-1 --label app=api --label color=blue app:1
```
- `--name` assigns the container's name.
- `--hostname` sets the container's own hostname; `--network-alias` adds a network-scoped alias, which is the option for discovery by other containers.
- `docker rename old new` renames a container.
- Labels can be used for filtering (`docker ps --filter label=color=blue`).

## Verify
`docker ps -a --format '{{.Names}}\t{{.Status}}'` shows expected states;
`docker inspect -f '{{.State.ExitCode}} {{.State.OOMKilled}}' app` explains exits.

## Checked
2026-10-25, against docker/docs engine pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master) and the restart-policy page. Confirmed: stop sends SIGTERM then SIGKILL after a grace period, first signal via STOPSIGNAL / `--stop-signal` or `docker stop -s`, `-t` timeout; `kill` default SIGKILL and `-s`; `rm -f` uses SIGKILL, `-v` removes anonymous volumes; `start -a/-i`; restart policies `always` and `unless-stopped` behaviour after a manual stop; container status values; `exitCode=143` after signal 15 in the events sample. Removed: Engine 23 gate, `--rm` and restart-policy conflict, DNS-name and generated-name claims, hostname resolution claim, rename-while-running and label-immutability claims, start exit-code claim.
Method: documentation only; no commands were run.
