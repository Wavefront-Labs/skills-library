---
id: computing-software.cloud-infrastructure-engineering.docker.run-bind-and-tmpfs-mounts
name: run-bind-and-tmpfs-mounts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildkit, bind-mount-build, run-bind-mount, run-tmpfs-mount, dockerfile, build-performance]
level: advanced
description: "Use RUN --mount=type=bind to read context or stage files without COPYing them into a layer, and type=tmpfs for scratch space that never persists."
sources: ["https://docs.docker.com/reference/dockerfile/#run---mounttypebind", "https://docs.docker.com/reference/dockerfile/#run---mounttypetmpfs", "https://docs.docker.com/build/cache/optimize/#use-bind-mounts"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RUN --mount type=bind and type=tmpfs

**Goal:** stop paying for `COPY` layers that exist only to feed one build step, and keep
throwaway files (temp downloads, test artefacts) out of the image.

## type=bind
```dockerfile
# syntax=docker/dockerfile:1
FROM golang AS build
WORKDIR /src
# Download modules using only go.mod/go.sum, no COPY layer for them
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=bind,source=go.mod,target=go.mod \
    --mount=type=bind,source=go.sum,target=go.sum \
    go mod download
# Compile from the whole context, still no source layer in this stage
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=bind,target=. \
    CGO_ENABLED=0 go build -o /out/app ./cmd/app
```
Options: `source` (path in the `from`, default its root), `target` / `dst` (mount path,
required), `from` (build stage, context or image name for the root of the source; default the
build context), `rw` / `readwrite` (allow writes; written data is discarded after the `RUN`
instruction and not committed to the image layer).

Mounting from another stage or image:
```dockerfile
RUN --mount=type=bind,from=tools,source=/usr/local/bin/protoc,target=/usr/local/bin/protoc \
    protoc --go_out=. api.proto
```

## type=tmpfs
```dockerfile
RUN --mount=type=tmpfs,target=/tmp,size=512m \
    curl -fsSLo /tmp/pkg.tgz https://example.com/pkg.tgz && tar -xzf /tmp/pkg.tgz -C /opt
```
Options are `target` (required) and `size`, an upper limit on the size of the filesystem.
Files written to the tmpfs are not part of the image layer.

## When bind beats COPY
- Final image built from a separate stage anyway: the build stage's COPY layers are waste.
- Large monorepo context where the step only needs to read it.

## Gotchas
- Bind mounts are **read-only** by default; a step that writes next to its sources needs `rw`
  or a different output directory.
- With `rw`, writes are thrown away after the `RUN`; copy results to a non-mounted path in the
  same `RUN`.

## Verify
`docker history app:dev` shows no layer for the module files.

## Checked

Date: 2026-10-24. Documentation release: Dockerfile reference (moby/buildkit frontend docs, main) and Docker build cache optimisation guide.
Confirmed: bind mounts are read-only by default, the `target`/`dst`, `source`, `from`, `rw`/`readwrite` options and that
written data is discarded after the `RUN`, tmpfs `target` and `size` options, and the existence of the "Use bind
mounts" section in the optimisation guide. Removed: the pinned Go image tag, the claim about cache invalidation,
`.dockerignore` and WORKDIR interactions, builder memory behaviour and the tool-specific examples, which the
reference does not state.

Method: documentation only; no commands were run.
