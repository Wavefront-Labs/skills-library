---
id: computing-software.cloud-infrastructure-engineering.docker.diagnosing-docker-disk-usage-and-full-disks
name: diagnosing-docker-disk-usage-and-full-disks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, disk-usage, docker-system-df, system-df-verbose, reclaimable, overlay2, overlay2-internals, upperdir, lowerdir, docker-ps-size, writable-layer, disk-full, no-space-left]
level: advanced
description: "Find what fills /var/lib/docker (system df -v, ps -s, overlay2 upperdir mapping, logs, build cache) and recover a host that hit no space left on device."
sources: ["https://docs.docker.com/reference/cli/docker/system/df/", "https://docs.docker.com/engine/storage/drivers/overlayfs-driver/", "https://docs.docker.com/reference/cli/docker/container/ls/#size", "https://docs.docker.com/reference/cli/docker/container/diff/", "https://docs.docker.com/reference/cli/docker/buildx/du/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Diagnosing Docker disk usage and full disks

## 1. Overview
```sh
df -h /var/lib/docker
docker system df
docker system df -v                                     # per image, container, volume, cache
```
`docker system df` reports `TOTAL`, `ACTIVE`, `SIZE` and `RECLAIMABLE` per type; the verbose
output also lists images with `SHARED SIZE` and `UNIQUE SIZE`, containers, local volumes and
build cache.

## 2. Fat writable layers
```sh
docker ps -as --format 'table {{.Names}}\t{{.Size}}' | sort -k2 -h
# size = the container's writable layer; virtual size = writable layer plus read-only image data
docker diff <container>                               # A added, C changed, D deleted
```
Causes: logs written to files inside the container, temp files, caches, a DB writing to
a path that should be a volume.

## 3. overlay2 internals: map a directory back to a container
Each layer directory under `/var/lib/docker/overlay2/` holds `diff/` (its contents); the lowest
layer has a `link` file, and higher layers also have `lower`, `merged` and `work`. A container's
overlay mount is built from `lowerdir` (image layers), `upperdir` (the writable layer), `merged`
(the unified view) and `workdir`.
```sh
du -xh --max-depth=1 /var/lib/docker/overlay2 | sort -h | tail
```
Do not delete directories under `overlay2/` by hand.

## 4. Other usual suspects
```sh
docker buildx du                                                   # BuildKit cache usage
docker system df -v                                                # includes local volumes
```

## Recovering a full host (`no space left on device`)
1. Identify the writer (`docker ps -as`, `docker diff`, container logs).
2. Free space with prune: `docker builder prune -af`, `docker image prune -af --filter until=72h`,
   `docker container prune -f` (`until` compares creation time).
3. If dockerd will not start, free space outside Docker first, then start it.
4. Prevent: `json-file` log rotation (`max-size`, `max-file`) or the `local` driver, a separate
   filesystem for `data-root`, scheduled prune, volumes for data.

## Gotchas
- Pruning images with `-a` removes every image not referenced by a container; images used by
  stopped containers are kept until those containers are removed.

## Verify
`df -h` back under threshold; `docker system df` reclaimable figures drop after prune.

## Checked

Date: 2026-10-24. Documentation release: Docker CLI references (`system df`, `ps --size`, `diff`, `buildx du`) and the overlayfs driver page (docker/cli, docker/docs main).
Confirmed: `docker system df` columns and verbose sections, `docker ps --size` meaning of size versus virtual size,
`docker diff` symbols (A, C, D), overlay2 directory contents (`diff`, `link`, `lower`, `merged`, `work`) and the
`lowerdir`/`upperdir`/`merged`/`workdir` constructs, `docker buildx du`, prune filters and `image prune -a` semantics. Replaced
`docker builder du` (no such documented command) with `docker buildx du`. Removed: log-truncation advice, inspect
GraphDriver paths, journal and `lsof` commands, inode-exhaustion and runtime claims, none covered by the docs.

Method: documentation only; no commands were run.
