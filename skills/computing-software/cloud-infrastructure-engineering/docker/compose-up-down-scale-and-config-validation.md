---
id: computing-software.cloud-infrastructure-engineering.docker.compose-up-down-scale-and-config-validation
name: compose-up-down-scale-and-config-validation
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, docker-compose, compose-scale, replicas, remove-orphans, force-recreate, compose-config-validate, compose-config-resolve]
level: practitioner
status: docs-checked
description: "Drive Compose lifecycle precisely: up flags (--build, --force-recreate, --no-deps, --wait, --remove-orphans), down options, scaling, and docker compose config to validate."
sources: ["https://docs.docker.com/reference/cli/docker/compose/up/", "https://docs.docker.com/reference/cli/docker/compose/down/", "https://docs.docker.com/reference/cli/docker/compose/config/", "https://docs.docker.com/reference/compose-file/deploy/#replicas", "https://docs.docker.com/reference/compose-file/services/#container_name"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Compose up/down, scale and config validation

## up
```sh
docker compose up -d                          # create/start; recreate services whose config or image changed
docker compose up -d --build                  # build images before starting
docker compose up -d --pull always            # always|missing|never
docker compose up -d --force-recreate api     # recreate even if config and image are unchanged
docker compose up -d --no-recreate            # leave existing containers alone
docker compose up -d --no-deps api            # don't start linked services
docker compose up -d --remove-orphans         # remove containers for services not in the file
docker compose up -d --wait --wait-timeout 120   # wait for running|healthy (--wait implies -d)
```
- If a service's configuration or image changed after the container was created, `up`
  stops and recreates it, preserving mounted volumes; `--no-recreate` prevents this.
- Orphans are containers for services no longer defined in the file. `COMPOSE_REMOVE_ORPHANS`
  (a documented environment variable) can set the removal behaviour globally.
- `--wait` is a CI-friendly alternative to sleep loops. Other useful flags:
  `--abort-on-container-exit`, `--exit-code-from <service>`, `--no-start`, `-V` (renew
  anonymous volumes) and `-w/--watch`.
- Exit code: 1 if the command hits an error; 0 if interrupted with SIGINT or SIGTERM
  (containers are stopped).

## down
```sh
docker compose down                     # remove containers, networks from the file, the default network
docker compose down -v                  # also named volumes declared in the file + anonymous volumes
docker compose down --rmi local         # remove images without a custom tag ("all" removes all used images)
docker compose down -t 30               # shutdown timeout in seconds
docker compose down --remove-orphans
```
Networks and volumes defined as external are never removed. Anonymous volumes are not
removed by default. `stop` keeps containers; `rm` removes stopped ones.

## Scaling
```yaml
services:
  worker:
    deploy:
      replicas: 3
```
```sh
docker compose up -d --scale worker=5          # overrides the scale setting in the file
```
- `scale` (service level) and `deploy.replicas` must be consistent when both are set.
- Compose does not scale a service beyond one container when the file sets
  `container_name`; attempting it results in an error.

## config: validate and resolve
```sh
docker compose config                    # merged, interpolated, normalised model
docker compose config --quiet            # validate only; use the exit code in CI
docker compose config --services         # also --volumes, --networks, --profiles, --images
docker compose config --no-interpolate   # see raw ${VARS}
docker compose -f compose.yaml -f compose.prod.yaml config -o resolved.yaml
docker compose config --format json      # yaml (default) or json
```
`config` renders the data model that will be applied to the engine: it merges the `-f`
files, resolves variables and expands short notation to the canonical format. Run it before
deploying overrides and compare the resolved output between environments.

## Verify
`docker compose ps -a` shows no unexpected orphaned or exited containers;
`docker compose config --quiet` exits 0 in CI.

## Checked
Date 2026-10-23. Documentation release: Compose v5.6.1 CLI reference and Docker docs
(docker/docs main). Method: documentation only; no commands were run.
Confirmed flag names and descriptions for `up`, `down` and `config` in the CLI reference
(including `--wait`, `--wait-timeout`, `--no-deps`, `--remove-orphans`, `--force-recreate`,
`--no-recreate`, `--build`, `--pull`, `--scale`, `-t`, `--rmi`, `-v`, `-q`, `--services`,
`--volumes`, `--networks`, `--profiles`, `--images`, `--no-interpolate`, `--format`, `-o`),
the `up` and `down` descriptions, the `container_name` scaling rule, and the `scale` versus
`replicas` consistency rule. Removed: fixed-host-port and DNS round-robin claims, exact
container naming and `jq` pipelines, none of which the documentation covers.
