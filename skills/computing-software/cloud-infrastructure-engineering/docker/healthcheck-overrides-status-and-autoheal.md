---
id: computing-software.cloud-infrastructure-engineering.docker.healthcheck-overrides-status-and-autoheal
name: healthcheck-overrides-status-and-autoheal
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, healthcheck, healthcheck-none, health-cmd, health-status, failing-streak, health-status-event, autoheal, restart-unhealthy]
level: practitioner
description: "Disable or override an image's HEALTHCHECK at run time, read State.Health and health_status events, and restart unhealthy containers, which plain Docker never does."
sources: ["https://docs.docker.com/reference/dockerfile/#healthcheck", "https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/cli/docker/container/ls/", "https://github.com/willfarrell/docker-autoheal"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HEALTHCHECK overrides, status inspection and autoheal

## Overriding
```dockerfile
FROM vendor/app:2
HEALTHCHECK NONE              # disable a check inherited from the base image
```
```sh
docker run --no-healthcheck vendor/app:2
docker run --health-cmd='<command> || exit 1' \
  --health-interval=10s --health-retries=5 --health-start-period=30s \
  --health-start-interval=2s --health-timeout=2s vendor/app:2
```
Compose: `healthcheck: {disable: true}` or `test: ["NONE"]`; `test: ["CMD", ...]` replaces the image's.
Only the last `HEALTHCHECK` in a Dockerfile counts.

## Reading health
```sh
docker ps --filter health=unhealthy
docker inspect -f '{{.State.Health.Status}} streak={{.State.Health.FailingStreak}}' app
docker inspect -f '{{range .State.Health.Log}}{{.ExitCode}} {{.Output}}{{end}}' app
docker events --filter event=health_status --format '{{.Time}} {{.Actor.Attributes.name}} {{.Status}}'
```
States: `starting` -> `healthy` / `unhealthy`. `FailingStreak` is the number of consecutive failures;
`Log` holds recent check results (with exit code and output) - the first place to look. `docker ps --filter health=` accepts `starting`, `healthy`, `unhealthy` or `none`.

## Who acts on health
| Consumer | Acts on unhealthy? |
|---|---|
| `docker run --restart` | **No.** Restart policies react to exit, not health |
| Compose `depends_on: condition: service_healthy` | Gates startup only |
| Swarm services, Kubernetes | Not covered here: check the Swarm and Kubernetes documentation for what they do with health status |

## Restarting unhealthy containers on a plain host
```sh
docker run -d --name autoheal --restart=always \
  -e AUTOHEAL_CONTAINER_LABEL=autoheal \
  -v /var/run/docker.sock:/var/run/docker.sock willfarrell/autoheal
docker run -d --label autoheal=true --health-cmd=... app:1
```
The autoheal README says a container is watched if it has the label `autoheal=true`, or if `AUTOHEAL_CONTAINER_LABEL` is `all` or names a label whose value is `true`; the image needs a `HEALTHCHECK` first. Alternatively make the app exit when it is stuck so that `--restart unless-stopped` handles it. autoheal needs the Docker socket, which is root-equivalent access; see the socket-proxy skill.

## Gotchas
- `.State.Health` exists only for containers with a check defined, so guard templates that run across all containers.
- Restarting a container that is unhealthy only because a dependency is down can create a restart storm; check the cause in the health `Log` first.

## Verify
Break the endpoint, watch `docker events --filter event=health_status` report `unhealthy` after `retries` consecutive failed checks, and see autoheal restart the container (check autoheal's logs for its actions).

## Checked

Checked against the `docker container run` reference (`--no-healthcheck`, `--health-*` options), `docker container ls` reference (`health` filter), the Dockerfile reference (`HEALTHCHECK NONE`, only the last instruction takes effect), the Compose Specification (`healthcheck`, `disable`, `NONE`), the Engine API swagger (`Health`, `FailingStreak`, `Log`) and the willfarrell/docker-autoheal README (docker/docs latest commit 2026-10-23, Engine 29).

- Override mechanisms, `docker ps --filter health=`, `FailingStreak`, `health_status` event, autoheal label rules and example run command.
- Removed as unconfirmed: the "last 5 results" count, the Swarm and Kubernetes rows, the `map has no entry` message and the socket-proxy endpoint advice.

Method: documentation only; no commands were run.
