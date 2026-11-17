---
id: computing-software.cloud-infrastructure-engineering.docker.run-cache-mount-sharing-modes-and-ids
name: run-cache-mount-sharing-modes-and-ids
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, buildkit, layer-caching, cache-mount, cache-mount-sharing, cache-mount-id, sharing-locked, sharing-private, uid-gid-cache-mount]
level: advanced
description: "Tune RUN --mount=type=cache: sharing=shared/locked/private, id= to split caches per target, uid/gid/mode for non-root installs, and from/source to seed a cache."
sources: ["https://docs.docker.com/reference/dockerfile/#run---mounttypecache", "https://docs.docker.com/build/cache/optimize/#use-cache-mounts", "https://docs.docker.com/reference/cli/docker/buildx/prune/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RUN --mount=type=cache: sharing modes, ids and ownership

**Goal:** persistent package caches that are safe under parallel stages and multi-platform
builds, and that work when the RUN executes as a non-root user.

## Options
| Option | Meaning |
|---|---|
| `target=/path` (also `dst`, `destination`) | mount path |
| `id=<name>` | identifies separate caches; defaults to `target` |
| `sharing=shared` | default; a shared cache can be used concurrently by multiple writers |
| `sharing=locked` | pauses the second writer until the first releases the mount |
| `sharing=private` | creates a new mount if there are multiple writers |
| `uid=`, `gid=`, `mode=` | owner and mode of a new cache directory (defaults 0, 0 and 0755) |
| `from=<stage, context or image>`, `source=<path>` | base of the cache mount (default empty directory) and subpath in it |
| `ro` / `readonly` | read-only if set |

## When sharing matters
The Dockerfile reference notes that apt needs exclusive access to its data, so the apt caches
use `sharing=locked` (`sharing=private` is the alternative, giving each build its own directory):
```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends curl
```
The reference example also disables the base image's package cleanup first, so the cache keeps
packages (shown for the `ubuntu` image):
```dockerfile
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
```

## Separate ids
Use `id` to keep caches apart, for example per project on a shared builder or per tool:
```dockerfile
RUN --mount=type=cache,target=/root/.cache/go-build,id=myproj-go-build \
    go build -o /out/app .
```

## Non-root installs
If the step runs as `USER app` (uid 1000), the default root-owned mount is unwritable:
```dockerfile
USER app
RUN --mount=type=cache,target=/var/cache/app-npm,uid=1000,gid=1000 npm ci
```

## Seeding and inspecting
`from=deps,source=/cache` uses the `/cache` directory of the `deps` stage as the base of the
cache mount (without `from` the mount starts as an empty directory). `docker buildx prune
--filter type=exec.cachemount` removes only cache mount records (`exec.cachemount` is a valid
`type` filter value).

## Gotchas
- Cache mounts live in the builder's local storage. They are not included in exported build
  cache (`--cache-to`) and are not restored by `--cache-from`; on CI runners that provision a
  fresh builder per job they start empty (see the Docker docs GitHub Actions "Cache mounts"
  page for a workaround).
- Contents persist between builds without invalidating the instruction cache, but another build
  may overwrite them or GC may clean them: the build must work with any cache contents. Use
  cache mounts only for performance.

## Verify
Rebuild after changing one dependency and check in `--progress=plain` output that the install
step reuses the cached packages instead of downloading everything.

## Checked

Checked 2026-10-23 against the Dockerfile reference (`RUN --mount=type=cache`, moby/buildkit `frontend/dockerfile/docs/reference.md`, main branch) and the docker/buildx `buildx prune` reference.

- Option names, defaults and meanings (`id`, `target`, `sharing`, `from`, `source`, `mode`, `uid`, `gid`, `ro`); apt example with `sharing=locked`.
- Cache mounts are builder-local, excluded from `--cache-to` / `--cache-from`, and may be garbage-collected.
- `docker buildx prune --filter type=exec.cachemount` is a valid filter.
- Removed the Gradle, Go-per-architecture (`$TARGETARCH` in `id`), `uv`/`pip` and `docker buildx du` claims, which the documentation does not cover.

Method: documentation only; no commands were run.
