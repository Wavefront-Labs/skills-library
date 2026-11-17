---
id: computing-software.cloud-infrastructure-engineering.docker.compose-ps-pull-top-and-images-commands
name: compose-ps-pull-top-and-images-commands
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-ps, compose-pull, compose-top, compose-images, compose-port]
level: practitioner
status: docs-checked
description: "Inspect and refresh a Compose project: compose ps filters and formats, pull policies and failure handling, top, images, port, stats and events for day-to-day operations."
sources: ["https://docs.docker.com/reference/cli/docker/compose/ps/", "https://docs.docker.com/reference/cli/docker/compose/pull/", "https://docs.docker.com/reference/cli/docker/compose/images/", "https://docs.docker.com/reference/cli/docker/compose/events/", "https://docs.docker.com/reference/cli/docker/compose/stats/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compose ps, pull, top, images and friends

## ps
```bash
docker compose ps                                  # running containers of this project
docker compose ps -a                               # include stopped (and those created by run)
docker compose ps --status exited --status restarting
docker compose ps --services --filter status=running
docker compose ps --format json                    # --format: table (default), json or 'table TEMPLATE'
docker compose ps -q web                           # container IDs for scripting
docker compose ps --orphans=false                  # hide orphaned services (shown by default)
```
`--status` accepts paused, restarting, removing, running, dead, created, exited. The only
supported `--filter` is `status`.

## pull
```bash
docker compose pull                                # all services with an image
docker compose pull --ignore-pull-failures         # pull what it can, ignore failures
docker compose pull --ignore-buildable             # skip images that can be built
docker compose pull --policy missing               # "missing" or "always"
docker compose pull --include-deps web             # web and the services it depends on
docker compose pull -q                             # no progress output
```
`pull` fetches images but does not start containers. For services that you build locally,
use `--ignore-buildable` (skip images that can be built) or `--ignore-pull-failures`. A
service-level `pull_policy` of `build` makes Compose build the image (other values:
`always`, `never`, `missing`, `daily`, `weekly`, `every_<duration>`).

## top, images, port
```bash
docker compose top                                 # running processes
docker compose images                              # images used by the project's containers
docker compose images --format json                # table (default) or json; -q for IDs only
docker compose port web 80                         # public address bound to container port 80
docker compose port --index 2 web 80               # replica index for scaled services
docker compose port --protocol udp web 53          # tcp (default) or udp
```

## stats and events
```bash
docker compose stats --no-stream                   # one sample instead of a stream
docker compose events --json                       # stream of JSON objects
docker compose events --since <timestamp> --until <timestamp>
```
`stats` also has `--all`, `--aggregate` (one line per project), `--all-projects`, `--format`
and `--no-trunc`.

## Typical update check
```bash
docker compose pull -q
docker compose images
docker compose up -d                               # recreates services whose image or config changed
```

## Gotchas
- Commands act on the project resolved from the current directory, `-f` files or `-p`; run
  them from the right directory or pass `-p name`.
- `ps` without `-a` shows only running containers; use `-a` when something "disappeared".
- `pull` does not restart anything; `up -d` applies new images.

## Checked
Date 2026-10-23. Documentation release: Compose v5.6.1 CLI reference (docker/compose
`docs/reference`, mirrored at docs.docker.com) and Compose file reference for `pull_policy`.
Method: documentation only; no commands were run.
Confirmed flag names, types and defaults for `ps` (`-a`, `--filter`, `--format`, `--orphans`,
`-q`, `--services`, `--status` values), `pull` (`--ignore-buildable`,
`--ignore-pull-failures`, `--include-deps`, `--policy`, `-q`), `images` (`--format table|json`,
`-q`), `port` (`--index`, `--protocol`), `stats`, `events`, and the `pull_policy` values.
Removed: JSON-processing pipelines, column claims for the ps health field and the
`up` recreation example's digest comparison.
