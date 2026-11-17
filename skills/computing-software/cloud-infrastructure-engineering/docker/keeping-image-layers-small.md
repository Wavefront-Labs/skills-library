---
id: computing-software.cloud-infrastructure-engineering.docker.keeping-image-layers-small
name: keeping-image-layers-small
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, layer-caching, image-size, apt-cache-cleanup, layer-size-reduction, no-install-recommends, combined-run, apk-no-cache, pip-no-cache-dir]
level: practitioner
description: "Keep each image layer small: clean package caches in the same RUN, skip recommends, avoid writing then deleting across layers, and verify with docker history."
sources: ["https://docs.docker.com/build/building/best-practices/", "https://docs.docker.com/build/cache/optimize/", "https://docs.docker.com/reference/cli/docker/image/history/", "https://github.com/opencontainers/image-spec/blob/main/layer.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keeping layers small

**Goal:** stop images carrying package indexes, downloaded archives and build leftovers
that are "deleted" but still present in an earlier layer.

## The layer rule
Image layers are changesets: the OCI layer spec represents a deletion in a later layer as a
whiteout entry, so the file still exists in the earlier layer and ships in the image.
Delete in the **same RUN** that creates the file.

## Package managers
```dockerfile
# Debian/Ubuntu
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*
```
Docker's best-practices page: always combine `apt-get update` with `apt-get install` in one
`RUN` (a separate `update` layer can be cached stale), list packages one per line, use
`--no-install-recommends`, and remove `/var/lib/apt/lists` so the apt cache is not stored in
the layer. Official Debian and Ubuntu images run `apt-get clean` automatically, so you do
not need to.

Cache mounts (`RUN --mount=type=cache,target=...`) keep a persistent package cache on the
builder, so rebuilding a layer only downloads new or changed packages and the cache stays out
of the layer. For other package managers, use that manager's own no-cache or clean options
(check its documentation).

## Build tools in the runtime image
Do not install compilers in the runtime image. Use a multi-stage build; the runtime stage
copies only artefacts.

## Other common bloat
- `COPY . .` bringing in `.git`, `node_modules` or test fixtures: use a `.dockerignore`
  (exclusion patterns).
- Downloaded archives: `ADD` supports `--checksum=sha256:...` validation of remote files.

## Measuring
```sh
docker history --format 'table {{.Size}}\t{{.CreatedBy}}' --no-trunc img
```
`docker history` takes `--format` (table, JSON or Go template) and `--no-trunc`.

## Gotchas
- Combining *everything* into one RUN hurts cache granularity; combine what belongs together
  (install and cleanup), keep separate concerns separate.

## Verify
`docker history` shows no layer dominated by package indexes or caches, and
`docker image inspect --format '{{.Size}}'` matches expectations.

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23) Dockerfile best-practices and build cache optimisation pages, `docker image history` reference; OCI image-spec layer.md (whiteouts). Confirmed: apt guidance, `apt-get clean` note, `.dockerignore`, `ADD --checksum`, cache mounts, multi-stage, `docker history` flags, whiteout semantics. Removed as unconfirmed: dnf, pip, npm and Go cleanup commands, the compile-and-purge one-liner, dpkg nodoc config, PYTHONDONTWRITEBYTECODE advice, the chown duplication claim, `--squash` and apk gotchas, dive efficiency figures (about 95%), the `sort -h` pipeline.
Method: documentation only; no commands were run.
