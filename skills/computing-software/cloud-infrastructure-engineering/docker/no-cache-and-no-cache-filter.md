---
id: computing-software.cloud-infrastructure-engineering.docker.no-cache-and-no-cache-filter
name: no-cache-and-no-cache-filter
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, buildkit, layer-caching, build-cache, no-cache, no-cache-filter, cache-bust, cache-invalidation, selective-rebuild]
level: practitioner
description: "Force rebuilds precisely: --no-cache for everything, --no-cache-filter for one stage, and ARG-based cache busting for a single RUN, without throwing the whole cache away."
sources: ["https://docs.docker.com/build/cache/invalidation/", "https://docs.docker.com/reference/cli/docker/buildx/build/#no-cache-filter", "https://docs.docker.com/reference/compose-file/build/#no_cache", "https://docs.docker.com/reference/cli/docker/compose/build/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# --no-cache, --no-cache-filter and targeted cache busting

**Goal:** re-run the step that fetches "latest" security patches or an unpinned download
without discarding the expensive, still-valid layers around it.

## The three levers
```sh
docker build --no-cache .                           # ignore cache for every instruction
docker build --no-cache-filter deps,runtime .       # ignore cache only in the named stages
docker build --build-arg CACHEBUST=$(date +%s) .    # invalidate from one ARG downwards
```

### --no-cache
Every instruction is rebuilt. Add `--pull` to also attempt to pull newer base images:
`docker build --pull --no-cache .`.

### --no-cache-filter (BuildKit)
Takes one or more stage names of a multi-stage Dockerfile, comma-separated
(`--no-cache-filter stage1,stage2`). The arguments must be stage names. Cache is ignored for
those stages; typical use is a stage whose only job is to fetch the latest packages.

### ARG cache bust
```dockerfile
FROM alpine
RUN apk add --no-cache curl          # cached
ARG CACHEBUST=1
RUN curl -fsSLo /tool https://example.com/tool/latest   # rebuilt when CACHEBUST changes
```
Build arguments result in cache invalidation, so changing the value invalidates the
instructions from the `ARG` onwards. Place it immediately above the step you want to refresh.
Build arguments are not suitable for secrets; use secret mounts.

## Related invalidation facts
- For `COPY`, `ADD` and `RUN --mount=type=bind` the builder computes a cache checksum from file
  metadata; the modification time (`mtime`) is not taken into account.
- For other instructions, including `RUN`, only the command string is compared; the files a
  `RUN apt-get -y update` changed are not examined, so it never re-runs on its own. Chain
  `apt-get update && apt-get install` in one `RUN`.
- Once one instruction is invalidated, every later instruction is rebuilt.
- Changing `SOURCE_DATE_EPOCH` invalidates the cache for `WORKDIR` and everything after it.
- Secret contents are not part of the cache; changing a secret does not invalidate it.

## In Compose
`docker compose build --no-cache` disables the cache for the build; the Compose file attribute
is `build.no_cache: true`, which enforces a full rebuild for all image layers.

## Gotchas
- To clear the builder cache itself use `docker builder prune` or `docker buildx prune`;
  `--no-cache` only skips reading it.

## Verify
Run `docker build --no-cache-filter deps --progress=plain .` and confirm the steps of the named
stage lack `CACHED`.

## Checked

Checked 2026-10-23 against the Docker docs "Build cache invalidation" page, the docker/buildx `build --no-cache-filter` reference, the compose-spec build reference and the Docker Compose `compose build` reference (main branches).

- `--no-cache-filter` takes comma-separated stage names; the `ARG` cache-bust technique and the secrets note from the invalidation page.
- COPY/ADD/bind-mount cache checksums use file metadata and ignore `mtime`; RUN compares only the command string; `SOURCE_DATE_EPOCH` and `WORKDIR`.
- `docker compose build --no-cache` and the `no_cache` build attribute.
- Removed the "Docker 23+" gate, the ADD URL `Last-Modified`/ETag claim, the `ADD --checksum` caching claim, and the `--no-cache` / remote-cache and `.dockerignore` claims, none of which the docs state. The `--pull` behaviour is from the CLI flag description.

Method: documentation only; no commands were run.
