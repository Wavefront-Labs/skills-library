---
id: computing-software.cloud-infrastructure-engineering.docker.prune-commands-filters-and-scheduled-cleanup
name: prune-commands-filters-and-scheduled-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, prune, image-prune, system-prune, dangling-images, prune-until, prune-filter, system-prune-all, prune-volumes, container-prune, stopped-containers, network-prune, cleanup-cron, scheduled-prune, housekeeping]
level: practitioner
description: "Use docker image/container/network/system prune with -a, --volumes and until/label filters safely, and schedule cleanup with a systemd timer or cron."
sources: ["https://docs.docker.com/engine/manage-resources/pruning/", "https://docs.docker.com/reference/cli/docker/system/prune/", "https://docs.docker.com/reference/cli/docker/image/prune/", "https://docs.docker.com/reference/cli/docker/container/prune/", "https://docs.docker.com/reference/cli/docker/volume/prune/", "https://docs.docker.com/reference/cli/docker/builder/prune/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prune commands, filters and scheduled cleanup

## What each command removes
| Command | Removes |
|---|---|
| `docker container prune` | all **stopped** containers |
| `docker image prune` | **dangling** images (`<none>:<none>`, untagged, unreferenced) |
| `docker image prune -a` | every image not used by an existing container (incl. stopped ones) |
| `docker network prune` | user-defined networks with no containers |
| `docker volume prune` | unused anonymous volumes by default; `--all` adds unused named ones |
| `docker builder prune` | build cache (`-a` / `--all` includes internal and frontend images) |
| `docker system prune` | stopped containers + unused networks + dangling images + unused build cache |
| `docker system prune -a --volumes` | the above with all unused images and unused anonymous volumes |

All take `-f` to skip the prompt.

## Filters
```sh
docker image prune -a -f --filter "until=168h"          # older than 7 days
docker container prune -f --filter "until=24h"
docker image prune -a -f --filter "label!=keep=true"   # protect labelled images
docker volume prune -f --filter "label!=keep"
```
- `until` takes Unix timestamps, date-formatted timestamps or Go duration strings (`24h`,
  `10m`); it matches items **created** before the given time, not last use - a base image
  created months ago is "old" even if pulled today.
- `label=` / `label!=` work for containers, images, networks and volumes; the documented
  `volume prune` filter is `label` (no `until`).
- Different filter keys combine with AND; repeating the same key combines with OR.

## Scheduled cleanup
Run the prune commands from your scheduler of choice (for example a timer or cron job on each
host), for instance:
```sh
docker system prune -af --filter "until=168h" --filter "label!=keep=true"
docker builder prune -af --keep-storage 20GB
```
`docker builder prune` has `-a`, `--filter`, `-f` and `--keep-storage` (disk space to keep for
cache). Each builder keeps its own cache; use `--builder` on `docker buildx prune` to target one.

## Gotchas
- `-a` on a CI runner deletes cached base images, so the next build re-pulls them. Prefer
  `until=` filters and keep-storage budgets.
- `--volumes` deletes unused anonymous volumes, which may hold data of stopped Compose stacks.
  Do not schedule `--volumes` on hosts with stateful containers.
- `image prune -a` keeps images referenced by any container, including stopped ones; prune
  containers first if you want those images freed.

## Verify
`docker system df` before and after.

## Checked

Date: 2026-10-24. Documentation release: Docker pruning guide and CLI references for system, image, container, volume and builder prune (docker/docs, docker/cli main).
Confirmed: what each prune command removes, `volume prune` removing only anonymous volumes by default and `--all`,
`system prune --volumes` pruning anonymous volumes only, `until` accepted forms and creation-time semantics, `label`
and `label!=` filters, AND/OR combination of filters, `volume prune` filter list, and `docker builder prune` flags
including `--keep-storage`. Corrected: `system prune` removes unused (not only dangling) build cache and the Engine 23
version gate was dropped. Removed: systemd unit and cron examples, the Compose project label filter, the journalctl
check and the Swarm statement, which the documentation does not cover.

Method: documentation only; no commands were run.
